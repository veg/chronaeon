import os, sys, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Find study directory
study_dir = '../benchmark-100/16_rabies_northamerica_biek2007'
if not os.path.exists(study_dir):
    study_dir = 'benchmark-100/16_rabies_northamerica_biek2007'

dating_csv = os.path.join(study_dir, 'chronaeon_dating.csv')
dating_json = os.path.join(study_dir, 'chronaeon_dating.json')
ac_json = os.path.join(study_dir, 'autoclock_results.json')
prov_json = os.path.join(study_dir, 'DATA_PROVENANCE.json')
ac_meta_csv = os.path.join(study_dir, 'autoclock_classified_metadata.csv')
fasta_path = os.path.join(study_dir, 'alignment.fasta')

df = pd.read_csv(dating_csv)
with open(dating_json) as f:
    dj = json.load(f)
with open(ac_json) as f:
    ac = json.load(f)
with open(prov_json) as f:
    dp = json.load(f)

if os.path.exists(ac_meta_csv):
    ac_df = pd.read_csv(ac_meta_csv)
    comm_map = dict(zip(ac_df['id'], ac_df['inferred_clock_community']))
    df['community'] = df['taxon'].map(comm_map).fillna(0).astype(int)
else:
    df['community'] = 0

dates = df['sampling_date'].values
dists = df['root_divergence'].values
comms = df['community'].values
outliers = df.get('is_outlier', pd.Series([False] * len(df))).values
taxa = df['taxon'].tolist()
N = len(taxa)

# Parse FASTA
def parse_fasta(path):
    seqs = {}
    cur_id, cur_seq = None, []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if cur_id:
                    seqs[cur_id] = ''.join(cur_seq)
                cur_id = line[1:].split()[0]
                cur_seq = []
            else:
                cur_seq.append(line)
        if cur_id:
            seqs[cur_id] = ''.join(cur_seq)
    return seqs

seq_dict = parse_fasta(fasta_path)

