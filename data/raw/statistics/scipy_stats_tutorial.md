Statistics (scipy.stats) — SciPy v1.17.0 Manual

document.documentElement.dataset.mode = localStorage.getItem("mode") || "";
document.documentElement.dataset.theme = localStorage.getItem("theme") || "";



.pst-js-only { display: none !important; }

























DOCUMENTATION\_OPTIONS.pagename = 'tutorial/stats';

DOCUMENTATION\_OPTIONS.theme\_version = '0.16.1';
DOCUMENTATION\_OPTIONS.theme\_switcher\_json\_url = 'https://scipy.github.io/devdocs/\_static/version\_switcher.json';
DOCUMENTATION\_OPTIONS.theme\_switcher\_version\_match = '1.17.0';
DOCUMENTATION\_OPTIONS.show\_version\_warning\_banner =
true;



[Skip to main content](#main-content)

Back to top




`Ctrl`+`K`

[![](../_static/logo.svg)
![](../_static/logo.svg)

SciPy](../index.html)

* [Installing](https://scipy.org/install/)
* [User Guide](index.html)
* [API reference](../reference/index.html)
* [Building from source](../building/index.html)
* [Development](../dev/index.html)
* [Release notes](../release.html)

Choose version

* [GitHub](https://github.com/scipy/scipy "GitHub")
* [Scientific Python Forum](https://discuss.scientific-python.org/c/contributor/scipy/ "Scientific Python Forum")

* [Installing](https://scipy.org/install/)
* [User Guide](index.html)
* [API reference](../reference/index.html)
* [Building from source](../building/index.html)
* [Development](../dev/index.html)
* [Release notes](../release.html)

Choose version

* [GitHub](https://github.com/scipy/scipy "GitHub")
* [Scientific Python Forum](https://discuss.scientific-python.org/c/contributor/scipy/ "Scientific Python Forum")

Search
`Ctrl`+`K`

Section Navigation

User guide

* [Fourier Transforms (`scipy.fft`)](fft.html)
* [Integration (`scipy.integrate`)](integrate.html)
* [Interpolation (`scipy.interpolate`)](interpolate.html)
* [File IO (`scipy.io`)](io.html)
* [Linear Algebra (`scipy.linalg`)](linalg.html)
* [Multidimensional Image Processing (`scipy.ndimage`)](ndimage.html)
* [Optimization (`scipy.optimize`)](optimize.html)
* [Signal Processing (`scipy.signal`)](signal.html)
* [Sparse Arrays (`scipy.sparse`)](sparse.html)
* [Spatial Data Structures and Algorithms (`scipy.spatial`)](spatial.html)
* [Special Functions (`scipy.special`)](special.html)
* [Statistics (`scipy.stats`)](#)
* [Sparse eigenvalue problems with ARPACK](arpack.html)
* [Compressed Sparse Graph Routines (`scipy.sparse.csgraph`)](csgraph.html)
* [Parallel execution support in SciPy](parallel_execution.html)
* [Thread Safety in SciPy](thread_safety.html)

* [SciPy User Guide](index.html)
* Statistics (`scipy.stats`)

# Statistics ([`scipy.stats`](../reference/stats.html#module-scipy.stats "scipy.stats"))[#](#statistics-scipy-stats "Link to this heading")

In this tutorial, we discuss many, but certainly not all, features of
`scipy.stats`. The intention here is to provide a user with a
working knowledge of this package. We refer to the
[reference manual](../reference/stats.html#statsrefmanual) for further details.

Note: This documentation is work in progress.

Contents

* [Probability distributions](stats/probability_distributions.html)
  + [Continuous Statistical Distributions](stats/continuous.html)
  + [Discrete Statistical Distributions](stats/discrete.html)
  + [Getting help](stats/probability_distributions.html#getting-help)
  + [Common methods](stats/probability_distributions.html#common-methods)
  + [Random number generation](stats/probability_distributions.html#random-number-generation)
  + [Shifting and scaling](stats/probability_distributions.html#shifting-and-scaling)
  + [Shape parameters](stats/probability_distributions.html#shape-parameters)
  + [Freezing a distribution](stats/probability_distributions.html#freezing-a-distribution)
  + [Broadcasting](stats/probability_distributions.html#broadcasting)
  + [Specific points for discrete distributions](stats/probability_distributions.html#specific-points-for-discrete-distributions)
  + [Fitting distributions](stats/probability_distributions.html#fitting-distributions)
  + [Performance issues and cautionary remarks](stats/probability_distributions.html#performance-issues-and-cautionary-remarks)
  + [Remaining issues](stats/probability_distributions.html#remaining-issues)
  + [Building specific distributions](stats/probability_distributions.html#building-specific-distributions)
* [Random Variable Transition Guide](stats/rv_infrastructure.html)
  + [Background](stats/rv_infrastructure.html#background)
  + [Basics](stats/rv_infrastructure.html#basics)
  + [New and Advanced Features](stats/rv_infrastructure.html#new-and-advanced-features)
  + [Conclusion](stats/rv_infrastructure.html#conclusion)
* [Universal Non-Uniform Random Number Sampling in SciPy](stats/sampling.html)
  + [Introduction](stats/sampling.html#introduction)
  + [Basic concepts of the Interface](stats/sampling.html#basic-concepts-of-the-interface)
  + [Generators in `scipy.stats.sampling`](stats/sampling.html#generators-in-scipy-stats-sampling)
  + [References](stats/sampling.html#references)
* [Kernel density estimation](stats/kernel_density_estimation.html)
  + [Univariate estimation](stats/kernel_density_estimation.html#univariate-estimation)
  + [Multivariate estimation](stats/kernel_density_estimation.html#multivariate-estimation)
* [Multiscale Graph Correlation (MGC)](stats/multiscale_graphcorr.html)
* [Quasi-Monte Carlo](stats/quasi_monte_carlo.html)
  + [Calculate the discrepancy](stats/quasi_monte_carlo.html#calculate-the-discrepancy)
  + [Using a QMC engine](stats/quasi_monte_carlo.html#using-a-qmc-engine)
  + [Making a QMC engine, i.e., subclassing `QMCEngine`](stats/quasi_monte_carlo.html#making-a-qmc-engine-i-e-subclassing-qmcengine)
  + [Guidelines on using QMC](stats/quasi_monte_carlo.html#guidelines-on-using-qmc)
* [Trimming and winsorization transition guide](stats/outliers.html)
  + [Motivation](stats/outliers.html#motivation)
  + [Identifying the threshold](stats/outliers.html#identifying-the-threshold)
  + [Trimming and winsorizing](stats/outliers.html#trimming-and-winsorizing)
  + [Computing the statistic](stats/outliers.html#computing-the-statistic)
  + [Recipes](stats/outliers.html#recipes)

Sample statistics and hypothesis tests

* [Analysing one sample](stats/analysing_one_sample.html)
  + [Descriptive statistics](stats/analysing_one_sample.html#descriptive-statistics)
  + [T-test and KS-test](stats/analysing_one_sample.html#t-test-and-ks-test)
  + [Tails of the distribution](stats/analysing_one_sample.html#tails-of-the-distribution)
  + [Special tests for normal distributions](stats/analysing_one_sample.html#special-tests-for-normal-distributions)
* [Comparing two samples](stats/comparing_two_samples.html)
  + [Comparing means](stats/comparing_two_samples.html#comparing-means)
  + [Kolmogorov-Smirnov test for two samples ks\_2samp](stats/comparing_two_samples.html#kolmogorov-smirnov-test-for-two-samples-ks-2samp)
* [Resampling and Monte Carlo Methods](stats/resampling.html)
  + [Introduction](stats/resampling.html#introduction)
  + [Resampling and Monte Carlo methods tutorials](stats/resampling.html#resampling-and-monte-carlo-methods-tutorials)
* [Hypothesis tests](stats/hypothesis_tests.html)
  + [Bartlettâs test for equal variances](stats/hypothesis_bartlett.html)
  + [Chi-square test](stats/hypothesis_chisquare.html)
  + [Chi-square test of independence of variables in a contingency table](stats/hypothesis_chi2_contingency.html)
  + [Dunnettâs test](stats/hypothesis_dunnett.html)
  + [Fisherâs exact test](stats/hypothesis_fisher_exact.html)
  + [Fligner-Killeen test for equality of variance](stats/hypothesis_fligner.html)
  + [Friedman test for repeated samples](stats/hypothesis_friedmanchisquare.html)
  + [Jarque-Bera goodness of fit test](stats/hypothesis_jarque_bera.html)
  + [Kendallâs tau test](stats/hypothesis_kendalltau.html)
  + [Kurtosis test](stats/hypothesis_kurtosistest.html)
  + [Levene test for equal variances](stats/hypothesis_levene.html)
  + [Normal test](stats/hypothesis_normaltest.html)
  + [Odds ratio for a contingency table](stats/hypothesis_odds_ratio.html)
  + [Pearsonâs Correlation](stats/hypothesis_pearsonr.html)
  + [Shapiro-Wilk test for normality](stats/hypothesis_shapiro.html)
  + [Skewness test](stats/hypothesis_skewtest.html)
  + [Spearman correlation coefficient](stats/hypothesis_spearmanr.html)

[previous

Special Functions (`scipy.special`)](special.html "previous page")
[next

Probability distributions](stats/probability_distributions.html "next page")





Â© Copyright 2008, The SciPy community.

Created using [Sphinx](https://www.sphinx-doc.org/) 8.1.3.

Built with the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html) 0.16.1.