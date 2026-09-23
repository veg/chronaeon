#!/usr/bin/env python3
"""
NextStrain Grand Challenge Benchmark Harness
Compares ChronAeon Date & AutoClock head-to-head against TreeTime across official NextStrain streaming surveillance feeds.
"""

import os
import sys
import time
import json
import gzip
import urllib.request
import pandas as pd
import numpy as np
import subprocess

NEXTSTRAIN_BUILDS = {
    "h3n2_12y": {
        "url": "https://data.nextstrain.org/seasonal-flu_h3n2_ha_12y.json",
        "title": "Influenza A/H3N2 HA (12-Year Longitudinal)",
        "cds_start": 17,  # 0-indexed, start at nt 18
        "cds_end": 1718,
    },
    "h1n1pdm_12y": {
        "url": "https://data.nextstrain.org/seasonal-flu_h1n1pdm_ha_12y.json",
        "title": "Influenza A/H1N1pdm HA (12-Year Longitudinal)",
        "cds_start": 20,  # 0-indexed, start at nt 21
        "cds_end": 1721,
    }
}

def download_and_extract(build_id, cfg, base_dir):
    build_dir = os.path.join(base_dir, build_id)
    data_dir = os.path.join(build_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"\n==========================================================================")
    print(f"[+] FETCHING NEXTSTRAIN BUILD: {cfg['title']}")
    print(f"    URL: {cfg['url']}")
    print(f"==========================================================================")
    
    t0 = time.time()
    req = urllib.request.Request(cfg['url'], headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(gzip.decompress(resp.read()).decode('utf-8'))
    
    root_nuc = list(data['root_sequence']['nuc'])
    tips = {}
    tip_dates = {}
    tip_meta = {}
    treetime_root = data['tree'].get('node_attrs', {}).get('num_date', {})

    def traverse(node, current_seq):
        seq = list(current_seq)
        muts = node.get('branch_attrs', {}).get('mutations', {}).get('nuc', [])
        for m in muts:
            ref, pos, alt = m[0], int(m[1:-1]), m[-1]
            idx = pos - 1
            if 0 <= idx < len(seq):
                seq[idx] = alt
        if 'children' in node:
            for c in node['children']:
                traverse(c, seq)
        else:
            name = node['name']
            full_s = ''.join(seq)
            start = cfg.get('cds_start', 0)
            end = cfg.get('cds_end', len(full_s))
            tips[name] = full_s[start:end]
            attrs = node.get('node_attrs', {})
            if 'num_date' in attrs:
                tip_dates[name] = attrs['num_date']['value']
            tip_meta[name] = {
                'clade': attrs.get('clade_membership', {}).get('value', ''),
                'subclade': attrs.get('subclade', {}).get('value', ''),
                'region': attrs.get('region', {}).get('value', ''),
                'country': attrs.get('country', {}).get('value', '')
            }

    traverse(data['tree'], root_nuc)
    t1 = time.time()
    print(f"[✓] Reconstructed {len(tips)} genomes ({len(list(tips.values())[0])} bp) in {t1-t0:.2f}s")
    
    fasta_path = os.path.join(data_dir, "alignment.fasta")
    dates_path = os.path.join(data_dir, "dates.csv")
    meta_path = os.path.join(data_dir, "metadata.csv")
    truth_path = os.path.join(build_dir, "treetime_truth.json")
    
    with open(fasta_path, "w") as f:
        for k, v in tips.items():
            f.write(f">{k}\n{v}\n")
            
    df_dates = pd.DataFrame([{'sequence_id': k, 'date': v} for k, v in tip_dates.items()])
    df_dates.to_csv(dates_path, index=False)
    
    df_meta = pd.DataFrame([{'sequence_id': k, 'date': tip_dates.get(k), **tip_meta.get(k, {})} for k in tips.keys()])
    df_meta.to_csv(meta_path, index=False)
    
    with open(truth_path, "w") as f:
        json.dump({'treetime_root_date': treetime_root, 'n_tips': len(tips), 'url': cfg['url']}, f, indent=2)
        
    return build_dir, fasta_path, dates_path, meta_path, treetime_root

    env = os.environ.copy()
    search_paths = []
    if os.environ.get("CHRONAEON_SRC"):
        search_paths.append(os.environ["CHRONAEON_SRC"])
    for rel in ["../HyphAeon/chronaeon/src", "../../HyphAeon/chronaeon/src", "../../../HyphAeon/chronaeon/src"]:
        cand = os.path.abspath(os.path.join(os.path.dirname(__file__), rel))
        if os.path.isdir(cand):
            search_paths.append(cand)
    if search_paths:
        env["PYTHONPATH"] = ":".join(search_paths) + (":" + env["PYTHONPATH"] if "PYTHONPATH" in env else "")
    
    print(f"\n[+] Running ChronAeon Date on {build_id}...")
    t0 = time.time()
    date_cmd = [
        "python3", "-m", "chronaeon.cli", "date",
        "-a", fasta_path,
        "-d", dates_path,
        "--no-tree",
        "--ci-method", "fieller",
        "-o", os.path.join(build_dir, "chronaeon_results.json"),
        "-c", os.path.join(build_dir, "chronaeon_results.csv"),
        "--plot",
        "--plot-path", os.path.join(build_dir, "chronaeon_dating.pdf")
    ]
    subprocess.run(date_cmd, env=env, check=True)
    t_date = time.time() - t0
    
    print(f"\n[+] Running ChronAeon AutoClock on {build_id}...")
    t0 = time.time()
    auto_cmd = [
        "python3", "-m", "chronaeon.cli", "autoclock",
        "-a", fasta_path,
        "-d", dates_path,
        "-k", "6",
        "--output-dir", os.path.join(build_dir, "autoclock_out"),
        "-o", os.path.join(build_dir, "autoclock_results.json"),
        "-c", os.path.join(build_dir, "autoclock_metadata.csv"),
        "--plot",
        "--plot-path", os.path.join(build_dir, "autoclock_plot.pdf")
    ]
    subprocess.run(auto_cmd, env=env, check=True)
    t_auto = time.time() - t0
    
    # Load and print cross-tabulation
    df_meta = pd.read_csv(meta_path)
    df_auto = pd.read_csv(os.path.join(build_dir, "autoclock_metadata.csv"))
    merged = pd.merge(df_auto, df_meta, left_on="id", right_on="sequence_id")
    
    print(f"\n==========================================================================")
    print(f"BENCHMARK SUMMARY: {build_id}")
    print(f"==========================================================================")
    print(f"Taxa: {len(df_meta)}")
    print(f"ChronAeon Date Runtime:     {t_date:.2f} seconds")
    print(f"ChronAeon AutoClock Runtime:{t_auto:.2f} seconds")
    with open(os.path.join(build_dir, "autoclock_results.json")) as f:
        auto_res = json.load(f)
    print(f"AutoClock Optimal Communities (K*): {auto_res.get('optimal_k')}")

    communities = auto_res.get('communities', {})
    if isinstance(communities, dict):
        comm_items = communities.values()
    else:
        comm_items = communities

    for comm in comm_items:
        cid = comm.get('community_id')
        n = comm.get('taxa_count')
        mrca = comm.get('calibrated_tmrca', comm.get('t_mrca'))
        rate = comm.get('calibrated_rate', comm.get('rate'))
        r2 = comm.get('r2')
        print(f"  • Community {cid} (N={n}): t_MRCA={mrca:.2f}, Rate={rate:.6f}, R^2={r2:.3f}")
        
    print(f"\nCross-Tabulation of Inferred Community vs. NextStrain Clade:")
    ct = pd.crosstab(merged['inferred_clock_community'], merged['clade'], margins=True)
    print(ct.to_string())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NextStrain Grand Challenge Benchmark Harness")
    default_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    parser.add_argument("--base-dir", type=str, default=default_base, help="Base directory for downloading/extracting data")
    args = parser.parse_args()
    base_dir = args.base_dir
    os.makedirs(base_dir, exist_ok=True)
    
    for build_id, cfg in NEXTSTRAIN_BUILDS.items():
        build_dir, fasta_path, dates_path, meta_path, treetime_root = download_and_extract(build_id, cfg, base_dir)
        run_chronaeon(build_id, build_dir, fasta_path, dates_path, meta_path, treetime_root)
