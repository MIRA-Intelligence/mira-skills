# Model Inspection and Visualizations Reference

## Overview

Understanding why a model makes specific predictions is crucial for clinical, financial, and other high-stakes domains. Scikit-learn provides built-in tools for model inspection, interpretability, and visualization.

## 1. Permutation Feature Importance

**Permutation Importance (`sklearn.inspection.permutation_importance`)**
- Measures the decrease in a model score when a single feature value is randomly shuffled.
- Model agnostic (works with any fitted estimator).
- Captures non-linear and interaction effects (unlike linear coefficients).
- **Use when:** You want a reliable feature importance metric that doesn't suffer from the high cardinality bias of tree-based `feature_importances_`.

```python
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import pandas as pd

# Assuming `model` is already fitted on X_train, y_train
# It's best practice to compute permutation importance on a held-out test set
result = permutation_importance(
    model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=-1
)

# Organize into a DataFrame
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance Mean': result.importances_mean,
    'Importance Std': result.importances_std
}).sort_values(by='Importance Mean', ascending=False)

# Plot
importance_df.plot.barh(x='Feature', y='Importance Mean', xerr='Importance Std')
plt.title("Permutation Feature Importance (Test Set)")
plt.gca().invert_yaxis()
plt.show()
```

## 2. Partial Dependence Plots (PDP)

**Partial Dependence (`sklearn.inspection.PartialDependenceDisplay`)**
- Shows the marginal effect one or two features have on the predicted outcome of a machine learning model.
- Tells you whether the relationship is linear, monotonic, or more complex.
- **Use when:** You want to understand the *direction* and *shape* of the relationship between key features and the target.

```python
from sklearn.inspection import PartialDependenceDisplay
import matplotlib.pyplot as plt

# Features to plot (can be indices or names)
features = [0, 1, (0, 1)] # Plot feature 0, feature 1, and their 2D interaction

# Plot PDP
fig, ax = plt.subplots(figsize=(12, 4))
display = PartialDependenceDisplay.from_estimator(
    model, 
    X_train, 
    features, 
    feature_names=feature_names,
    ax=ax,
    n_jobs=-1,
    grid_resolution=50
)
plt.subplots_adjust(wspace=0.3)
plt.show()
```

## 3. Individual Conditional Expectation (ICE) Plots

**ICE Plots**
- Similar to PDP, but plots one line per sample (instead of the average).
- Highlights heterogeneous effects (e.g., if a feature has a positive effect for some samples but negative for others, the PDP might average to zero, but ICE will show the true spread).

```python
from sklearn.inspection import PartialDependenceDisplay
import matplotlib.pyplot as plt

# To plot ICE, simply set kind='individual' or kind='both' (ICE + PDP)
fig, ax = plt.subplots(figsize=(10, 6))
display = PartialDependenceDisplay.from_estimator(
    model, 
    X_test, 
    features=[0, 1], # Only 1D plots support ICE
    kind='both',     # Plots ICE lines (light) and PDP line (bold)
    feature_names=feature_names,
    ax=ax
)
plt.show()
```

## 4. Built-in Visualization APIs

Scikit-learn provides modern, object-oriented plotting APIs (`*Display` classes) that allow for quick visualizations without writing extensive matplotlib code.

### ROC Curve and Precision-Recall Curve
```python
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# ROC Curve
RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax1)
ax1.set_title("ROC Curve")

# Precision-Recall Curve
PrecisionRecallDisplay.from_estimator(model, X_test, y_test, ax=ax2)
ax2.set_title("Precision-Recall Curve")

plt.show()
```

### Confusion Matrix
```python
from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_estimator(
    model, X_test, y_test, 
    cmap='Blues', 
    normalize='true' # Normalize by true class
)
plt.title("Normalized Confusion Matrix")
plt.show()
```

### Calibration Curve (Reliability Diagram)
Used to evaluate if predicted probabilities are well-calibrated (i.e., if a model predicts 0.8, the event should happen 80% of the time).
```python
from sklearn.calibration import CalibrationDisplay

CalibrationDisplay.from_estimator(model, X_test, y_test, n_bins=10)
plt.title("Calibration Curve")
plt.show()
```

### Decision Boundary
Useful for visualizing 2D toy datasets or 2D projections of features.
```python
from sklearn.inspection import DecisionBoundaryDisplay

# Assuming X_train is 2D
DecisionBoundaryDisplay.from_estimator(
    model, X_train, response_method="predict", cmap="RdBu", alpha=0.5
)
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, edgecolors="k")
plt.show()
```

## Best Practices for Inspection

1.  **Test Set vs. Train Set**: Compute Permutation Importance on a **held-out validation or test set**. Computing it on the training set will incorrectly assign high importance to features the model has overfit to.
2.  **Multicollinearity**: If features are highly correlated, Permutation Importance can be misleading (permuting one feature might not drop performance much if the model relies on the correlated feature). Use hierarchical clustering or drop redundant features first.
3.  **Scaling**: Inspection methods do not strictly require scaled features, but understanding the axes of PDPs is much easier if the features are kept in their original unscaled format (use `ColumnTransformer` properly so you can pass raw features to the PDP function).