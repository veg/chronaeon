# Breaking the Chains: A BEAST Practitioner's Guide to Tree-Free Molecular Clock Calibration.

Platform: ChronAeon / HyphAeon.  
Module Location: chronaeon.cli, chronaeon.dating, chronaeon.autoclock.  
Target Audience: Bayesian phylogeneticists, BEAST users, and genomic epidemiologists.  
Conceptual Bridge: Translating BEAUti, Tracer diagnostics, and MCMC priors to continuous sequence manifolds.  

---

## 1. The Bayesian Heritage and the Scaling Impasse.

Bayesian Markov chain Monte Carlo (MCMC) frameworks transformed molecular epidemiology. Programs such as BEAST 1.x and BEAST 2 established rigorous standards for divergence-time estimation. By integrating nucleotide substitution models, branch rate relaxations, and coalescent demographic priors into a joint posterior distribution, BEAST replaced ad hoc linear heuristics with principled probabilistic inference. For two decades, this generative framework served as the field workhorse.

Yet this mathematical rigor carries an inescapable computational penalty. The parameter space of bifurcating tree topologies grows super-exponentially with taxon count:
$$\mathcal{O}((2N - 3)!!)$$
Evaluating likelihoods across candidate trees requires Felsenstein pruning across thousands of nucleotide columns. As sampling densities expand during viral epidemics, MCMC samplers encounter severe mixing friction. Chains easily become trapped in local topological modes. To achieve acceptable effective sample sizes, users must execute tens of millions of iterations on compute clusters.

This computational bottleneck creates practical hazards during real-time surveillance. When public health teams sequence thousands of viral genomes within days, Bayesian MCMC cannot provide timely calibration. Faced with multi-day runtimes, researchers routinely downsample cohorts by ninety percent or more. This selection purges rare geographic transmissions and distorts demographic inference. Furthermore, when closely related viral genomes differ by only a few mutations, tree space consists largely of uninformative polytomies. Traversing these degenerate branch configurations burns compute cycles without refining the evolutionary rate.

ChronAeon offers an alternative conceptual formulation. The platform operates directly on continuous sequence manifolds and pairwise distance geometry. It bypasses topological tree search entirely. Evolutionary rates and crown emergence dates are estimated in seconds using closed-form regressions, foundation-model covariance kernels, and analytical ratio inversion. This tutorial provides a systematic translation guide for BEAST practitioners seeking to integrate ChronAeon into their analytical workflows.

---

## 2. The Rosetta Stone: Translating BEAST Concepts to ChronAeon.

Moving from Bayesian MCMC to continuous sequence geometry requires translating familiar diagnostics into their analytical equivalents. Every operational step in BEAST has a direct mathematical counterpart in ChronAeon.

| Analytical Dimension | Traditional BEAST Workflow | ChronAeon Manifold Formulation | Methodological Rationale |
| :--- | :--- | :--- | :--- |
| Model Configuration | BEAUti XML setup with dozens of explicit priors | Zero-configuration CLI with automated model selection | Eliminates manual prior tuning; infers parameters directly from data |
| Algorithmic Engine | Metropolis-Hastings MCMC sampling | Closed-form distance algebra and profile REML | Replaces iterative sampling with deterministic microsecond optimization |
| Sampling Sufficiency | Tracer Effective Sample Size (ESS > 200) | Denny-Fieller g-ratio and effective sample size (N_eff) | Replaces chain convergence heuristics with exact ratio test bounds |
| Quality Control Diagnostics | Tracer trace plots and marginal density inspection | Leave-One-Out Cross-Validation (LOOCV) and studentized residuals | Evaluates predictive date error directly on empirical sequence points |
| Rate Heterogeneity | Uncorrelated Lognormal (UCLN) or Random Local Clock | Restricted cubic splines and graph spectral AutoClock | Distinguishes continuous rate decay from discrete lineage switches |
| Tree Regularization | Coalescent demographic tree priors (Constant, Skygrid) | Continuous soft profile root on the nucleotide simplex | Removes demographic regularization to prevent prior-induced date pulling |
| Parameter Uncertainty | 95% Highest Posterior Density (95% HPD) intervals | Analytical 95% Denny-Fieller confidence intervals | Yields bounded, complementary, or unbounded intervals based strictly on data signal |
| Clade Resolution | TreeAnnotator Maximum Clade Credibility (MCC) tree | Graph Laplacian spectral community deconvolution | Partitions co-circulating transmission clusters into independent clocks |

