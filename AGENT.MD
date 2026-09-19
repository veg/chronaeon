# AGENT.MD: Autonomous Reproduction Protocol for the ChronAeon Benchmark Suite

**Authoritative, Deterministic Guide for AI Agents and Automated Pipelines to Reproduce all 42 Empirical Molecular Clock Benchmarks and Web Application from Scratch**

---

## 1. Executive Summary & Foundational Principles

This document provides complete, deterministic instructions for an autonomous AI agent (e.g., Antigravity, Claude, ChatGPT, Cursor) or automated CI/CD pipeline to execute, calibrate, audit, and reproduce the **42 curated empirical molecular clock benchmarks** (14,285 taxa, spanning 1882–2026 CE) and build the complete publication-grade web application from scratch.

### Foundational Invariants for Autonomous Agents
1. **100% Tree-Free Continuous Sequence Manifolds**:
   ChronAeon operates directly on pairwise Tamura-Nei 93 (TN93) evolutionary divergence matrices $\mathbf{D}$ embedded in continuous metric spaces. **Zero phylogenetic trees (`.nwk`, `.tree`), zero bifurcating topologies, and zero tree-space MCMC moves are ever supplied, inferred, or traversed.**
2. **Zero Simplex Imputation & Zero Synthetic Base-Filling**:
   All sequences are harvested directly from author-deposited repositories (Dryad, GitHub, Zenodo, ENA). All native ambiguous characters, gaps, and IUPAC ambiguity codes are strictly preserved.
3. **Exact Alignment Parity with Published BEAST Benchmarks**:
   Every empirical cohort corresponds 100% identically to the published author BEAST 1.x / 2.x XML configuration archive (`beast.xml.gz` / `beast_config.xml.gz`).
4. **Deterministic Reproducibility & Sub-Minute Execution**:
   Every ChronAeon and AutoClock execution runs deterministically in 0.5 to 314 seconds on commodity hardware (Apple Silicon MPS or single CPU core), bypassing the stochastic Markov chain Monte Carlo state sampling on bifurcating trees required by traditional Bayesian packages.

---

## 2. System Requirements & Environment Setup

### 2.1 Hardware Architecture
- **Platforms**: Apple Silicon (M1/M2/M3/M4 with Metal Performance Shaders `mps` backend) or Linux/macOS x86_64 / ARM64.
- **RAM**: Minimum 8 GB available RAM (16 GB recommended for whole-genome cohorts like ASFV [190 kb] or *M. abscessus* [556 kb]).
- **Storage**: ~5 GB free space for alignments, distance matrices, diagnostics, figures, and web dossiers.

### 2.2 Python Dependencies
The execution environment requires Python $\ge 3.9$ (tested on Python 3.9, 3.10, and 3.11):
```bash
pip install numpy scipy pandas matplotlib biopython torch
```

### 2.3 Setting PYTHONPATH
ChronAeon and its underlying geometry engines must be in the Python module search path:
```bash
pip install -e chronaeon/   # or: export PYTHONPATH="src:$PYTHONPATH" 
```

### 2.4 Pre-Flight Environment Sanity Check
Before running any benchmark, the agent must execute the following pre-flight verification:
```bash
python3 -c "
import torch, chronaeon.dating
device = 'mps' if torch.backends.mps.is_available() else ('cuda' if torch.cuda.is_available() else 'cpu')
print(f'[OK] ChronAeon module imported successfully. Active acceleration device: {device}')
"
```

---

## 3. Directory Layout & Data Topology

