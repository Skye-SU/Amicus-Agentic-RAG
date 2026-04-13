Linear Regression - statsmodels 0.14.6








:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}



\_\_md\_scope=new URL(".",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}





[Skip to content](#examples)

[![logo](_static/statsmodels-logo-v2-bw.svg)](index.html "statsmodels 0.14.6")




statsmodels 0.14.6

Linear Regression



Initializing search

[statsmodels](https://github.com/statsmodels/statsmodels/ "Go to repository")

[![logo](_static/statsmodels-logo-v2-bw.svg)](index.html "statsmodels 0.14.6")
statsmodels 0.14.6

[statsmodels](https://github.com/statsmodels/statsmodels/ "Go to repository")

* [Installing statsmodels](install.html)
* [Getting started](gettingstarted.html)
* [User Guide](user-guide.html)

  User Guide
  + [Background](user-guide.html#background)
  + [Regression and Linear Models](user-guide.html#regression-and-linear-models)

    Regression and Linear Models
    - [Linear Regression](#)

      Linear Regression
      * [Module Reference](#module-statsmodels.regression.linear_model)

        Module Reference
        + [Model Classes](#model-classes)

          Model Classes
          - [statsmodels.regression.linear\_model.OLS](generated/statsmodels.regression.linear_model.OLS.html)
          - [statsmodels.regression.linear\_model.GLS](generated/statsmodels.regression.linear_model.GLS.html)
          - [statsmodels.regression.linear\_model.WLS](generated/statsmodels.regression.linear_model.WLS.html)
          - [statsmodels.regression.linear\_model.GLSAR](generated/statsmodels.regression.linear_model.GLSAR.html)
          - [statsmodels.regression.linear\_model.yule\_walker](generated/statsmodels.regression.linear_model.yule_walker.html)
          - [statsmodels.regression.linear\_model.burg](generated/statsmodels.regression.linear_model.burg.html)
          - [statsmodels.regression.quantile\_regression.QuantReg](generated/statsmodels.regression.quantile_regression.QuantReg.html)
          - [statsmodels.regression.recursive\_ls.RecursiveLS](generated/statsmodels.regression.recursive_ls.RecursiveLS.html)
          - [statsmodels.regression.rolling.RollingWLS](generated/statsmodels.regression.rolling.RollingWLS.html)
          - [statsmodels.regression.rolling.RollingOLS](generated/statsmodels.regression.rolling.RollingOLS.html)
          - [statsmodels.regression.process\_regression.GaussianCovariance](generated/statsmodels.regression.process_regression.GaussianCovariance.html)
          - [statsmodels.regression.process\_regression.ProcessMLE](generated/statsmodels.regression.process_regression.ProcessMLE.html)
          - [statsmodels.regression.dimred.SlicedInverseReg](generated/statsmodels.regression.dimred.SlicedInverseReg.html)
          - [statsmodels.regression.dimred.PrincipalHessianDirections](generated/statsmodels.regression.dimred.PrincipalHessianDirections.html)
          - [statsmodels.regression.dimred.SlicedAverageVarianceEstimation](generated/statsmodels.regression.dimred.SlicedAverageVarianceEstimation.html)
        + [Results Classes](#results-classes)

          Results Classes
          - [statsmodels.regression.linear\_model.RegressionResults](generated/statsmodels.regression.linear_model.RegressionResults.html)
          - [statsmodels.regression.linear\_model.OLSResults](generated/statsmodels.regression.linear_model.OLSResults.html)
          - [statsmodels.regression.linear\_model.PredictionResults](generated/statsmodels.regression.linear_model.PredictionResults.html)
          - [statsmodels.base.elastic\_net.RegularizedResults](generated/statsmodels.base.elastic_net.RegularizedResults.html)
          - [statsmodels.regression.quantile\_regression.QuantRegResults](generated/statsmodels.regression.quantile_regression.QuantRegResults.html)
          - [statsmodels.regression.recursive\_ls.RecursiveLSResults](generated/statsmodels.regression.recursive_ls.RecursiveLSResults.html)
          - [statsmodels.regression.rolling.RollingRegressionResults](generated/statsmodels.regression.rolling.RollingRegressionResults.html)
          - [statsmodels.regression.process\_regression.ProcessMLEResults](generated/statsmodels.regression.process_regression.ProcessMLEResults.html)
          - [statsmodels.regression.dimred.DimReductionResults](generated/statsmodels.regression.dimred.DimReductionResults.html)
    - Linear Regression

      [Linear Regression](#)



      Contents
      * [Examples](#examples)
      * [Technical Documentation](#technical-documentation)

        + [References](#references)
        + [Attributes](#attributes)
      * [Module Reference](#module-statsmodels.regression.linear_model)

        + [Model Classes](#model-classes)

          - [statsmodels.regression.linear\_model.OLS](generated/statsmodels.regression.linear_model.OLS.html)
          - [statsmodels.regression.linear\_model.GLS](generated/statsmodels.regression.linear_model.GLS.html)
          - [statsmodels.regression.linear\_model.WLS](generated/statsmodels.regression.linear_model.WLS.html)
          - [statsmodels.regression.linear\_model.GLSAR](generated/statsmodels.regression.linear_model.GLSAR.html)
          - [statsmodels.regression.linear\_model.yule\_walker](generated/statsmodels.regression.linear_model.yule_walker.html)
          - [statsmodels.regression.linear\_model.burg](generated/statsmodels.regression.linear_model.burg.html)
          - [statsmodels.regression.quantile\_regression.QuantReg](generated/statsmodels.regression.quantile_regression.QuantReg.html)
          - [statsmodels.regression.recursive\_ls.RecursiveLS](generated/statsmodels.regression.recursive_ls.RecursiveLS.html)
          - [statsmodels.regression.rolling.RollingWLS](generated/statsmodels.regression.rolling.RollingWLS.html)
          - [statsmodels.regression.rolling.RollingOLS](generated/statsmodels.regression.rolling.RollingOLS.html)
          - [statsmodels.regression.process\_regression.GaussianCovariance](generated/statsmodels.regression.process_regression.GaussianCovariance.html)
          - [statsmodels.regression.process\_regression.ProcessMLE](generated/statsmodels.regression.process_regression.ProcessMLE.html)
          - [statsmodels.regression.dimred.SlicedInverseReg](generated/statsmodels.regression.dimred.SlicedInverseReg.html)
          - [statsmodels.regression.dimred.PrincipalHessianDirections](generated/statsmodels.regression.dimred.PrincipalHessianDirections.html)
          - [statsmodels.regression.dimred.SlicedAverageVarianceEstimation](generated/statsmodels.regression.dimred.SlicedAverageVarianceEstimation.html)
        + [Results Classes](#results-classes)

          - [statsmodels.regression.linear\_model.RegressionResults](generated/statsmodels.regression.linear_model.RegressionResults.html)
          - [statsmodels.regression.linear\_model.OLSResults](generated/statsmodels.regression.linear_model.OLSResults.html)
          - [statsmodels.regression.linear\_model.PredictionResults](generated/statsmodels.regression.linear_model.PredictionResults.html)
          - [statsmodels.base.elastic\_net.RegularizedResults](generated/statsmodels.base.elastic_net.RegularizedResults.html)
          - [statsmodels.regression.quantile\_regression.QuantRegResults](generated/statsmodels.regression.quantile_regression.QuantRegResults.html)
          - [statsmodels.regression.recursive\_ls.RecursiveLSResults](generated/statsmodels.regression.recursive_ls.RecursiveLSResults.html)
          - [statsmodels.regression.rolling.RollingRegressionResults](generated/statsmodels.regression.rolling.RollingRegressionResults.html)
          - [statsmodels.regression.process\_regression.ProcessMLEResults](generated/statsmodels.regression.process_regression.ProcessMLEResults.html)
          - [statsmodels.regression.dimred.DimReductionResults](generated/statsmodels.regression.dimred.DimReductionResults.html)
    - [Generalized Linear Models](glm.html)
    - [Generalized Estimating Equations](gee.html)
    - [Generalized Additive Models (GAM)](gam.html)
    - [Robust Linear Models](rlm.html)
    - [Linear Mixed Effects Models](mixed_linear.html)
    - [Regression with Discrete Dependent Variable](discretemod.html)
    - [Generalized Linear Mixed Effects Models](mixed_glm.html)
    - [ANOVA](anova.html)
    - [Other Models othermod](other_models.html)
  + [Time Series Analysis](user-guide.html#time-series-analysis)
  + [Other Models](user-guide.html#other-models)
  + [Statistics and Tools](user-guide.html#statistics-and-tools)
  + [Data Sets](user-guide.html#data-sets)
  + [Sandbox](user-guide.html#sandbox)
* [Examples](examples/index.html)
* [API Reference](api.html)
* [About statsmodels](about.html)
* [Developer Page](dev/index.html)
* [Release Notes](release/index.html)

Contents

* [Examples](#examples)
* [Technical Documentation](#technical-documentation)

  + [References](#references)
  + [Attributes](#attributes)
* [Module Reference](#module-statsmodels.regression.linear_model)

  + [Model Classes](#model-classes)
  + [Results Classes](#results-classes)

# Linear Regression[¶](#linear-regression "Link to this heading")

Linear models with independently and identically distributed errors, and for
errors with heteroscedasticity or autocorrelation. This module allows
estimation by ordinary least squares (OLS), weighted least squares (WLS),
generalized least squares (GLS), and feasible generalized least squares with
autocorrelated AR(p) errors.

See [Module Reference](#module-reference) for commands and arguments.

## Examples[¶](#examples "Link to this heading")

```
# Load modules and data
In [1]: import numpy as np

In [2]: import statsmodels.api as sm

In [3]: spector_data = sm.datasets.spector.load()

In [4]: spector_data.exog = sm.add_constant(spector_data.exog, prepend=False)

# Fit and summarize OLS model
In [5]: mod = sm.OLS(spector_data.endog, spector_data.exog)

In [6]: res = mod.fit()

In [7]: print(res.summary())
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  GRADE   R-squared:                       0.416
Model:                            OLS   Adj. R-squared:                  0.353
Method:                 Least Squares   F-statistic:                     6.646
Date:                Fri, 05 Dec 2025   Prob (F-statistic):            0.00157
Time:                        18:37:29   Log-Likelihood:                -12.978
No. Observations:                  32   AIC:                             33.96
Df Residuals:                      28   BIC:                             39.82
Df Model:                           3                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
GPA            0.4639      0.162      2.864      0.008       0.132       0.796
TUCE           0.0105      0.019      0.539      0.594      -0.029       0.050
PSI            0.3786      0.139      2.720      0.011       0.093       0.664
const         -1.4980      0.524     -2.859      0.008      -2.571      -0.425
==============================================================================
Omnibus:                        0.176   Durbin-Watson:                   2.346
Prob(Omnibus):                  0.916   Jarque-Bera (JB):                0.167
Skew:                           0.141   Prob(JB):                        0.920
Kurtosis:                       2.786   Cond. No.                         176.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

Detailed examples can be found here:

* [OLS](examples/notebooks/generated/ols.html)
* [WLS](examples/notebooks/generated/wls.html)
* [GLS](examples/notebooks/generated/gls.html)
* [Recursive LS](examples/notebooks/generated/recursive_ls.html)
* [Rolling LS](examples/notebooks/generated/rolling_ls.html)

## Technical Documentation[¶](#technical-documentation "Link to this heading")

The statistical model is assumed to be

> \(Y = X\beta + \epsilon\), where \(\epsilon\sim N\left(0,\Sigma\right).\)

Depending on the properties of \(\Sigma\), we have currently four classes available:

* GLS : generalized least squares for arbitrary covariance \(\Sigma\)
* OLS : ordinary least squares for i.i.d. errors \(\Sigma=\textbf{I}\)
* WLS : weighted least squares for heteroskedastic errors \(\text{diag}\left (\Sigma\right)\)
* GLSAR : feasible generalized least squares with autocorrelated AR(p) errors
  \(\Sigma=\Sigma\left(\rho\right)\)

All regression models define the same methods and follow the same structure,
and can be used in a similar fashion. Some of them contain additional model
specific methods and attributes.

GLS is the superclass of the other regression classes except for RecursiveLS,
RollingWLS and RollingOLS.

### References[¶](#references "Link to this heading")

General reference for regression models:

* D.C. Montgomery and E.A. Peck. “Introduction to Linear Regression Analysis.” 2nd. Ed., Wiley, 1992.

Econometrics references for regression models:

* R.Davidson and J.G. MacKinnon. “Econometric Theory and Methods,” Oxford, 2004.
* W.Green. “Econometric Analysis,” 5th ed., Pearson, 2003.

### Attributes[¶](#attributes "Link to this heading")

The following is more verbose description of the attributes which is mostly
common to all regression classes

pinv\_wexogarray
:   The p x n Moore-Penrose pseudoinverse of the whitened design matrix.
    It is approximately equal to
    \(\left(X^{T}\Sigma^{-1}X\right)^{-1}X^{T}\Psi\), where
    \(\Psi\) is defined such that \(\Psi\Psi^{T}=\Sigma^{-1}\).

cholsimgainvarray
:   The n x n upper triangular matrix \(\Psi^{T}\) that satisfies
    \(\Psi\Psi^{T}=\Sigma^{-1}\).

df\_modelfloat
:   The model degrees of freedom. This is equal to p - 1, where p is the
    number of regressors. Note that the intercept is not counted as using a
    degree of freedom here.

df\_residfloat
:   The residual degrees of freedom. This is equal n - p where n is the
    number of observations and p is the number of parameters. Note that the
    intercept is counted as using a degree of freedom here.

llffloat
:   The value of the likelihood function of the fitted model.

nobsfloat
:   The number of observations n

normalized\_cov\_paramsarray
:   A p x p array equal to \((X^{T}\Sigma^{-1}X)^{-1}\).

sigmaarray
:   The n x n covariance matrix of the error terms:
    \(\epsilon\sim N\left(0,\Sigma\right)\).

wexogarray
:   The whitened design matrix \(\Psi^{T}X\).

wendogarray
:   The whitened response variable \(\Psi^{T}Y\).

## Module Reference[¶](#module-statsmodels.regression.linear_model "Link to this heading")

### Model Classes[¶](#model-classes "Link to this heading")

|  |  |
| --- | --- |
| [`OLS`](generated/statsmodels.regression.linear_model.OLS.html#statsmodels.regression.linear_model.OLS "statsmodels.regression.linear_model.OLS (Python class) — Ordinary Least Squares")(endog[, exog, missing, hasconst]) | Ordinary Least Squares |
| [`GLS`](generated/statsmodels.regression.linear_model.GLS.html#statsmodels.regression.linear_model.GLS "statsmodels.regression.linear_model.GLS (Python class) — Generalized Least Squares")(endog, exog[, sigma, missing, hasconst]) | Generalized Least Squares |
| [`WLS`](generated/statsmodels.regression.linear_model.WLS.html#statsmodels.regression.linear_model.WLS "statsmodels.regression.linear_model.WLS (Python class) — Weighted Least Squares")(endog, exog[, weights, missing, hasconst]) | Weighted Least Squares |
| [`GLSAR`](generated/statsmodels.regression.linear_model.GLSAR.html#statsmodels.regression.linear_model.GLSAR "statsmodels.regression.linear_model.GLSAR (Python class) — Generalized Least Squares with AR covariance structure")(endog[, exog, rho, missing, hasconst]) | Generalized Least Squares with AR covariance structure |
| [`yule_walker`](generated/statsmodels.regression.linear_model.yule_walker.html#statsmodels.regression.linear_model.yule_walker "statsmodels.regression.linear_model.yule_walker (Python function) — Estimate AR(p) parameters from a sequence using the Yule-Walker equations.")(x[, order, method, df, inv, demean]) | Estimate AR(p) parameters from a sequence using the Yule-Walker equations. |
| [`burg`](generated/statsmodels.regression.linear_model.burg.html#statsmodels.regression.linear_model.burg "statsmodels.regression.linear_model.burg (Python function) — Compute Burg's AP(p) parameter estimator.")(endog[, order, demean]) | Compute Burg's AP(p) parameter estimator. |

|  |  |
| --- | --- |
| [`QuantReg`](generated/statsmodels.regression.quantile_regression.QuantReg.html#statsmodels.regression.quantile_regression.QuantReg "statsmodels.regression.quantile_regression.QuantReg (Python class) — Quantile Regression")(endog, exog, \*\*kwargs) | Quantile Regression |

|  |  |
| --- | --- |
| [`RecursiveLS`](generated/statsmodels.regression.recursive_ls.RecursiveLS.html#statsmodels.regression.recursive_ls.RecursiveLS "statsmodels.regression.recursive_ls.RecursiveLS (Python class) — Recursive least squares")(endog, exog[, constraints]) | Recursive least squares |

|  |  |
| --- | --- |
| [`RollingWLS`](generated/statsmodels.regression.rolling.RollingWLS.html#statsmodels.regression.rolling.RollingWLS "statsmodels.regression.rolling.RollingWLS (Python class) — Rolling Weighted Least Squares")(endog, exog[, window, weights, ...]) | Rolling Weighted Least Squares |
| [`RollingOLS`](generated/statsmodels.regression.rolling.RollingOLS.html#statsmodels.regression.rolling.RollingOLS "statsmodels.regression.rolling.RollingOLS (Python class) — Rolling Ordinary Least Squares")(endog, exog[, window, min\_nobs, ...]) | Rolling Ordinary Least Squares |

|  |  |
| --- | --- |
| [`GaussianCovariance`](generated/statsmodels.regression.process_regression.GaussianCovariance.html#statsmodels.regression.process_regression.GaussianCovariance "statsmodels.regression.process_regression.GaussianCovariance (Python class) — An implementation of ProcessCovariance using the Gaussian kernel.")() | An implementation of ProcessCovariance using the Gaussian kernel. |
| [`ProcessMLE`](generated/statsmodels.regression.process_regression.ProcessMLE.html#statsmodels.regression.process_regression.ProcessMLE "statsmodels.regression.process_regression.ProcessMLE (Python class) — Fit a Gaussian mean/variance regression model.")(endog, exog, exog\_scale, ...[, cov]) | Fit a Gaussian mean/variance regression model. |

|  |  |
| --- | --- |
| [`SlicedInverseReg`](generated/statsmodels.regression.dimred.SlicedInverseReg.html#statsmodels.regression.dimred.SlicedInverseReg "statsmodels.regression.dimred.SlicedInverseReg (Python class) — Sliced Inverse Regression (SIR)")(endog, exog, \*\*kwargs) | Sliced Inverse Regression (SIR) |
| [`PrincipalHessianDirections`](generated/statsmodels.regression.dimred.PrincipalHessianDirections.html#statsmodels.regression.dimred.PrincipalHessianDirections "statsmodels.regression.dimred.PrincipalHessianDirections (Python class) — Principal Hessian Directions (PHD)")(endog, exog, \*\*kwargs) | Principal Hessian Directions (PHD) |
| [`SlicedAverageVarianceEstimation`](generated/statsmodels.regression.dimred.SlicedAverageVarianceEstimation.html#statsmodels.regression.dimred.SlicedAverageVarianceEstimation "statsmodels.regression.dimred.SlicedAverageVarianceEstimation (Python class) — Sliced Average Variance Estimation (SAVE)")(endog, exog, ...) | Sliced Average Variance Estimation (SAVE) |

### Results Classes[¶](#results-classes "Link to this heading")

Fitting a linear regression model returns a results class. OLS has a
specific results class with some additional methods compared to the
results class of the other linear models.

|  |  |
| --- | --- |
| [`RegressionResults`](generated/statsmodels.regression.linear_model.RegressionResults.html#statsmodels.regression.linear_model.RegressionResults "statsmodels.regression.linear_model.RegressionResults (Python class) — This class summarizes the fit of a linear regression model.")(model, params[, ...]) | This class summarizes the fit of a linear regression model. |
| [`OLSResults`](generated/statsmodels.regression.linear_model.OLSResults.html#statsmodels.regression.linear_model.OLSResults "statsmodels.regression.linear_model.OLSResults (Python class) — Results class for for an OLS model.")(model, params[, ...]) | Results class for for an OLS model. |
| [`PredictionResults`](generated/statsmodels.regression.linear_model.PredictionResults.html#statsmodels.regression.linear_model.PredictionResults "statsmodels.regression.linear_model.PredictionResults (Python class) — Results class for predictions.")(predicted\_mean, ...[, df, ...]) | Results class for predictions. |

|  |  |
| --- | --- |
| [`RegularizedResults`](generated/statsmodels.base.elastic_net.RegularizedResults.html#statsmodels.base.elastic_net.RegularizedResults "statsmodels.base.elastic_net.RegularizedResults (Python class) — Results for models estimated using regularization")(model, params) | Results for models estimated using regularization |

|  |  |
| --- | --- |
| [`QuantRegResults`](generated/statsmodels.regression.quantile_regression.QuantRegResults.html#statsmodels.regression.quantile_regression.QuantRegResults "statsmodels.regression.quantile_regression.QuantRegResults (Python class) — Results instance for the QuantReg model")(model, params[, ...]) | Results instance for the QuantReg model |

|  |  |
| --- | --- |
| [`RecursiveLSResults`](generated/statsmodels.regression.recursive_ls.RecursiveLSResults.html#statsmodels.regression.recursive_ls.RecursiveLSResults "statsmodels.regression.recursive_ls.RecursiveLSResults (Python class) — Class to hold results from fitting a recursive least squares model.")(model, params, filter\_results) | Class to hold results from fitting a recursive least squares model. |

|  |  |
| --- | --- |
| [`RollingRegressionResults`](generated/statsmodels.regression.rolling.RollingRegressionResults.html#statsmodels.regression.rolling.RollingRegressionResults "statsmodels.regression.rolling.RollingRegressionResults (Python class) — Results from rolling regressions")(model, store, ...) | Results from rolling regressions |

|  |  |
| --- | --- |
| [`ProcessMLEResults`](generated/statsmodels.regression.process_regression.ProcessMLEResults.html#statsmodels.regression.process_regression.ProcessMLEResults "statsmodels.regression.process_regression.ProcessMLEResults (Python class) — Results class for Gaussian process regression models.")(model, mlefit) | Results class for Gaussian process regression models. |

|  |  |
| --- | --- |
| [`DimReductionResults`](generated/statsmodels.regression.dimred.DimReductionResults.html#statsmodels.regression.dimred.DimReductionResults "statsmodels.regression.dimred.DimReductionResults (Python class) — Results class for a dimension reduction regression.")(model, params, eigs) | Results class for a dimension reduction regression. |

Dec 05, 2025



© Copyright 2009-2023, Josef Perktold, Skipper Seabold, Jonathan Taylor, statsmodels-developers.

Created using
[Sphinx](https://www.sphinx-doc.org/)
7.3.7.
and
[Sphinx-Immaterial](https://github.com/jbms/sphinx-immaterial/)

{"base": ".", "features": [], "translations": {"clipboard.copied": "Copied to clipboard", "clipboard.copy": "Copy to clipboard", "search.result.more.one": "1 more on this page", "search.result.more.other": "# more on this page", "search.result.none": "No matching documents", "search.result.one": "1 matching document", "search.result.other": "# matching documents", "search.result.placeholder": "Type to start searching", "search.result.term.missing": "Missing", "select.version": "Select version"}, "version": {"provider": "mike", "staticVersions": null, "versionPath": "../versions-v3.json"}}


window.MathJax = {"tex": {"inlineMath": [["$", "$"], ["\\(", "\\)"]], "processEscapes": true}, "options": {"ignoreHtmlClass": "tex2jax\_ignore|mathjax\_ignore|document", "processHtmlClass": "tex2jax\_process|mathjax\_process|math|output\_area"}}