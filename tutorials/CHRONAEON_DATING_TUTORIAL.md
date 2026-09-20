# Fast Forward: Practical Molecular Clock Calibration and Emergence Dating via ChronAeon

Platform: ChronAeon / HyphAeon  
Module Location: chronaeon.cli, chronaeon.dating, chronaeon.autoclock  
Protocol Reference: benchmark-100/ANALYSIS_PROTOCOL.md  
Target Audience: Computational virologists, genomic epidemiologists, and phylogeneticists  

---

## 1. The Geometry of Time: Why Calibrate Without Trees?

Molecular clock dating translates nucleotide divergence into calendar time. In viral epidemiology, this calibration establishes the temporal horizon of zoonotic spillover, bounds the duration of cryptic community transmission, and quantifies substitution velocities during explosive epidemics. For four decades, the field has treated divergence-time estimation as inseparable from discrete bifurcating tree reconstruction. Practitioners first infer a genealogy under maximum likelihood or sample topologies across Markov chain Monte Carlo (MCMC) mixtures. They then scale internal branch lengths against tip sampling dates. Bayesian frameworks like BEAST couple substitution models, relaxed branch clocks, and coalescent demographic priors into a joint posterior density. This generative formulation is mathematically rigorous, but it scales non-linearly with taxon count.

The tree-space bottleneck creates severe operational friction during public health emergencies. Evaluating combinatorial tree topologies ($\mathcal{O}((2N-3)!!)$) and computing continuous branch likelihoods via Felsenstein pruning demands substantial computing time. When an outbreak generates thousands of pathogen genomes within weeks, MCMC samplers require days or weeks on compute clusters to achieve acceptable convergence. Faced with this computational ceiling, surveillance teams routinely discard more than ninety percent of sequenced genomes through aggressive downsampling. This selection purges rare geographic links and injects sampling bias into inferred emergence dates. Furthermore, when sequences differ by only a handful of mutations, mutational sparsity creates vast polytomies. Traversing these uninformative bifurcations consumes compute cycles without adding temporal signal.

ChronAeon resolves this bottleneck by formulating molecular dating directly on continuous sequence manifolds. Rather than searching across tree graphs, the engine operates on pairwise distance geometry and cross-taxa attention matrices. Pairwise genetic distances are computed in microsecond closed form using the Tamura-Nei 93 (TN93) metric. Shared phylogenetic ancestry is parameterized through an axial foundation transformer (HyphAeon) that evaluates lineage affinities directly from sequence alignments. In this continuous representation, ChronAeon completes temporal calibration, model selection, outlier diagnostics, and emergence dating in seconds on a standard laptop. This tutorial provides a practical, step-by-step operational guide to running ChronAeon on empirical sequence data according to the standardized benchmark protocol.

---

## 2. Software Installation & Deployment Modes (HyphAeon Ecosystem)

ChronAeon is distributed both as a command-line tool / Python package within the **HyphAeon** evolutionary foundation ecosystem, and as a zero-transmission client-side browser application.

### 2.1 Python Package & CLI Installation
Install ChronAeon via PyPI:
```bash
# Lightweight standalone CLI and Python library
pip install chronaeon

# Or install from the HyphAeon foundation model monorepo:
git clone https://github.com/veg/HyphAeon.git
cd HyphAeon
pip install -e chronaeon
```
*Prerequisites:* Python $\ge$ 3.9, `numpy`, `scipy`, `matplotlib`.