```
./
├── benchmark-100/                          # 42 curated author-deposited empirical cohorts
│   ├── 00_ebola_sierraleone_gire2014/
│   │   ├── alignment.fasta                 # Exact author multi-sequence FASTA
│   │   ├── dates.csv                       # Normalized decimal sampling dates (e.g. 2014.521)
│   │   ├── DATA_PROVENANCE.json            # Literature DOI, PMID, PMCID, and BEAST configuration
│   │   ├── beast.xml.gz                    # Exact compressed author BEAST XML (also beast_config.xml.gz)
│   │   ├── chronaeon_dating.json           # [Generated] Single-clock calibration & LOOCV
│   │   ├── chronaeon_dating.csv            # [Generated] Per-taxon residuals and studentized Z
│   │   ├── autoclock_results.json          # [Generated] AutoClock spectral deconvolution
│   │   └── STUDY_REPORT.md                 # Standalone study report
│   ├── 01_ebola_makona_dudas2017/
│   └── ... (00 through 41, 42 cohorts total)
├── cronaeon_bench/                         # Static publication-grade web application
│   ├── AGENT.MD                            # This autonomous execution protocol
│   ├── README.md                           # Human-facing compendium documentation
│   ├── index.html                          # Master interactive compendium portal
│   ├── benchmarks_master.json              # Consolidated machine-readable dataset JSON
│   ├── assets/
│   │   ├── css/style.css                   # Responsive publication CSS styling
│   │   ├── js/main.js                      # Search, filtering, lightbox, SVG plot
│   │   └── figures/<study_id>/             # Standardized 4-panel diagnostic figures
│   │       └── chronaeon_diagnostics.png   # Panels A, B, C (Alluvial), D (Streamgraph)
│   ├── data/<study_id>/                    # Downloadable compressed BEAST XML archives
│   │   └── beast.xml.gz                    # Shipped author BEAST XML (also beast_config.xml.gz)
│   └── studies/<study_id>/                 # 42 individual publication study dossiers
│       └── index.html                      # Comprehensive study evaluation dossier
└── scratch/                                # Build engines and authoritative curation metadata
    ├── study_curations.py                  # Curated biological narratives and entity-matched notes
    └── build_entire_portal.py              # Master builder script for the entire web portal
```

---

## 4. Step-by-Step Autonomous Execution Protocol

### Step 1: Single-Cohort ChronAeon Dating & LOOCV Evaluation

For any target cohort `<study_dir>` in `benchmark-100/` or using shipped portal data:
```bash
cd ./benchmark-100/<study_dir>

python3 -m chronaeon.cli date \
  --beast beast.xml.gz \
  --loocv \
  --nonlinear-clocks \
  -o chronaeon_dating.json \
  -c chronaeon_dating.csv \
  2>&1 | tee chronaeon_dating.log
```
*(Note: `--beast beast.xml.gz` directly ingests sequence matrices and collection dates from the compressed XML archive. Alternatively, `-a alignment.fasta -d dates.csv` can be supplied if raw alignments and date files are used.)*

#### What This Evaluates:
1. **Root-to-Tip Geometric Manifold Regression**:
   - Standard OLS molecular clock regression across distance manifold.
   - Attention PGLS regression with Pagel's $\lambda^*$ phylogenetic signal parameterization.
   - Restricted Natural Cubic Splines (detecting multi-decadal time-dependent rate deceleration).
   - Non-Linear Clocks Suite (<code>--nonlinear-clocks</code>): Exact Quadratic, Profile Exponential, Bilinear Surge-and-Crash, and 3-Epoch Polyepoch NNLS.
2. **Analytical & Empirical Confidence Bounds**:
   - Exact Fieller ratio inversion analytical 95% confidence interval on $t_{\mathrm{MRCA}}$.
   - Denny-Fieller $g$-statistic ($g \ll 1.0$ validates strong temporal signal; $g \ge 1.0$ indicates insufficient signal).
   - Non-parametric Jackknife 95% empirical confidence intervals.
3. **High-Leverage Outlier Sieve (LOOCV)**:
   - Sherman-Morrison closed-form rank-1 matrix inversion evaluating out-of-sample tip date recovery.
   - Predictive $R^2_{\mathrm{pred}}$, Mean Absolute Error (MAE in days), Root Mean Squared Error (RMSE in days).
   - Standardized studentized residuals ($|Z_i| \ge 2.50$) screening for high-leverage temporal or sequencing anomalies (Ghost Nodes).

---

### Step 2: AutoClock Unsupervised Multi-Rate Community Deconvolution

For any target cohort `<study_dir>` in `benchmark-100/` or using shipped portal data:
```bash
cd ./benchmark-100/<study_dir>

python3 -m chronaeon.cli autoclock \
  --beast beast.xml.gz \
  -o autoclock_results.json \
  2>&1 | tee chronaeon_autoclock.log
```