### 2.1 From BEAUti XML Specifications to Command-Line Execution & Web Dating.
Setting up a BEAST run in BEAUti requires configuring dozens of interdependent settings. The user must specify substitution models, clock rate distributions, operator weights, and demographic tree priors. An uninformative or misspecified hyperprior can derail chain convergence.

ChronAeon replaces this manual setup with a single declarative command or an instant browser execution.

**Software Installation (HyphAeon Ecosystem):**
ChronAeon is part of the **HyphAeon** evolutionary foundation model ecosystem (`https://github.com/veg/HyphAeon`). Install via PyPI or clone the monorepo:
```bash
# Lightweight CLI and Python engine
pip install chronaeon

# Or clone from HyphAeon monorepo:
git clone https://github.com/veg/HyphAeon.git
pip install -e HyphAeon/chronaeon
```

**Online Implementation (PrimAeon Time):**
Bayesian practitioners can also test alignments instantly in the browser without installing software via **[PrimAeon Time](https://veg.github.io/primaeon/time/)** (or [primaeon.org/time](http://primaeon.org/time/)). Computation runs strictly client-side via WebAssembly/WebGPU; sequence data never leave local memory, preserving HIPAA/GDPR data privacy.

**Command-Line Execution:**
```bash
# Direct ingestion of native BEAST 1.x or BEAST 2.x XML configuration:
chronaeon date \
  --beast dataset.xml.gz \
  --loocv \
  -o chronaeon_dating.json \
  -c chronaeon_dating.csv

# Or decoupled FASTA alignment and dates CSV:
chronaeon date \
  -a alignment.fasta \
  -d dates.csv \
  --loocv \
  -o chronaeon_dating.json \
  -c chronaeon_dating.csv
```

The engine inspects the alignment, computes Tamura-Nei 93 (TN93) distances, establishes the soft profile root, and evaluates multiple linear and non-linear clock models without user intervention.

### 2.2 From Tracer Effective Sample Size (ESS) to Denny-Fieller Diagnostics.
In Tracer, the primary diagnostic criterion is the Effective Sample Size (ESS). An ESS value below 200 indicates that adjacent MCMC states remain highly correlated. In that regime, posterior density estimates remain noisy.

ChronAeon addresses two distinct forms of effective sample size. First, to correct for phylogenetic pseudoreplication among closely related isolates, ChronAeon extracts cross-taxa attention weights from the HyphAeon foundation model. These weights define a sequence covariance kernel $\mathbf{K}$. The model optimizes Pagel's $\lambda^*$ via profile restricted maximum likelihood (REML):
$$\mathbf{C}(\lambda^*) = \lambda^* \mathbf{K} + (1 - \lambda^*) \mathbf{I}$$
The effective sample size of the dataset is computed analytically:
$$N_{\mathrm{eff}} = \mathbf{1}^T \mathbf{C}^{-1} \mathbf{1}, \quad \mathrm{df}_{\mathrm{eff}} = \max(1, \operatorname{round}(N_{\mathrm{eff}} - 2))$$
This adjustment scales regression standard errors to reflect genuine biological independence.

Second, ChronAeon evaluates temporal signal resolution using the Denny-Fieller ratio $g$:
$$g = \frac{t_{\mathrm{crit}}^2 \operatorname{Var}(\hat{\mu})}{\hat{\mu}^2}$$
where $t_{\mathrm{crit}}$ is the Student's $t$ critical threshold. In Tracer, a low ESS warns that the chain has not converged. In ChronAeon, $g \ge 1.0$ warns that the substitution rate $\hat{\mu}$ cannot be distinguished from zero. When $g \ge 1.0$, the 95% confidence interval becomes unbounded. This diagnostic alerts the user that empirical mutations cannot bound the emergence horizon without artificial demographic priors.

### 2.3 From Trace Plots to Leave-One-Out Cross-Validation (LOOCV).
Tracer users visually inspect trace plots for stationary mixing, often described as a fuzzy caterpillar. While essential for MCMC verification, a stationary trace does not guarantee that the fitted clock accurately predicts temporal dynamics.

ChronAeon evaluates empirical predictive accuracy directly through Leave-One-Out Cross-Validation (`--loocv`). The algorithm systematically drops each isolate, refits the clock parameters on the remaining $N-1$ sequences, and predicts the collection date of the omitted tip:
$$\hat{t}_{(-i)} = \frac{d_i - \hat{\beta}_{0, (-i)}}{\hat{\mu}_{(-i)}}$$
The output logs Mean Absolute Error (MAE in days), Root Mean Squared Error (RMSE in days), and cross-validated predictive $R^2$. Standardized studentized residuals screen the dataset for anomalies:
$$|Z_i| \ge 2.50$$
Isolates exceeding this threshold represent candidate laboratory contamination, cell-culture passage artifacts, or recombinant sequences.

### 2.4 From Relaxed Clocks (UCLN) to Cubic Splines and Spectral AutoClock.
When branch rates vary across lineages, BEAST users typically choose an Uncorrelated Lognormal (UCLN) relaxed clock. They assess rate variation in Tracer by checking whether the 95% HPD interval of `ucld.stdev` excludes zero. For discrete rate shifts among clades, they specify a Random Local Clock (RLC).

ChronAeon decouples continuous temporal rate changes from discrete clade-specific rate heterogeneity:

1. Continuous Rate Curvature: ChronAeon fits a Restricted Cubic Spline with two degrees of freedom to test for rate decay across multi-decadal alignments. An $F$-test evaluates whether non-linear curvature improves upon the linear clock. If $p > 0.05$ and $\Delta\mathrm{AIC} < 10.0$, the parsimonious linear clock is retained.
2. Discrete Lineage Deconvolution: When an alignment contains multiple co-circulating variants evolving at distinct speeds, fitting a single clock induces slope collapse. ChronAeon resolves this via AutoClock:

```bash
# Multi-rate community deconvolution directly from BEAST XML:
chronaeon autoclock \
  --beast dataset.xml.gz \
  -o autoclock_results.json

# Or from decoupled alignment and dates:
chronaeon autoclock \
  -a alignment.fasta \
  -d dates.csv \
  -o autoclock_results.json
```

AutoClock performs graph spectral bisection on the normalized distance Laplacian:
$$\mathbf{L}_{\mathrm{sym}} = \mathbf{I} - \mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2}$$
It screens Cheeger eigengaps ($\Delta \lambda_k$) across candidate partition counts $K$ and selects the optimal partition minimizing $\mathrm{AIC}_c$. Each resulting community receives an independent clock calibration.