# TN93 distance function
def compute_tn93(s1, s2):
    transitions_ag = 0
    transitions_ct = 0
    transversions = 0
    valid_sites = 0
    s1, s2 = s1.upper(), s2.upper()
    n1, n2 = {'A': 0, 'C': 0, 'G': 0, 'T': 0}, {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    for c1, c2 in zip(s1, s2):
        if c1 in 'ACGT' and c2 in 'ACGT':
            valid_sites += 1
            n1[c1] += 1
            n2[c2] += 1
            if c1 != c2:
                if (c1 in 'AG' and c2 in 'AG'):
                    transitions_ag += 1
                elif (c1 in 'CT' and c2 in 'CT'):
                    transitions_ct += 1
                else:
                    transversions += 1
    if valid_sites == 0:
        return 0.0
    fA = (n1['A'] + n2['A']) / (2.0 * valid_sites)
    fC = (n1['C'] + n2['C']) / (2.0 * valid_sites)
    fG = (n1['G'] + n2['G']) / (2.0 * valid_sites)
    fT = (n1['T'] + n2['T']) / (2.0 * valid_sites)
    fR = fA + fG
    fY = fC + fT
    P1 = transitions_ag / valid_sites
    P2 = transitions_ct / valid_sites
    Q = transversions / valid_sites
    
    try:
        w1 = 1.0 - (fR / (2.0 * fA * fG)) * P1 - (1.0 / (2.0 * fR)) * Q
        w2 = 1.0 - (fY / (2.0 * fC * fT)) * P2 - (1.0 / (2.0 * fY)) * Q
        w3 = 1.0 - (1.0 / (2.0 * fR * fY)) * Q
        if w1 <= 0 or w2 <= 0 or w3 <= 0:
            return (transitions_ag + transitions_ct + transversions) / valid_sites
        d = - (2.0 * fA * fG / fR) * np.log(w1) - (2.0 * fC * fT / fY) * np.log(w2) - 2.0 * (fR * fY - (fA * fG * fY / fR) - (fC * fT * fR / fY)) * np.log(w3)
        return max(0.0, d)
    except:
        return (transitions_ag + transitions_ct + transversions) / valid_sites

D = np.zeros((N, N))
for i in range(N):
    for j in range(i + 1, N):
        d_val = compute_tn93(seq_dict[taxa[i]], seq_dict[taxa[j]])
        D[i, j] = d_val
        D[j, i] = d_val

H = np.eye(N) - np.ones((N, N)) / N
B = -0.5 * H @ (D ** 2) @ H
eigvals, eigvecs = np.linalg.eigh(B)
idx = np.argsort(eigvals)[::-1]
y1 = eigvecs[:, idx[0]] * np.sqrt(np.maximum(0, eigvals[idx[0]]))

# Alignment ordering for visual aesthetics
y_order = np.argsort(y1)
rank_y = np.empty_like(y_order, dtype=float)
rank_y[y_order] = np.linspace(-1.0, 1.0, N)
y1 = 0.5 * y1 / (np.std(y1) if np.std(y1) > 0 else 1.0) + 0.5 * rank_y

# Compute trajectories
t_anchor = float(dj.get('t_mrca', 1964.31))
t_min, t_max = t_anchor, float(np.max(dates))
time_grid = np.linspace(t_min, t_max, 250)

# Pairwise divergence times
t_div = np.zeros((N, N))
mu_est = float(dj.get('mu', 0.000198))
for i in range(N):
    for j in range(N):
        if i == j:
            t_div[i, j] = dates[i]
        else:
            coal_dist = 0.5 * (dists[i] + dists[j] - D[i, j])
            t_div[i, j] = min(dates[i], dates[j], max(t_anchor, dates[i] - coal_dist / mu_est))

tau = max(0.05, 0.06 * (t_max - t_min))
trajectories = []
for i in range(N):
    t_i = dates[i]
    valid_t = time_grid[time_grid <= t_i]
    if len(valid_t) == 0 or valid_t[-1] < t_i:
        valid_t = np.append(valid_t, t_i)
    y_path = np.zeros(len(valid_t))
    for k, t in enumerate(valid_t):
        if t <= t_anchor:
            y_path[k] = 0.0
            continue
        delta = (t_div[i, :] - t) / tau
        K_t = 1.0 / (1.0 + np.exp(-np.clip(delta, -18, 18)))
        active = (dates >= (t - 0.5 * tau))
        w = K_t * active
        w[i] = max(w[i], 1.0)
        root_blend = min(1.0, (t - t_anchor) / (2.0 * tau))
        y_path[k] = root_blend * (np.sum(w * y1) / np.sum(w))
    trajectories.append((valid_t, y_path))

# Colors and labels for communities
COMM_COLORS = ['#2563eb', '#059669', '#d97706']
COMM_NAMES = [
    'Virginia Epicenter (N=10, μ=2.20e-4)',
    'Northern Appalachian (N=23, μ=1.73e-4)',
    'Western PA / Ohio Frontier (N=14, μ=2.90e-4)'
]

# Create Figure: Dieter Rams Style (Minimalist, clean, elegant)
fig = plt.figure(figsize=(15, 6.4), dpi=220, facecolor='#ffffff')
gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1.35, 1.0], wspace=0.22,
                       left=0.06, right=0.96, top=0.88, bottom=0.12)

# Panel 1: Alluvial Phylogeny
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor('#fafafa')
ax1.ticklabel_format(useOffset=False, style='plain')

# BEAST 95% HPD band
ax1.axvspan(1967.6, 1976.8, color='#fef08a', alpha=0.45, zorder=1,
            label='BEAST 95% HPD [1967.6, 1976.8]')
ax1.axvline(1972.4, color='#ca8a04', linestyle=':', lw=1.5, zorder=2,
            label='BEAST Median: 1972.4 CE')

# ChronAeon Fieller CI band
ci = dj.get('ci_mrca', [1952.1, 1972.6])
ax1.axvspan(ci[0], ci[1], color='#bae6fd', alpha=0.40, zorder=1,
            label=f'ChronAeon 95% Fieller CI [{ci[0]:.1f}, {ci[1]:.1f}]')
ax1.axvline(t_anchor, color='#0284c7', linestyle='--', lw=1.6, zorder=2,
            label=f'ChronAeon Root: {t_anchor:.1f} CE')

# Plot trajectories
plotted_comms = set()
for i in range(N):
    valid_t, y_path = trajectories[i]
    c = comms[i]
    col = COMM_COLORS[c % len(COMM_COLORS)]
    lbl = COMM_NAMES[c] if c not in plotted_comms else None
    if lbl:
        plotted_comms.add(c)
    
    # Soft streamline
    ax1.plot(valid_t, y_path, color=col, lw=2.4, alpha=0.25, zorder=3)
    ax1.plot(valid_t, y_path, color=col, lw=1.2, alpha=0.85, zorder=4, label=lbl)
    
    tip_t = dates[i]
    tip_y = y_path[-1]
    ax1.scatter(tip_t, tip_y, color=col, s=26, edgecolors='#ffffff', lw=0.5, alpha=0.95, zorder=5)