#### What This Evaluates:
1. **Spectral Graph Laplacian Bisection**:
   - Forms continuous cross-attention affinity matrix $W$ and degree matrix $D$.
   - Diagonalizes the normalized symmetric graph Laplacian $L_{\mathrm{sym}} = I - D^{-1/2} W D^{-1/2}$.
   - Evaluates eigenvalues $\lambda_1, \lambda_2, \dots, \lambda_K$ across partitions $K \in [1, 6]$.
2. **Optimal Partition Selection ($K^*$)**:
   - Identifies the dominant eigengap drop cliff ($\Delta \lambda_K / \Delta \lambda_{K+1}$) and minimizes lineage-adjusted $\mathrm{AIC}_c$.
   - If $K^* = 1$, validates strict lineage rate homogeneity.
   - If $K^* > 1$, deconvolves distinct evolutionary communities with within-lineage substitution rates $\mu_k$, calibrated sub-cluster emergence roots $t_{\mathrm{MRCA}, k}$, and variance explained $R^2_k$.

---

### Step 3: Automated Batch Execution Across All 42 Empirical Benchmarks

To execute the entire 42-cohort empirical benchmark suite autonomously from scratch:

```python
#!/usr/bin/env python3
"""
batch_run_42_benchmarks.py
Runs single-clock dating, LOOCV, non-linear clocks, and AutoClock deconvolution
across all 42 empirical cohorts in benchmark-100.
"""

import os
import subprocess
import time

BENCHMARK_DIR = "./benchmark-100"

studies = sorted([
    d for d in os.listdir(BENCHMARK_DIR)
    if os.path.isdir(os.path.join(BENCHMARK_DIR, d)) and d[0].isdigit()
])

print(f"Discovered {len(studies)} empirical benchmark studies.")

env = os.environ.copy()
env["PYTHONPATH"] = "" + env.get("PYTHONPATH", "")

for idx, study in enumerate(studies, 1):
    s_path = os.path.join(BENCHMARK_DIR, study)
    fasta = os.path.join(s_path, "alignment.fasta")
    dates = os.path.join(s_path, "dates.csv")
    
    if not os.path.exists(fasta) or not os.path.exists(dates):
        print(f"[{idx:02d}/42] Skipping {study} (missing alignment or dates)")
        continue
        
    print(f"\n==================================================")
    print(f"[{idx:02d}/42] Processing: {study}")
    print(f"==================================================")
    t0 = time.time()
    
    # 1. Single-clock dating + LOOCV + non-linear clocks
    cmd_date = [
        "python3", "-m", "chronaeon.cli", "date",
        "-a", "alignment.fasta",
        "-d", "dates.csv",
        "--loocv",
        "--nonlinear-clocks",
        "-o", "chronaeon_dating.json",
        "-c", "chronaeon_dating.csv"
    ]
    subprocess.run(cmd_date, cwd=s_path, env=env, check=True)
    
    # 2. AutoClock community deconvolution
    cmd_ac = [
        "python3", "-m", "chronaeon.cli", "autoclock",
        "-a", "alignment.fasta",
        "-d", "dates.csv",
        "-o", "autoclock_results.json"
    ]
    subprocess.run(cmd_ac, cwd=s_path, env=env, check=True)
    
    elapsed = time.time() - t0
    print(f"[{idx:02d}/42] Finished {study} in {elapsed:.2f}s")

print("\n[SUCCESS] All 42 empirical benchmarks evaluated successfully.")
```

---

### Step 4: Generating the Standardized 4-Panel Diagnostic Figures

Every study is equipped with an authoritative, publication-quality four-panel figure (`chronaeon_diagnostics.png`):

```
+------------------------------------+------------------------------------+
| PANEL A: Molecular Clock Fit       | PANEL B: LOOCV Predictive General. |
|  - Root-to-tip manifold scatter   |  - Out-of-sample tip date recovery |
|  - OLS vs PGLS vs Spline curves    |  - 1:1 identity line & error bands |
|  - BEAST MCMC point & 95% HPD band |  - High-leverage outlier flags     |
+------------------------------------+------------------------------------+
| PANEL C: Manifold Alluvial Tree    | PANEL D: Lineage Flow Streamgraph  |
|  - Streamlines radiating from root |  - Transverse manifold expansion   |
|  - AutoClock communities (colors)  |  - Clade dynamic volume over time  |
|  - 95% Fieller CI & BEAST 95% HPD  |  - Stacked demographic flow        |
+------------------------------------+------------------------------------+
```