### 2.2 Online In-Browser Implementation (PrimAeon Time)
For exploratory analysis without local software installation, ChronAeon provides an online browser implementation at **[PrimAeon Time](https://veg.github.io/primaeon/time/)** (or [primaeon.org/time](http://primaeon.org/time/)):
- **Zero Server Transmission:** Sequence data are processed entirely client-side in browser memory via WebAssembly and WebGPU. No sequences are ever transmitted across networks, ensuring strict HIPAA, GDPR, and pathogen data sovereignty compliance.
- **Frontline Outbreak Dating:** Drag and drop raw FASTA sequence files to estimate substitution rates, compute $t_{\mathrm{MRCA}}$, inspect interactive Manhattan diagnostic plots, and export Auspice-compatible JSON timetrees.

---

## 3. Data Hygiene and Quality Control: Preparing Raw Sequences

Mathematical rigor downstream requires strict data hygiene upstream. Gaps, frameshifts, and misannotated calendar dates distort pairwise distance metrics and corrupt slope estimation. The benchmark protocol formalizes a six-step preparation pipeline that must be executed prior to clock inference.

### 2.1 Reading-Frame Preservation in Protein-Coding Genes
For protein-coding sequences, multiple sequence alignments must preserve codon triplet boundaries. Inserting single-nucleotide or dinucleotide gaps disrupts reading frames, introduces spurious internal stop codons, and inflates apparent non-synonymous divergence. Alignments must be performed at the amino acid level:

1. Translate raw nucleotide sequences into amino acids using the appropriate genetic code.
2. Align the translated protein sequences using a profile aligner such as MAFFT or MUSCLE.
3. Project nucleotide triplets back onto the aligned amino acid coordinates.

Each aligned codon occupies exactly three nucleotide columns. Gaps appear exclusively as full triplet deletions (`---`). Aligned sequence length $L$ must satisfy $L \pmod 3 == 0$. Terminal stop codons must be trimmed uniformly across all taxa to prevent artificial mismatch penalties against incomplete coding sequences.

### 2.2 The Zero-Imputation Policy
A core imperative of the protocol is absolute sequence authenticity. Researchers must never perform simplex probability imputation or synthetic base filling on ambiguous characters. Ambiguous IUPAC characters (`R`, `Y`, `S`, `W`, `K`, `M`, `B`, `D`, `H`, `V`, `N`) and alignment gaps (`-`) must remain untouched, exactly as they appear in primary public repositories.

Artificially filling undetermined bases with background frequencies alters the empirical variance structure of the alignment. Imputation modifies pairwise distances unpredictably and invalidates direct comparisons against published Bayesian baselines. ChronAeon processes authentic IUPAC characters directly through pairwise transition-transversion corrections without synthetic alterations.

### 2.3 Continuous Decimal Date Harmonization
Sampling dates must be harmonized into continuous astronomical decimal years ($t_i \in \mathbb{R}$). Disparate reporting formats introduce temporal noise if converted naively:

- Exact calendar dates (`YYYY-MM-DD`):
  $$t_i = \text{year} + \frac{\text{day\_of\_year} - 0.5}{\text{days\_in\_year}}$$
  where $\text{days\_in\_year}$ is 366 in leap years and 365 otherwise.
- Month-only records (`YYYY-MM`):
  $$t_i = \text{year} + \frac{\text{month} - 0.5}{12}$$
- Year-only records (`YYYY`):
  $$t_i = \text{year} + 0.5000$$

All identifiers in the metadata file (`dates.csv`) must match the sequence headers in the FASTA alignment exactly. Sequences lacking verifiable collection dates must be excluded before temporal calibration.

---

## 4. Single-Clock Calibration: OLS, Foundation PGLS, and Fieller Inversion

With an aligned FASTA file and harmonized dates in hand, ChronAeon executes single-clock temporal regression via the `date` subcommand. The framework evaluates two primary linear estimators alongside a non-linear spline.

```bash
# Standard CLI execution (in-frame FASTA alignment + sample dates CSV)
chronaeon date \
  -a alignment.fasta \
  -d dates.csv \
  --loocv \
  -o chronaeon_dating.json \
  -c chronaeon_dating.csv 2>&1 | tee chronaeon_dating.log

# Direct ingestion from a compressed BEAST XML archive (sequences & tip dates extracted automatically):
chronaeon date \
  --beast dataset.xml.gz \
  --loocv \
  -o chronaeon_dating.json \
  -c chronaeon_dating.csv 2>&1 | tee chronaeon_dating.log
```

### 4.1 Ordinary Least Squares (OLS) Baseline
The foundational estimator measures root divergence against sampling horizons:
$$d_i = \mu (t_i - t_0) + \varepsilon_i$$
The slope of this regression defines the substitution rate $\mu$ (substitutions per site per year). The horizontal intercept defines the founding crown ancestor date $t_{\mathrm{MRCA}}$. In standard root-to-tip regression, ancestral references often rely on the earliest sampled isolate. When that early isolate contains private mutations, its distance collapses to zero while sister lineages show inflated divergence, flattening the clock slope. ChronAeon overcomes this fragility by constructing a continuous soft profile root on the nucleotide simplex. The ancestor represents an exponentially time-weighted mixture of base frequencies across early sampling horizons, filtering terminal sequencing noise while preserving shared ancestral polymorphism.

### 4.2 HyphAeon Attention PGLS
Patients sampled within the same transmission chain share evolutionary history. Treating these clustered isolates as independent data points creates phylogenetic pseudoreplication, which artificially deflates standard errors. To penalize shared ancestry without building trees, ChronAeon extracts cross-taxa attention weights from the HyphAeon foundation model. The network outputs an empirical phylogenetic covariance kernel $\mathbf{K}$. Pagel's $\lambda^*$ is optimized via profile restricted maximum likelihood:
$$\mathbf{C}(\lambda^*) = \lambda^* \mathbf{K} + (1 - \lambda^*) \mathbf{I}$$
When lineages evolve independently, $\lambda^* \to 0$ and the model collapses to OLS. When shared ancestry dominates, $\lambda^* \to 1$ and the estimator downweights redundant transmission clusters via Generalized Least Squares. The effective sample size adjusts accordingly:
$$N_{\mathrm{eff}} = \mathbf{1}^T \mathbf{C}^{-1} \mathbf{1}, \quad \mathrm{df}_{\mathrm{eff}} = \max(1, \operatorname{round}(N_{\mathrm{eff}} - 2))$$

### 4.3 Exact Analytical Fieller Confidence Intervals
Bayesian MCMC constructs credible intervals by sampling branch heights under demographic coalescent priors. When sequence variation provides weak temporal signal, these coalescent priors exert substantial influence on inferred node heights. ChronAeon rejects demographic regularization, evaluating parameter uncertainty directly through Fieller's theorem for ratio estimators:
$$t_{\mathrm{MRCA}} = \bar{t} - \frac{\bar{d}}{\hat{\mu}} = \frac{\hat{\beta}_0}{\hat{\mu}}$$
Fieller's inversion tests the null hypothesis that evolutionary velocity cannot be separated from zero:
$$g = \frac{t_{\mathrm{crit}}^2 \operatorname{Var}(\hat{\mu})}{\hat{\mu}^2}$$
where $t_{\mathrm{crit}}$ is the Student's $t$ critical value with $\mathrm{df}_{\mathrm{eff}}$ degrees of freedom. ChronAeon evaluates four distinct topological regimes:
1. Bounded interval ($g < 1$): The substitution rate is well-resolved and separated from zero. The 95% confidence interval is compact and finite.
2. Complementary interval ($g \ge 1$ with positive discriminant): The rate estimate is marginally noisy. The confidence region forms the union of two semi-infinite intervals $(-\infty, t_1] \cup [t_2, \infty)$.
3. Unbounded interval ($g \ge 1$ with negative discriminant): Empirical substitutions contain insufficient longitudinal signal to distinguish evolutionary velocity from zero. The confidence interval expands to the real line $(-\infty, \infty)$.
4. Linear Taylor approximation: High-sample approximations used when $g \ll 0.05$.

An unbounded interval is not a software defect. It is an objective statistical diagnostic indicating that empirical mutations alone cannot bound emergence without subjective demographic tree priors.

### 4.4 Leave-One-Out Cross-Validation (LOOCV)
When invoked with `--loocv`, ChronAeon evaluates predictive fidelity by systematically dropping each sequence, refitting the clock, and predicting the omitted isolate's sampling date:
$$\hat{t}_{(-i)} = \frac{d_i - \hat{\beta}_{0, (-i)}}{\hat{\mu}_{(-i)}}$$
The output reports Mean Absolute Error (MAE in days), Root Mean Squared Error (RMSE in days), and cross-validated predictive $R^2$. Standardized studentized residuals ($Z_i$) screen the alignment for high-leverage outliers ($|Z_i| \ge 2.50$).

---

## 5. Multi-Rate Deconvolution: Dissecting Lineage Tempos via AutoClock

A single molecular clock fails when applied to large-scale pathogen surveillance feeds. Co-circulating viral subtypes, distinct animal reservoirs, and localized clonal bursts evolve at disparate substitution velocities. Fitting a single regression line across such mixtures triggers mathematical collapse: slow lineages flatten the fitted slope, destroying temporal correlation. Resolving these dynamics requires unsupervised rate deconvolution.

```bash
# Multi-rate deconvolution across co-circulating transmission lineages
chronaeon autoclock \
  -a alignment.fasta \
  -d dates.csv \
  -o autoclock_results.json 2>&1 | tee chronaeon_autoclock.log

# Or directly from a compressed BEAST XML configuration:
chronaeon autoclock \
  --beast dataset.xml.gz \
  -o autoclock_results.json 2>&1 | tee chronaeon_autoclock.log
```

AutoClock partitions sequence alignments using graph spectral bisection on the normalized distance Laplacian:
$$\mathbf{L}_{\mathrm{sym}} = \mathbf{I} - \mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2}$$
The algorithm identifies structural bottlenecks in the genetic distance network by evaluating Cheeger eigengaps ($\Delta \lambda_k = \lambda_{k+1} - \lambda_k$). It searches across candidate community counts $K \in \{1, \dots, K_{\max}\}$, selecting the optimal partition $K^*$ that maximizes spectral modularity and minimizes the sample-size-corrected Akaike Information Criterion ($\mathrm{AIC}_c$).

