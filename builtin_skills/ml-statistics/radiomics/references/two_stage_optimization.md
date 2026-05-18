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

## Stage 2: Fine-Tuning with Elite Evolution

Instead of an exhaustive search across all combinations, Stage 2 uses a hierarchical selection process to ensure efficiency.

### 1. Feature Anchoring
Identify the Top-3 to Top-5 feature configurations from Stage 1. A configuration includes the Normalizer, Dimension Reduction (PCC 0.99), and the Feature Selector with its optimal $K$.

### 2. Enriched Model Shootout
Evaluate a broad palette of advanced classifiers on the anchored feature sets using wide-range search.

| Category | Models |
| :--- | :--- |
| **Boosting** | XGBoost, LightGBM, CatBoost |
| **Bagging** | Random Forest, ExtraTrees |
| **Kernels** | SVM (RBF, Poly) |
| **Linear+** | ElasticNet, Ridge |
| **Others** | MLP, LDA, Naive Bayes |

### 3. Deep Hyperparameter Tuning
Pick the best-performing model-feature combination and perform dense optimization using `HalvingGridSearchCV` or similar efficient methods.

## Compute Time Estimation

- **Coarse search**: 9,000 combos × 0.1-0.5s = 15-45 minutes (with n_jobs=-1)
- **Fine-tuning per iteration**: 20 configs × 1-5 min each = 20-100 min
- **Total (5 iterations)**: 1.5-4 hours depending on dataset size and hardware

## Why Two Stages?

A single fine-grained search over all 9,000 configurations with full hyperparameter grids would be computationally intractable — potentially millions of combinations. The two-stage approach:

1. Uses the coarse stage to identify which pipeline components (balance, normalize, selector, classifier) work well together for the specific dataset
2. Focuses compute budget on the top configurations with dense hyperparameter tuning
3. Auto-iteration ensures diminishing returns are detected early, avoiding wasted compute