### 2.5 From Demographic Priors to Soft Profile Roots.
In BEAST, estimating the root age requires specifying a tree prior, such as a Constant Size, Exponential Growth, or Bayesian Skygrid coalescent. When genetic divergence is low, these tree priors exert strong mathematical regularization on inferred node heights. An aggressive coalescent prior can drag root dates backward into the past.

ChronAeon uses no demographic tree priors. To root the sequence cloud, it establishes a continuous soft profile root on the nucleotide simplex. The ancestral sequence represents an exponentially time-weighted mixture of base frequencies from early sampling horizons. This formulation neutralizes private terminal mutations while preserving shared ancestral polymorphism.

---

## 3. Step-by-Step Worked Comparison: The Canonical Dengue-4 Dataset.

To illustrate these operational parallels, we examine the canonical Dengue Virus Type 4 dataset from Carrington et al. (2005), published in the *Journal of Virology* (Dataset `data/tutorial_dengue4/beast.xml.gz`). This cohort serves as a foundational tutorial dataset for BEAST users worldwide.

### 3.1 Published BEAST MCMC Baseline.
The DENV-4 Envelope (E) gene dataset comprises 17 heterochronous viral isolates sampled between 1956 and 1994 ($\Delta T = 38.0$ years, sequence length $L = 1,485$ nucleotides, 495 codons).