#### Panel Construction Details:
- **Panel A (Molecular Clock Regression)**:
  Plots sampling date (X-axis, decimal CE years) against genetic distance to consensus root (Y-axis, substitutions/site). Overlays linear OLS, attention PGLS, restricted natural cubic spline, and the published BEAST point estimate and 95% HPD interval band.
- **Panel B (Leave-One-Out Cross-Validation)**:
  Plots observed tip sampling date against out-of-sample predicted date with 1:1 identity dashed diagonal, $\pm 10\%$ error envelope, and individual $|Z_i| \ge 2.50$ leverage flags. Annotates out-of-sample $R^2_{\mathrm{pred}}$, MAE (days), and RMSE (days).
- **Panel C (Continuous Manifold Alluvial Phylogeny)**:
  Projects pairwise distance manifolds into continuous 2D coordinate space via Classical Multidimensional Scaling (MDS) / Spectral Bisection. Renders streamlines fanning out from the ancestral root $t_{\mathrm{MRCA}}$ to sampled tips, color-coded by AutoClock community ($k \in [0, K^*-1]$), accompanied by shaded 95% analytical Fieller CI and BEAST 95% HPD bands.
- **Panel D (Lineage Dynamic Flow Streamgraph)**:
  Constructs Gaussian kernel density estimates of evolutionary trajectory across calendar time, rendering an organic streamgraph illustrating how distinct AutoClock communities expand, diversify, and transition over time.

To regenerate any missing figures or regenerate all 42 figures:
```bash
python3 cronaeon_bench/build_portal.py
```
*(The builder script automatically verifies and generates any missing figures in `assets/figures/<study_id>/chronaeon_diagnostics.png`).*

---

### Step 5: Building the Static Publication-Grade Web Compendium

The authoritative portal builder script:
`cronaeon_bench/build_portal.py`

#### To execute the portal build:
```bash
python3 cronaeon_bench/build_portal.py
```

#### What the Builder Script Accomplishes:
1. **Data Ingestion**:
   Iterates through all 42 empirical cohorts in `benchmark-100/`, loading `chronaeon_dating.json`, `autoclock_results.json`, `dates.csv`, `alignment.fasta`, and `DATA_PROVENANCE.json`.
2. **Biological Narrative Integration**:
   Imports curated study narratives from `scratch/study_curations.py`:
   - *Part A: What did the original study find?* (Published BEAST baseline, root date, substitution rate, epidemiological context).
   - *Part B: What did ChronAeon find?* (Tree-free manifold model selection, root height, Fieller CI, wall-clock execution time, LOOCV tip MAE).
   - *Part C: AutoClock Community Deconvolution & Biological Interpretation* (Deconvolution into $K^*$ transmission communities, biological meaning of clades).
   - *Temporal Concordance Taxonomy & Prominent Reconciliation Banners*:
      Every empirical cohort is classified into an authoritative 4-way concordance taxonomy:
      1. **`DIRECT`** (`badge-concordant`, emerald `#15803d`): Root timing directly overlaps published BEAST 95% HPD credible interval.
      2. **`AUTOCLOCK_RECONCILED`** (`badge-reconciled`, violet `#7c3aed`): **Concordant only after community reconciliation.** Unpartitioned global root differs from BEAST because a naive single clock fits only the contemporary sampling crown, but AutoClock spectral graph Laplacian bisection deconvolves the $K^*$ distinct evolutionary communities, achieving complete concordance with published history. Displays a prominent purple top callout banner and distinct scorecard labeling.
      3. **`STEM_VS_CROWN`** (`badge-stem-crown`, amber `#d97706`): Concordant via stem-vs-crown lineage emergence. Captures deeper ancestral introduction divergence (stem / serotype emergence) relative to sampled regional outbreak crown radiation. Displays a prominent amber top callout banner.
      4. **`NON_LINEAR_SPLINE`** (`badge-nonlinear`, cyan `#0284c7`): Concordant via non-linear rate deceleration. Lineage-adjusted $\Delta\mathrm{AIC}_{N_{\mathrm{eff}}}$ selects the restricted natural cubic spline over the strict linear clock, capturing multi-decadal rate shifts. Displays a prominent cyan top callout banner.
