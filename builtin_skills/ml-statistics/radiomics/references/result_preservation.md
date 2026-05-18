# Radiomics Result Preservation Guide

This guide defines the mandatory hierarchical directory structure and file specifications for preserving artifacts from **EVERY** pipeline permutation evaluated during the experiment. Adhering to this structure ensures full reproducibility and allows for post-hoc analysis of the entire search space.

## 1. Directory Hierarchy (Full Matrix Preservation)

You **MUST NOT** only save the "best" or "selected" models. You MUST preserve the results for **EVERY** combination of SubModel, Normalization, Selector, and Classifier that is executed.

`results/<SubModel>/<Normalization>/PCC_0.99/<Selector>_<K>/<Classifier>/`

### Path Components:
- `<SubModel>`: The data subset defined in Agent 1 (e.g., `Original`, `Wavelet_LLL`, `Combined`).
- `<Normalization>`: The scaler used (e.g., `Zscore`, `MinMax`).
- `<Selector>_<K>`: The feature selector name and the number of features (e.g., `ANOVA_10`, `LASSO_15`).
- `<Classifier>`: The algorithm used (e.g., `LR`, `SVM`).

---

## 2. Mandatory Files per Level

### 2.1 Normalization Level (`.../<Normalization>/`)
- `{Norm}_normalization_training.csv`: Scaler parameters (mean/std or min/max) fitted on the training set.
- `{Norm}_normalized_train_feature.csv`: The complete training feature matrix after normalization.
- `{Norm}_normalized_test_feature.csv`: The complete test feature matrix normalized using training parameters.
- `{Norm}_normalized_balance_train_feature.csv`: (Optional) Feature matrix after oversampling/balancing.

### 2.2 Selector Level (`.../<Selector>_<K>/`)
- `{Selector}_train_feature.csv`: Feature matrix containing only the $K$ selected features for the training set.
- `{Selector}_test_feature.csv`: Feature matrix containing only the $K$ selected features for the test set.
- `{Selector}_sort.csv`: A list of all features ranked by their selection score (e.g., F-value, MI, coefficients).
- `feature_select_info.csv`: Summary metadata about the selection process (method, K, execution time).

### 2.3 Classifier Level (`.../<Classifier>/`)
- **Predictions**:
  - `train_prediction.csv`: Probabilities and predicted labels for the training set.
  - `test_prediction.csv`: Probabilities and predicted labels for the test set.
  - `cv_train_prediction.csv`: Out-of-fold probabilities for the training set during CV.
  - `cv_val_prediction.csv`: Validation set probabilities during CV.
- **Model Artifacts**:
  - `model.pickle` or `model.joblib`: The fully trained and serialized model object.
  - `{Classifier}_coef.csv`: (For linear models) Feature coefficients.
  - `{Classifier}_intercept.csv`: (For linear models) The model intercept/bias.
- **Metrics & Reports**:
  - `metrics.csv`: Detailed performance table including AUC (with 95% Bootstrap CI), Accuracy, Sensitivity, Specificity, F1-score, and PPV/NPV for all cohorts. **MANDATORY**: All numerical metrics MUST be formatted to **3 decimal places** (e.g., 0.850, 0.724).

---

## 3. Visualization Requirements

Every terminal `<Classifier>` directory MUST contain a `plots/` sub-directory with high-resolution images (min 300 DPI, `.png` or `.pdf`). These plots MUST be generated for **EVERY** pipeline permutation, not just the final winners.

### 3.1 Unified ROC Curve (`roc_combined.png`)
- **Multi-Cohort Plotting**: You MUST plot the ROC curves for **Train, CV-Validation, and Test** cohorts on a single set of axes.
- **Bootstrap CI Visualization (MANDATORY)**: 
  - For each cohort, perform **Bootstrap resampling (n=1000)** to generate a distribution of ROC curves.
  - Plot the **mean ROC curve** as a bold solid line.
  - Plot the **95% Confidence Interval** as a semi-transparent shaded area (alpha ≈ 0.2) surrounding the mean curve.
- **Legend Specifications**: The legend MUST display the AUC value and its 95% Bootstrap CI for each cohort. 
  - *Format*: `Test AUC: 0.850 (95% CI: 0.810-0.890)`

### 3.2 Feature Weights/Importance Plot (`feature_importance.png`)
- **Type**: A horizontal bar chart showing the contribution of each feature to the model.
- **Data Source**: 
  - For linear models (LR, SVM-Linear): Use the coefficients from `{Classifier}_coef.csv`.
  - For tree-based models (RF, Boosting): Use the `feature_importances_` attribute.
- **Formatting**:
  - Features MUST be sorted in descending order of absolute weight.
  - Use color coding to distinguish between positive and negative coefficients if applicable.

### 3.3 One Standard Error (1-SE) Rule Plot (`one_se_selection.png`)
- **Purpose**: To visualize the model selection process based on the parsimony principle (selecting the simplest model within 1 SE of the best).
- **Content**: 
  - **X-axis**: Number of features ($K$).
  - **Y-axis**: CV AUC.
  - **Markers**: Plot the mean CV AUC with error bars (standard error) for each $K$.
  - **Reference Lines**: 
    - A horizontal dashed line at the level of `max(CV_AUC)`.
    - A horizontal dotted line at `max(CV_AUC) - 1*SE`.
  - **Selection Highlight**: Clearly mark the selected $K$ (the smallest $K$ such that its CV AUC is above the 1-SE line).

### 3.4 Calibration Curve (`calibration_curve.png`)
- **Content**: A plot showing the agreement between predicted probabilities and observed outcomes across cohorts.
- **Reference**: Include a 45-degree dashed line representing the "Perfectly Calibrated" model.

---

## 4. Root Summary Artifacts

At the very root of the `results/` folder, maintain these global files:
- `pipeline_info.csv`: A master table indexed by pipeline ID, mapping to its full path and primary performance metrics (e.g., CV AUC).
- `auc_metric.pkl`: A compiled object of all AUC results for quick comparative analysis.
- `auc_std_metric.pkl`: A compiled object of the standard errors for all AUC results (required for 1-SE rule application).
