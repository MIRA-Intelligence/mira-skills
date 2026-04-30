# Best Practices, Common Pitfalls, and Scaling

## 1. Common Pitfalls to Avoid

### A. Data Leakage (The #1 ML Error)
**What it is:** When information from outside the training dataset is used to create the model.
**Symptoms:** Unrealistically high performance during cross-validation that collapses in production or on independent test sets.

**How to avoid it:**
1.  **Always use `Pipeline`**: Never fit transformers (StandardScaler, PCA, Imputer) on the entire dataset before splitting.
    ```python
    # WRONG (Data Leakage)
    X_scaled = StandardScaler().fit_transform(X) # Information from test set leaked into scaling parameters
    cross_val_score(model, X_scaled, y, cv=5)

    # CORRECT
    pipeline = make_pipeline(StandardScaler(), model)
    cross_val_score(pipeline, X, y, cv=5) # Scaling is computed strictly within each training fold
    ```
2.  **Temporal/Grouped Splitting**: If data is time-series, use `TimeSeriesSplit`. If there are multiple samples per patient, use `GroupKFold`. Standard random splitting will leak patient-specific or future information into the training set.

### B. Inappropriate Metrics
- **Accuracy on Imbalanced Data**: Predicting "No Cancer" for everyone yields 99% accuracy if prevalence is 1%. Use `roc_auc`, `average_precision`, `f1_macro`, or `balanced_accuracy` instead.
- **Handling Imbalance**: Instead of over/undersampling (which can distort probability distributions), try setting `class_weight='balanced'` inside the estimator.

## 2. Model Persistence (Saving/Loading)

For production, models must be saved to disk. **joblib** is the recommended tool for scikit-learn objects, as it is more efficient than standard `pickle` for large numpy arrays.

```python
import joblib

# 1. Save the COMPLETE pipeline (includes all preprocessing and the model)
joblib.dump(best_pipeline, 'production_model.joblib')

# 2. Load the pipeline in production
loaded_pipeline = joblib.load('production_model.joblib')

# 3. Predict on raw new data
# Because we saved the Pipeline, it automatically handles imputation, scaling, and encoding!
predictions = loaded_pipeline.predict(X_new_raw)
```

## 3. Computing and Scaling to Large Datasets

When datasets grow beyond RAM limits (e.g., > 10GB) or training takes too long, scikit-learn offers several scaling strategies.

### A. Parallelism (`n_jobs`)
Many estimators and search functions support parallel processing across multiple CPU cores.
- Set `n_jobs=-1` to use all available cores.
- **Supported by:** `RandomForest`, `GridSearchCV`, `cross_val_score`, `HistGradientBoosting`.

### B. Out-of-Core Learning (Streaming)
For data that doesn't fit in RAM, you can stream it in chunks (mini-batches).
- **Supported Estimators (must have `.partial_fit()` method):**
  - Classification: `SGDClassifier`, `MultinomialNB`, `MiniBatchKMeans`
  - Regression: `SGDRegressor`
  - Preprocessing: `StandardScaler` (has `partial_fit`)

```python
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

# Initialize
scaler = StandardScaler()
model = SGDClassifier(loss='log_loss')
classes = np.array([0, 1])

# Simulate reading data in chunks
for chunk_X, chunk_y in get_data_chunks(file_path, chunk_size=10000):
    # 1. Update scaler
    scaler.partial_fit(chunk_X)
    X_scaled = scaler.transform(chunk_X)
    
    # 2. Update model
    model.partial_fit(X_scaled, chunk_y, classes=classes)
```

### C. Fast Alternatives for Big Data
If Random Forest or standard Gradient Boosting (`GradientBoostingClassifier`) is too slow:
- **Use `HistGradientBoostingClassifier`**: Scikit-learn's fastest ensemble method, inspired by LightGBM. It bins continuous features into integer-valued bins, drastically speeding up training on datasets with tens of thousands of samples. It also natively supports missing values and categorical features without needing OneHotEncoder.

```python
from sklearn.ensemble import HistGradientBoostingClassifier

model = HistGradientBoostingClassifier(
    max_iter=100,
    categorical_features='from_dtype', # Automatically handles pandas categorical columns
    early_stopping=True
)
model.fit(X_train, y_train) # Missing values in X_train are handled natively!
```

## 4. Metadata Routing (Advanced)

*(Introduced in recent versions of scikit-learn)*
Sometimes you need to pass metadata (like `sample_weight` or `groups`) through a complex Pipeline or to specific scorers.

```python
import sklearn

# Enable metadata routing globally
sklearn.set_config(enable_metadata_routing=True)

# Now you can route sample weights explicitly to the classifier step in a pipeline
pipeline.fit(X, y, classifier__sample_weight=sample_weights)
```