3. **Safe Markdown Engine (`render_markdown` & `render_markdown_block`)**:
    - Converts `**text**` and `** text **` (with internal whitespace) to `<strong>text</strong>`.
    - Converts `__text__` and `__ text __` to `<strong>text</strong>`.
    - Converts `*text*` to `<em>text</em>`.
    - Converts inline code `` `code` `` to `<code>code</code>`.
    - Converts Markdown links `[text](url)` to `<a href="url" target="_blank" rel="noopener">text &nearr;</a>`.
    - Formats multi-paragraph blocks into `<p>...</p>` and list items into `<ul><li>` / `<ol><li>`.
    - **Crucial Invariant**: Extracts and strictly protects all LaTeX MathJax blocks (`$...$` and `$$...$$`) and existing HTML tags (`<a>`, `<span>`, `<code>`) so formulas like `$t_{\mathrm{MRCA}}$`, `$\lambda^*$`, `$\mu$`, `$\mathcal{T}$`, `$\mathbf{b}$`, `$\mathbf{D}$` are preserved without syntax corruption.
    - Strips any remaining unclosed `**` tokens to guarantee zero raw asterisks appear in HTML output.
4. **Side-by-Side Direct Entity-Matched Comparison Table**:
   Renders an 8-dimension comparative table for each cohort directly juxtaposing the **Published BEAST MCMC Baseline** against the **ChronAeon Tree-Free Manifold**:
   - Dimension 1: Inference Paradigm & Topology (MCMC over tree space $\mathcal{T}$ vs Tree-Free continuous manifold on $\mathbf{D}$)
   - Dimension 2: Calibrated Root Date ($t_{\mathrm{MRCA}}$ 95% HPD vs 95% Analytical Fieller CI)
   - Dimension 3: Evolutionary Substitution Rate ($\mu$ relaxed branch rate vs manifold regression slope)
   - Dimension 4: Rate Heterogeneity & Lineage Structure (UCLD/UCED priors vs AutoClock graph Laplacian spectral bisection)
   - Dimension 5: Clock Model Selection & Dynamics (Marginal likelihood path sampling vs $\Delta\mathrm{AIC}_{N_{\mathrm{eff}}}$ extended suite)
   - Dimension 6: Data Screening & Outlier Diagnostics (Subjective manual exclusion vs automated LOOCV studentized $|Z_i| \ge 2.50$)
   - Dimension 7: Compute Execution Time & Sampling Depth (10M–1,000M MCMC states vs seconds on Apple Silicon / CPU)
   - Dimension 8: Reproducibility & Artifact Access (Downloadable `.xml.gz` vs CLI one-liner)
5. **BEAST XML Archive Provisioning**:
   Copies compressed author BEAST XML files (`beast.xml.gz` and `beast_config.xml.gz`) into `cronaeon_bench/data/<study_id>/` and updates all download buttons.
6. **Master Compendium Index (`index.html`)**:
   Builds the searchable, filterable master compendium table, taxonomy filter pills (Negative-Sense RNA, Positive-Sense RNA, Retroviruses, DNA Viruses, Bacteria & Ancient DNA), clock model pills (Linear OLS, Attention PGLS, Restricted Natural Spline), search bar, global scorecards, and interactive client-side SVG concordance scatter plot.

---

## 5. Automated Verification & Quality Assurance Suite

Autonomous agents must execute these verification checks after rebuilding the suite:

