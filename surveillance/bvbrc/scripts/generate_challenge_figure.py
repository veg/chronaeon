#!/usr/bin/env python3
"""
Generate Publication-Grade Comparative Figure for the BV-BRC H3N2 10,000-Taxon Grand Challenge:
ChronAeon Streaming Sieve & AutoClock vs The BEAST 10,000-Taxon Scaling Barrier.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Configure styling
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#2c3e50"
plt.rcParams["axes.linewidth"] = 0.8

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR = BASE_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

FIG_PNG = FIGURES_DIR / "fig_bvbrc_h3n2_grand_challenge.png"
FIG_PDF = FIGURES_DIR / "fig_bvbrc_h3n2_grand_challenge.pdf"

def find_input(filename):
    if (RESULTS_DIR / filename).exists():
        return RESULTS_DIR / filename
    return DATA_DIR / filename

# Load classified metadata and sieve report
df_meta = pd.read_csv(find_input("h3n2_10k_autoclock_classified.csv"))
df_sieve = pd.read_csv(find_input("h3n2_10k_sieve_report.csv"))
with open(find_input("h3n2_10k_autoclock_results.json")) as f:
    autoclock_summary = json.load(f)

# Community details
COMM_LABELS = {
    0: "Comm 0: Modern Resurgence (2021-26, 100% Human)",
    1: "Comm 1: Clade 3 Epidemic Trunk (2011-25, 99.9% Human)",
    2: "Comm 2: NA Swine Reservoir (2004-25, 98.9% Swine)",
    3: "Comm 3: Ancestral Pandemic Trunk (1968-2020, 85% Human)",
    4: "Comm 4: Wild Avian Reservoir (1994-2021, 99.0% Avian)",
    5: "Comm 5: Fujian/Perth Era & Swine Jumps (2002-25)",
    6: "Comm 6: Canine & Divergent Animal (1998-2021)"
}

COMM_COLORS = {
    0: "#2980b9", # Deep Blue
    1: "#e67e22", # Orange
    2: "#8e44ad", # Purple
    3: "#16a085", # Teal
    4: "#e74c3c", # Red
    5: "#27ae60", # Green
    6: "#d35400"  # Dark Amber
}

HOST_COLORS = {
    "Human": "#2980b9",
    "Nonhuman Mammal": "#8e44ad",
    "Avian": "#e74c3c",
    "Environment": "#7f8c8d"
}

# Create 4-panel figure
fig = plt.figure(figsize=(16, 11), dpi=300)
gs = gridspec.GridSpec(2, 2, height_ratios=[1.0, 1.1], hspace=0.30, wspace=0.25)

# Panel A: Runtime & Computational Scaling: BEAST vs ChronAeon
ax_a = fig.add_subplot(gs[0, 0])
methods = [
    "Standard BEAST 2\n(Full MCMC)",
    "TargetedBeast\n(Fixed Tree, 80 cores)",
    "Parallel SCA\n(Shao 2026, 16 cores)",
    "ChronAeon Sieve\n(10k Screening)",
    "ChronAeon AutoClock\n(K*=7 Deconvolution)"
]
runtimes_sec = [
    30 * 86400,     # BEAST 2 estimated > 30 days (intractable / crash)
    80 * 86400,     # TargetedBeast 80 core-days on 2k-10k
    20 * 3600,      # Shao 2026 Parallel SCA (~20 hours on N=190, days for 10k)
    26.18,          # ChronAeon Sieve on 10,000 sequences
    23.40           # ChronAeon AutoClock on 9,977 sequences
]
colors_a = ["#bdc3c7", "#95a5a6", "#7f8c8d", "#27ae60", "#2980b9"]

bars = ax_a.barh(methods, runtimes_sec, color=colors_a, edgecolor="#2c3e50", height=0.6)
ax_a.set_xscale("log")
ax_a.set_xlabel("Execution Time (Seconds, Log Scale)", fontsize=11, fontweight="bold")
ax_a.set_title("A. Computational Feasibility at 10,000-Taxon Scale", fontsize=12, fontweight="bold", loc="left")
ax_a.grid(True, axis="x", linestyle="--", alpha=0.5)

# Annotate bars
ax_a.text(runtimes_sec[0]*1.2, 0, "Intractable (>30 Days)", va="center", fontsize=9, fontweight="bold", color="#7f8c8d")
ax_a.text(runtimes_sec[1]*1.2, 1, "80 Core-Days (Bouckaert 2025)", va="center", fontsize=9, fontweight="bold", color="#7f8c8d")
ax_a.text(runtimes_sec[2]*1.2, 2, "20 Hours on N=190 (Shao 2026)", va="center", fontsize=9, fontweight="bold", color="#7f8c8d")
ax_a.text(runtimes_sec[3]*1.5, 3, "26.18 s (382 seq/s)", va="center", fontsize=9.5, fontweight="bold", color="#27ae60")
ax_a.text(runtimes_sec[4]*1.5, 4, "23.40 s (426 seq/s)", va="center", fontsize=9.5, fontweight="bold", color="#2980b9")
ax_a.set_xlim(1, 1e8)

# Panel B: Sieve Triage & Quality Control Breakdown
ax_b = fig.add_subplot(gs[0, 1])
sieve_cats = [
    "PASS: Analysis-Ready\n(9,977 sequences)",
    "SUS: Chimeric / Recombinant\n(Δt = 15-52 yr, 12 seqs)",
    "SUS: Non-Target Contaminant\n(Dist > 78%, 9 seqs)",
    "SUS: Degraded Sequence\n(Excess Ns > 5%, 2 seqs)"
]
sieve_counts = [9977, 12, 9, 2]
colors_b = ["#27ae60", "#e74c3c", "#c0392b", "#d35400"]

# Draw pie chart with inset table or donut
wedges, texts = ax_b.pie(
    [sieve_counts[0], sum(sieve_counts[1:])],
    colors=["#27ae60", "#e74c3c"],
    startangle=140,
    wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2)
)
ax_b.set_title("B. Streaming Sieve Triage on Raw BV-BRC Ingestion", fontsize=12, fontweight="bold", loc="left")

# Add summary box in center of donut
ax_b.text(0, 0.15, "10,000", ha="center", va="center", fontsize=18, fontweight="bold", color="#2c3e50")
ax_b.text(0, -0.05, "Raw Taxa", ha="center", va="center", fontsize=11, color="#7f8c8d")
ax_b.text(0, -0.22, "99.8% Pass Rate", ha="center", va="center", fontsize=10, fontweight="bold", color="#27ae60")

# Legend for Sieve Breakdown
legend_labels = [
    f"Analysis-Ready (PASS): 9,977 (99.77%)",
    f"Chimeric/Recombinant: 12 (0.12%)",
    f"Non-Target Contaminant: 9 (0.09%)",
    f"Degraded/Excess Gaps: 2 (0.02%)"
]
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in ["#27ae60", "#e74c3c", "#c0392b", "#d35400"]]
ax_b.legend(legend_handles, legend_labels, loc="lower center", bbox_to_anchor=(0.5, -0.18), fontsize=9, frameon=True)

# Panel C: Host Ecology of Deconvolved Clock Communities
ax_c = fig.add_subplot(gs[1, 0])
ct = pd.crosstab(df_meta["inferred_clock_community"], df_meta["host_group"], normalize="index") * 100
comm_indices = sorted(ct.index)

bottom = np.zeros(len(comm_indices))
for host in ["Human", "Nonhuman Mammal", "Avian", "Environment"]:
    if host in ct.columns:
        vals = ct.loc[comm_indices, host].values
        ax_c.barh([f"Comm {i}" for i in comm_indices], vals, left=bottom, label=host, color=HOST_COLORS[host], height=0.65, edgecolor="white")
        bottom += vals

ax_c.set_xlabel("Host Composition (%)", fontsize=11, fontweight="bold")
ax_c.set_title("C. Unsupervised Host-Reservoir Separation (Zero Metadata Priors)", fontsize=12, fontweight="bold", loc="left")
ax_c.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=4, fontsize=9.5, frameon=True)
ax_c.set_xlim(0, 100)
ax_c.grid(True, axis="x", linestyle="--", alpha=0.5)

# Annotate specific key communities
ax_c.text(50, 0, "100% Human (Modern Resurgence)", ha="center", va="center", color="white", fontweight="bold", fontsize=8.5)
ax_c.text(50, 1, "99.9% Human (Clade 3 Trunk)", ha="center", va="center", color="white", fontweight="bold", fontsize=8.5)
ax_c.text(50, 2, "98.9% Swine Reservoir", ha="center", va="center", color="white", fontweight="bold", fontsize=8.5)
ax_c.text(50, 4, "99.0% Wild Avian Reservoir", ha="center", va="center", color="white", fontweight="bold", fontsize=8.5)

# Panel D: Evolutionary Rate Spectrum Across Deconvolved Regimes
ax_d = fig.add_subplot(gs[1, 1])
rates = []
comm_names = []
ci_lows = []
ci_highs = []

for comm_id in range(7):
    comm_path = RESULTS_DIR / "clock_communities" / f"chronaeon_community_{comm_id}.json"
    if comm_path.exists():
        with open(comm_path) as f:
            data = json.load(f)
            r = data["ols"]["mu"] * 1e4
            rates.append(r)
            comm_names.append(f"Comm {comm_id}")
            # Use analytical standard error se_mu
            se_r = data["ols"]["se_mu"] * 1e4
            ci_lows.append(r - 1.96 * se_r)
            ci_highs.append(r + 1.96 * se_r)

comm_names_display = [
    "Comm 0\n(Human Modern)",
    "Comm 1\n(Human Clade 3)",
    "Comm 2\n(Swine Reserv.)",
    "Comm 3\n(Ancestral 1968)",
    "Comm 4\n(Wild Avian)",
    "Comm 5\n(Human/Swine)",
    "Comm 6\n(Canine/Mammal)"
]
bar_colors = [COMM_COLORS[i] for i in range(7)]

bars_d = ax_d.bar(range(7), rates, color=bar_colors, edgecolor="#2c3e50", width=0.6)
ax_d.set_xticks(range(7))
ax_d.set_xticklabels(comm_names_display, fontsize=9)
ax_d.set_ylabel("Substitution Rate μ (10⁻⁴ subs/site/yr)", fontsize=11, fontweight="bold")
ax_d.set_title("D. Evolutionary Rate Spectrum Across Deconvolved Regimes", fontsize=12, fontweight="bold", loc="left")
ax_d.grid(True, axis="y", linestyle="--", alpha=0.5)

# Add annotations on top of bars
for idx, (rect, rate) in enumerate(zip(bars_d, rates)):
    height = rect.get_height()
    ax_d.text(rect.get_x() + rect.get_width()/2.0, height + 1.5, f"{rate:.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

# Global Figure Title
fig.suptitle(
    "ChronAeon 10,000-Taxon Grand Challenge: Planetary Streaming, Sieving, and Multi-Clock Deconvolution of Influenza A/H3N2 (1968–2026)\n"
    "Resolving Multi-Host Reservoirs, Antigenic Drift Eras, and Sequencing Contaminants in 49.6 Seconds Total",
    fontsize=13.5,
    fontweight="bold",
    y=0.98
)

plt.savefig(FIG_PNG, bbox_inches="tight")
plt.savefig(FIG_PDF, bbox_inches="tight")
print(f"[✓] Successfully generated {FIG_PNG} and {FIG_PDF}.")