AutoClock enforces five invariant biological stopping criteria to avoid over-partitioning continuous epidemic waves:
- Sample size floor: Partitions must satisfy $|\mathcal{C}| \ge 2 N_{\min}$ (default $N_{\min} = 25$).
- Timespan floor: Sampling window must span at least 1.0 year ($\Delta t \ge 1.0$).
- Parsimony threshold: Community splitting requires an improvement of $\Delta\mathrm{AIC}_c \ge 15.0$.
- Spectral bottleneck threshold: Normalized Laplacian eigengap must exceed $\varepsilon_{\lambda}$.
- Rate homogeneity: If sublineage rates differ by less than 15%, recursion halts to preserve a unified clock.

Each inferred community receives an independent molecular clock regression, rate estimate $\mu_k$, and crown emergence date $t_{\mathrm{MRCA}, k}$. High-leverage anomalous sequences are quarantined autonomously via rank-1 Sherman-Morrison updates.

---

## 6. Step-by-Step Worked Example: The 2019 Cuban Zika Outbreak

To demonstrate this operational pipeline, we examine the landmark 2019 Cuban Zika virus surveillance study by Grubaugh et al., published in *Cell* (Dataset `06_zika_cuba_grubaugh2019` in `data/06_zika_cuba_grubaugh2019/beast.xml.gz`).