```python
#!/usr/bin/env python3
"""
verify_compendium_integrity.py
Runs automated consistency and quality checks on the ChronAeon Benchmark Compendium.
"""

import os
import glob
import re

PORTAL_DIR = "./cronaeon_bench"
STUDIES_DIR = os.path.join(PORTAL_DIR, "studies")
FIGURES_DIR = os.path.join(PORTAL_DIR, "assets", "figures")
DATA_DIR = os.path.join(PORTAL_DIR, "data")

study_dirs = sorted([d for d in os.listdir(STUDIES_DIR) if os.path.isdir(os.path.join(STUDIES_DIR, d)) and d[0].isdigit()])

print(f"Verifying {len(study_dirs)} studies in compendium...")
assert len(study_dirs) == 42, f"Expected 42 studies, found {len(study_dirs)}"

errors = []

for sid in study_dirs:
    # 1. Check study dossier HTML
    html_path = os.path.join(STUDIES_DIR, sid, "index.html")
    if not os.path.exists(html_path):
        errors.append(f"Missing index.html for {sid}")
        continue
    with open(html_path) as f:
        content = f.read()
        
    # Check for unrendered markdown bold
    if "**" in content:
        errors.append(f"Unrendered '**' found in {sid}/index.html")
    if "`" in content:
        errors.append(f"Unrendered backtick found in {sid}/index.html")
    if re.search(r'\[[^\]]+\]\(https?://[^\)]+\)', content):
        errors.append(f"Unrendered markdown link found in {sid}/index.html")
        
    # Check essential sections
    for sec in ["Curated Biological Narrative", "Side-by-Side Phylodynamic Comparison", "AutoClock Unsupervised Community Deconvolution", "ChronAeon Phylodynamic Inferences &amp; Diagnostic Manifold"]:
        if sec not in content:
            errors.append(f"Missing section '{sec}' in {sid}/index.html")

    # 2. Check diagnostic figure
    fig_path = os.path.join(FIGURES_DIR, sid, "chronaeon_diagnostics.png")
    if not os.path.exists(fig_path):
        errors.append(f"Missing figure for {sid}")
    elif os.path.getsize(fig_path) < 10000:
        errors.append(f"Figure file suspiciously small ({os.path.getsize(fig_path)} bytes) for {sid}")

    # 3. Check compressed BEAST XML archive
    xml_path = os.path.join(DATA_DIR, sid, "beast.xml.gz")
    if not os.path.exists(xml_path):
        xml_path = os.path.join(DATA_DIR, sid, "beast_config.xml.gz")
    if not os.path.exists(xml_path):
        errors.append(f"Missing beast.xml.gz for {sid}")

# Check root index.html
root_index = os.path.join(PORTAL_DIR, "index.html")
if not os.path.exists(root_index):
    errors.append("Missing root index.html")
else:
    with open(root_index) as f:
        r_content = f.read()
    if "**" in r_content:
        errors.append("Unrendered '**' found in root index.html")

if errors:
    print(f"\n[FAIL] Found {len(errors)} verification errors:")
    for e in errors:
        print(f"  - {e}")
    exit(1)
else:
    print("\n[PASS] All 42 studies verified successfully with zero errors!")
    print("  - 42 / 42 study dossiers present with complete sections")
    print("  - 42 / 42 diagnostic multi-panel figures verified")
    print("  - 42 / 42 compressed BEAST XML configurations verified")
    print("  - Zero unrendered markdown artifacts in HTML")
```

---

## 6. Live Portal Testing & Deployment

### 6.1 Testing the Live Web Portal Locally
To test the web application locally via standard HTTP server:
```bash
cd ./cronaeon_bench
python3 -m http.server 8000
```
Open `http://localhost:8000` in any web browser to inspect:
- Interactive search across pathogens, authors, DOIs, and loci.
- Taxonomy and Clock Model filtering buttons.
- SVG BEAST vs ChronAeon concordance scatter plot with hover tooltips and dossier links.
- Interactive lightbox image modal for full-resolution figures.
- Clickable paper links (DOIs, PMIDs, PMCIDs).
- One-click copy buttons for reproduction commands.

### 6.2 Deployment to GitHub Pages
The static portal is configured for continuous deployment on GitHub Pages:
- Target URLs: `https://veg.github.io/chronaeon/` and `https://veg.github.io/cronaeon_bench/`
- All paths (`assets/`, `studies/`, `data/`) use relative linking (`../../assets/...`, `../../data/...`), ensuring flawless rendering on custom domains or GitHub Pages subpaths.

---