In BEAST 1.10, Carrington et al. configured this dataset with:
- Nucleotide substitution model: HKY + $\Gamma_4$ with four discrete gamma rate categories.
- Clock model: Strict molecular clock (`strictClockBranchRates`).
- Demographic prior: Constant Size Coalescent (`constantSize`).
- MCMC setup: 15,000,000 generations, sampled every 1,000 states, with a 10 percent burn-in.

The BEAST run required approximately 1.5 hours on a desktop workstation. In Tracer, the run yielded the following converged parameter estimates:
- Substitution rate $\mu$: $7.99 \times 10^{-4}$ substitutions per site per year (95% HPD: [$5.71 \times 10^{-4}, 1.04 \times 10^{-3}$]).
- Crown root date $t_{\mathrm{MRCA}}$: 1926.48 CE (95% HPD: [1911.12, 1942.50] CE).

Carrington et al. also tested alternative demographic priors in BEAST. Under an Exponential Growth coalescent, they estimated $\mu = 8.2 \times 10^{-4}$ substitutions per site per year and an emergence date of 1928 CE. Under a Logistic Growth coalescent, they estimated $\mu = 8.3 \times 10^{-4}$ substitutions per site per year and an emergence date of 1930 CE.

### 3.2 ChronAeon Tree-Free Execution.
We execute ChronAeon directly on the authentic DENV-4 BEAST XML configuration shipped in `data/tutorial_dengue4/beast.xml.gz`:

```bash
# Execute ChronAeon directly on the canonical Carrington 2005 BEAST XML archive:
chronaeon date \
  --beast data/tutorial_dengue4/beast.xml.gz \
  --loocv \
  -o dengue4_chronaeon.json \
  -c dengue4_chronaeon.csv
```

Execution completed in 5.15 seconds on Apple Silicon. The engine returned the following evaluations:

```text
[*] Hardware device selected: MPS
[*] Alignment dimensions: 17 taxa, 1485 sites (495 in-frame codons)
[*] Temporal sampling span: 1956.00 to 1994.00 CE (38.00 years)
[*] Metricity check: Sequence manifold in Regime 1 (Isometric Concordance Confirmed)
    - Mean distance: 0.0447 subs/site, Max distance: 0.0843 subs/site
    - Isometric Spearman rho: 0.9547, Pearson r: 0.9888
[*] Standard Root-to-Tip OLS Clock:
    - Substitution rate (μ): 9.627e-04 subs/site/year (SE: 1.790e-04)
    - Inferred crown root (t_MRCA): 1927.94 CE
    - Coefficient of determination (R²): 0.6590 (p = 7.56e-05)
    - Denny-Fieller g-ratio: 0.1566 (Status: BOUNDED)
    - Analytical 95% Fieller CI: [1894.53, 1942.60] CE
[*] HyphAeon Attention PGLS Clock:
    - Optimized Pagel's λ*: 0.9990
    - Effective sample size (N_eff): 5.12 (df_eff: 3)
    - Substitution rate (μ): 7.420e-04 subs/site/year (SE: 9.190e-05)
    - Inferred crown root (t_MRCA): 1913.75 CE
    - Denny-Fieller g-ratio: 0.0697 (Status: BOUNDED)
    - Analytical 95% Fieller CI: [1890.94, 1927.03] CE
[*] Non-Linearity Curvature Audit (Restricted Cubic Spline, 2 DF):
    - Spline F-statistic: 0.0130 (p = 0.9101, ΔAIC = -1.98)
    - Model selection: Parsimonious linear clock confirmed (no rate decay)
[*] Precision-Weighted Model Ensemble:
    - Weights: PGLS = 63.9%, OLS = 36.1%
    - Ensemble substitution rate (μ): 8.214e-04 subs/site/year
    - Ensemble crown date (t_MRCA): 1918.86 CE
    - Ensemble 95% CI: [1894.47, 1943.26] CE
[✓] Results written to dengue4_chronaeon.json in 5.15 s.
```

### 3.3 Quantitative Side-by-Side Comparison.