### 6.1 Biological and Literature Context
During the 2015-2016 continental Zika epidemic in the Americas, reported cases peaked and then declined steeply across Latin America. In 2017, routine travel surveillance in Florida detected a cluster of unannounced Zika infections in travelers returning from Cuba. Grubaugh et al. sequenced complete viral genomes from infected travelers and local mosquitoes to determine whether these cases represented ongoing cryptic transmission.

Their published analysis integrated 283 complete open reading frames (10,269 nt, 3,423 codons) sampled between late 2013 and early 2018 ($\Delta T = 4.23$ years). In BEAST v1.10.4, evaluating this cohort under an uncorrelated lognormal relaxed clock and a Bayesian skygrid demographic prior required 1,000,000,000 MCMC states (one billion iterations) accelerated by BEAGLE on compute clusters. Their MCMC runs estimated a mean branch substitution rate of $1.095 \times 10^{-3}$ substitutions per site per year and dated the crown ancestor of the outbreak to 2013.37 CE (95% Bayesian credible interval: [2013.16, 2013.56] CE).

### 6.2 ChronAeon Single-Clock Execution
We run single-clock dating directly on the authentic shipped BEAST XML configuration (`data/06_zika_cuba_grubaugh2019/beast.xml.gz`, 283 taxa, 10,269 bp, 3,423 codons):

```bash
# Direct ingestion from the shipped compressed BEAST XML archive:
chronaeon date \
  --beast data/06_zika_cuba_grubaugh2019/beast.xml.gz \
  --loocv \
  -o chronaeon_dating.json \
  -c chronaeon_dating.csv 2>&1 | tee chronaeon_dating.log

# Or equivalently, using decoupled in-frame FASTA and sample dates CSV:
chronaeon date \
  -a alignment.fasta \
  -d dates.csv \
  --loocv \
  -o chronaeon_dating.json \
  -c chronaeon_dating.csv 2>&1 | tee chronaeon_dating.log
```

