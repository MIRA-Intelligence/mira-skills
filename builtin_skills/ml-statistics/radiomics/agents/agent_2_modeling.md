# Agent 2: Feature Selection & Baseline Modeling (特征筛选与基础建模)

**Goal:** Reduce dimensionality, eliminate noise features, and build interpretability-focused baseline sub-models to establish initial performance.

## 1. Pre-experiment Pipeline Planning (预实验管线规划)

Before executing a single feature selection or modeling run, you MUST systematically plan the pre-experiment combinations by iterating over the core components defined in the [Methodology Reference](../references/methodology.md). 

Generate a grid of basic pipeline configurations to test as baselines. A standard pre-experiment grid includes combinations of:
- **Normalization (参数迁移)**: [Z-Score (StandardScaler), MinMax (MinMaxScaler), Robust (RobustScaler), MaxAbs (MaxAbsScaler)]
- **Dimension Reduction (降维)**: [PCC (threshold=0.99), PCA, TruncatedSVD]
- **Feature Selection (特征选择)**: 
  - *Filter Methods*: [ANOVA (f_classif), Chi-Squared (chi2), Mutual Information (mutual_info_classif), Kruskal-Wallis (KW)]
  - *Wrapper/Embedded Methods*: [RFE, mRMR, LASSO (L1-based SelectFromModel), ReliefF, Random Forest Importance (SelectFromModel)]
- **Classifiers (分类器)**: 
  - *Linear*: [LR (Logistic Regression), SVM-Linear (LinearSVC), RidgeClassifier, SGDClassifier]
  - *Tree/Ensemble*: [Random Forest, Gradient Boosting, HistGradientBoosting, AdaBoost, Decision Tree]
  - *Other*: [SVM-RBF/Poly (SVC), Naive Bayes (GaussianNB, BernoulliNB), KNN (KNeighborsClassifier), MLP (MLPClassifier), LDA (LinearDiscriminantAnalysis)]

*Note*: You are running a preliminary sweep to establish which broad categories of algorithms work best on this specific dataset before moving to deep tuning in Agent 3.
**Efficiency Mandate**: To drastically reduce the time spent searching across this vast grid, you MUST enable parallel computing by setting `n_jobs=-1` whenever possible in cross-validation functions (e.g., `cross_val_score`, `GridSearchCV`, `SelectFromModel`) and capable estimators (e.g., `RandomForestClassifier`, `HistGradientBoostingClassifier`).

## 2. Iterative Pipeline Execution (迭代执行预实验管线)

For EACH configuration planned in Step 1, you MUST construct and evaluate a machine learning pipeline. To implement these pipelines, you MUST invoke the `@builtin_skills/ml-statistics/scikit-learn` skill to leverage its robust pipeline and cross-validation capabilities.

### Feature Selection & Preprocessing
Within each pipeline iteration, apply the selected components to transform ~1000 raw features into a robust signature. You MUST write custom Python code using the `scikit-learn` skill to construct these pipelines. The pre-built utility scripts provided in `builtin_skills/ml-statistics/radiomics/scripts/` should be used as logic references only, do NOT run them directly with `run_shell_command`.

1. **Robustness (ICC)** (Optional): If test-retest scans exist, retain features with `ICC > 0.75`.
2. **Standardization**: Apply the chosen normalizer (e.g., `StandardScaler`, `MinMaxScaler`) (fit on training set ONLY).
3. **LASSO Pre-filter** (Optional): Use L1-regularization to drop non-predictive features.
   - *Reference Implementation*: `builtin_skills/ml-statistics/radiomics/scripts/lasso_filter.py`
   - *Reference*: [LASSO Methodology](../references/lasso_prefilter.md)
4. **Collinearity (PCC) & Statistical Ranking**: Apply the chosen dimension reduction. Calculate Pearson Correlation; if `|r| > threshold`, drop the feature with lower variance. Default threshold is `0.95`. Then apply the chosen selector (ANOVA, mRMR, or RFE) to rank and select features.
   - *Reference Implementation*: `builtin_skills/ml-statistics/radiomics/scripts/feature_selection.py`

### Selection Deliverables
- `features_selected.csv`: Final feature matrix for the best performing pipeline.
- `selection_report.json`: List of selected features and their selection scores for the best pipeline.