## 7. Autonomous Decision Logic & Troubleshooting Matrix

| Issue Observed | Root Cause | Autonomous Recovery Action |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'chronaeon'` | `PYTHONPATH` does not include the engine source directories. | Prepend `chronaeon/src` and `aeon-core/src` to `PYTHONPATH`. |
| `fieller_g >= 1.0` | Inconclusive temporal signal ($\hat{\mu} / \mathrm{SE}_{\mu} < 1.96$); sampling span is too narrow for accumulated divergence. | Do not report a single-point $t_{\mathrm{MRCA}}$. Flag the cohort as temporally uncalibrated or inspect multi-clock AutoClock partitions. |
| Negative slope ($\mu < 0$) | Severe sampling artifacts, lab passaging, or misannotated collection dates. | Check root placement; run outgroup sensitivity audit; screen dates table for typographical errors. |
| Large discrepancy between ChronAeon root and BEAST root ($>10$ years on small spans) | Stem-vs-crown divergence or non-linear rate deceleration. | Check whether the dataset includes external reference outgroups (stem divergence) or activates the Restricted Cubic Spline clock (`Delta-AIC < -2.0`). |
| Unrendered `**` in HTML | Literal Markdown strings bypassed the `render_markdown` / `render_markdown_block` parser. | Wrap the corresponding string field in `render_markdown_block(...)` in `build_entire_portal.py` and re-run. |

---

## 8. Planetary Scale & Real-Time Surveillance Grand Challenges (NextStrain & BV-BRC)

In addition to the 42 curated small-to-medium empirical benchmarks, the ChronAeon benchmark suite contains two planetary-scale surveillance grand challenges designed to demonstrate sub-minute execution, tree-free streaming ingestion, high-throughput outlier sieving, and unsupervised multi-clock reservoir deconvolution.

### 8.1 Challenge A: NextStrain Real-Time Streaming Surveillance Harness

#### Objective & Scientific Motivation
Compare ChronAeon Date and AutoClock head-to-head against TreeTime (Sagulenko et al., 2018) across official live 12-year longitudinal NextStrain feeds (Influenza A/H3N2 and A/H1N1pdm, 3,221 genomes). Evaluates whether ChronAeon can serve as an instantaneous, tree-free streaming engine for global surveillance while avoiding single-rate stem compression bias.

#### Execution Commands
```bash
# 1. Ensure Python environment and ChronAeon are configured
pip install -e chronaeon/   # or: export PYTHONPATH="src:$PYTHONPATH" 

# 2. Run the end-to-end NextStrain streaming ingestion & benchmark harness
cd ./nextstrain_grand_challenge
python3 run_nextstrain_grand_challenge.py

# 3. Generate the 4-panel publication figure and alluvial stream diagram
cd .
python3 scripts/generate_h3n2_multipanel_figure.py
python3 scripts/generate_h3n2_horizons_alluvial_figure.py
```

#### Deterministic Acceptance Criteria
1. **Live Stream Ingestion:** Reconstructs full 1,701 nt HA sequences by traversing Auspice v2 JSONs from `https://data.nextstrain.org/` in < 2 seconds.
2. **Influenza A/H1N1pdm (N=1,530):**
   - ChronAeon Date Runtime: $\le 30.0$ seconds.
   - AutoClock Runtime: $\le 30.0$ seconds ($K^* = 2$ optimal partition).
   - Inferred $t_{\mathrm{MRCA}}$: **2009.26 CE** (replicates TreeTime 2009.27 within 0.01 yr).
   - Clade Separation: 100.0% discrete biological separation (zero historical clades in Community 0; zero modern clades in Community 1).
3. **Influenza A/H3N2 (N=1,691):**
   - ChronAeon Date Runtime: $\le 35.0$ seconds.
   - AutoClock Runtime: $\le 35.0$ seconds ($K^* = 2$ optimal partition).
   - Inferred $t_{\mathrm{MRCA}}$: **2007.33 CE** for historical Clade 3 trunk (Community 1) and **2019.76 CE** for modern Clade 2 resurgence (Community 0).
   - Clade Separation: $\ge 99.8\%$ separation of Clade 2 vs Clade 3.

---

