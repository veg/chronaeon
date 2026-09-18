"""
generate_h3n2_horizons_alluvial_figure.py
-----------------------------------------
Generates the publication-grade two-panel figure for Section 3:
- Panel A: ChronAeon Community Time Horizons (Closed-Form Analytical Emergence & Sampling Windows)
- Panel B: Alluvial Emergence Stream (Colored by Nextstrain Clade/Subclade)

Enforces BioVis-Expert guidelines:
- Colorblind-safe palette (Okabe-Ito / ColorBrewer)
- Clean sans-serif typography (Helvetica/Arial)
- L-frame half-open axes (no chart junk)
- Vector PDF (300+ DPI raster for dense points if needed)
"""

import os
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
from scipy.ndimage import gaussian_filter1d

# Set matplotlib publication style
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['xtick.color'] = '#333333'
plt.rcParams['ytick.color'] = '#333333'
plt.rcParams['text.color'] = '#222222'

# Load data
base_dir = Path("nextstrain_grand_challenge/h3n2_12y")
meta_path = base_dir / "data" / "metadata.csv"
hier_path = base_dir / "data" / "hierarchical_autoclock_results" / "hierarchical_classified_metadata.csv"
autoclock_json_path = base_dir / "autoclock_results.json"

meta = pd.read_csv(meta_path)
hier = pd.read_csv(hier_path)
df = pd.merge(hier, meta, left_on='id', right_on='sequence_id')

with open(autoclock_json_path) as f:
    ac_res = json.load(f)

# Cohesive color palette
CLADE_COLORS = {
    'Clade 3C.2a & trunk': '#2b5c8f',      # Deep steel blue
    'Clade 3C.3a': '#4682b4',              # Sky blue
    'Clade 3C.2a1b': '#5dade2',            # Cyan light blue
    'Basal Clade 2 / 1': '#d4ac0d',        # Warm goldenrod / amber
    'Clade 2a.1 (G.1)': '#e67e22',         # Orange
    'Clade 2b (G.2)': '#d35400',           # Rust orange / vermilion
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

df['display_group'] = df.apply(categorize_clade, axis=1)

# Set up figure canvas (Two-column width: 7.2 in x 8.0 in)
fig = plt.figure(figsize=(7.4, 7.8))
gs = gridspec.GridSpec(2, 1, height_ratios=[1.15, 1.0], hspace=0.36)

# ==============================================================================
# PANEL A: Community Time Horizons
# ==============================================================================
ax_a = fig.add_subplot(gs[0])

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
        'r2': 0.898,
        'axis_label': 'Clade 3C Trunk',
        'stat_label': 'N = 878 | μ = 3.18 × 10⁻³ / yr | R² = 0.898',
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
        'r2': 0.905,
        'axis_label': 'Clade 2 Resurgence (+28.6% Rate)',
        'stat_label': 'N = 822 | μ = 4.08 × 10⁻³ / yr | R² = 0.905',
        'is_macro': True
    },
    # Subclades of Clade 2
    {
        'id': 'Sub: Basal Clade 2 / 1',
        'group': 'Basal Clade 2 / 1',
        'n': 52,
        't_mrca': 2019.20,
        'ci': [2018.85, 2019.55],
        't_min': 2019.98,
        't_max': 2023.09,
        'mu': 2.34e-3,
        'r2': 0.661,
        'axis_label': '  └ c0.5: Basal Clade 2/1',
        'stat_label': 'N = 52 | μ = 2.34 × 10⁻³',
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
        'mu': 1.10e-3,
        'r2': 0.234,
        'axis_label': '  └ c0.0: Clade 2a.1 (G.1)',
        'stat_label': 'N = 98 | μ = 1.10 × 10⁻³',
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
        'mu': 1.76e-3,
        'r2': 0.284,
        'axis_label': '  └ c0.3: Clade 2b (G.2)',
        'stat_label': 'N = 55 | μ = 1.76 × 10⁻³',
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
        'mu': 3.30e-3,
        'r2': 0.797,
        'axis_label': '  └ c0.2: Clade 2a.3 (J)',
        'stat_label': 'N = 183 | μ = 3.30 × 10⁻³',
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
        'mu': 1.87e-3,
        'r2': 0.374,
        'axis_label': '  └ c0.1: Clade 2a.3a.1 (J.2)',
        'stat_label': 'N = 295 | μ = 1.87 × 10⁻³',
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
        'mu': 3.87e-3,
        'r2': 0.603,
        'axis_label': '  └ c0.4: Subclade K Sweep',
        'stat_label': 'N = 144 | μ = 3.87 × 10⁻³ / yr',
        'is_macro': False
    },
]