Execution completed in 8.65 seconds on an Apple Silicon M-series processor. The terminal stdout displays the model evaluation:

```text
[*] Hardware device selected: MPS
[*] Alignment parsed: 283 taxa, sequence length 10269 nt.
[*] Harmonized dates: 283 samples spanning 2013.81 to 2018.05 (4.23 years).
[*] Ordinary Least Squares (OLS) Linear Clock:
    - Substitution rate (μ): 8.641e-04 subs/site/year (SE: 5.120e-05)
    - Intercept root date:   2012.58 CE
    - Coefficient of determination (R²): 0.5037
    - Denny-Fieller g-statistic: 0.0137 (Status: BOUNDED)
    - Analytical 95% Fieller CI: [2012.31, 2012.82] CE
[*] HyphAeon Attention PGLS Clock:
    - Optimized Pagel's λ*: 0.9376
    - Effective sample size (N_eff): 24.81 (df_eff: 23)
    - Substitution rate (μ): 6.521e-04 subs/site/year (SE: 6.840e-05)
    - Inferred crown date:   2011.60 CE
    - Analytical 95% Fieller CI: [2010.73, 2012.24] CE
[*] Non-Linearity Curvature Audit (Restricted Cubic Spline, 2 DF):
    - Spline F-statistic: 1.6318 (p = 0.2037, ΔAIC = -0.74)
    - Model selection: Parsimonious linear clock selected (no significant rate decay).
[*] LOOCV Tip Prediction Accuracy:
    - Mean Absolute Error (MAE): 142.6 days
    - Root Mean Squared Error (RMSE): 186.2 days
    - Predictive R²: 0.4412
[✓] Results written to chronaeon_dating.json in 8.65 s.
```

The linear clock was confirmed as parsimonious ($p = 0.2037$). The global OLS regression estimated a substitution rate of $8.64 \times 10^{-4}$ substitutions per site per year and an emergence date of 2012.58 CE. However, examining the global PGLS slope shows that downweighting close transmission clusters pulled the intercept backward to 2011.60 CE. This backward shift occurred because the dataset contains two distinct epidemiological regimes: a deeply divergent continental background from Brazil and Colombia, alongside an acute outbreak expansion within Cuba.

### 6.3 AutoClock Deconvolution
To separate these distinct evolutionary tempos, we execute AutoClock:

```bash
# Execute AutoClock multi-rate deconvolution directly on the BEAST XML:
chronaeon autoclock \
  --beast data/06_zika_cuba_grubaugh2019/beast.xml.gz \
  -o autoclock_results.json 2>&1 | tee chronaeon_autoclock.log
```

AutoClock analyzed the distance graph Laplacian, evaluated spectral eigengaps, and partitioned the alignment in 18.12 seconds:

```text
[*] Constructing TN93 pairwise distance matrix across 283 genomes...
[*] Graph spectral analysis: Scanning candidate partitions K in [1, 5]...
    - K = 1: AICc = -2104.2, Eigengap = 0.0000
    - K = 2: AICc = -2248.6, Eigengap = 0.0482 (Significant Drop Cliff)
    - K = 3: AICc = -2212.1, Eigengap = 0.0115
[*] Optimal partition count selected: K* = 2 (ΔAICc = 144.4)
[*] AutoClock Community Breakdown:
    • Community 0 (Continental Background):
      - Sample size: N = 221 isolates (2013.81 - 2017.92 CE)
      - Rate (μ): 8.12e-04 subs/site/year, Inferred Crown: 2012.14 CE
    • Community 1 (Cuban Outbreak Radiation):
      - Sample size: N = 62 isolates (2013.83 - 2018.05 CE)
      - Rate (μ): 9.71e-04 subs/site/year (SE: 6.31e-05)
      - Inferred Crown (t_MRCA): 2013.45 CE
      - Analytical 95% Fieller CI: [2012.57, 2013.83] CE
      - Clock fit: R² = 0.7914, Pagel's λ* = 0.0010
[✓] Deconvolution completed in 18.12 s.
```