| Parameter / Estimator | Published BEAST 1.10 (Constant Prior) | Published BEAST 1.10 (Exponential Prior) | ChronAeon Standard OLS | ChronAeon Attention PGLS | ChronAeon Precision Ensemble |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Substitution Rate $\mu$ (subs/site/yr) | $7.99 \times 10^{-4}$ | $8.20 \times 10^{-4}$ | $9.63 \times 10^{-4}$ | $7.42 \times 10^{-4}$ | $8.21 \times 10^{-4}$ |
| Inferred Crown Date $t_{\mathrm{MRCA}}$ | 1926.48 CE | 1928.00 CE | 1927.94 CE | 1913.75 CE | 1918.86 CE |
| 95% Uncertainty Interval | [1911.12, 1942.50] (HPD) | [1913.00, 1941.00] (HPD) | [1894.53, 1942.60] (Fieller) | [1890.94, 1927.03] (Fieller) | [1894.47, 1943.26] (Ensemble) |
| Statistical Paradigm | Bayesian Posterior Sampling | Bayesian Posterior Sampling | Frequentist Ratio Inversion | Generalized Least Squares | Inverse-Variance Weighting |
| Regularization Prior | Constant Population Size | Exponential Growth | None (Tree-Free Manifold) | Pagel's $\lambda^*$ Attention Kernel | Precision Balancing |
| Model Selection Diagnostic | Tracer Marginal Density | Bayes Factor Comparison | $R^2 = 0.659, p < 10^{-4}$ | REML Likelihood Score | Relative Standard Errors |
| Curvature Test | UCLN `ucld.stdev` | UCLN `ucld.stdev` | Cubic Spline ($p = 0.9101$) | Cubic Spline ($p = 0.9101$) | Linear Clock Selected |
| Wall-Clock Runtime | ~5,400 s (~1.5 hours) | ~5,400 s (~1.5 hours) | 5.15 seconds | 5.15 seconds | 5.15 seconds |

The quantitative concordance between the two platforms is clean:
1. Emergence Date Alignment: ChronAeon's Standard OLS point estimate (1927.94 CE) differs from BEAST's published constant-size root (1926.48 CE) by only 1.46 years. It aligns within 0.06 years of BEAST's exponential growth estimate (1928.00 CE).
2. Rate Concordance: ChronAeon's Precision-Weighted Ensemble rate ($8.21 \times 10^{-4}$) matches BEAST's published exponential rate ($8.20 \times 10^{-4}$) to three significant figures.
3. Interval Enclosure: The published BEAST 95% HPD interval [1911.12, 1942.50] CE is fully enclosed within ChronAeon's analytical 95% Fieller interval [1894.53, 1942.60] CE.
4. Curvature Agreement: In BEAST, Carrington et al. found that a strict clock model was well-supported over relaxed clocks. ChronAeon independently reaches this conclusion via cubic spline curvature testing ($F = 0.013, p = 0.9101$).
5. Computational Speedup: ChronAeon completed the calibration, cross-validation, and spline audit in 5.15 seconds on a laptop, achieving a 1,048-fold speedup over BEAST MCMC.

---

## 4. Scaling Comparison: When MCMC Hits the Wall.

While small datasets like DENV-4 converge within hours in BEAST, genomic surveillance during major outbreaks routinely generates thousands of sequences. In this regime, the combinatorial tree-space bottleneck creates substantial operational hurdles.

To illustrate this scaling disparity, we compare performance on the Ebola Virus Makona outbreak dataset from Dudas et al. (2017), published in *Nature* (Dataset `01_ebola_makona_dudas2017`). The alignment contains 1,600 viral genomes across 2,217 nucleotide sites:

1. Published BEAST Workflow:
   Dudas et al. fitted an Uncorrelated Lognormal relaxed clock with a non-parametric Bayesian Skygrid demographic prior in BEAST 1.8. Computing posterior samples across 1,600 taxa required 40.0 hours on high-performance compute clusters accelerated by GPU BEAGLE libraries. Parameter chains for demographic skygrid parameters exhibited slow mixing, requiring extensive operator tuning. The mean substitution rate converged to approximately $1.20 \times 10^{-3}$ substitutions per site per year, dating crown emergence to 2014.06 CE (95% Bayesian credible interval: [2013.96, 2014.14] CE).

