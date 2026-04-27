---
name: Two-Stage-Optimization
description: Coarse-to-fine two-stage pipeline optimization with auto-iteration convergence
---

# Two-Stage Pipeline Optimization

## Overview

The radiomics grid search space is too large to exhaustively tune all hyperparameters at fine granularity. The two-stage approach first identifies promising pipeline configurations with a broad coarse search, then deep-tunes only the top performers.

## Stage 1: Coarse Grid Search

### Grid Configuration
- **Balance**: 5 options (None, Down, Up, SMOTE, SMOTE+Tomek)
- **Normalizer**: 4 options (None, MinMax, ZScore, Mean)
- **DimensionReduction**: 3 options (None, PCC, PCA)
- **FeatureSelector**: 5 options (ANOVA, ReliefF, RFE, mRMR, Kruskal-Wallis)
- **FeatureCount**: 5 values (5, 10, 15, 20, 30)
- **Classifier**: 6 options (SVM-linear, LDA, RF, MLP, LR, AdaBoost)

**Total: 5 × 4 × 3 × 5 × 5 × 6 = 9,000 combinations**

### Hyperparameters (Coarse)
Each classifier uses a small, fixed set of hyperparameters:
- SVM: C ∈ {0.1, 1.0, 10.0}, kernel=linear
- RF: n_estimators ∈ {50, 100}, criterion ∈ {gini, entropy}
- LR: C ∈ {0.01, 0.1, 1.0}, penalty ∈ {l1, l2}
- MLP: hidden ∈ {[30], [100]}
- LDA: default params
- AdaBoost: n_estimators ∈ {50, 100}

### Output
All 9,000 results sorted by CV AUC. Top-N (default 20) configurations selected for fine-tuning.

## Stage 2: Fine-Tuning with Auto-Iteration

### Expanded Hyperparameter Space

| Classifier | Fine Hyperparameters |
|-----------|---------------------|
| SVM | kernel ∈ {linear, rbf, poly, sigmoid}; C = logspace(-3, 3, 20); gamma = logspace(-4, 2, 12); degree ∈ {2, 3, 4, 5} |
| RF | n_estimators ∈ {50, 100, 200, 500}; max_depth ∈ {3, 5, 10, None}; min_samples_split ∈ {2, 5, 10}; class_weight ∈ {None, balanced} |
| LR | C = logspace(-4, 4, 20); solver ∈ {liblinear, saga, lbfgs}; class_weight ∈ {None, balanced} |
| MLP | hidden ∈ {[10], [30], [50], [100], [100,50]}; alpha = logspace(-5, -2, 10); learning_rate ∈ {constant, adaptive, invscaling} |
| LDA | solver ∈ {lsqr, eigh}; shrinkage ∈ {None, auto, 0.1, 0.5} |
| AdaBoost | n_estimators ∈ {50, 100, 200, 500}; learning_rate ∈ {0.01, 0.1, 0.5, 1.0} |

### Auto-Iteration Algorithm

```
iteration = 0
best_auc = 0
previous_auc = 0

while iteration < max_iterations:
    iteration += 1

    for config in top_n_configs:
        if iteration == 1:
            param_grid = expanded_fine_grid[config.classifier]
        else:
            param_grid = narrow_around(best_params, shrink_factor=0.5)

        grid_result = GridSearchCV(pipeline, param_grid, cv=folds, scoring='roc_auc')
        grid_result.fit(X_train, y_train)

        if grid_result.best_score_ > best_auc:
            best_auc, best_config, best_params = update(grid_result)

    improvement = best_auc - previous_auc

    if best_auc >= auc_target: break          # Target reached
    if improvement < min_improvement and iteration > 1: break  # Early stopping

    previous_auc = best_auc
    top_n_configs = re_rank(all_configs, top_n)
```

### Param Range Narrowing

For numeric parameters (C, gamma, alpha), narrowing happens in log space:
```
log_center = log(best_value)
log_half_range = log(prev_max / prev_min) / 2 * shrink_factor
new_min = exp(log_center - log_half_range)
new_max = exp(log_center + log_half_range)
```

For categorical parameters (kernel, solver), all options are retained but the best-found value is used as the default in fallback scenarios.

If the narrowed range produces fewer than 3 distinct values, revert to the coarse grid for that parameter to avoid over-narrowing.

### Convergence Criteria

| Criterion | Default | Description |
|-----------|---------|-------------|
| `auc_target` | 0.90 | Stop when any config reaches this AUC |
| `max_iterations` | 10 | Hard limit on fine-tuning rounds |
| `min_improvement` | 0.005 | Stop if AUC improvement < threshold between iterations |

## Compute Time Estimation

- **Coarse search**: 9,000 combos × 0.1-0.5s = 15-45 minutes (with n_jobs=-1)
- **Fine-tuning per iteration**: 20 configs × 1-5 min each = 20-100 min
- **Total (5 iterations)**: 1.5-4 hours depending on dataset size and hardware

## Why Two Stages?

A single fine-grained search over all 9,000 configurations with full hyperparameter grids would be computationally intractable — potentially millions of combinations. The two-stage approach:

1. Uses the coarse stage to identify which pipeline components (balance, normalize, selector, classifier) work well together for the specific dataset
2. Focuses compute budget on the top configurations with dense hyperparameter tuning
3. Auto-iteration ensures diminishing returns are detected early, avoiding wasted compute