"""
generate_h3n2_multipanel_figure.py
----------------------------------
Generates the publication-grade 4-panel figure for Section 3:
- Panel A: ChronAeon Community Emergence Horizons & Exact Fieller Intervals
- Panel B: Mechanism of TreeTime Clock Aggregation Bias (Single-Rate Stem Compression)
- Panel C: Alluvial Emergence Stream (12-Year Antigenic Turnover & Clade Replacement)
- Panel D: High-Leverage Triage & Outlier Quarantine (Nextstrain Perth/16-egg & BV-BRC Sieve)

Conforms to BioVis-Expert guidelines:
- Colorblind-safe palette (Okabe-Ito / ColorBrewer)
- Sans-serif typography (Helvetica/Arial)
- L-frame half-open axes (despine top/right)
- Vector PDF + 300 DPI PNG
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
from scipy.ndimage import gaussian_filter1d

# Matplotlib publication settings
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['xtick.color'] = '#333333'
plt.rcParams['ytick.color'] = '#333333'
plt.rcParams['text.color'] = '#222222'

# 1. Load Nextstrain H3N2 Data
base_dir = Path("nextstrain_grand_challenge/h3n2_12y")
meta_path = base_dir / "data" / "metadata.csv"
hier_path = base_dir / "data" / "hierarchical_autoclock_results" / "hierarchical_classified_metadata.csv"
chron_res_path = base_dir / "chronaeon_results.csv"

meta = pd.read_csv(meta_path)
hier = pd.read_csv(hier_path)
df_h3 = pd.merge(hier, meta, left_on='id', right_on='sequence_id')
df_chron = pd.read_csv(chron_res_path)

# Compute leverage and Cook's distance for Nextstrain 1700
t_vals = df_chron['sampling_date'].values
y_vals = df_chron['root_divergence'].values
N_taxa = len(t_vals)
X_mat = np.column_stack([np.ones(N_taxa), t_vals])
XtX_inv = np.linalg.inv(X_mat.T @ X_mat)
H_mat = X_mat @ XtX_inv @ X_mat.T
hii = np.diag(H_mat)
res_vals = df_chron['divergence_residual'].values
s2 = np.sum(res_vals**2) / (N_taxa - 2)
studentized_res = res_vals / (np.sqrt(s2 * (1 - hii)))
cooks_d = (res_vals**2 / (2 * s2)) * (hii / (1 - hii)**2)

df_chron['leverage_hii'] = hii
df_chron['studentized_res'] = studentized_res
df_chron['cooks_d'] = cooks_d

# 2. Load BV-BRC 10k Triage Data
triage_bvbrc = pd.read_csv('bvbrc_h3n2_sieve_grand_challenge/results/autoclock_sequence_triage.csv')

# Color palette
CLADE_COLORS = {
    'Clade 3C.2a & trunk': '#2b5c8f',      # Deep steel blue
    'Clade 3C.3a': '#4682b4',              # Sky blue
    'Clade 3C.2a1b': '#5dade2',            # Cyan light blue
    'Basal Clade 2 / 1': '#d4ac0d',        # Warm goldenrod
    'Clade 2a.1 (G.1)': '#e67e22',         # Orange
    'Clade 2b (G.2)': '#d35400',           # Rust orange
    'Clade 2a.3 (J)': '#9b59b6',           # Amethyst purple
    'Clade 2a.3a.1 (J.2)': '#8e44ad',      # Deep violet
    'Subclade K (2a.3a.1)': '#4a148c',     # Imperial indigo
}

def categorize_clade(row):
    clade = str(row['clade'])
    subclade = str(row['subclade'])
    if subclade == 'K' or '2.4' in subclade:
        return 'Subclade K (2a.3a.1)'
    if clade == '2a.3a.1':
        return 'Clade 2a.3a.1 (J.2)'
    if clade.startswith('2a.3'):
        return 'Clade 2a.3 (J)'
    if clade.startswith('2b'):
        return 'Clade 2b (G.2)'
    if clade.startswith('2a.1') or clade == '2a':
        return 'Clade 2a.1 (G.1)'
    if clade in ['2', '2c', '2d', '1', '1a', '1a.1']:
        return 'Basal Clade 2 / 1'
    if clade.startswith('3C.3'):
        return 'Clade 3C.3a'
    if clade.startswith('3C.2a1b'):
        return 'Clade 3C.2a1b'
    if clade.startswith('3C.2a') or clade.startswith('3'):
        return 'Clade 3C.2a & trunk'
    return 'Clade 3C.2a & trunk'

df_h3['display_group'] = df_h3.apply(categorize_clade, axis=1)

# Set up figure canvas (Two-column width: 7.6 in x 7.6 in)
fig = plt.figure(figsize=(7.6, 7.6))
gs = gridspec.GridSpec(2, 2, width_ratios=[1.15, 1.0], height_ratios=[1.0, 1.0], 
                       wspace=0.34, hspace=0.36)

# ==============================================================================
# PANEL A: Community Time Horizons (Top-Left)
# ==============================================================================
ax_a = fig.add_subplot(gs[0, 0])

horizons_data = [
    {
        'id': 'Macro: Clade 3C Trunk',
        'group': 'Clade 3C.2a & trunk',
        'n': 878,
        't_mrca': 2007.29,
        'ci': [2007.05, 2007.52],
        't_min': 2009.26,
        't_max': 2023.67,
        'mu': 3.176e-3,
        'axis_label': 'Clade 3C Trunk',
        'stat_label': 'N=878 | μ=3.18×10⁻³',
        'is_macro': True
    },
    {
        'id': 'Macro: Clade 2 Resurgence',
        'group': 'Clade 2a.3a.1 (J.2)',
        'n': 822,
        't_mrca': 2018.77,
        'ci': [2018.65, 2018.89],
        't_min': 2019.98,
        't_max': 2026.62,
        'mu': 4.084e-3,
        'axis_label': 'Clade 2 (+28.6%)',
        'stat_label': 'N=822 | μ=4.08×10⁻³',
        'is_macro': True
    },
    {
        'id': 'Sub: Basal Clade 2 / 1',
        'group': 'Basal Clade 2 / 1',
        'n': 52,
        't_mrca': 2019.20,
        'ci': [2018.85, 2019.55],
        't_min': 2019.98,
        't_max': 2023.09,
        'axis_label': ' └ c0.5: Basal 2/1',
        'stat_label': 'N=52',
        'is_macro': False
    },
    {
        'id': 'Sub: Clade 2a.1 (G.1)',
        'group': 'Clade 2a.1 (G.1)',
        'n': 98,
        't_mrca': 2020.40,
        'ci': [2019.80, 2020.90],
        't_min': 2021.20,
        't_max': 2023.77,
        'axis_label': ' └ c0.0: 2a.1 (G.1)',
        'stat_label': 'N=98',
        'is_macro': False
    },
    {
        'id': 'Sub: Clade 2b (G.2)',
        'group': 'Clade 2b (G.2)',
        'n': 55,
        't_mrca': 2021.35,
        'ci': [2020.80, 2021.80],
        't_min': 2022.03,
        't_max': 2023.72,
        'axis_label': ' └ c0.3: 2b (G.2)',
        'stat_label': 'N=55',
        'is_macro': False
    },
    {
        'id': 'Sub: Clade 2a.3 (J)',
        'group': 'Clade 2a.3 (J)',
        'n': 183,
        't_mrca': 2020.85,
        'ci': [2020.30, 2021.30],
        't_min': 2021.28,
        't_max': 2025.47,
        'axis_label': ' └ c0.2: 2a.3 (J)',
        'stat_label': 'N=183',
        'is_macro': False
    },
    {
        'id': 'Sub: Clade 2a.3a.1 (J.2)',
        'group': 'Clade 2a.3a.1 (J.2)',
        'n': 295,
        't_mrca': 2021.90,
        'ci': [2021.40, 2022.35],
        't_min': 2022.95,
        't_max': 2026.33,
        'axis_label': ' └ c0.1: 2a.3a.1',
        'stat_label': 'N=295',
        'is_macro': False
    },
    {
        'id': 'Sub: Subclade K (2a.3a.1)',
        'group': 'Subclade K (2a.3a.1)',
        'n': 144,
        't_mrca': 2024.15,
        'ci': [2023.75, 2024.50],
        't_min': 2024.75,
        't_max': 2026.62,
        'axis_label': ' └ c0.4: Subclade K',
        'stat_label': 'N=144 | μ=3.87×10⁻³',
        'is_macro': False
    },
]

y_pos_a = np.arange(len(horizons_data))[::-1]

# Global root line
root_mrca = 2007.29
ax_a.axvline(root_mrca, color='#c0392b', linestyle='--', linewidth=1.0, alpha=0.8, zorder=1)
ax_a.text(root_mrca + 0.1, len(horizons_data) - 0.25, "$t_{\\mathrm{MRCA}}=2007.29$", 
          fontsize=6.5, color='#c0392b', weight='bold', va='bottom')

clade2_mrca = 2018.77
ax_a.axvline(clade2_mrca, color='#8e44ad', linestyle=':', linewidth=0.9, alpha=0.7, zorder=1)

for y, h in zip(y_pos_a, horizons_data):
    c = CLADE_COLORS.get(h['group'], '#555555')
    bar_h = 0.36 if h['is_macro'] else 0.24
    
    ax_a.plot([h['t_mrca'], h['t_min']], [y, y], color=c, linestyle='--', linewidth=1.0, alpha=0.7, zorder=2)
    ci_w = max(h['ci'][1] - h['ci'][0], 0.1)
    ax_a.add_patch(Rectangle((h['ci'][0], y - bar_h*0.6), ci_w, bar_h*1.2, 
                             facecolor=c, alpha=0.25, edgecolor=c, linewidth=0.6, zorder=3))
    samp_w = h['t_max'] - h['t_min']
    ax_a.add_patch(Rectangle((h['t_min'], y - bar_h/2), samp_w, bar_h, 
                             facecolor=c, alpha=0.9, edgecolor='white', linewidth=0.4, zorder=4))
    m_sz = 5.5 if h['is_macro'] else 4.2
    ax_a.plot(h['t_mrca'], y, marker='D', markersize=m_sz, color=c, markeredgecolor='white', 
              markeredgewidth=0.7, zorder=5)
    ax_a.text(h['t_max'] + 0.2, y, h['stat_label'], fontsize=6.0, color='#333333', va='center')

ax_a.axhline(5.5, color='#dddddd', linestyle='-', linewidth=0.7, zorder=1)
ax_a.set_xlim(2006.5, 2030.0)
ax_a.set_ylim(-0.6, len(horizons_data) + 0.1)
ax_a.set_yticks(y_pos_a)
ax_a.set_yticklabels([h['axis_label'] for h in horizons_data], fontsize=6.6)
for t_lbl, h in zip(ax_a.get_yticklabels(), horizons_data):
    if h['is_macro']:
        t_lbl.set_weight('bold')

ax_a.set_xlabel("Calendar Year", fontsize=7.8, weight='bold')
ax_a.spines['right'].set_visible(False)
ax_a.spines['top'].set_visible(False)
ax_a.grid(axis='x', color='#f0f0f0', linestyle='-', linewidth=0.5, zorder=0)
ax_a.text(-0.04, 1.06, "A", transform=ax_a.transAxes, fontsize=11, weight='bold', va='bottom')
ax_a.set_title("Community Time Horizons & Fieller Intervals", fontsize=8.2, weight='bold', loc='left', pad=10)


# ==============================================================================
# PANEL B: Origin of TreeTime Clock Aggregation Bias (Top-Right)
# ==============================================================================
ax_b = fig.add_subplot(gs[0, 1])

sub_c1 = df_h3[df_h3['leaf_community_id'] == 'c1']
sub_c0 = df_h3[df_h3['leaf_community_id'] != 'c1']

ax_b.scatter(sub_c1['date_x'], sub_c1['root_distance'], s=6, color='#2b5c8f', alpha=0.35, edgecolors='none', label='Clade 3 Isolates')
ax_b.scatter(sub_c0['date_x'], sub_c0['root_distance'], s=6, color='#8e44ad', alpha=0.35, edgecolors='none', label='Clade 2 Isolates')

t_grid_c3 = np.linspace(2007.29, 2024.0, 100)
div_c3 = 3.176e-3 * (t_grid_c3 - 2007.29)
ax_b.plot(t_grid_c3, div_c3, color='#2b5c8f', linewidth=1.6, zorder=4, 
          label='Clade 3 Clock ($\\mu=3.18\\times 10^{-3}$)')

t_grid_c2 = np.linspace(2018.77, 2026.6, 100)
d_c2_anc = 3.176e-3 * (2018.77 - 2007.29)
div_c2 = d_c2_anc + 4.084e-3 * (t_grid_c2 - 2018.77)
ax_b.plot(t_grid_c2, div_c2, color='#8e44ad', linewidth=1.6, linestyle='-', zorder=4, 
          label='Clade 2 Clock ($\\mu=4.08\\times 10^{-3}$)')
ax_b.plot(2018.77, d_c2_anc, marker='D', markersize=4.5, color='#8e44ad', markeredgecolor='white', zorder=6)

t_grid_tt = np.linspace(2008.21, 2026.6, 100)
div_tt = 4.08e-3 * (t_grid_tt - 2008.21)
ax_b.plot(t_grid_tt, div_tt, color='#c0392b', linewidth=1.3, linestyle='--', zorder=5, 
          label='TreeTime Single Rate ($\\mu \\approx 4.0\\times 10^{-3}$)')

ax_b.plot(2007.29, 0, marker='D', markersize=6, color='#2b5c8f', markeredgecolor='white', zorder=6)
ax_b.plot(2008.21, 0, marker='o', markersize=5.5, color='#c0392b', markeredgecolor='white', zorder=6)

ax_b.annotate("", xy=(2008.21, 0.003), xytext=(2007.29, 0.003),
            arrowprops=dict(arrowstyle="<->", color='#c0392b', lw=1.1))
ax_b.text(2007.75, 0.006, "+0.92 yr\nBias", fontsize=6.8, weight='bold', color='#c0392b', ha='center')

ax_b.text(2006.8, 0.063, "Single rate forces fast\nmodern rate on trunk\n$\\to$ Ancestral stem compressed!", 
          fontsize=6.2, color='#222222', bbox=dict(boxstyle='round,pad=0.2', facecolor='#fdfefe', edgecolor='#cccccc', lw=0.6))

ax_b.set_xlim(2006.0, 2027.5)
ax_b.set_ylim(-0.002, 0.082)
ax_b.set_xlabel("Calendar Year", fontsize=7.8, weight='bold')
ax_b.set_ylabel("Root Divergence (subs/site)", fontsize=7.8, weight='bold')
ax_b.spines['right'].set_visible(False)
ax_b.spines['top'].set_visible(False)
ax_b.grid(color='#f0f0f0', linestyle='-', linewidth=0.5, zorder=0)
ax_b.legend(loc='lower right', frameon=False, fontsize=6.0)

ax_b.text(-0.04, 1.06, "B", transform=ax_b.transAxes, fontsize=11, weight='bold', va='bottom')
ax_b.set_title("Mechanism of TreeTime Stem Compression Bias", fontsize=8.2, weight='bold', loc='left', pad=10)


# ==============================================================================
# PANEL C: Alluvial Emergence Stream (Bottom-Left)
# ==============================================================================
ax_c = fig.add_subplot(gs[1, 0])

time_grid = np.linspace(2009.2, 2026.6, 180)
bandwidth = 0.35
clade_order = [
    'Clade 3C.2a & trunk',
    'Clade 3C.3a',
    'Clade 3C.2a1b',
    'Basal Clade 2 / 1',
    'Clade 2a.1 (G.1)',
    'Clade 2b (G.2)',
    'Clade 2a.3 (J)',
    'Clade 2a.3a.1 (J.2)',
    'Subclade K (2a.3a.1)'
]

densities = np.zeros((len(clade_order), len(time_grid)))
for i, c_name in enumerate(clade_order):
    sub = df_h3[df_h3['display_group'] == c_name]
    d_vals = sub['date_x'].values
    if len(d_vals) > 0:
        diff = time_grid[:, np.newaxis] - d_vals[np.newaxis, :]
        densities[i, :] = np.exp(-0.5 * (diff / bandwidth)**2).sum(axis=1)

tot_dens = densities.sum(axis=0)
tot_dens[tot_dens == 0] = 1e-6
rel_freq = (densities / tot_dens) * 100.0
for i in range(len(clade_order)):
    rel_freq[i, :] = gaussian_filter1d(rel_freq[i, :], sigma=1.8)
rel_freq = (rel_freq / rel_freq.sum(axis=0)) * 100.0

y_stack = np.vstack([np.zeros(len(time_grid)), np.cumsum(rel_freq, axis=0)])
for i, c_name in enumerate(clade_order):
    c_col = CLADE_COLORS[c_name]
    ax_c.fill_between(time_grid, y_stack[i], y_stack[i+1], color=c_col, alpha=0.88, edgecolor='white', linewidth=0.3)

ax_c.set_xlim(2009.0, 2026.8)
ax_c.set_ylim(0, 100)
ax_c.set_xlabel("Calendar Year", fontsize=7.8, weight='bold')
ax_c.set_ylabel("Circulating Proportion (%)", fontsize=7.8, weight='bold')
ax_c.spines['right'].set_visible(False)
ax_c.spines['top'].set_visible(False)
ax_c.grid(axis='x', color='#f0f0f0', linestyle='-', linewidth=0.5, zorder=0)

ax_c.text(2014.0, 85, "3C.2a Dominance", fontsize=6.0, weight='bold', color='#ffffff', ha='center',
          bbox=dict(boxstyle='round,pad=0.15', facecolor='black', alpha=0.35, edgecolor='none'))
ax_c.text(2020.2, 50, "COVID-19\nBottleneck", fontsize=6.0, weight='bold', color='#222222', ha='center')
ax_c.text(2022.8, 70, "2a.1 / 2b", fontsize=6.0, weight='bold', color='#ffffff', ha='center',
          bbox=dict(boxstyle='round,pad=0.15', facecolor='black', alpha=0.35, edgecolor='none'))
ax_c.text(2025.8, 25, "Subclade K\nSweep", fontsize=6.0, weight='bold', color='#ffffff', ha='center',
          bbox=dict(boxstyle='round,pad=0.15', facecolor='black', alpha=0.35, edgecolor='none'))

ax_c.text(-0.04, 1.06, "C", transform=ax_c.transAxes, fontsize=11, weight='bold', va='bottom')
ax_c.set_title("Alluvial Emergence Stream: 12-Year Turnover", fontsize=8.2, weight='bold', loc='left', pad=10)


# ==============================================================================
# PANEL D: High-Leverage Triage & Outlier Quarantine (Bottom-Right)
# ==============================================================================
ax_d = fig.add_subplot(gs[1, 1])

ax_d.scatter(df_chron['leverage_hii'], df_chron['studentized_res'], s=10, color='#7f8c8d', alpha=0.45, 
             edgecolors='none', label='Nextstrain Isolates ($N=1{,}700$)')

egg_pt = df_chron[df_chron['taxon'] == 'A/Perth/16/2009-egg'].iloc[0]
wt_pt = df_chron[df_chron['taxon'] == 'A/Perth/16/2009'].iloc[0]

ax_d.scatter(egg_pt['leverage_hii'], egg_pt['studentized_res'], s=48, color='#e74c3c', marker='^', 
             edgecolors='black', linewidth=0.8, zorder=6, label='Egg Seed (Perth/16-egg)')
ax_d.scatter(wt_pt['leverage_hii'], wt_pt['studentized_res'], s=36, color='#2980b9', marker='o', 
             edgecolors='black', linewidth=0.8, zorder=6, label='Wild-Type (Perth/16)')

sus_bvbrc = triage_bvbrc[triage_bvbrc['is_sus']]
ax_d.scatter([0.0014]*len(sus_bvbrc), sus_bvbrc['studentized_residual'], s=20, color='#c0392b', 
             marker='x', alpha=0.75, linewidth=0.9, zorder=5, label='BV-BRC 10k Quarantined ($|Z|>3\\sigma$)')

ax_d.axhline(3.0, color='#e74c3c', linestyle=':', linewidth=0.9, alpha=0.8)
ax_d.axhline(-3.0, color='#e74c3c', linestyle=':', linewidth=0.9, alpha=0.8)
lev_thresh = 2 * 2 / N_taxa  # 2p/N
ax_d.axvline(lev_thresh, color='#d35400', linestyle='--', linewidth=0.8, alpha=0.7)

ax_d.annotate("A/Perth/16/2009-egg\n(Max $h_{ii}=0.0063$, 2 RBS muts)", 
              xy=(egg_pt['leverage_hii'], egg_pt['studentized_res']),
              xytext=(0.0031, -3.2),
              arrowprops=dict(arrowstyle="->", color='#e74c3c', lw=0.9),
              fontsize=6.2, weight='bold', color='#c0392b')

ax_d.text(0.0017, -9.8, "BV-BRC Frozen\nArtifacts ($Z = -10.9\\sigma$)", 
          fontsize=6.2, weight='bold', color='#c0392b')

ax_d.set_xlim(-0.0002, 0.0072)
ax_d.set_ylim(-11.5, 10.5)
ax_d.set_xlabel("Statistical Leverage ($h_{ii}$)", fontsize=7.8, weight='bold')
ax_d.set_ylabel("Studentized Residual ($Z_i$)", fontsize=7.8, weight='bold')
ax_d.spines['right'].set_visible(False)
ax_d.spines['top'].set_visible(False)
ax_d.grid(color='#f0f0f0', linestyle='-', linewidth=0.5, zorder=0)
ax_d.legend(loc='upper right', frameon=False, fontsize=5.8)

ax_d.text(-0.04, 1.06, "D", transform=ax_d.transAxes, fontsize=11, weight='bold', va='bottom')
ax_d.set_title("High-Leverage Triage & Outlier Quarantine", fontsize=8.2, weight='bold', loc='left', pad=10)

# Save figure
output_dir = Path("figures")
output_dir.mkdir(exist_ok=True)
pdf_path = output_dir / "fig_nextstrain_h3n2_multipanel.pdf"
png_path = output_dir / "fig_nextstrain_h3n2_multipanel.png"

plt.subplots_adjust(left=0.12, right=0.96, top=0.93, bottom=0.07, wspace=0.34, hspace=0.36)
plt.savefig(pdf_path)
plt.savefig(png_path, dpi=300)
print(f"[✓] Saved 4-panel publication figure to:")
print(f"    - {pdf_path}")
print(f"    - {png_path}")
