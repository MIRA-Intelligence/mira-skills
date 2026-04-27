# Agent 4: Modeling & Testing Agent (建模测试Agent)

**Goal:** Build statistical or ML models (Rad-score) predicting the clinical outcome using the selected features.

## Guidelines
1. **Model Building**: Fit Logistic Regression, SVM, or Random Forest models. Handle class imbalances (SMOTE or class weights).
2. **Evaluation Metrics**: Generate AUC (Area Under Curve). Plot the ROC curve and the precision Calibration Curve.
3. **Rad-score Computation**: Calculate the Rad-score (linear combination of the LASSO coefficients and selected features). Evaluate distribution across groups using t-tests or Mann-Whitney.

## Two-Stage Grid Search

See `references/two_stage_optimization.md` for the full methodology.

### Stage 1: Coarse Grid Search

```python
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

coarse_params = {
    'classifier': [
        SVC(kernel='linear', probability=True),
        LogisticRegression(max_iter=5000),
        RandomForestClassifier(),
        MLPClassifier(max_iter=500),
        LinearDiscriminantAnalysis(),
        AdaBoostClassifier(),
    ],
    'classifier__C': np.logspace(-3, 3, 5),  # For SVM, LR, AdaBoost
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = []
for clf in coarse_params['classifier']:
    param_grid = {'classifier__C': np.logspace(-3, 3, 5)}
    if isinstance(clf, (RandomForestClassifier, LinearDiscriminantAnalysis)):
        param_grid = {}

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', clf),
    ])

    grid = GridSearchCV(pipeline, param_grid, cv=cv, scoring='roc_auc', n_jobs=-1)
    grid.fit(X_train, y_train)
    results.append({
        'classifier': type(clf).__name__,
        'best_auc': grid.best_score_,
        'best_params': grid.best_params_,
    })
```

### Stage 2: Fine-Tuning with Auto-Iteration

```python
def fine_tune(top_configs, X_train, y_train, X_val, y_val,
              auc_target=0.90, max_iterations=10, min_improvement=0.005):
    best_auc = 0
    previous_auc = 0

    for iteration in range(1, max_iterations + 1):
        for config in top_configs:
            param_grid = config.get('fine_grid', {})
            if iteration > 1 and best_params:
                param_grid = narrow_around(best_params, shrink_factor=0.5)

            grid = GridSearchCV(config['pipeline'], param_grid,
                                cv=cv, scoring='roc_auc', n_jobs=-1)
            grid.fit(X_train, y_train)

            val_auc = grid.best_estimator_.score(X_val, y_val)
            if val_auc > best_auc:
                best_auc = val_auc
                best_config = config
                best_params = grid.best_params_

        improvement = best_auc - previous_auc
        if best_auc >= auc_target:
            print(f"Target AUC {auc_target} reached at iteration {iteration}")
            break
        if improvement < min_improvement and iteration > 1:
            print(f"Converged at iteration {iteration}: improvement={improvement:.4f}")
            break
        previous_auc = best_auc

    return best_config, best_params, best_auc
```

### Rad-Score Computation

```python
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression

# Train final model on full training set
model = LogisticRegression(penalty='l1', solver='saga', max_iter=5000)
model.fit(X_train_scaled, y_train)

# Compute Rad-score as linear combination
rad_score_train = X_train_scaled @ model.coef_[0] + model.intercept_[0]
rad_score_test = X_test_scaled @ model.coef_[0] + model.intercept_[0]

# Compare distributions between groups
t_stat, t_p = stats.ttest_ind(
    rad_score_test[y_test == 1],
    rad_score_test[y_test == 0]
)
print(f"Rad-score group difference: t={t_stat:.3f}, p={t_p:.2e}")
```

### Evaluation & Visualization

```python
import matplotlib.pyplot as plt
from sklearn.metrics import (roc_curve, auc, calibration_curve,
                             precision_recall_curve, auc as calc_auc)
from sklearn.metrics import confusion_matrix, classification_report

def evaluate_and_plot(y_true, y_scores, model_name="Model"):
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = calc_auc(fpr, tpr)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # ROC Curve
    axes[0].plot(fpr, tpr, label=f'{model_name} (AUC={roc_auc:.3f})')
    axes[0].plot([0, 1], [0, 1], 'k--', alpha=0.5)
    axes[0].set_xlabel('False Positive Rate')
    axes[0].set_ylabel('True Positive Rate')
    axes[0].legend()

    # Calibration Curve
    prob_scores = _sigmoid(y_scores)
    frac_pos, mean_pred = calibration_curve(y_true, prob_scores, n_bins=10)
    axes[1].plot(mean_pred, frac_pos, 's-', label=model_name)
    axes[1].plot([0, 1], [0, 1], 'k--', alpha=0.5)
    axes[1].set_xlabel('Mean Predicted Probability')
    axes[1].set_ylabel('Fraction of Positives')
    axes[1].legend()

    # PR Curve
    prec, rec, _ = precision_recall_curve(y_true, prob_scores)
    pr_auc = calc_auc(rec, prec)
    axes[2].plot(rec, prec, label=f'{model_name} (PR-AUC={pr_auc:.3f})')
    axes[2].set_xlabel('Recall')
    axes[2].set_ylabel('Precision')
    axes[2].legend()

    plt.suptitle(f'{model_name}: AUC={roc_auc:.3f}')
    plt.tight_layout()
    plt.savefig('evaluation.png', dpi=150)

def _sigmoid(x):
    return 1 / (1 + np.exp(-x))
```

### Result Reporting

Save a JSON summary of the best configuration:

```python
import json

report = {
    "best_classifier": type(best_config['pipeline'].named_steps['classifier']).__name__,
    "best_params": {str(k): str(v) for k, v in best_params.items()},
    "cv_auc": float(best_auc),
    "selected_features": selected_feature_names,
    "rad_score_t_stat": float(t_stat),
    "rad_score_p_value": float(t_p),
}

with open('results/model_report.json', 'w') as f:
    json.dump(report, f, indent=2)
```