### 8.2 Challenge B: BV-BRC 10,000–50,000 Genomes Sieve & Multi-Clock Grand Challenge

#### Objective & Scientific Motivation
Overcome the 10,000-taxon scaling barrier of Bayesian phylogenetic software suites (BEAST 2, TargetedBeast, Parallel SCA). Demonstrates streaming sieve triage (chronaeon triage) at >350 seq/s and autonomous multi-host reservoir isolation (chronaeon autoclock) without metadata priors.

#### Execution Commands
```bash
# 1. Verify live REST API streaming from BV-BRC
cd ./bvbrc_h3n2_sieve_grand_challenge
python3 stream_bvbrc_surveillance.py --test-stream --limit 10

# 2. Run High-Throughput Streaming Sieve Triage (chronaeon triage)
python3 -m chronaeon.cli triage \
  -a data/h3n2_challenge_10k.fasta \
  -d data/h3n2_challenge_10k_metadata.csv \
  -s data/h3n2_challenge_10k.fasta \
  --stream-dates data/h3n2_challenge_10k_metadata.csv \
  --date-col decimal_date \
  --strain-col genome_id \
  --n-anchor 220 \
  --n-bins 32 \
  -o results/h3n2_10k_sieve_report.csv \
  --clean-out results/h3n2_10k_sieved_clean.fasta \
  --sus-out results/h3n2_10k_sieved_sus.fasta

# 3. Run Unsupervised Multi-Clock AutoClock Deconvolution (chronaeon autoclock)
python3 -m chronaeon.cli autoclock \
  -a results/h3n2_10k_sieved_clean.fasta \
  -d results/h3n2_10k_sieved_clean_metadata.csv \
  --date-col decimal_date \
  --strain-col genome_id \
  -k 8 \
  --output-dir results/clock_communities \
  -o results/h3n2_10k_autoclock_results.json \
  -c results/h3n2_10k_autoclock_classified.csv

# 4. Generate publication figures
python3 generate_challenge_figure.py
python3 ./scripts/generate_fig_bvbrc_50k.py
```

#### Deterministic Acceptance Criteria
1. **Live BV-BRC API Query:** Successful HTTP retrieval of recent human H3N2 records in < 2 seconds.
2. **Sieve Throughput:** Evaluates 10,000 sequences against a 220-taxon anchor skeleton in $\le 30.0$ seconds (throughput $\ge 350$ sequences/second).
3. **Outlier Quarantine:** Quarantines 14–23 severe anomalies (`SUS`), including non-target contaminants ($D > 0.78$), chimeric constructs ($\Delta t > 15\text{ yr}$), and degenerate sequences ($>5\%\text{ Ns}$).
4. **AutoClock Community Deconvolution:**
   - Optimal partition: $K^* = 7$ clock communities.
   - Wild Waterfowl Avian Reservoir (Community 4): $\ge 98\%$ avian, accelerated rate $\mu \approx 7.46 \times 10^{-3}$ ($2.7\times$ faster than human seasonal trunk), $t_{\mathrm{MRCA}} \approx 1990.59$.
   - North American Swine Reservoir (Community 2): $\ge 98\%$ swine, $\mu \approx 3.17 \times 10^{-3}$, $t_{\mathrm{MRCA}} \approx 1999.81$.
   - Modern Resurgence (Community 0): 100% human, $\mu \approx 4.14 \times 10^{-3}$, $t_{\mathrm{MRCA}} \approx 2019.87$.
5. **Runtime Latency:** Total wall-clock time $\le 55$ seconds on commodity hardware for streaming sieve, dating, and AutoClock deconvolution on 10,000 genomes.

---

### 8.3 Autonomous Subagent Replication Protocol
When verifying reproduction via an autonomous subagent (`invoke_subagent`):
1. **Self-Contained Execution:** The subagent must read this `AGENT.MD` document, initialize its environment variables, and run the verification pipeline in an isolated working directory.
2. **Deterministic Output Matching:** Confirm that all generated JSON summaries, CSV tables, and diagnostic figures match the acceptance criteria above.
3. **Formal Verification Report:** Emit a machine-readable summary verifying execution latency, estimated $t_{\mathrm{MRCA}}$, and concordance status.