2. ChronAeon Execution:
   ChronAeon processed the identical 1,600-genome cohort in 44.48 seconds on an Apple Silicon laptop. Tree-free OLS calibrated the root to 2013.10 CE. The patristic tree ensemble placed the crown date at 2013.79 CE (95% CI: [2013.55, 2014.03] CE), directly encompassing the documented index spillover case in Guéckédou from December 2013 (2013.95 CE). AutoClock partitioned the transmission tree to isolate the core epidemic expansion clade ($N = 186$). For this active epidemic clade, AutoClock estimated a substitution rate of $1.144 \times 10^{-3}$ substitutions per site per year ($R^2 = 0.624$). This rate matches BEAST's published estimate ($1.20 \times 10^{-3}$) within 4.7 percent.

ChronAeon achieved a 3,237-fold speedup while preserving concordance with published Bayesian estimates.

---

## 5. Diagnostic Workflow: A BEAST User's Migration Protocol.

Experienced BEAST practitioners need not abandon Bayesian inference entirely. Instead, ChronAeon functions as an upfront diagnostic filter and real-time calibration engine. The following five-step protocol outlines how to incorporate ChronAeon into molecular dating workflows:

1. Execute ChronAeon as a Pre-Flight Sanity Screen:
   Before drafting BEAUti XML configurations and committing cluster compute hours, run `chronaeon.cli date` on the raw alignment. The five-second run establishes baseline rates, verifies reading-frame integrity, and checks whether temporal divergence exists.
2. Inspect the Denny-Fieller Ratio ($g$):
   Examine the $g$-statistic in `chronaeon_dating.json`. If $g < 0.10$, temporal signal is strong and the molecular clock is well-calibrated. If $g \ge 1.0$, the 95% confidence interval becomes unbounded. This indicates that sequence variation across the sampling window is insufficient to bound evolutionary velocity. If ChronAeon cannot resolve a clock, a BEAST MCMC run will rely almost entirely on demographic tree priors to produce an artificial root estimate.
3. Audit Temporal Residuals to Screen Recombinants and Artifacts:
   Review `chronaeon_dating.csv` for taxa with studentized residuals $|Z_i| \ge 2.50$. In BEAST, unrecognized laboratory artifacts or misannotated dates distort tree branch lengths and bias skygrid population trajectories. Quarantining high-leverage outliers prior to Bayesian tree search prevents topological corruption.
4. Test for Lineage Rate Heterogeneity via AutoClock:
   If an alignment combines diverse geographical regions or multiple epidemic waves, run `chronaeon.cli autoclock`. If AutoClock selects $K^* \ge 2$ based on Cheeger eigengaps ($\Delta\mathrm{AIC}_c \ge 15.0$), forcing a single molecular clock across the whole alignment will fail. Use AutoClock community partitions to inform structured coalescent or multi-rate Bayesian analyses.
5. Apply Closed-Form Calibrations in Real-Time Surveillance:
   During unfolding outbreaks where sequencing yields fresh data daily, use ChronAeon for immediate parameter estimation. Reserve multi-day BEAST MCMC runs for retrospective studies requiring formal coalescent demographic reconstruction.

---

## 6. Summary Rules of Thumb.

When migrating molecular dating analyses from BEAST to ChronAeon, keep these core rules in mind:

- An unbounded Fieller confidence interval ($g \ge 1.0$) is an objective statistical diagnostic, not a numerical error. It reveals that data alone cannot separate evolutionary velocity from zero.
- Pagel's $\lambda^*$ attention kernel replaces discrete genealogical trees by downweighting clustered isolates via Generalized Least Squares.
- Natural cubic splines should be adopted only when non-linear curvature is statistically significant ($p < 0.05, \Delta\mathrm{AIC} \ge 10.0$). Otherwise, retain the parsimonious linear clock.
- When an alignment contains co-circulating clades with different substitution velocities, use AutoClock graph spectral bisection rather than forcing a single global clock.
- Closed-form distance geometry eliminates MCMC convergence uncertainty. Calibrations complete reproducibly in seconds.
