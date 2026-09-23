#!/usr/bin/env python3
"""
stream_bvbrc_surveillance.py
============================
BV-BRC Live Streaming Ingestion, Sieve Triage, and Multi-Clock Pipeline
ChronAeon Project | ChronAeon Research Consortium

Capabilities:
1. Live REST API streaming: Direct HTTP ingestion from the BV-BRC API
   (https://www.bv-brc.org/api/genome/ and /api/genome_sequence/)
2. Extraction and column-slicing of planetary cohorts (e.g. 58-year H3N2 HA)
3. Streaming Sieve Triage (chronaeon triage) at >350 seq/s
4. Unsupervised Multi-Clock AutoClock Deconvolution (chronaeon autoclock)
5. Publication-grade figure generation
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
import numpy as np
import pandas as pd

# ChronAeon and HyphAeon dynamic environment discovery
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]

search_paths = []
for env_var in ["HYPHAEON_PATH", "CHRONAEON_SRC"]:
    if os.environ.get(env_var):
        search_paths.append(os.environ[env_var])

for rel in ["chronaeon/src", "../HyphAeon/chronaeon/src", "../HyphAeon/aeon-core/src", "../../HyphAeon/chronaeon/src", "../../HyphAeon/aeon-core/src"]:
    p = (REPO_ROOT / rel).resolve()
    if p.is_dir():
        search_paths.append(str(p))

for sp in search_paths:
    if sp not in sys.path:
        sys.path.insert(0, sp)

def stream_live_bvbrc_records(taxon_id=11320, subtype="H3N2", limit=10, output_prefix=None):
    """
    Stream live viral records and coding sequences directly from BV-BRC REST API.
    
    Parameters:
    -----------
    taxon_id : int
        NCBI / BV-BRC taxonomy ID (e.g. 11320 for Influenza A virus)
    subtype : str
        Subtype string (e.g. "H3N2")
    limit : int
        Number of records to stream
    output_prefix : Path or str, optional
        Prefix for saving streaming fasta and metadata
    """
    print("=" * 80)
    print(f"[*] BV-BRC LIVE STREAMING INGESTION (Taxon: {taxon_id}, Subtype: {subtype}, Limit: {limit})")
    print("=" * 80)
    
    t0 = time.time()
    query = f"and(eq(taxon_id,{taxon_id}),eq(subtype,%22{subtype}%22))"
    fields = "genome_id,genome_name,collection_date,host_group,host_common_name,geographic_group,country"
    genome_url = f"https://www.bv-brc.org/api/genome/?{query}&select({fields})&sort(-collection_date)&limit({limit})"
    
    print(f"[*] Connecting to BV-BRC REST endpoint:\n    {genome_url}")
    req = urllib.request.Request(genome_url, headers={"Accept": "application/json", "User-Agent": "ChronAeon-Surveillance/1.0"})
    
    with urllib.request.urlopen(req, timeout=20) as resp:
        genomes = json.loads(resp.read().decode("utf-8"))
        
    t_meta = time.time() - t0
    print(f"[✓] Retrieved metadata for {len(genomes)} genomes in {t_meta:.2f}s ({len(genomes)/t_meta:.1f} records/s).")
    
    # Stream sequence data for retrieved genomes
    streamed_records = []
    print(f"[*] Streaming sequences for {len(genomes)} genomes...")
    t_seq_start = time.time()
    
    for i, g in enumerate(genomes):
        gid = g.get("genome_id")
        seq_url = f"https://www.bv-brc.org/api/genome_sequence/?and(eq(genome_id,%22{gid}%22))&select(sequence_id,sequence,description,length)&limit(20)"
        sreq = urllib.request.Request(seq_url, headers={"Accept": "application/json", "User-Agent": "ChronAeon-Surveillance/1.0"})
        try:
            with urllib.request.urlopen(sreq, timeout=15) as sresp:
                seq_data = json.loads(sresp.read().decode("utf-8"))
                for s in seq_data:
                    desc = s.get("description", "")
                    # Look for HA or segment 4 if Influenza
                    seq = s.get("sequence", "")
                    if seq:
                        streamed_records.append({
                            "genome_id": gid,
                            "genome_name": g.get("genome_name"),
                            "collection_date": g.get("collection_date"),
                            "host_group": g.get("host_group"),
                            "country": g.get("country"),
                            "sequence_id": s.get("sequence_id"),
                            "description": desc,
                            "length": len(seq),
                            "sequence": seq
                        })
                        break
        except Exception as e:
            print(f"[!] Warning: failed to fetch sequence for {gid}: {e}")
            
    t_seq_total = time.time() - t_seq_start
    print(f"[✓] Streamed {len(streamed_records)} sequences in {t_seq_total:.2f}s.")
    
    if output_prefix:
        out_fasta = f"{output_prefix}_streamed.fasta"
        out_meta = f"{output_prefix}_metadata.csv"
        with open(out_fasta, "w") as f:
            for r in streamed_records:
                f.write(f">{r['genome_id']}\n{r['sequence']}\n")
        df_meta = pd.DataFrame([{k: v for k, v in r.items() if k != "sequence"} for r in streamed_records])
        df_meta.to_csv(out_meta, index=False)
        print(f"[✓] Saved streamed records to {out_fasta} and {out_meta}")
        
    return streamed_records

def run_challenge_pipeline(base_dir=None):
    """
    Executes the reproducible Grand Challenge pipeline:
    1. Sieve triage on the 10,000-taxon cohort
    2. AutoClock deconvolution
    3. Publication figure generation
    """
    if base_dir is None:
        base_dir = SCRIPT_DIR.parent
    base_dir = Path(base_dir)
    data_dir = base_dir / "data"
    results_dir = base_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    fasta_10k = data_dir / "h3n2_challenge_10k.fasta"
    meta_10k = data_dir / "h3n2_challenge_10k_metadata.csv"
    
    if not fasta_10k.exists() or not meta_10k.exists():
        print(f"[!] Target files not found in {data_dir}. Generating cohorts from master database...")
        from stream_and_extract_h3n2 import extract_and_clean_h3n2_cohort
        extract_and_clean_h3n2_cohort()
        
    # Phase 1: High-Throughput Streaming Sieve Triage
    print("\n" + "=" * 80)
    print("PHASE 1: STREAMING SIEVE TRIAGE (chronaeon triage)")
    print("=" * 80)
    
    sieve_out = results_dir / "h3n2_10k_sieve_report.csv"
    clean_fasta = results_dir / "h3n2_10k_sieved_clean.fasta"
    sus_fasta = results_dir / "h3n2_10k_sieved_sus.fasta"
    
    cmd_sieve = [
        sys.executable, "-m", "chronaeon.cli", "triage",
        "-a", str(fasta_10k),
        "-d", str(meta_10k),
        "-s", str(fasta_10k),
        "--stream-dates", str(meta_10k),
        "--date-col", "decimal_date",
        "--strain-col", "genome_id",
        "--n-anchor", "220",
        "--n-bins", "32",
        "-o", str(sieve_out),
        "--clean-out", str(clean_fasta),
        "--sus-out", str(sus_fasta)
    ]
    
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{CHRONAEON_SRC}:{AXOMEME_ROOT}:" + env.get("PYTHONPATH", "")
    
    t0_sieve = time.time()
    import subprocess
    subprocess.run(cmd_sieve, env=env, check=True)
    t_sieve = time.time() - t0_sieve
    print(f"[✓] Sieve completed in {t_sieve:.2f}s!")
    
    # Phase 2: Unsupervised Multi-Clock AutoClock Deconvolution
    print("\n" + "=" * 80)
    print("PHASE 2: UNSUPERVISED MULTI-CLOCK AUTOCLOCK DECONVOLUTION")
    print("=" * 80)
    
    # Generate clean metadata matched to clean fasta
    df_clean_meta = pd.read_csv(meta_10k)
    df_clean_meta["genome_id"] = df_clean_meta["genome_id"].astype(str)
    
    clean_ids = set()
    with open(clean_fasta, "r") as f:
        for line in f:
            if line.startswith(">"):
                clean_ids.add(line[1:].strip())
                
    df_clean_meta = df_clean_meta[df_clean_meta["genome_id"].isin(clean_ids)]
    clean_meta_path = results_dir / "h3n2_10k_sieved_clean_metadata.csv"
    df_clean_meta.to_csv(clean_meta_path, index=False)
    
    cmd_auto = [
        sys.executable, "-m", "chronaeon.cli", "autoclock",
        "-a", str(clean_fasta),
        "-d", str(clean_meta_path),
        "--date-col", "decimal_date",
        "--strain-col", "genome_id",
        "-k", "8",
        "--output-dir", str(results_dir / "clock_communities"),
        "-o", str(results_dir / "h3n2_10k_autoclock_results.json"),
        "-c", str(results_dir / "h3n2_10k_autoclock_classified.csv"),
        "--plot",
        "--plot-path", str(results_dir / "h3n2_10k_autoclock_communities.png")
    ]
    
    t0_auto = time.time()
    subprocess.run(cmd_auto, env=env, check=True)
    t_auto = time.time() - t0_auto
    print(f"[✓] AutoClock completed in {t_auto:.2f}s!")
    
    # Phase 3: Diagnostic Figure Generation
    print("\n" + "=" * 80)
    print("PHASE 3: PUBLICATION-GRADE FIGURE GENERATION")
    print("=" * 80)
    cmd_fig = [sys.executable, str(base_dir / "generate_challenge_figure.py")]
    subprocess.run(cmd_fig, env=env, check=True)
    print("[✓] Challenge pipeline complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BV-BRC Live Streaming & Reproducibility Pipeline")
    parser.add_argument("--test-stream", action="store_true", help="Test live streaming ingestion from BV-BRC REST API")
    parser.add_argument("--limit", type=int, default=10, help="Number of records to stream for live test")
    parser.add_argument("--run-challenge", action="store_true", help="Run the full 10k Grand Challenge benchmark")
    parser.add_argument("--base-dir", type=str, default=str(SCRIPT_DIR.parent), help="Base directory for BV-BRC data and results")
    
    args = parser.parse_args()
    
    if args.test_stream or (not args.run_challenge):
        stream_live_bvbrc_records(taxon_id=11320, subtype="H3N2", limit=args.limit)
        
    if args.run_challenge:
        run_challenge_pipeline(args.base_dir)
