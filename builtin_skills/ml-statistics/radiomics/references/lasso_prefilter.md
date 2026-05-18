---
name: LASSO-PreFilter
description: LASSO-based feature pre-filtering methodology for radiomics
---

# LASSO Feature Selection

## Role in Pipeline

In this workflow, LASSO (L1-regularized logistic regression) is used as a **Parallel Feature Selector** within the Agent 2 Grid Search, alongside methods like ANOVA and RFE.

### Why LASSO?
LASSO provides a statistically principled way to achieve sparsity by forcing coefficients of redundant or irrelevant features to exactly zero. This makes it an ideal selector for radiomics, where the feature-to-sample ratio is often high.

## Implementation Standard

### Algorithm
Use `LogisticRegression(penalty='l1', solver='liblinear', random_state=42)` during the grid search.

### Feature Selection Logic
1. During the grid search, the model is fit on the training fold.
2. Features with non-zero coefficients (`|coefficient| > 1e-6`) are identified.
3. If the number of non-zero features is greater than the target $K$ for that pipeline:
   - Features are ranked by the absolute magnitude of their coefficients.
   - The Top-$K$ features are retained.
4. If the number is less than $K$, all non-zero features are used, and the pipeline is evaluated.

## Integration in Agent 2 Grid

```
...
  Feature Selection:
    - ANOVA
    - LASSO (As described here)
    - Chi-squared
    - MI
    - KW
    - ReliefF
    - RFE
...
```

### Advantage of Parallel Integration
By placing LASSO in the grid rather than as a pre-filter, we can directly compare its feature subsets with those chosen by ANOVA or mRMR using the same downstream classifier, ensuring a fair and comprehensive evaluation of the entire search space.
