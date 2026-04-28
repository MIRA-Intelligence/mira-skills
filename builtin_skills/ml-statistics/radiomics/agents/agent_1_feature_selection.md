# Agent 3: Feature Selection Agent (特征筛选Agent)

**Goal:** Filter the noise. Radiomics generates hundreds of features; highly collinear ones must be eliminated.

## Guidelines
1. **Robustness (ICC)**: If test-retest scans are available, drop features with ICC < 0.75.
2. **Standardization**: Implement `sklearn.preprocessing.StandardScaler`.
3. **Collinearity Filter**: Drop features using Pearson/Spearman correlation (e.g., if correlation > 0.85, drop one).
4. **Advanced Selection**: Use algorithms like LASSO regression (L1 regularization), mRMR, or Recursive Feature Elimination. Keep only an essential subset (e.g., 5-15 features).

## Selection Pipeline

```
features.csv (~1000 features)
  → ICC filter (optional, if test-retest available)
  → LASSO pre-filter (~50-100 features)     [see references/lasso_prefilter.md]
  → PCC correlation filter
  → Statistical selector (ANOVA/mRMR/RFE/KW)
  → StandardScaler
  → features_selected.csv
```

### Step 1: LASSO Pre-Filter

Reduces ~1000 PyRadiomics features to ~50-100 before combinatorial grid search. See `references/lasso_prefilter.md` for methodology.

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import StandardScaler

def lasso_prefilter(X, y, alpha_range=None, retain_fraction=0.3, cv_folds=5):
    if alpha_range is None:
        alpha_range = [0.0001, 0.001, 0.01, 0.1, 1.0]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    best_auc = 0
    best_alpha = None
    best_coef = None
    auc_curve = []

    for alpha in alpha_range:
        lr = LogisticRegressionCV(
            Cs=[1.0 / (len(X) * alpha)],
            penalty='l1',
            solver='saga',
            cv=cv_folds,
            scoring='roc_auc',
            max_iter=5000
        )
        lr.fit(X_scaled, y)
        auc = lr.score(X_scaled, y)  # training AUC for screening
        nonzero = np.abs(lr.coef_[0]) > 1e-6
        n_feat = nonzero.sum()
        auc_curve.append({
            'alpha': alpha,
            'n_features': int(n_feat),
            'train_auc': round(auc, 4)
        })

        target = int(X.shape[1] * retain_fraction)
        if n_feat <= target and auc >= best_auc:
            best_auc = auc
            best_alpha = alpha
            best_coef = lr.coef_[0]

    selected_mask = np.abs(best_coef) > 1e-6
    selected_names = X.columns[selected_mask].tolist()

    return X[selected_mask], selected_names, auc_curve
```

### Step 2: PCC Correlation Filter

Remove highly correlated feature pairs (see FAE methodology in `references/faq.md`):

```python
import pandas as pd
import numpy as np

def pcc_filter(df, threshold=0.99):
    """Remove one of each pair with |r| > threshold. Drops feature with lower variance."""
    corr_matrix = df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]

    for col in to_drop:
        correlated = upper[col][upper[col] > threshold].index.tolist()
        candidates = [col] + correlated
        # Keep the feature with highest variance
        keep = max(candidates, key=lambda c: df[c].var())
        to_drop_local = [c for c in candidates if c != keep]
        df = df.drop(columns=to_drop_local)

    return df
```

### Step 3: Statistical Feature Selectors

Choose one based on dataset characteristics:

```python
from sklearn.feature_selection import SelectKBest, RFE, f_classif, mutual_info_classif
from sklearn.svm import SVC
from scipy.stats import kruskal

# ANOVA (parametric F-test)
selector_anova = SelectKBest(score_func=f_classif, k=10)

# mRMR proxy (mutual information)
selector_mrmr = SelectKBest(score_func=mutual_info_classif, k=10)

# RFE with linear SVM
svc = SVC(kernel='linear', C=1.0, class_weight='balanced')
selector_rfe = RFE(estimator=svc, n_features_to_select=10)

# Kruskal-Wallis (non-parametric)
def kw_selector(X, y, k=10):
    scores = []
    for col in X.columns:
        groups = [X.loc[y == cls, col].values for cls in np.unique(y)]
        _, p = kruskal(*groups)
        scores.append(p)
    # Lowest p-values → highest relevance
    indices = np.argsort(scores)[:k]
    return X.iloc[:, indices]
```

### Step 4: StandardScaler (always apply after selection)

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_final = scaler.fit_transform(X_selected)  # Fit on training set only
# scaler.transform(X_test)  # Transform test set separately
```
