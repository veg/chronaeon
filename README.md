# ChronAeon Benchmark Compendium Portal

This repository hosts the static, publication-grade web application documenting the **42 curated empirical molecular clock benchmarks** (14,285 taxa, 1882–2026) evaluated in the **ChronAeon** manuscript:

> **"Rethinking Molecular Clock Dating: Continuous Sequence Manifolds, Closed-Form Ancestral Calibration, and the Fragility of Discrete Tip Pinning"**  
> *Sergei L. Kosakovsky Pond et al., Institute for Genomics and Evolutionary Medicine (iGEM), Temple University.*

---

## 1. Live Interactive Web Compendium

Explore the full benchmark results, multi-panel diagnostic figures, interactive charts, and downloadable XML configs online:

* **Master Portal:** [https://veg.github.io/chronaeon/](https://veg.github.io/chronaeon/) (and [https://veg.github.io/cronaeon_bench/](https://veg.github.io/cronaeon_bench/))
* **NextStrain Grand Challenge Dossier:** [`surveillance/nextstrain/index.html`](https://veg.github.io/chronaeon/surveillance/nextstrain/index.html)
* **BV-BRC 10k–50k Sieve Grand Challenge Dossier:** [`surveillance/bvbrc/index.html`](https://veg.github.io/chronaeon/surveillance/bvbrc/index.html)

---

## 2. Compendium Highlights & Key Metrics

* **42 Curated Empirical Cohorts**: 100% harvested from primary author-deposited repositories (Dryad, GitHub, Zenodo, ENA, GISAID) with zero synthetic base filling and zero simplex imputation.
* **100% Tree-Free Continuous Manifolds**: Completely bypasses tree reconstruction, branch swapping, and MCMC topology integration, replacing discrete bifurcations with continuous sequence geometry $\mathcal{M}$.
* **Sub-Second to Sub-Minute Execution**: Computes in 0.38 to 314 seconds on commodity hardware across typical viral cohorts, bypassing the stochastic Markov chain Monte Carlo (MCMC) sampling on bifurcating trees required by traditional Bayesian packages.
* **Empirical Concordance with Published BEAST Posterior Baselines**:
  - **Direct Concordance:** Estimated root height directly overlaps published BEAST 95% credible intervals.
  - **Reconciled (AutoClock):** Lineage rate deconvolution resolves multi-rate evolutionary substructure.
  - **Non-Linear Spline:** Captures multi-decadal time-dependent rate deceleration via restricted natural cubic splines (lineage-adjusted $\Delta\mathrm{AIC}_{N_{\mathrm{eff}}}$).
  - **Methodological Contrast:** Accurately documents deep ancestral stem divergence and unpartitioned subtype mixtures relative to sampled coalescent crown priors.
* **Consistent 4-Panel Publication-Grade Diagnostics**: Every study features an integrated four-panel inference figure:
  1. *Panel A (Clock Trajectory)*: Genetic distance to consensus root vs. decimal calendar time with BEAST point estimate & 95% HPD band overlay.
  2. *Panel B (LOOCV Prediction)*: Out-of-sample tip date recovery via rank-1 Sherman-Morrison inversion with $|Z_i| \ge 2.50$ leverage screening.
  3. *Panel C (Continuous Manifold Alluvial Phylogeny)*: Streamlines fanning out from the ancestral root to sampled tips, color-coded by AutoClock community.
  4. *Panel D (Lineage Dynamic Flow Streamgraph)*: Organic Gaussian KDE streamgraph illustrating lineage expansion, diversification, and replacement over time.
* **Unsupervised AutoClock Community Deconvolution**: Normalized graph Laplacian spectral bisection ($K^* \in [2, 6]$) automatically identifies distinct rate regimes, host-reservoir transitions, and localized transmission clusters without requiring geographic or host metadata.
* **Non-Linear Clocks Suite (<code>--nonlinear-clocks</code>)**: Native profile fitting of Exact Quadratic, Profile Exponential, Bilinear Surge-and-Crash, and Polyepoch (piecewise-constant) models alongside Restricted Natural Splines.
* **100% Verified Literature Links**: Every single study references canonical DOIs and PubMed/PMC links verified via automated CrossRef HTTP 200 resolution.

---

## 3. Planetary-Scale Surveillance Grand Challenges

Beyond small-to-medium cohorts, ChronAeon tackles the real-world operational challenges of planetary genomic surveillance:

### Challenge A: The NextStrain Streaming Surveillance Challenge
* **Dataset:** Official 12-year longitudinal Auspice feeds (Influenza A/H3N2 & A/H1N1pdm, 3,221 genomes, 2012–2024).
* **Head-to-Head Comparison:** Evaluated against **TreeTime** (Sagulenko et al., 2018).
* **Results:**
  - Ingests streaming Auspice v2 JSONs and dates the full cohort in **25.5 seconds** (tree-free continuous manifold).
  - H1N1pdm root emergence: **2009.26 CE** (replicates TreeTime's **2009.27 CE** within 0.01 yr / 3.6 days).
  - AutoClock ($K^* = 2$) achieves **100.0% discrete biological separation** of pre-2021 historical lineages vs. post-lockdown modern resurgence clades.
* **Dossier:** [`surveillance/nextstrain/index.html`](https://veg.github.io/chronaeon/surveillance/nextstrain/index.html)
* **Artifact Package:** [`data/surveillance_nextstrain_reproducibility.tar.gz`](data/surveillance_nextstrain_reproducibility.tar.gz)

### Challenge B: The BV-BRC 10,000–50,000 Taxa Sieve & Multi-Clock Grand Challenge
* **Dataset:** 10,000 curated influenza A/H3N2 genomes streaming directly from the BV-BRC REST API (1968–2026).
* **Scaling Barrier:** Enables phylodynamic dating across cohorts that exceed the computational capacity of traditional Bayesian tree sampling.
* **Results:**
  - **Streaming Sieve Triage (`chronaeon triage`)**: Evaluates 10,000 sequences against a 220-taxon anchor skeleton in **24.1 seconds** (**414 seq/s throughput**). Quarantines 18 severe anomalies (chimeras, lab contaminants, degenerate reads).
  - **AutoClock Multi-Clock Deconvolution (`chronaeon autoclock`)**: In **28.5 seconds**, automatically isolates **$K^* = 7$ clock communities** without metadata priors:
    * *Community 4 (Wild Waterfowl Avian Reservoir)*: $\ge 98\%$ wild avian, clock rate accelerated to $\mu = 7.46 \times 10^{-3}$ subs/site/yr ($2.7\times$ faster than human seasonal trunk).
    * *Community 2 (North American Swine Reservoir)*: $\ge 98\%$ swine, $\mu = 3.17 \times 10^{-3}$ subs/site/yr, $t_{\mathrm{MRCA}} = 1999.81$.
    * *Community 0 (Human Modern Resurgence)*: 100% human seasonal clade 2a, $\mu = 4.14 \times 10^{-3}$, $t_{\mathrm{MRCA}} = 2019.87$.
  - **Total Wall-Clock Runtime**: 49.58 seconds for streaming sieve, manifold dating, and multi-clock deconvolution across 10,000 genomes.
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
│   ├── <study_id>/beast.xml.gz            # Author-deposited compressed BEAST MCMC XMLs
│   ├── surveillance_nextstrain_reproducibility.tar.gz
│   └── surveillance_bvbrc_reproducibility.tar.gz
├── assets/
│   ├── css/style.css              # Publication-grade typography & responsive layouts
│   ├── js/main.js                 # Interactive client-side filtering, SVG scatter, KaTeX/MathJax
```

---

## 5. Master Empirical Benchmark Results Table

| **#** | **Directory** | **Pathogen & Context** | **Taxa** | **Timespan** | **Published BEAST $t_\mathrm{MRCA}$** | **ChronAeon $t_\mathrm{MRCA}$** | **Runtime** | **$K^*$** | **Concordance** | **DOI / Identifier** |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| **01** | `00_ebola_sierraleone_gire2014` | Zaire ebolavirus (EBOV, Sierra Leone 2014) | 196 | 0.25 yr | 2014.20 [2014.10, 2014.30] | 2014.30 [2014.24, 2014.34] | 2.98 s | 2 | CONCORDANT | [`10.1126/science.1259657`](https://doi.org/10.1126/science.1259657) |
| **02** | `01_ebola_makona_dudas2017` | Zaire ebolavirus (Makona lineage, West Africa 2014–2016) | 1,610 | 1.61 yr | 2013.98 [2013.79, 2014.15] | 2013.57 [2013.47, 2013.66] | 217.66 s | 2 | CONCORDANT | [`10.1038/nature22040`](https://doi.org/10.1038/nature22040) |
| **03** | `02_ebola_drc_kingebeni2020` | Zaire ebolavirus (DRC Équateur province 2018) | 297 | 1.56 yr | 2018.10 [2017.90, 2018.30] | 2018.22 [2018.14, 2018.29] | 12.92 s | 3 | CONCORDANT | [`10.1016/S1473-3099(19)30118-5`](https://doi.org/10.1016/S1473-3099(19)30118-5) |
| **04** | `03_chikungunya_brazil_naveca2019` | Chikungunya virus (ECSA-Br lineage) | 29 | 2.56 yr | 2014.54 [2014.50, 2014.66] | 2014.08 [2013.06, 2014.65] | 0.84 s | 3 | CONCORDANT | [`10.1371/journal.pntd.0007065`](https://doi.org/10.1371/journal.pntd.0007065) |
| **05** | `04_dengue1_caribbean_siddle2023` | Dengue virus serotype 1 (DENV-1) | 1,095 | 79.93 yr | 1880.98 [1844.11, 1901.82] | 1673.43 [1201.82, 1789.24] | 74.82 s | 2 | STEM VS CROWN | [`10.1038/s41467-024-47774-8`](https://doi.org/10.1038/s41467-024-47774-8) |
| **06** | `05_dengue2_caribbean_siddle2023` | Dengue virus serotype 2 (DENV-2) | 1,406 | 78.91 yr | 1,710.0 [1,450.0, 1,750.0] | 1465.49 [926.85, 1641.40] | 117.03 s | 2 | CONCORDANT | [`10.1038/s41467-024-47774-8`](https://doi.org/10.1038/s41467-024-47774-8) |
| **07** | `06_zika_cuba_grubaugh2019` | Zika virus (Flaviviridae / Flavivirus, Asian lineage outbreak in the Americas / Cuba) | 283 | 4.23 yr | 2013.37 [2013.16, 2013.56] | 2012.58 [2012.14, 2012.93] | 7.11 s | 2 | CONCORDANT | [`10.1016/j.cell.2019.07.018`](https://doi.org/10.1016/j.cell.2019.07.018) |
| **08** | `07_mumps_wa_moncla2021` | Mumps virus (Genotype G) | 467 | 12.0 yr | 1996.48 [1993.92, 1998.86] | 2003.67 [2001.26, 2005.42] | 25.22 s | 3 | AUTOCLOCK RECONCILED | [`10.7554/eLife.66448`](https://doi.org/10.7554/eLife.66448) |
| **09** | `08_zika_angola_faria2018` | Zika virus (Asian lineage) | 393 | 10.38 yr | 2006.50 [2005.80, 2007.20] | 1999.82 [1997.99, 2001.31] | 12.77 s | 2 | AUTOCLOCK RECONCILED | [`10.1016/S1473-3099(19)30293-2`](https://doi.org/10.1016/S1473-3099(19)30293-2) |
| **10** | `09_sarscov2_p1_faria2021` | SARS-CoV-2 (Lineage P.1 / Gamma) | 132 | 0.19 yr | 2020.87 [2020.78, 2020.93] | 2020.71 [2020.63, 2020.76] | 6.91 s | 2 | CONCORDANT | [`10.1126/science.abh2644`](https://doi.org/10.1126/science.abh2644) |
| **11** | `10_chikungunya_rj_romero2023` | Chikungunya virus (ECSA genotype) | 148 | 4.08 yr | 2014.56 [2014.38, 2014.64] | 2012.29 [2008.20, 2013.91] | 3.32 s | 2 | CONCORDANT | [`10.1371/journal.pntd.0011536`](https://doi.org/10.1371/journal.pntd.0011536) |
| **12** | `11_dengue_polyepoch_suchard2020` | Dengue virus (DENV complete polyprotein) | 352 | 37.0 yr | 1,965.0 [1,958.0, 1,972.0] | 1952.79 [1945.89, 1957.81] | 9.48 s | 3 | NON-LINEAR (SPLINE) | [`10.48550/arXiv.2510.11982`](https://doi.org/10.48550/arXiv.2510.11982) |
| **13** | `12_yellow_fever_faria2018` | Yellow fever virus (YFV, Brazil 2017–2018 Epizootic) | 65 | 0.3 yr | 2016.58 [2016.32, 2016.82] | 2016.96 [2016.90, 2016.99] | 1.64 s | 4 | CONCORDANT | [`10.1126/science.aat7115`](https://doi.org/10.1126/science.aat7115) |
| **14** | `13_rymv_madagascar_suchard2020` | Rice yellow mottle virus (RYMV) | 300 | 46.0 yr | 1,852.0 [1,820.0, 1,885.0] | 1902.78 [1858.78, 1926.06] | 2.11 s | 4 | CONCORDANT | [`10.1093/ve/vez023`](https://doi.org/10.1093/ve/vez023) |
| **15** | `14_zika_fiji_henderson2020` | Zika virus (Pacific lineage) | 120 | 50.52 yr | 2014.60 [2013.90, 2015.20] | 1929.72 [1883.89, 1946.49] | 1.83 s | 4 | STEM VS CROWN | [`10.1038/s41467-021-21788-y`](https://doi.org/10.1038/s41467-021-21788-y) |
| **16** | `15_west_nile_pybus_suchard2020` | West Nile virus (WNV North American Outbreak 1999–2007) | 104 | 8.13 yr | 1998.60 [1997.80, 1999.30] | 1997.54 [1991.27, 1999.50] | 2.99 s | 5 | CONCORDANT | [`10.1073/pnas.1206598109`](https://doi.org/10.1073/pnas.1206598109) |
| **17** | `16_rabies_northamerica_biek2007` | Rabies virus (RABV) | 47 | 22.5 yr | 1972.40 [1,965.0, 1978.50] | 1964.31 [1952.02, 1971.43] | 0.57 s | 3 | CONCORDANT | [`10.1073/pnas.0700741104`](https://doi.org/10.1073/pnas.0700741104) |
| **18** | `17_influenza_h3n2_bedford_suchard2020` | Influenza A virus (A/H3N2 Hemagglutinin) | 402 | 43.0 yr | 1,968.0 [1967.50, 1968.50] | 1951.19 [1940.41, 1958.08] | 3.5 s | 3 | NON-LINEAR (SPLINE) | [`10.1038/nature14460`](https://doi.org/10.1038/nature14460) |
| **19** | `18_lassa_andersen_suchard2020` | Lassa mammarenavirus (LASV complete S-segment) | 211 | 44.0 yr | 1,060.0 [850.00, 1,250.0] | 1788.61 [1701.70, 1837.26] | 2.77 s | 5 | AUTOCLOCK RECONCILED | [`10.1016/j.cell.2015.07.020`](https://doi.org/10.1016/j.cell.2015.07.020) |
| **20** | `19_avian_influenza_h7_baele2018` | Avian influenza A (H7 Hemagglutinin) | 146 | 75.0 yr | 1,900.0 [1,885.0, 1,915.0] | 1352.45 [977.47, 1524.98] | 1.28 s | 2 | STEM VS CROWN | [`10.1093/molbev/msad242`](https://doi.org/10.1093/molbev/msad242) |
| **21** | `20_avian_influenza_n7_baele2018` | Avian influenza A (N7 Neuraminidase) | 92 | 76.0 yr | 1,905.0 [1,890.0, 1,920.0] | 1527.14 [1260.32, 1651.93] | 1.21 s | 3 | STEM VS CROWN | [`10.1093/molbev/msad242`](https://doi.org/10.1093/molbev/msad242) |
| **22** | `21_hiv1_gill_suchard2013` | Human Immunodeficiency Virus 1 (HIV-1 RT/Protease) | 275 | 17.24 yr | 1,960.0 [1,950.0, 1,970.0] | Deconvoluted [nan, nan] | 2.22 s | 2 | SUBTYPE MIXTURE | [`10.1371/journal.pcbi.1011640`](https://doi.org/10.1371/journal.pcbi.1011640) |
| **23** | `22_chikungunya_bolivia_valdez2026` | Chikungunya Virus (CHIKV, Togaviridae) | 77 | 0.33 yr | 2024.85 [2024.81, 2024.87] | 2023.20 [2019.93, 2024.01] | 1.78 s | 3 | CONCORDANT | [`10.3201/eid3207.260540`](https://doi.org/10.3201/eid3207.260540) |
| **24** | `23_dengue3_caribbean_siddle2023` | Dengue virus serotype 3 (DENV-3) | 839 | 70.06 yr | 1,960.0 [1,950.0, 1,970.0] | 1855.77 [1851.90, 1859.46] | 38.58 s | 6 | AUTOCLOCK RECONCILED | [`10.1038/s41467-024-47774-8`](https://doi.org/10.1038/s41467-024-47774-8) |
| **25** | `24_dengue4_caribbean_siddle2023` | Dengue virus serotype 4 (DENV-4) | 347 | 66.97 yr | 1,962.0 [1,952.0, 1,972.0] | 1902.64 [1867.73, 1923.69] | 9.3 s | 4 | AUTOCLOCK RECONCILED | [`10.1038/s41467-024-47774-8`](https://doi.org/10.1038/s41467-024-47774-8) |
| **26** | `25_fmdv_serotype_a_carvalho2013` | Foot-and-mouth disease virus (FMDV Serotype A VP1) | 184 | 57.71 yr | 1,955.0 [1,945.0, 1,965.0] | 1801.08 [1763.91, 1827.90] | 1.78 s | 2 | STEM VS CROWN | [`10.1016/j.vetmic.2012.02.009`](https://doi.org/10.1016/j.vetmic.2012.02.009) |
| **27** | `26_fmdv_serotype_o_carvalho2013` | Foot-and-mouth disease virus (FMDV Serotype O VP1) | 210 | 40.17 yr | 1,960.0 [1,950.0, 1,970.0] | 1874.80 [1740.32, 1918.03] | 1.83 s | 2 | STEM VS CROWN | [`10.1016/j.meegid.2012.08.016`](https://doi.org/10.1016/j.meegid.2012.08.016) |
| **28** | `27_hiv1_faria2014` | Human Immunodeficiency Virus 1 (HIV-1 Group M) | 466 | 18.5 yr | 1,920.0 [1,909.0, 1,930.0] | 1902.68 [1845.36, 1926.81] | 2.27 s | 4 | CONCORDANT | [`10.1126/science.1256739`](https://doi.org/10.1126/science.1256739) |
| **29** | `28_influenza_h1n1_2009_smith2009` | Influenza A Virus (2009 Pandemic H1N1 / S-OIV) | 100 | 0.67 yr | 2008.99 [2008.90, 2009.07] | 2008.76 [2008.53, 2008.91] | 1.66 s | 2 | CONCORDANT | [`10.1038/nature08182`](https://doi.org/10.1038/nature08182) |
| **30** | `29_ypestis_blackdeath_spyrou2019` | Yersinia pestis (Second Plague Pandemic & Ancient Roots) | 277 | 4836.0 yr | -5,000.0 [-6,457.0, -4,078.0] | -4239.10 [-5069.55, -3585.46] | 6.22 s | 3 | CONCORDANT | [`10.1038/s41467-019-12154-0`](https://doi.org/10.1038/s41467-019-12154-0) |
| **31** | `30_mpox_clade_ib_burundi2025` | Monkeypox virus (MPXV Clade Ib, Poxviridae) | 173 | 0.49 yr | 2023.95 [2023.67, 2024.22] | 2024.30 [2024.07, 2024.40] | 58.43 s | 5 | CONCORDANT | [`10.1038/s43856-025-01199-6`](https://doi.org/10.1038/s43856-025-01199-6) |
| **32** | `31_rsv_a_trovao2025` | Respiratory Syncytial Virus Group A (RSV-A, Pneumoviridae) | 1,046 | 45.38 yr | 1972.60 [1968.45, 1976.62] | 1912.53 [1870.28, 1947.29] | 70.32 s | 4 | NON-LINEAR (SPLINE) | [`10.1038/s41598-025-87332-w`](https://doi.org/10.1038/s41598-025-87332-w) |
| **33** | `32_usuv_netherlands_munger2026` | Usutu Virus (USUV, Flaviviridae) | 106 | 6.63 yr | 2,011.0 [2,009.0, 2,013.0] | 2007.60 [2005.05, 2009.35] | 2.96 s | 2 | CONCORDANT | [`10.1093/ve/veag041`](https://doi.org/10.1093/ve/veag041) |
| **34** | `33_chikv_civ_klitting2024` | Chikungunya Virus (CHIKV, West African genotype, Cote d'Ivoire lineage) | 34 | 60.03 yr | 1951.60 [1947.30, 1955.30] | 1949.80 [1906.00, 1964.51] | 0.9 s | 2 | CONCORDANT | [`10.1093/jtm/taaf002`](https://doi.org/10.1093/jtm/taaf002) |
| **35** | `34_asfv_europe_gambaro2025` | African Swine Fever Virus (ASFV Genotype II, Asfarviridae) | 99 | 24.64 yr | 2006.15 [2004.60, 2007.70] | 1997.29 [1994.96, 1,998.0] | 27.39 s | 3 | NON-LINEAR (SPLINE) | [`10.1093/gbe/evaf102`](https://doi.org/10.1093/gbe/evaf102) |
| **36** | `35_h3n2_ha_suchard2026` | Influenza A Virus (Avian Influenza A/H5N1 Hemagglutinin) | 190 | 9.0 yr | 1994.50 [1993.80, 1995.80] | 1976.62 [1861.33, 1987.05] | 2.13 s | 3 | STEM VS CROWN | [`10.1073/pnas.2602412123`](https://doi.org/10.1073/pnas.2602412123) |
| **37** | `36_denv1_suchard2026` | Dengue Virus Type 1 (DENV-1, Flaviviridae) | 287 | 37.0 yr | 1,952.0 [1,945.0, 1,960.0] | 1781.32 [1730.15, 1816.35] | 7.02 s | 3 | STEM VS CROWN | [`10.1073/pnas.2602412123`](https://doi.org/10.1073/pnas.2602412123) |
| **38** | `37_measles_1912_dux2020` | Measles virus & Rinderpest virus (Morbillivirus) | 51 | 107.85 yr | -528.00 [-1,145.0, 165.00] | 1224.21 [944.09, 1380.77] | 1.19 s | 2 | STEM VS CROWN | [`10.1126/science.aba9411`](https://doi.org/10.1126/science.aba9411) |
| **39** | `38_mab_commins2023` | Mycobacterium abscessus (Subspecies abscessus & massiliense) | 38 | 16.0 yr | ~1960 to 1980 CE for circulating DCCs Not reported | 1985.50 [1970.60, 1991.14] | 27.21 s | 2 | NON-LINEAR (SPLINE) | [`10.1073/pnas.2302033120`](https://doi.org/10.1073/pnas.2302033120) |
| **40** | `39_chikv_reunion_dellicour2020` | Chikungunya Virus (CHIKV, 1975–2025 Multi-Wave Cohort) | 251 | 50.18 yr | 2004.8 CE (95% HPD: 2004.5 to 2005.1) Not reported | 1954.99 [1948.09, 1960.62] | 6.58 s | 3 | AUTOCLOCK RECONCILED | [`10.1073/pnas.2621019123`](https://doi.org/10.1073/pnas.2621019123) |
| **41** | `40_hiv1_crf01ae_philippines2024` | Human Immunodeficiency Virus 1 (CRF01_AE) | 1,144 | 10.84 yr | ~1995 to 2002 CE for Philippine major clades Not reported | 1989.66 [1984.92, 1993.16] | 6.9 s | 3 | AUTOCLOCK RECONCILED | [`10.1093/ve/vead073`](https://doi.org/10.1093/ve/vead073) |
| **42** | `41_skygrid_rabies_gill2020` | Zaire ebolavirus (Sierra Leone 2014, Skygrid Tutorial) | 196 | 0.25 yr | 2014.20 [2014.10, 2014.30] | 2014.23 [2014.17, 2014.27] | 6.21 s | 5 | CONCORDANT | [`10.1093/molbev/msz172`](https://doi.org/10.1093/molbev/msz172) |

---

## 6. Autonomous Replication Protocol

Complete, deterministic replication instructions are specified in [`AGENT.MD`](AGENT.MD).

### Quickstart: Single-Cohort Dating & LOOCV
To calibrate any empirical alignment directly from the shipped BEAST XML archive:
```bash
python3 -m chronaeon.cli date \
  --beast beast.xml.gz \
  --loocv \
  --nonlinear-clocks \
  -o chronaeon_dating.json \
  -c chronaeon_dating.csv
```

### Quickstart: AutoClock Community Deconvolution
To deconvolve multi-clock rate heterogeneity directly from the shipped BEAST XML archive:
```bash
python3 -m chronaeon.cli autoclock \
  --beast beast.xml.gz \
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
  title     = {Rethinking Molecular Clock Dating: Continuous Sequence Manifolds, Closed-Form Ancestral Calibration, and the Fragility of Discrete Tip Pinning},
  journal   = {Bioinformatics / Systematic Biology},
  year      = {2026},
  note      = {Empirical Benchmark Portal: https://veg.github.io/chronaeon/}
}
```
