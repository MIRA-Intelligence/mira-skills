# Agent 2: Pyramid Feature Selection & Modeling (金字塔特征筛选与建模)

**Goal:** Execute a FAE-inspired hierarchical "Pyramid" selection strategy to reduce dimensionality, ensure interpretability, and build robust sub-models using process-level parallelization.

## 1. Pyramid Selection Strategy (金字塔合并策略)

You MUST iterate through three distinct levels of feature selection. At EACH level, you perform a full Grid Search (Normalizer × Mutually-Exclusive-Selector × Classifier).

### Level 1: Atomic Base (底层原子筛选)
- **Input**: Every atomic sub-model matrix created in Agent 1 (e.g., `df_shape`, `df_glcm`, `df_log_sigma_1_glrlm`).
- **Execution**: Perform independent Grid Searches for every group.
- **Mandate**: Select the best performing features from each atomic group to pass to Level 2.

### Level 2: Intermediate Merge (中层语义合并)
- **Input**: Concatenate the selected features from Level 1 into intermediate semantic groups (e.g., `Original`, `LoG`, `Wavelet`).
- **Execution**: Perform a new full Grid Search on these merged matrices.

### Level 3: Global Fusion (全局顶层融合)
- **Input**: Concatenate the selected features from Level 2 into a single `Global Radiomics` matrix.
- **Execution**: Perform the final Grid Search and hyperparameter optimization.

## 2. Exhaustive Pipeline Grid

Within each level, iterate over ALL combinations of the following parallel dimensions:

1. **Normalization**: [StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler]
2. **Feature Selection (Mutually Exclusive)**: 
   - *Filter*: [ANOVA (f_classif), Chi-Squared, MI, Kruskal-Wallis]
   - *Embedded*: [LASSO (LogisticRegression with penalty='l1'), Random Forest Importance]
   *Constraint*: You MUST NOT chain LASSO and ANOVA. Pick exactly ONE for each pipeline.
3. **Classifiers**: [LogisticRegression, SVM (Linear/RBF), Random Forest, LDA, AdaBoost]

## 3. Computational Efficiency & Parallelization (进程级加速)

### Parallel Orchestration (Mandatory)
- **Level 1 Acceleration**: When evaluating the multiple independent atomic sub-models, you MUST NOT use a sequential `for` loop.
- **Mandate**: Use `joblib.Parallel` or `multiprocessing` to dispatch sub-model evaluations to separate CPU cores.

### Efficiency Optimizations
- **Fold Consistency**: Pre-calculate `StratifiedKFold` indices and reuse them across the entire grid to ensure statistical fairness.
- **Feature Ranking Caching**: For score-based selectors, calculate rankings once per normalization method and use "Lazy Slicing" for different $K$ (Top-K) values.

## 4. FAE-Inspired Implementation Standard (参考代码)

You MUST generate Python code that adheres to these robust patterns:

### A. DataContainer & Parameter Migration
```python
# Encapsulate data and handle training-to-test parameter migration (Mean/Std)
class DataContainer:
    def __init__(self, X, y, feature_names, case_names):
        self.X, self.y = X, y
        self.feature_names, self.case_names = feature_names, case_names

    def transform_and_evaluate(self, pipeline, cv_indices):
        # Pipeline ensures Scaler is fit on training fold only (Anti-Leakage)
        return cross_val_score(pipeline, self.X, self.y, cv=cv_indices, scoring='roc_auc')
```

### B. Process-Level Parallelization
```python
from joblib import Parallel, delayed

# DISPATCH independent Level 1 sub-models to separate processes
results = Parallel(n_jobs=-1)(
    delayed(run_grid_search)(submodel_X, submodel_y) 
    for submodel_X, submodel_y in atomic_groups
)
```

### C. Advanced Interpretability (SHAP)
Alongside ROC curves, generate SHAP explanations for the final model:
```python
import shap
def save_interpretability_plots(model, X_train, output_dir):
    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_train)
    # Global Importance (Bar) and Local Contribution (Beeswarm)
    shap.plots.bar(shap_values, show=False)
    plt.savefig(f"{output_dir}/SHAP_Global.png")
    shap.plots.beeswarm(shap_values, show=False)
    plt.savefig(f"{output_dir}/SHAP_Local.png")
```

## 5. Deliverables & Mandatory Reporting

You MUST generate and save all artifacts specified in the **[Result Preservation Guide](../references/result_preservation.md)**. Key requirements include:

1. **Comprehensive AUC Reporting**: For the selected optimal models at each pyramid level, the output report to the user MUST explicitly list:
   - **Train AUC** (with 95% Bootstrap CI)
   - **CV AUC** (with 95% CI or standard deviation)
   - **Test AUC** (with 95% Bootstrap CI) - if a test set exists.
2. **Metrics Persistence**: For EVERY pipeline permutation evaluated in the grid search, the saved performance metrics (`metrics.csv` or `pipeline_info.csv`) MUST include the **Train AUC** alongside the CV AUC. This is critical for evaluating the generalization gap (Train AUC - CV AUC).
3. **Unified ROC Curve**: Combined Train/CV/Test plot with **shaded 95% Bootstrap CI regions**.
4. **Interpretability Plots**: Feature Importance (Bar chart) and SHAP visualizations (Global Bar + Local Beeswarm) for the final model.
5. **Artifacts Directory**: A folder containing the saved `.pkl` / `.joblib` pipelines, selected features CSVs, and predictions for reproducible inference.