# Agent 2: Baseline Modeling Grid (基线建模网格搜索)

**Goal:** Execute a comprehensive grid search of standardized radiomics pipelines to identify promising feature-classifier combinations using interpretable baseline models.

## 1. Exhaustive Pipeline Grid (标准网格维度)

You MUST iterate through ALL combinations of the following dimensions using the partitioned matrices from Agent 1.

1. **Normalization (归一化)**: 
   - `Z-score` (StandardScaler)
   - `MinMax` (MinMaxScaler)
2. **Dimension Reduction (相关性剔除)**:
   - `PCC` (Pearson Correlation Coefficient): **Mandatory**. Remove features with $|r| > 0.99$.
3. **Feature Selection (特征筛选 - 并列互斥)**:
   - `ANOVA` (F-classif)
   - `LASSO` (Logistic Regression with L1 penalty)
   - `Chi-squared` (chi2)
   - `MI` (Mutual Information)
   - `KW` (Kruskal-Wallis)
   - `ReliefF`
   - `RFE` (Recursive Feature Elimination): **Mandatory Consistency**. You MUST use the same classifier for RFE as the final model in the pipeline (e.g., if the classifier is LR, RFE must use an LR estimator). Cross-usage of estimators (e.g., SVM-RFE with an LR classifier) is strictly prohibited.
4. **Interpretable Classifiers (基线分类器)**:
   - `LR` (Logistic Regression)
   - `SVM-Linear` (Support Vector Machine with linear kernel)

## 2. Computational Execution

- **Parallelization**: Use `joblib.Parallel` to evaluate sub-models and pipeline permutations across CPU cores.
- **Data Integrity**: Use the `DataContainer` class to ensure parameter migration (fitting Scaler/PCC on training data only).
- **Metric Tracking**: For every permutation, calculate and save:
  - **Train AUC** (with 95% Bootstrap CI)
  - **CV AUC** (mean and standard error across folds)
  - **Test AUC** (if test set is available)

## 3. Deliverables & Mandatory Reporting (全量保存)

You MUST generate and save all artifacts specified in the **[Result Preservation Guide](../references/result_preservation.md)**.

1. **Full Matrix Preservation**: Save results for **EVERY** pipeline permutation. Do not discard results.
2. **Exhaustive Visualization**: For **EVERY** permutation, generate:
   - `roc_combined.png`: Combined Train/CV/Test plot with shaded 95% CI.
   - `feature_importance.png`: Bar chart of coefficients/weights.
   - `one_se_selection.png`: Plot of CV AUC vs. $K$ with 1-SE thresholds (Note: 1-SE selection is analyzed in Agent 4).
3. **Master Summary**: Generate `pipeline_info.csv` at the root of the `results/` folder, indexing all pipelines by their performance.

**Handoff**: Once the baseline grid is complete and all artifacts are saved, proceed to **Agent 3: Optimization & Selection**. Do NOT perform the 1-SE selection or final model picking in this Agent.