# Specialized Clinical & Diagnostic Plots

This reference provides guidance for specialized plots common in clinical and diagnostic research (ROC, DCA, Nomograms).

## 1. ROC Curves (Receiver Operating Characteristic)
Used to evaluate the diagnostic ability of binary classifiers.
- **Python**: Use `sklearn.metrics.roc_curve` and `roc_auc_score`.
- **R**: Use the `pROC` package for publication-quality curves with confidence intervals.
- **Rule**: Always report the AUC (Area Under Curve) with 95% CI.

## 2. DCA Curves (Decision Curve Analysis)
Used to evaluate the clinical net benefit of a prediction model.
- **R (Recommended)**: Use the `dcaplot` or `ggdca` packages.
- **Python**: Can be implemented via `dcurves` library.
- **Rule**: Include the "All" (treat all) and "None" (treat none) strategies as reference lines.

## 3. Nomogram (列线图)
A graphical calculating device for predicting probabilities in survival or logistic models.
- **R (Standard)**: Use the `rms` package (`nomogram()` function).
- **Python**: Can be implemented via `pySurvival` or custom Matplotlib drawing (complex).
- **Rule**: Ensure the "Points" scale at the top and "Total Points" scale at the bottom are clearly aligned.

## 4. Calibration Curves (校准曲线)
Often paired with Nomograms to show predicted vs. observed probability.
- **R**: Use `rms::calibrate`.
- **Rule**: Use a diagonal 45-degree dashed line to represent the "Ideal" model.

## 5. Fitting Plots (拟合图)
- **Linear/Non-linear**: Use `seaborn.regplot` or R's `geom_smooth(method="lm" or "gam")`.
- **Confidence Band**: Always show the 95% confidence interval as a shaded area.

## 6. Pie Charts (饼图)
- **Status**: Generally DISCOURAGED in scientific papers.
- **Alternative**: Use **Stacked Bar Charts** or **Donut Charts** (if necessary) to allow easier comparison of proportions.

## 7. Multi-Group Comparisons (Violin & Box Plots)
- **Significance**: Use `statannot` (Python) or `ggpubr` (R) to add p-value brackets automatically.
- **Transparency**: Always overlay individual data points (jitter) on top of box/violin plots to show the true distribution.