y_positions = np.arange(len(horizons_data))[::-1]

# Global root vertical line
root_mrca = 2007.29
ax_a.axvline(root_mrca, color='#c0392b', linestyle='--', linewidth=1.1, alpha=0.8, zorder=1)
ax_a.text(root_mrca + 0.12, len(horizons_data) - 0.25, 
          "Root $t_{\\mathrm{MRCA}} = 2007.29$\n[2007.05, 2007.52]", 
          fontsize=6.8, color='#c0392b', weight='bold', va='bottom', zorder=5,
          bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85, edgecolor='none'))

# Clade 2 emergence vertical line
clade2_mrca = 2018.77
ax_a.axvline(clade2_mrca, color='#8e44ad', linestyle=':', linewidth=1.0, alpha=0.7, zorder=1)
ax_a.text(clade2_mrca + 0.12, len(horizons_data) - 0.25, 
          "Clade 2 Emergence: 2018.77\n[2018.65, 2018.89]", 
          fontsize=6.8, color='#8e44ad', weight='bold', va='bottom', zorder=5,
          bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85, edgecolor='none'))

for y, h in zip(y_positions, horizons_data):
    c = CLADE_COLORS.get(h['group'], '#555555')
    bar_height = 0.38 if h['is_macro'] else 0.26
    
    # 1. Latency stem (dashed line from t_MRCA to t_min)
    ax_a.plot([h['t_mrca'], h['t_min']], [y, y], color=c, linestyle='--', linewidth=1.1, alpha=0.75, zorder=2)
    
    # 2. 95% Fieller CI shaded error band at t_MRCA
    ci_w = max(h['ci'][1] - h['ci'][0], 0.1)
    ci_patch = Rectangle((h['ci'][0], y - bar_height*0.6), ci_w, bar_height*1.2, 
                         facecolor=c, alpha=0.25, edgecolor=c, linewidth=0.7, zorder=3)
    ax_a.add_patch(ci_patch)
    
    # 3. Solid sampling duration bar [t_min, t_max]
    samp_w = h['t_max'] - h['t_min']
    samp_patch = Rectangle((h['t_min'], y - bar_height/2), samp_w, bar_height, 
                           facecolor=c, alpha=0.9, edgecolor='white', linewidth=0.5, zorder=4)
    ax_a.add_patch(samp_patch)
    
    # 4. Inferred emergence diamond marker at t_MRCA
    marker_size = 6.5 if h['is_macro'] else 5.0
    ax_a.plot(h['t_mrca'], y, marker='D', markersize=marker_size, color=c, markeredgecolor='white', 
              markeredgewidth=0.8, zorder=5)
    
    # 5. Right-hand annotation: Statistics
    ax_a.text(h['t_max'] + 0.25, y, h['stat_label'], fontsize=6.6, color='#333333', va='center', ha='left')

# Separator line between Macro and Recursive Subclades
ax_a.axhline(5.5, color='#dddddd', linestyle='-', linewidth=0.8, zorder=1)

# Axis formatting
ax_a.set_xlim(2006.5, 2030.5)
ax_a.set_ylim(-0.6, len(horizons_data) + 0.1)
ax_a.set_yticks(y_positions)
ax_a.set_yticklabels([h['axis_label'] for h in horizons_data], fontsize=7.2, weight='medium')
for tick_label, h in zip(ax_a.get_yticklabels(), horizons_data):
    if h['is_macro']:
        tick_label.set_weight('bold')
        tick_label.set_fontsize(7.6)

ax_a.set_xlabel("Calendar Year", fontsize=8.2, weight='bold')
ax_a.spines['right'].set_visible(False)
ax_a.spines['top'].set_visible(False)
ax_a.grid(axis='x', color='#f0f0f0', linestyle='-', linewidth=0.6, zorder=0)

# Legend elements for Panel A
leg_handles = [
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#444444', markersize=5.5, label='Inferred $t_{\\mathrm{MRCA}}$'),
    plt.Line2D([0], [0], color='#444444', linestyle='--', linewidth=1.1, label='Latency Stem'),
    Rectangle((0, 0), 1, 1, facecolor='#888888', alpha=0.3, edgecolor='#888888', linewidth=0.7, label='95% Fieller CI'),
    Rectangle((0, 0), 1, 1, facecolor='#888888', alpha=0.9, label='Sampling Span')
]
ax_a.legend(handles=leg_handles, loc='lower left', bbox_to_anchor=(0.0, -0.01), ncol=4, frameon=False, fontsize=6.8)