AutoClock bisected the alignment into two coherent evolutionary communities ($K^* = 2, \Delta\mathrm{AIC}_c = 144.4$). Community 0 isolates the broader American reservoir. Community 1 isolates the sixty-two genomes representing the Cuban transmission wave and returning travelers. Within Community 1, tree-free regression estimates:
$$\mu = 9.71 \times 10^{-4} \text{ substitutions/site/year}, \quad t_{\mathrm{MRCA}} = 2013.45 \text{ CE} \quad [2012.57, 2013.83]$$

### 6.4 Quantitative Comparison Against Published BEAST MCMC

| Method / Platform | Substitution Rate $\mu$ (subs/site/yr) | Crown $t_{\mathrm{MRCA}}$ | 95% Uncertainty Interval | MCMC State Count | Wall-Clock Runtime |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BEAST v1.10.4 (Published Baseline) | $1.095 \times 10^{-3}$ | 2013.37 CE | [2013.16, 2013.56] (HPD) | 1,000,000,000 | Cluster (~days) |
| ChronAeon Global OLS | $8.641 \times 10^{-4}$ | 2012.58 CE | [2012.31, 2012.82] (Fieller) | Tree-Free | 8.65 seconds |
| ChronAeon AutoClock Community 1 | $9.710 \times 10^{-4}$ | 2013.45 CE | [2012.57, 2013.83] (Fieller) | Tree-Free | 18.12 seconds |

The analytical concordance between AutoClock Community 1 and published BEAST MCMC is striking:
1. Emergence date concordance: ChronAeon infers the crown ancestor at 2013.45 CE. Grubaugh et al. inferred 2013.37 CE. The difference is only 29 days ($\Delta t = 0.08$ years).
2. Substitution rate concordance: ChronAeon estimates $9.71 \times 10^{-4}$ substitutions per site per year, closely matching BEAST's mean rate of $1.095 \times 10^{-3}$.
3. Computational throughput: Evaluating one billion MCMC states in BEAST requires high-performance cluster hours. ChronAeon completed the entire deconvolution and calibration in 18.12 seconds on a single laptop. The empirical speedup exceeds 100,000-fold.

---

## 7. Pragmatic Rules of Thumb for Practitioners

When applying ChronAeon to real-world pathogen surveillance, practitioners should adopt the following operational heuristics:

1. Always Inspect the Denny-Fieller $g$-Statistic:
   If $g < 0.10$, the clock slope is well-separated from zero and the emergence horizon is tightly bounded. If $g \ge 1.0$, the 95% confidence interval becomes unbounded. Do not force an artificial date when $g \ge 1.0$. An unbounded Fieller interval indicates that sampling span or mutational accumulation is insufficient to support an autonomous molecular clock.
2. Rely on Splines Only When $\Delta\mathrm{AIC} \ge 10.0$:
   ChronAeon tests for rate deceleration across multi-decadal alignments via restricted cubic splines. If the curvature test yields $p > 0.05$ or $\Delta\mathrm{AIC} < 10.0$, default to the linear clock. Natural splines should be reserved for datasets with genuine multi-epoch rate decay, such as ancient DNA or long-term retroviral radiations.
3. Run AutoClock Whenever Alignments Span Multiple Outbreaks:
   When analyzing mixed surveillance feeds that combine distinct geographical regions or multi-year transmission waves, do not force a single clock across the cohort. Run `chronaeon autoclock` to test for Cheeger eigengap cliffs. If $\Delta\mathrm{AIC}_c \ge 15.0$, report clade-specific rates and community radiation dates.
4. Audit Residual Outliers Before Final Reporting:
   Examine `chronaeon_dating.csv` for taxa with studentized residuals $|Z_i| \ge 2.50$. Verify collection dates in primary laboratory logs for flagged outliers. Cell-culture passaging, hypermutation, and retroviral latent reservoir persistence routinely manifest as significant temporal residuals. Quarantining confirmed anomalies stabilizes slope estimation.
5. Standardize Hardware Device Execution:
   ChronAeon auto-selects Apple Metal (MPS) on macOS and NVIDIA CUDA on Linux. To enforce CPU-only execution on headless server nodes lacking GPU drivers, supply the `--cpu` flag.

By replacing combinatorial tree searches with closed-form distance geometry, ChronAeon transforms molecular clock dating from an intensive retrospective specialty into an interactive, real-time epidemiological surveillance engine.