### Critical Guardrails
- **Zero-Variance**: Remove constant features before any analysis.
- **Leakage**: NEVER perform feature selection or normalization on the combined train+test set. Ensure all preprocessing steps are encapsulated within an `sklearn.pipeline.Pipeline` to prevent data leakage during Cross-Validation.

## 3. Baseline Modeling Strategy

### Sub-Model Hierarchy
To ensure interpretability, build baseline models in this sequence:
1. **Clinical Model**: Clinical features only.
2. **Simple Radiomics Model**: Original (Shape + Firstorder + Texture).
3. **Advanced Radiomics Model**: Tier 1 + LoG/Wavelet sub-bands.
4. **Combined Model**: Clinical + Radiomics signature.

### Validation Paths & Model Selection
- **Metric Priority**: Models MUST be selected primarily based on the **Validation AUC** (or CV AUC).
- **1-SE Rule**: When analyzing the relationship between Feature Number and Validation AUC, select the simplest model (fewest features) whose AUC is within one standard error (1-SE) of the highest Validation AUC.
- **Result Persistence**: For EVERY evaluated pipeline, you MUST save the complete output dictionary for Train, Valid (CV), and Test sets, including:
  - Raw prediction probabilities and predicted class labels.
  - The optimized cutoff/threshold value.
  - The fitted model weights (coefficients/feature importances).
  - The serialized model object (e.g., via `joblib` or `pickle`).
- **Confidence Intervals**: The 95% CI for the Validation and Test AUCs MUST be calculated using the **Bootstrap algorithm**.

### External Cohort Harmonization
If overfitting occurs on external data or batch effects are detected:
- **Normalization Migration**: Use the `mean` and `std` from the Training Set to normalize the External Set.
- **ComBat**: Apply ComBat harmonization to eliminate systematic differences between internal and external centers.

### Baseline Algorithms
You MUST construct `sklearn` pipelines for modeling using the `scikit-learn` skill. You can refer to the logic in the following script as an example, but do NOT run it directly:
- *Reference Implementation*: `builtin_skills/ml-statistics/radiomics/scripts/modeling.py`

- **LR (Logistic Regression)**: Baseline for interpretability.
- **SVM**: Try both **Linear** and **Non-Linear (RBF/Poly)** kernels.
- **Random Forest**: For non-linear relationships and feature importance ranking.

## Implementation Guide & Visualizations (Python)

### Bootstrap AUC Confidence Interval
```python
import numpy as np
from sklearn.metrics import roc_auc_score

def bootstrap_auc_ci(y_true, y_pred_prob, n_bootstraps=1000, alpha=0.95):
    """Calculate the 95% Confidence Interval of AUC using Bootstrapping."""
    bootstrapped_scores = []
    rng = np.random.RandomState(42)
    
    # Convert inputs to numpy arrays for indexing
    y_true = np.array(y_true)
    y_pred_prob = np.array(y_pred_prob)
    
    for i in range(n_bootstraps):
        # Bootstrap by sampling with replacement
        indices = rng.randint(0, len(y_pred_prob), len(y_pred_prob))
        if len(np.unique(y_true[indices])) < 2:
            continue
        score = roc_auc_score(y_true[indices], y_pred_prob[indices])
        bootstrapped_scores.append(score)
        
    sorted_scores = np.array(bootstrapped_scores)
    sorted_scores.sort()
    
    lower_bound = sorted_scores[int((1.0 - alpha) / 2.0 * len(sorted_scores))]
    upper_bound = sorted_scores[int((1.0 + alpha) / 2.0 * len(sorted_scores))]
    return lower_bound, upper_bound
```

## Deliverables & Mandatory Plots
1. **Performance Table**: Comprehensive table displaying AUC (with 95% Bootstrap CI), Accuracy, Sensitivity, and Specificity for Train, 5-Fold CV, and Test/External sets.
2. **Unified ROC Curve**: A single, composite plot containing the ROC curves (optionally with shaded 95% CI bounds) for Train, CV Valid, and Test sets on the same axes.
3. **Feature Selection Curve**: A line plot showing **Feature Number (X-axis) vs. Validation AUC (Y-axis)**. Highlight the peak AUC and the final model chosen via the **1-SE rule**.
4. **Feature Weights Plot**: A horizontal bar chart visualizing the coefficients or feature importances for each final sub-model.
5. **Artifacts Directory**: A folder containing the saved `.pkl` / `.joblib` models, probabilities CSVs, and threshold cutoffs for reproducible inference. 