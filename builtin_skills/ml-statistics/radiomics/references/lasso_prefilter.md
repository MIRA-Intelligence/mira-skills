---
name: LASSO-PreFilter
description: LASSO-based feature pre-filtering methodology for radiomics
---

# LASSO Feature Pre-Filter

## Purpose

PyRadiomics extracts 500-2000 features per ROI, but typical radiomics studies have 50-500 samples. This extreme high-dimensionality causes:
1. Severe overfitting in any downstream model
2. Intractable grid search (feature selectors operate on too many features)
3. Uninterpretable results with hundreds of near-noise features

LASSO (L1-regularized logistic regression) provides a statistically principled first pass to reduce the feature space before the combinatorial grid search.

## Method

### Algorithm
Use `LogisticRegressionCV(penalty='l1', solver='saga', cv=5, scoring='roc_auc')` with a log-spaced alpha range:
```
alpha_range = [0.0001, 0.001, 0.01, 0.1, 1.0]
```

### Alpha Selection
1. Fit LASSO CV across all alpha values
2. For each alpha, count the number of non-zero coefficients
3. Plot AUC vs. number of features (each alpha gives one point)
4. Select the alpha that achieves near-maximum AUC with the fewest features (parsimony principle)
5. If too many features remain (> `retain_fraction` × total), use a higher alpha

### Feature Selection
A feature is retained if `|coefficient| > 1e-6` at the selected alpha. Typically this reduces:
- 1000+ raw features → 50-100 features (with retain_fraction=0.3)
- The retained features have the strongest univariate relationship with the outcome

### Output
- `features_lasso_filtered.csv`: Only retained features
- `lasso_report.json`:
  ```json
  {
    "alpha_used": 0.01,
    "n_features_original": 1247,
    "n_features_selected": 68,
    "selected_feature_names": ["glcm_Mean", ...],
    "coefficients": {"glcm_Mean": 0.342, ...},
    "cv_auc_curve": [{"alpha": 0.0001, "n_features": 450, "auc": 0.82}, ...]
  }
  ```

## Why Before Grid Search, Not Within It?

FAE includes LRLasso as a classifier but not as a pre-filter. The key differences:

| LRLasso Classifier | LASSO Pre-Filter |
|---|---|
| Applies L1 penalty during classification | Filters features before any model sees them |
| Only one method in grid | Orthogonal to all downstream selectors (ANOVA, mRMR, etc.) |
| Penalized coefficients not zero-feature | Truly removes features from matrix |
| Doesn't reduce grid search space | Dramatically reduces dimensionality for all 9000 combos |

## Integration in Pipeline

```
PyRadiomics extraction (features.csv, ~1000 features)
    → LASSO pre-filter (features_lasso_filtered.csv, ~50-100 features)
    → Coarse grid search over Balance×Norm×DimRed×Selector×Count×Classifier
    → Fine-tuning top-N with expanded hyperparams
```

## Parameters

Configurable in `radiomics_plan.yaml`:
```yaml
lasso_prefilter:
  alpha_range: [0.0001, 0.001, 0.01, 0.1, 1.0]
  retain_fraction: 0.3    # Keep at most 30% of original features
  cv_folds: 5
```
