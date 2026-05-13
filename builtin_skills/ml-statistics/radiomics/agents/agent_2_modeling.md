# Agent 2: Feature Selection & Baseline Modeling (特征筛选与基础建模)

**Goal:** Reduce dimensionality, eliminate noise features, and build interpretability-focused baseline sub-models to establish initial performance.

## 1. Pre-experiment Pipeline Planning (预实验管线规划)

Before executing a single feature selection or modeling run, you MUST systematically plan the pre-experiment combinations. A "pipeline" is defined as a unique path from raw data subsets to final prediction. You MUST iterate over ALL combinations of the following dimensions to establish robust baselines.

### Exhaustive Permutation Grid
The total number of pre-experiment pipelines is the product of these dimensions:

1. **Sub-model Data Inputs (from Agent 1)**:
   - *Independent*: [Clinical, Original_Shape, Original_Firstorder, Original_Texture]
   - *Tiered*: [Tier 1 All (Shape+Firstorder+Texture), Tier 2 LoG (specific sigma), Tier 2 Wavelet (specific sub-band)]
   - *Global*: [Advanced Radiomics (Tier 1 + Tier 2 All)]
2. **Normalization (参数迁移)**: [Z-Score (StandardScaler), MinMax (MinMaxScaler), Robust (RobustScaler), MaxAbs (MaxAbsScaler)]
3. **Dimension Reduction (降维)**: [PCC (threshold=0.99), PCA, TruncatedSVD]
4. **Feature Selection (特征选择)**: 
   - *Filter Methods*: [ANOVA (f_classif), Chi-Squared (chi2), Mutual Information (mutual_info_classif), Kruskal-Wallis (KW)]
   - *Wrapper/Embedded Methods*: [RFE, mRMR, LASSO (L1-based SelectFromModel), ReliefF, Random Forest Importance (SelectFromModel)]
5. **Classifiers (分类器)**: 
   - *Linear*: [LR (Logistic Regression), SVM-Linear (LinearSVC), RidgeClassifier, SGDClassifier]
   - *Tree/Ensemble*: [Random Forest, Gradient Boosting, HistGradientBoosting, AdaBoost, Decision Tree]
   - *Other*: [SVM-RBF/Poly (SVC), Naive Bayes (GaussianNB, BernoulliNB), KNN (KNeighborsClassifier), MLP (MLPClassifier), LDA (LinearDiscriminantAnalysis)]

### Dynamic Feature Count & Evaluation Strategy
For EACH combination above, you MUST:
- **Iterate Top-K Features**: Vary the number of selected features (K) from **1 to 1/10 of the training sample size** ($N_{train} / 10$).
- **Apply 1-SE Rule**: For every pipeline, evaluate both:
  1. The **Best Model** (highest Validation AUC).
  2. The **1-SE Model** (the simplest model with the fewest features whose AUC is within one standard error of the best).
  *Note*: This dual-evaluation effectively doubles the pipeline combinations per grid cell to prioritize parsimonious models.

*Note*: You are running a preliminary sweep to establish which broad categories of algorithms and feature subsets work best on this specific dataset before moving to deep tuning in Agent 3.
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
- **Result Persistence**: For EVERY evaluated pipeline permutation, you MUST save all outputs into the standardized hierarchical directory structure.
  - **Mandatory Standards**: Refer to **[Result Preservation Guide](../references/result_preservation.md)** for exact folder paths, required filenames, and metric precision (3 decimal places).
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
You MUST generate and save all artifacts specified in the **[Result Preservation Guide](../references/result_preservation.md)**. Key requirements include:
1. **Performance Table**: AUC (with 95% Bootstrap CI), Accuracy, Sens, and Spec, all reported to **3 decimal places**.
2. **Unified ROC Curve**: Combined Train/CV/Test plot with **shaded 95% Bootstrap CI regions**.
3. **Feature Selection Curve**: Feature Number vs. Validation AUC, highlighting the 1-SE model.
4. **Feature Weights Plot**: Sorted horizontal bar chart of coefficients or importances.
5. **Artifacts Directory**: A folder containing the saved `.pkl` / `.joblib` models, probabilities CSVs, and threshold cutoffs for reproducible inference. 
 