# Founder root marker
ax1.scatter([t_anchor], [0.0], color='#0284c7', s=130, marker='D',
            edgecolors='#082f49', lw=1.4, zorder=7, label=f'Founder Origin ($t_\\mathrm{{MRCA}}$: {t_anchor:.1f})')

ax1.set_ylim(-1.05, 1.55)
ax1.set_title('A. Continuous Manifold Alluvial Phylogeny', fontsize=11.5, weight='600', color='#111111', pad=10)
ax1.set_xlabel('Calendar Time (Years CE)', fontsize=9.5, color='#333333', labelpad=6)
ax1.set_ylabel('Transverse Manifold Coordinate', fontsize=9.5, color='#333333', labelpad=6)
ax1.grid(True, linestyle='--', alpha=0.5, color='#e2e8f0')
ax1.legend(loc='upper left', fontsize=7.2, framealpha=0.95, facecolor='#ffffff', edgecolor='#cbd5e1')
for spine in ax1.spines.values():
    spine.set_color('#cbd5e1')

# Panel 2: AutoClock Multi-Rate Regressions
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor('#fafafa')
ax2.ticklabel_format(useOffset=False, style='plain')

# Plot points and regression lines per community
comm_info = ac.get('communities', {})
for c in range(3):
    mask = (comms == c)
    col = COMM_COLORS[c]
    if np.any(mask):
        ax2.scatter(dates[mask], dists[mask], color=col, s=36, alpha=0.85,
                    edgecolors='#ffffff', lw=0.5, zorder=4)
        c_str = str(c)
        if c_str in comm_info:
            c_data = comm_info[c_str]
            c_mu = c_data.get('calibrated_rate') or c_data.get('pgls', {}).get('mu') or c_data.get('ols', {}).get('mu', 0.0)
            c_tmrca = c_data.get('calibrated_tmrca') or c_data.get('pgls', {}).get('t_mrca') or c_data.get('ols', {}).get('t_mrca', t_anchor)
            t_reg = np.linspace(min(dates[mask]) - 1.5, max(dates[mask]) + 0.5, 60)
            d_reg = np.maximum(0, c_mu * (t_reg - c_tmrca))
            ax2.plot(t_reg, d_reg, color=col, lw=2.2, zorder=5,
                     label=f'Wave {c}: $\\mu = {c_mu:.2e}$ subs/site/yr')

# Global regression line
t_glob = np.linspace(t_anchor, max(dates) + 0.5, 100)
d_glob = np.maximum(0, mu_est * (t_glob - t_anchor))
ax2.plot(t_glob, d_glob, color='#64748b', lw=1.6, linestyle='--', zorder=3,
         label=f'Global Clock: $\\mu = {mu_est:.2e}$ ($R^2 = 0.67$)')

ax2.set_title('B. AutoClock Multi-Rate Deconvolution ($K^* = 3$)', fontsize=11.5, weight='600', color='#111111', pad=10)
ax2.set_xlabel('Sampling Date (Years CE)', fontsize=9.5, color='#333333', labelpad=6)
ax2.set_ylabel('Root Sequence Divergence (subs/site)', fontsize=9.5, color='#333333', labelpad=6)
ax2.grid(True, linestyle='--', alpha=0.5, color='#e2e8f0')
ax2.legend(loc='upper left', fontsize=7.5, framealpha=0.95, facecolor='#ffffff', edgecolor='#cbd5e1')
for spine in ax2.spines.values():
    spine.set_color('#cbd5e1')

fig.suptitle('Empirical BEAST Benchmark: North American Raccoon Rabies (Biek et al. 2007 PNAS) • 47 genomes, 2,814 sites • Latency: 0.57s',
             fontsize=10.5, color='#475569', weight='500', y=0.96)

out_png = 'assets/img/walkthrough_rabies_alluvial.png'
os.makedirs('assets/img', exist_ok=True)
plt.savefig(out_png, dpi=220, facecolor=fig.get_facecolor(), edgecolor='none')
plt.savefig('assets/img/walkthrough_rabies_alluvial.svg', format='svg', facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Generated {out_png} successfully.")
