# ChronAeon Benchmark Compendium Portal

This repository hosts the static, publication-grade web application documenting the **55 empirical molecular clock benchmarks** (51,962 taxa, 1927–2026) evaluated in the **ChronAeon** manuscript:

> **"ChronAeon: Tree-Free Continuous Sequence Manifolds Accelerate Molecular Clock Inference Over 10,000-Fold"**  
> *Sergei L. Kosakovsky Pond et al., Institute for Genomics and Evolutionary Medicine (iGEM), Temple University.*

## Live Portal
The interactive web portal is deployed on GitHub Pages:  
**https://veg.github.io/cronaeon_bench/**

## Key Compendium Metrics
- **55 Empirical Cohorts**: Covering Positive-Sense RNA, Negative-Sense RNA, Retroviruses, DNA Viruses, Bacteria & Ancient DNA, and Macroevolution.
- **51,962 Total Taxa**: From acute outbreaks ($N = 100$) to planetary surveillance ($N = 50,000$).
- **Near-Perfect Concordance**: Pearson $R = 0.9952$, $R^2 = 0.9904$ ($p < 10^{-30}$) against published Bayesian MCMC (BEAST 1.x / 2.x).
- **Extreme Speedup**: 1,200× to 480,000× faster than Markov Chain Monte Carlo (MCMC).
- **Unsupervised AutoClock Deconvolution**: Resolves lineage-specific rate heterogeneity ($K^* > 1$) or confirms strict rate homogeneity ($K^* = 1$).

## Directory Structure
- `index.html`: Master portal homepage featuring the global concordance scatter plot, live multi-faceted filters, and searchable benchmark data grid.
- `studies/`: 55 individual static study pages with dedicated biological narratives, AutoClock community breakdowns, high-resolution diagnostic figures, and deterministic reproduction commands.
- `assets/`:
  - `css/style.css`: Clean, modern scientific styling.
  - `js/main.js`: Interactive filtering, SVG plotting, lightbox zoom, and code copy tools.
  - `figures/`: Diagnostic multipanels and alluvial streamline figures for all 55 empirical studies.
- `benchmarks_master.json`: Complete structured JSON records for programmatic analysis.

## Deterministic Reproduction
Each study includes its complete CLI command. To run tree-free inference on any alignment:
```bash
python3 -m chronaeon.cli dating -a alignment.fasta -d dates.csv --loocv
```
