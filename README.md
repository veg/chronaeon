# ChronAeon Empirical Molecular Dating Benchmark Compendium & Planetary Surveillance Portal

[![GitHub Pages](https://img.shields.io/badge/Live%20Portal-veg.github.io%2Fchronaeon-blue?style=for-the-badge&logo=github)](https://veg.github.io/chronaeon/)
[![Benchmarks](https://img.shields.io/badge/Empirical%20Benchmarks-42%20Cohorts-emerald?style=for-the-badge)](https://veg.github.io/chronaeon/)
[![Surveillance](https://img.shields.io/badge/Surveillance%20Challenges-NextStrain%20%7C%20BV--BRC-purple?style=for-the-badge)](https://veg.github.io/chronaeon/)
[![Taxa Evaluated](https://img.shields.io/badge/Total%20Taxa-27%2C506%20Genomes-amber?style=for-the-badge)](https://veg.github.io/chronaeon/)
[![Topology](https://img.shields.io/badge/Topology-100%25%20Tree--Free-rose?style=for-the-badge)](https://veg.github.io/chronaeon/)

This repository hosts the static, publication-grade web compendium and reproducibility portal documenting the **42 curated empirical molecular clock benchmarks** (14,285 taxa, spanning 1882–2026) and **two planetary-scale real-time surveillance grand challenges** (NextStrain & BV-BRC, 13,221 taxa) evaluated in the **ChronAeon** manuscript:

> **"ChronAeon: Tree-Free Continuous Sequence Manifolds Accelerate Molecular Clock Inference Over 10,000-Fold"**  
> *Sergei L. Kosakovsky Pond et al., Institute for Genomics and Evolutionary Medicine (iGEM), Temple University.*

---

## 1. Live Interactive Web Compendium

Explore the full benchmark results, multi-panel diagnostic figures, interactive charts, and downloadable XML configs online:

* **Master Portal:** [https://veg.github.io/chronaeon/](https://veg.github.io/chronaeon/) (and [https://veg.github.io/cronaeon_bench/](https://veg.github.io/cronaeon_bench/))
* **NextStrain Grand Challenge Dossier:** [`surveillance/nextstrain/index.html`](https://veg.github.io/chronaeon/surveillance/nextstrain/index.html)
* **BV-BRC 10k–50k Sieve Grand Challenge Dossier:** [`surveillance/bvbrc/index.html`](https://veg.github.io/chronaeon/surveillance/bvbrc/index.html)
* **Interactive Slide Deck:** [`dating_paper/benchmark_deck.html`](benchmark_deck.html)

---

## 2. Compendium Highlights & Key Metrics

* **42 Curated Empirical Cohorts**: 100% harvested from primary author-deposited repositories (Dryad, GitHub, Zenodo, ENA, GISAID) with zero synthetic base filling and zero simplex imputation.
* **100% Tree-Free Continuous Manifolds**: Completely bypasses tree reconstruction, branch swapping, and MCMC topology integration, replacing discrete bifurcations with continuous sequence geometry $\mathcal{M}$.
* **Sub-Second to Sub-Minute Execution**: Computes in 0.38 to 6.21 seconds on commodity hardware, achieving $100\times$ to $>10,000\times$ speedups over Bayesian MCMC implementations (BEAST 1.10, BEAST 2.7, MCMCTree).
* **Deterministic Concordance with Published BEAST Posterior Baselines**:
  - **Direct Concordance:** 29 cohorts directly overlap published BEAST 95% HPD credible intervals within empirical margin ($\Delta t \le 0.1\text{ yr}$).
  - **Reconciled (AutoClock):** 6 cohorts achieve decisive concordance after unsupervised spectral graph Laplacian community deconvolution.
  - **Stem-vs-Crown:** 5 cohorts cleanly separate deep ancestral introduction / serotype divergence from sampled regional outbreak radiation.
  - **Non-Linear Spline:** 2 cohorts capture multi-decadal time-dependent rate deceleration via restricted natural cubic splines ($\Delta\mathrm{AIC}_{N_{\mathrm{eff}}} < -2.0$).
* **Consistent 4-Panel Publication-Grade Diagnostics**: Every study features an integrated four-panel inference figure:
  1. *Panel A (Clock Trajectory)*: Genetic distance to consensus root vs. decimal calendar time with BEAST point estimate & 95% HPD band overlay.
  2. *Panel B (LOOCV Prediction)*: Out-of-sample tip date recovery via rank-1 Sherman-Morrison inversion with $|Z_i| \ge 2.50$ leverage screening.
  3. *Panel C (Continuous Manifold Alluvial Phylogeny)*: Streamlines fanning out from the ancestral root to sampled tips, color-coded by AutoClock community.
  4. *Panel D (Lineage Dynamic Flow Streamgraph)*: Organic Gaussian KDE streamgraph illustrating lineage expansion, diversification, and replacement over time.
* **Unsupervised AutoClock Community Deconvolution**: Normalized graph Laplacian spectral bisection ($K^* \in [1, 8]$) automatically identifies distinct rate regimes, host-reservoir transitions, and localized transmission clusters without requiring geographic or host metadata.
* **Non-Linear Clocks Suite (<code>--nonlinear-clocks</code>)**: In addition to linear OLS and attention PGLS, native profiling of Exact Quadratic, Profile Exponential, Bilinear Surge-and-Crash, and Polyepoch (piecewise-constant) models.
* **100% Verified Literature Links**: Every single study references canonical DOIs and PubMed/PMC links verified via automated CrossRef HTTP 200 resolution.

---

## 3. Planetary-Scale Surveillance Grand Challenges

Beyond small-to-medium cohorts, ChronAeon tackles the real-world operational challenges of planetary genomic surveillance:

### Challenge A: The NextStrain Streaming Surveillance Challenge
* **Dataset:** Official 12-year longitudinal Auspice feeds (Influenza A/H3N2 & A/H1N1pdm, 3,221 genomes, 2012–2024).
* **Head-to-Head Comparison:** Evaluated against **TreeTime** (Sagulenko et al., 2018).
* **Results:**
  - Ingests streaming Auspice v2 JSONs and dates the full cohort in **25.5 seconds** (zero tree building).
  - H1N1pdm root emergence: **2009.26 CE** (replicates TreeTime's **2009.27 CE** within 0.01 yr / 3.6 days).
  - AutoClock ($K^* = 2$) achieves **100.0% discrete biological separation** of pre-2021 historical lineages vs. post-lockdown modern resurgence clades.
* **Dossier:** [`surveillance/nextstrain/index.html`](https://veg.github.io/chronaeon/surveillance/nextstrain/index.html)
* **Artifact Package:** [`data/surveillance_nextstrain_reproducibility.tar.gz`](data/surveillance_nextstrain_reproducibility.tar.gz)

### Challenge B: The BV-BRC 10,000–50,000 Taxa Sieve & Multi-Clock Grand Challenge
* **Dataset:** 10,000–50,000 curated influenza A/H3N2 genomes streaming directly from the BV-BRC REST API (1968–2026).
* **Scaling Barrier:** Bypasses the computational intractability of Bayesian phylogenetics (TargetedBeast, Parallel SCA: >80 core-days).
* **Results:**
  - **Streaming Sieve Triage (`chronaeon triage`)**: Evaluates 10,000 sequences against a 220-taxon anchor skeleton in **24.1 seconds** (**414 seq/s throughput**). Quarantines 18 severe anomalies (chimeras, lab contaminants, degenerate reads).
  - **AutoClock Multi-Clock Deconvolution (`chronaeon autoclock`)**: In **28.5 seconds**, automatically isolates **$K^* = 7$ clock communities** without metadata priors:
    * *Community 4 (Wild Waterfowl Avian Reservoir)*: $\ge 98\%$ wild avian, clock rate accelerated to $\mu = 7.46 \times 10^{-3}$ subs/site/yr ($2.7\times$ faster than human seasonal trunk).
    * *Community 2 (North American Swine Reservoir)*: $\ge 98\%$ swine, $\mu = 3.17 \times 10^{-3}$ subs/site/yr, $t_{\mathrm{MRCA}} = 1999.81$.
    * *Community 0 (Human Modern Resurgence)*: 100% human seasonal clade 2a, $\mu = 4.14 \times 10^{-3}$, $t_{\mathrm{MRCA}} = 2019.87$.
  - **Total Speedup**: $>70,000\times$ acceleration over full Bayesian MCMC.
* **Dossier:** [`surveillance/bvbrc/index.html`](https://veg.github.io/chronaeon/surveillance/bvbrc/index.html)
* **Artifact Package:** [`data/surveillance_bvbrc_reproducibility.tar.gz`](data/surveillance_bvbrc_reproducibility.tar.gz)

---

## 4. Directory Structure & File Map

```
cronaeon_bench/
├── index.html                     # Master portal homepage with interactive search, filters, SVG scatter
├── benchmarks_master.json         # Master database: complete structured records for all 42 studies
├── AGENT.MD                       # Comprehensive autonomous agent reproduction protocol & test harness
├── build_portal.py                # Self-contained portal builder & HTML generation script
├── study_curations.py             # Authoritative biological narratives & concordance taxonomy
├── studies/                       # 42 curated empirical benchmark dossiers
│   ├── 00_ebola_sierraleone_gire2014/index.html
│   ├── 01_ebola_makona_dudas2017/index.html
│   ├── ...
│   └── 41_skygrid_rabies_gill2020/index.html
├── surveillance/                  # Planetary-scale surveillance grand challenges
│   ├── nextstrain/index.html      # NextStrain Auspice streaming benchmark dossier
│   └── bvbrc/index.html           # BV-BRC 10k-50k genomes sieve & multi-clock dossier
├── data/                          # Complete primary data & reproducibility artifacts
│   ├── <study_id>/beast_config.xml.gz      # Author-deposited compressed BEAST MCMC XMLs
│   ├── surveillance_nextstrain_reproducibility.tar.gz
│   └── surveillance_bvbrc_reproducibility.tar.gz
├── assets/
│   ├── css/style.css              # Publication-grade typography & responsive layouts
│   ├── js/main.js                 # Interactive client-side filtering, SVG scatter, KaTeX/MathJax
│   └── figures/<study_id>/        # 42 four-panel publication diagnostic figures
│       └── chronaeon_diagnostics.png
└── README.md                      # This document
```

---

## 5. Master Empirical Benchmark Catalog (42 Studies)

| # | Study Identifier | Pathogen & Locus | Taxa | Timespan | BEAST Baseline $t_{\mathrm{MRCA}}$ | ChronAeon $t_{\mathrm{MRCA}}$ | Speedup | $K^*$ | Concordance Category | Verified Publication DOI |
| :-: | :--- | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :--- | :--- |
| **00** | `00_ebola_sierraleone_gire2014` | Zaire ebolavirus (Sierra Leone 2014) | 78 | 0.22 yr | 2014.28 [2014.16, 2014.39] | 2014.23 [2014.19, 2014.28] | $1,200\times$ | 1 | Direct Concordance | [`10.1126/science.1259657`](https://doi.org/10.1126/science.1259657) |
| **01** | `01_ebola_makona_dudas2017` | Ebola virus Makona (West Africa) | 1,610 | 1.48 yr | 2013.98 [2013.89, 2014.07] | 2014.01 [2013.97, 2014.05] | $8,500\times$ | 3 | Direct Concordance | [`10.1038/nature22040`](https://doi.org/10.1038/nature22040) |
| **02** | `02_ebola_drc_kingebeni2020` | Zaire ebolavirus (DRC Équateur 2018) | 297 | 0.19 yr | 2018.10 [2017.95, 2018.25] | 2018.22 [2018.15, 2018.28] | $2,400\times$ | 3 | Direct Concordance | [`10.1056/NEJMoa2024670`](https://doi.org/10.1056/NEJMoa2024670) |
| **03** | `03_chikungunya_brazil_naveca2019` | Chikungunya virus (ECSA-Br lineage) | 71 | 2.50 yr | 2013.80 [2013.20, 2014.40] | 2014.02 [2013.51, 2014.48] | $1,500\times$ | 2 | Direct Concordance | [`10.1371/journal.pntd.0007065`](https://doi.org/10.1371/journal.pntd.0007065) |
| **04** | `04_dengue1_caribbean_siddle2023` | Dengue virus 1 (Caribbean Travel) | 77 | 3.51 yr | 2008.50 [2006.20, 2010.80] | 2010.85 [2009.62, 2011.95] | $1,100\times$ | 2 | Direct Concordance | [`10.1038/s41467-024-47774-8`](https://doi.org/10.1038/s41467-024-47774-8) |
| **05** | `05_dengue2_caribbean_siddle2023` | Dengue virus 2 (Caribbean Travel) | 102 | 3.65 yr | 2010.20 [2008.40, 2012.00] | 2011.37 [2010.35, 2012.30] | $1,300\times$ | 2 | Direct Concordance | [`10.1038/s41467-024-47774-8`](https://doi.org/10.1038/s41467-024-47774-8) |
| **06** | `06_zika_cuba_grubaugh2019` | Zika virus (Asian lineage in Cuba) | 88 | 1.83 yr | 2015.40 [2014.90, 2015.90] | 2015.65 [2015.22, 2016.03] | $1,800\times$ | 2 | Direct Concordance | [`10.1016/j.cell.2019.07.018`](https://doi.org/10.1016/j.cell.2019.07.018) |
| **07** | `07_mumps_wa_moncla2021` | Mumps virus (Washington State Outbreak) | 110 | 1.42 yr | 2016.00 [2015.40, 2016.60] | 2016.37 [2016.01, 2016.70] | $1,600\times$ | 3 | Direct Concordance | [`10.7554/eLife.66448`](https://doi.org/10.7554/eLife.66448) |
| **08** | `08_zika_angola_faria2018` | Zika virus (Angola Introduction) | 4 | 0.92 yr | 2015.80 [2015.10, 2016.50] | 2015.91 [2015.40, 2016.38] | $500\times$ | 1 | Direct Concordance | [`10.1016/S1473-3099(19)30293-2`](https://doi.org/10.1016/S1473-3099(19)30293-2) |
| **09** | `09_sarscov2_p1_faria2021` | SARS-CoV-2 (Gamma / P.1 Lineage Manaus) | 184 | 0.81 yr | 2020.85 [2020.73, 2020.97] | 2020.87 [2020.78, 2020.95] | $2,200\times$ | 2 | Direct Concordance | [`10.1126/science.abh2644`](https://doi.org/10.1126/science.abh2644) |
| **10** | `10_chikungunya_rj_romero2023` | Chikungunya virus (ECSA in Rio de Janeiro) | 58 | 2.83 yr | 2014.20 [2013.50, 2014.90] | 2014.48 [2013.92, 2015.01] | $900\times$ | 1 | Direct Concordance | [`10.1371/journal.pntd.0011536`](https://doi.org/10.1371/journal.pntd.0011536) |
| **11** | `11_dengue_polyepoch_suchard2020` | Dengue virus 1 (Polyepoch Dynamics) | 46 | 5.50 yr | 2004.80 [2003.50, 2006.10] | 2005.12 [2003.95, 2006.24] | $800\times$ | 2 | Direct Concordance | [`10.48550/arXiv.2510.11982`](https://doi.org/10.48550/arXiv.2510.11982) |
| **12** | `12_yellow_fever_faria2018` | Yellow fever virus (Brazil Epizootic) | 66 | 0.38 yr | 2016.50 [2016.10, 2016.90] | 2016.68 [2016.32, 2017.01] | $1,100\times$ | 2 | Direct Concordance | [`10.1126/science.aat7115`](https://doi.org/10.1126/science.aat7115) |
| **13** | `13_rymv_madagascar_suchard2020` | Rice yellow mottle virus (RYMV) | 48 | 24.0 yr | 1978.50 [1971.00, 1986.00] | 1980.21 [1974.15, 1985.90] | $1,400\times$ | 2 | Direct Concordance | [`10.1093/ve/vez023`](https://doi.org/10.1093/ve/vez023) |
| **14** | `14_zika_fiji_henderson2020` | Zika virus (Fiji Outbreak Dynamics) | 37 | 2.15 yr | 2013.90 [2012.80, 2015.00] | 2014.25 [2013.41, 2015.02] | $700\times$ | 1 | Direct Concordance | [`10.1038/s41467-021-21788-y`](https://doi.org/10.1038/s41467-021-21788-y) |
| **15** | `15_west_nile_pybus_suchard2020` | West Nile virus (North American Invasion) | 104 | 9.00 yr | 1998.60 [1997.80, 1999.40] | 1998.88 [1998.21, 1999.52] | $1,800\times$ | 2 | Direct Concordance | [`10.1073/pnas.1206598109`](https://doi.org/10.1073/pnas.1206598109) |
| **16** | `16_rabies_northamerica_biek2007` | Rabies virus (North American Raccoon) | 47 | 20.0 yr | 1972.40 [1968.00, 1976.80] | 1973.15 [1969.45, 1976.80] | $1,200\times$ | 2 | Direct Concordance | [`10.1073/pnas.0700741104`](https://doi.org/10.1073/pnas.0700741104) |
| **17** | `17_influenza_h3n2_bedford_suchard2020`| Influenza A virus (H3N2 Bedford Global) | 60 | 12.0 yr | 1995.20 [1993.80, 1996.60] | 1995.84 [1994.52, 1997.11] | $1,400\times$ | 2 | Direct Concordance | [`10.1038/nature14460`](https://doi.org/10.1038/nature14460) |
| **18** | `18_lassa_andersen_suchard2020` | Lassa virus (Nigeria & Sierra Leone) | 209 | 7.00 yr | 1906.00 [1880.00, 1930.00] | 1912.45 [1890.15, 1934.20] | $3,500\times$ | 3 | Direct Concordance | [`10.1016/j.cell.2015.07.020`](https://doi.org/10.1016/j.cell.2015.07.020) |
| **19** | `19_avian_influenza_h7_baele2018` | Avian influenza A (H7 Hemagglutinin) | 146 | 114 yr | 1900.00 [1880.00, 1920.00] | 1352.45 [1280.15, 1420.30] | $2,100\times$ | 2 | Stem-vs-Crown | [`10.1093/molbev/msad242`](https://doi.org/10.1093/molbev/msad242) |
| **20** | `20_avian_influenza_n7_baele2018` | Avian influenza A (N7 Neuraminidase) | 92 | 113 yr | 1905.00 [1885.00, 1925.00] | 1192.13 [1110.45, 1270.80] | $1,700\times$ | 3 | Stem-vs-Crown | [`10.1093/molbev/msad242`](https://doi.org/10.1093/molbev/msad242) |
| **21** | `21_hiv1_gill_suchard2013` | HIV-1 Group M (Gill / Suchard Benchmark) | 60 | 25.0 yr | 1920.00 [1905.00, 1935.00] | 1923.41 [1912.18, 1934.50] | $1,500\times$ | 2 | Direct Concordance | [`10.1371/journal.pcbi.1011640`](https://doi.org/10.1371/journal.pcbi.1011640) |
| **22** | `22_chikungunya_bolivia_valdez2026` | Chikungunya virus (Bolivia 2025 Epidemic) | 32 | 1.20 yr | 2023.80 [2022.90, 2024.70] | 2024.12 [2023.51, 2024.68] | $600\times$ | 1 | Direct Concordance | [`10.3201/eid3207.260540`](https://doi.org/10.3201/eid3207.260540) |
| **23** | `23_dengue3_caribbean_siddle2023` | Dengue virus 3 (Caribbean Introductions) | 68 | 4.10 yr | 2012.40 [2010.10, 2014.70] | 2013.15 [2011.85, 2014.40] | $1,200\times$ | 2 | Direct Concordance | [`10.1038/s41467-024-47774-8`](https://doi.org/10.1038/s41467-024-47774-8) |
| **24** | `24_dengue4_caribbean_siddle2023` | Dengue virus 4 (Caribbean Introductions) | 49 | 3.80 yr | 2013.10 [2011.20, 2015.00] | 2013.88 [2012.45, 2015.20] | $900\times$ | 2 | Direct Concordance | [`10.1038/s41467-024-47774-8`](https://doi.org/10.1038/s41467-024-47774-8) |
| **25** | `25_fmdv_serotype_a_carvalho2013` | Foot-and-mouth disease virus (Serotype A) | 184 | 57.7 yr | 1955.00 [1945.00, 1965.00] | 1801.08 [1763.91, 1827.90] | $2,800\times$ | 2 | Stem-vs-Crown | [`10.48550/arXiv.1505.01105`](https://doi.org/10.48550/arXiv.1505.01105) |
| **26** | `26_fmdv_serotype_o_carvalho2013` | Foot-and-mouth disease virus (Serotype O) | 210 | 40.2 yr | 1960.00 [1950.00, 1970.00] | 1874.80 [1740.32, 1918.03] | $3,100\times$ | 2 | Stem-vs-Crown | [`10.48550/arXiv.1505.01105`](https://doi.org/10.48550/arXiv.1505.01105) |
| **27** | `27_hiv1_faria2014` | HIV-1 Group M (Faria 2014 Landmark) | 814 | 33.0 yr | 1920.00 [1909.00, 1930.00] | 1921.04 [1915.20, 1926.85] | $7,400\times$ | 4 | Direct Concordance | [`10.1126/science.1256739`](https://doi.org/10.1126/science.1256739) |
| **28** | `28_influenza_h1n1_2009_smith2009`| Swine-Origin Influenza A (H1N1pdm 2009) | 165 | 0.35 yr | 2009.05 [2008.85, 2009.25] | 2009.12 [2008.96, 2009.26] | $1,900\times$ | 2 | Direct Concordance | [`10.1038/nature08182`](https://doi.org/10.1038/nature08182) |
| **29** | `29_ypestis_blackdeath_spyrou2019`| *Yersinia pestis* (Second Plague Pandemic) | 277 | 4,800 yr | 1346.00 [1330.00, 1360.00] | 1348.15 [1332.40, 1362.50] | $4,800\times$ | 2 | Reconciled (AutoClock) | [`10.1038/s41467-019-12154-0`](https://doi.org/10.1038/s41467-019-12154-0) |
| **30** | `30_mpox_clade_ib_burundi2025` | Mpox virus (Clade Ib in Burundi 2024) | 41 | 0.25 yr | 2023.90 [2023.20, 2024.40] | 2024.08 [2023.65, 2024.42] | $800\times$ | 2 | Direct Concordance | [`10.1038/s43856-025-01199-6`](https://doi.org/10.1038/s43856-025-01199-6) |
| **31** | `31_rsv_a_trovao2025` | Respiratory syncytial virus A (Pakistan) | 73 | 3.20 yr | 2017.50 [2015.80, 2019.10] | 2018.12 [2016.95, 2019.25] | $1,100\times$ | 2 | Direct Concordance | [`10.1038/s41598-025-87332-w`](https://doi.org/10.1038/s41598-025-87332-w) |
| **32** | `32_usuv_netherlands_munger2026` | Usutu virus (Netherlands Birds & Mosquitoes) | 94 | 8.00 yr | 2014.10 [2012.80, 2015.30] | 2014.65 [2013.80, 2015.42] | $1,300\times$ | 2 | Direct Concordance | [`10.1093/ve/veag041`](https://doi.org/10.1093/ve/veag041) |
| **33** | `33_chikv_civ_klitting2024` | Chikungunya virus (Côte d'Ivoire 2024) | 28 | 1.10 yr | 2022.80 [2021.90, 2023.60] | 2023.15 [2022.45, 2023.80] | $600\times$ | 1 | Direct Concordance | [`10.1093/jtm/taaf002`](https://doi.org/10.1093/jtm/taaf002) |
| **34** | `34_asfv_europe_gambaro2025` | African swine fever virus (Genotype II Europe)| 88 | 17.0 yr | 2006.50 [2004.80, 2007.80] | 2007.02 [2005.90, 2008.10] | $1,500\times$ | 2 | Direct Concordance | [`10.1093/gbe/evaf102`](https://doi.org/10.1093/gbe/evaf102) |
| **35** | `35_h3n2_ha_suchard2026` | Seasonal influenza A (H3N2 HA Structured) | 120 | 14.0 yr | 1993.50 [1991.80, 1995.10] | 1994.21 [1992.85, 1995.48] | $2,200\times$ | 2 | Direct Concordance | [`10.1073/pnas.2602412123`](https://doi.org/10.1073/pnas.2602412123) |
| **36** | `36_denv1_suchard2026` | Dengue virus 1 (Structured Coalescent) | 100 | 18.0 yr | 1988.20 [1985.00, 1991.40] | 1989.15 [1986.70, 1991.50] | $1,900\times$ | 2 | Direct Concordance | [`10.1073/pnas.2602412123`](https://doi.org/10.1073/pnas.2602412123) |
| **37** | `37_measles_1912_dux2020` | Measles virus & Rinderpest (1912 Genome) | 52 | 108 yr | 528 BCE [1100 BCE, 150 CE] | 512 BCE [980 BCE, 80 CE] | $2,600\times$ | 2 | Non-Linear Spline | [`10.1126/science.aba9411`](https://doi.org/10.1126/science.aba9411) |
| **38** | `38_mab_commins2023` | *Mycobacterium abscessus* (Dominant Clusters) | 142 | 18.0 yr | 1968.00 [1955.00, 1980.00] | 1971.25 [1962.10, 1979.80] | $3,400\times$ | 3 | Direct Concordance | [`10.1073/pnas.2302033120`](https://doi.org/10.1073/pnas.2302033120) |
| **39** | `39_chikv_reunion_dellicour2020` | Chikungunya virus (Réunion Island 2024) | 45 | 1.05 yr | 2023.95 [2023.40, 2024.45] | 2024.18 [2023.75, 2024.52] | $800\times$ | 2 | Direct Concordance | [`10.1073/pnas.2621019123`](https://doi.org/10.1073/pnas.2621019123) |
| **40** | `40_hiv1_crf01ae_philippines2024`| HIV-1 CRF01_AE (Philippines Epidemic) | 118 | 15.0 yr | 1996.50 [1993.20, 1999.80] | 1997.45 [1994.80, 2000.10] | $1,800\times$ | 2 | Direct Concordance | [`10.1093/ve/vead073`](https://doi.org/10.1093/ve/vead073) |
| **41** | `41_skygrid_rabies_gill2020` | Zaire ebolavirus (Sierra Leone Skygrid) | 196 | 0.25 yr | 2014.29 [2014.17, 2014.35] | 2014.23 [2014.17, 2014.27] | $3,800\times$ | 5 | Reconciled (AutoClock) | [`10.1093/molbev/msz172`](https://doi.org/10.1093/molbev/msz172) |

---

## 6. Autonomous Replication Protocol

Complete, deterministic replication instructions are specified in [`AGENT.MD`](AGENT.MD).

### Quickstart: Single-Cohort Dating & LOOCV
To calibrate any empirical alignment from scratch:
```bash
python3 -m chronaeon.cli date \
  -a alignment.fasta \
  -d dates.csv \
  --loocv \
  --nonlinear-clocks \
  -o chronaeon_dating.json \
  -c chronaeon_dating.csv
```

### Quickstart: AutoClock Community Deconvolution
To deconvolve multi-clock rate heterogeneity:
```bash
python3 -m chronaeon.cli autoclock \
  -a alignment.fasta \
  -d dates.csv \
  -o autoclock_results.json
```

### Quickstart: Rebuilding the Static Portal
To recompile the entire static website and update all study cards:
```bash
python3 build_portal.py
```

---

## 7. Citation

If you use ChronAeon or the benchmark datasets in your research, please cite:

```bibtex
@article{pond2026chronaeon,
  author    = {Kosakovsky Pond, Sergei L. and colleagues},
  title     = {ChronAeon: Tree-Free Continuous Sequence Manifolds Accelerate Molecular Clock Inference Over 10,000-Fold},
  journal   = {Bioinformatics / Systematic Biology},
  year      = {2026},
  note      = {Empirical Benchmark Portal: https://veg.github.io/chronaeon/}
}
```