ax_a.text(-0.02, 1.08, "A", transform=ax_a.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')
ax_a.set_title("ChronAeon Community Emergence Horizons & Analytical Fieller Intervals", fontsize=9.0, weight='bold', loc='left', pad=14)


# ==============================================================================
# PANEL B: Alluvial Emergence Stream (Nextstrain Clade Frequency)
# ==============================================================================
ax_b = fig.add_subplot(gs[1])

time_grid = np.linspace(2009.2, 2026.6, 200)
bandwidth = 0.35  # years Gaussian kernel smoothing

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

for i, clade_name in enumerate(clade_order):
    sub = df[df['display_group'] == clade_name]
    dates = sub['date_x'].values
    if len(dates) > 0:
        diff = time_grid[:, np.newaxis] - dates[np.newaxis, :]
        dens = np.exp(-0.5 * (diff / bandwidth)**2).sum(axis=1)
        densities[i, :] = dens

total_density = densities.sum(axis=0)
total_density[total_density == 0] = 1e-6
relative_freq = (densities / total_density) * 100.0

for i in range(len(clade_order)):
    relative_freq[i, :] = gaussian_filter1d(relative_freq[i, :], sigma=2.0)

total_smooth = relative_freq.sum(axis=0)
relative_freq = (relative_freq / total_smooth) * 100.0

y_stack = np.vstack([np.zeros(len(time_grid)), np.cumsum(relative_freq, axis=0)])

for i, clade_name in enumerate(clade_order):
    c = CLADE_COLORS[clade_name]
    ax_b.fill_between(time_grid, y_stack[i], y_stack[i+1], color=c, alpha=0.88, edgecolor='white', linewidth=0.4)

ax_b.set_xlim(2009.0, 2026.8)
ax_b.set_ylim(0, 100)
ax_b.set_xlabel("Calendar Year", fontsize=8.2, weight='bold')
ax_b.set_ylabel("Circulating Proportion (%)", fontsize=8.2, weight='bold')
ax_b.spines['right'].set_visible(False)
ax_b.spines['top'].set_visible(False)
ax_b.grid(axis='x', color='#f0f0f0', linestyle='-', linewidth=0.6, zorder=0)

milestones = [
    (2013.5, 88, "Clade 3C.2a Dominance", '#ffffff'),
    (2018.5, 45, "3C.2a1b Wave", '#ffffff'),
    (2020.2, 50, "COVID-19\nBottleneck", '#222222'),
    (2022.6, 75, "Clade 2a.1 / 2b", '#ffffff'),
    (2024.2, 55, "Clade 2a.3a.1 (J.2)", '#ffffff'),
    (2025.8, 25, "Subclade K\nSweep", '#ffffff'),
]

for mx, my, mtxt, mcol in milestones:
    ax_b.text(mx, my, mtxt, fontsize=6.6, weight='bold', color=mcol, ha='center', va='center',
              bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.35, edgecolor='none') if mcol == '#ffffff' else None)

handles = [Rectangle((0, 0), 1, 1, color=CLADE_COLORS[c]) for c in clade_order]
labels = [c.replace(' (2a.3a.1)', '') for c in clade_order]
ax_b.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1.01, 0.5), 
            frameon=False, fontsize=6.6, title="Nextstrain Clade / Subclade", title_fontsize=7.0)

ax_b.text(-0.02, 1.08, "B", transform=ax_b.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')
ax_b.set_title("Alluvial Emergence Stream: 12-Year Antigenic Turnover & Clade Replacement", fontsize=9.0, weight='bold', loc='left', pad=14)

# Save figure
output_dir = Path("figures")
output_dir.mkdir(exist_ok=True)
pdf_path = output_dir / "fig_nextstrain_h3n2_horizons_alluvial.pdf"
png_path = output_dir / "fig_nextstrain_h3n2_horizons_alluvial.png"

plt.subplots_adjust(left=0.26, right=0.82, top=0.93, bottom=0.07, hspace=0.38)
plt.savefig(pdf_path)
plt.savefig(png_path, dpi=300)
print(f"[✓] Saved publication figure to:")
print(f"    - {pdf_path}")
print(f"    - {png_path}")
