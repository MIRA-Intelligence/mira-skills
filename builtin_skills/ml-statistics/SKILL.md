---
name: ml-statistics-orchestrator
description: "Orchestrator guide for machine learning, statistical, and survival analysis tasks. Use this skill to navigate between dedicated research methods (radiomics, survival-analysis, statistical-analysis) and their underlying toolkits (scikit-learn, scikit-survival)."
---

# Machine Learning & Statistics Orchestrator

This skill acts as a central hub for all machine learning and statistical modeling tasks in MedPilot. The `ml-statistics` module contains independent research methods (`radiomics`, `survival-analysis`, `statistical-analysis`) as well as the foundational toolkits (`scikit-learn`, `scikit-survival`) that power them.

## Sub-Skills & Toolkits

### 1. Independent Research Methods
These are complete, end-to-end scientific pipelines. You should trigger these when the user asks to conduct a full research study or analyze a dataset from start to finish.

- **`radiomics`**: End-to-end radiomics feature selection and machine learning pipeline. 
  - *Dependency Note*: Radiomics analysis operates on structured feature tables. If the user only provides raw images and masks, you MUST first invoke the `pyradiomics` tool (from `data_processing/tools/pyradiomics`) to extract the features into a tabular format (like CSV). Once the features are extracted, this `radiomics` skill will primarily utilize `scikit-learn` to build predictive signatures.
- **`survival-analysis`**: Time-to-event modeling pipeline.
  - *Dependency Note*: This skill coordinates the entire clinical survival study, from Kaplan-Meier estimation to Cox Proportional Hazards. It relies heavily on the `scikit-survival` toolkit for modeling and metrics.
- **`statistical-analysis`**: Comprehensive statistical testing toolkit for academic research. Covers hypothesis testing (t-test, ANOVA, Chi-square), correlation, assumption checks, power analysis, and Bayesian statistics.

### 2. Core Toolkits
These are the foundational libraries that provide the algorithms for the research methods. Invoke these when the user has a specific algorithmic request or needs advanced, customized machine learning implementations.

- **`scikit-learn`**: The industry standard for classical machine learning (classification, regression, clustering, PCA, pipelines, hyperparameter tuning).
- **`scikit-survival`**: The specialized library for survival analysis (Survival SVMs, Random Survival Forests, Gradient Boosting Survival, Concordance Index).

---

## Task-to-Skill Mapping (Decision Guide)

When a user presents a task, use the following examples to determine which skill to invoke:

### Scenario 1: Medical Image Phenotyping (Radiomics)
**User Request:** "I have a dataset of lung CTs and tumor masks. I want to predict whether the tumors are malignant using radiomics."
**Action:** 
1. Use `data_processing` tools to extract radiomic features into a CSV.
2. Invoke the **`radiomics`** skill to handle feature selection (e.g., LASSO, removing collinearity) and build the final machine learning classifier (via `scikit-learn`).

### Scenario 2: Clinical Time-to-Event Study (Survival Analysis)
**User Request:** "Here is a clinical dataset of breast cancer patients with follow-up time and death status. Can you analyze if gene expression affects their survival?"
**Action:** 
Invoke the **`survival-analysis`** skill. It will guide you to check proportional hazards assumptions, plot Kaplan-Meier curves, and fit a Cox model. If the user asks for advanced machine learning survival models (like Random Survival Forests), the pipeline will leverage **`scikit-survival`**.

### Scenario 3: General Academic Hypothesis Testing (Statistical Analysis)
**User Request:** "I have a spreadsheet with the blood pressure of three different patient groups before and after drug administration. Are the differences statistically significant?"
**Action:** 
Invoke the **`statistical-analysis`** skill. It will instruct you to first check normality and variance assumptions, select the proper test (e.g., Repeated Measures ANOVA or Kruskal-Wallis), calculate effect sizes, and generate an APA-style statistical report.

### Scenario 4: Standard Machine Learning / Predictive Modeling
**User Request:** "I want to train an XGBoost model on this tabular electronic health record data to classify patient readmission risk, and I need to handle missing values and tune hyperparameters."
**Action:** 
Invoke the **`scikit-learn`** skill directly. It provides complete references for setting up robust `Pipeline` objects, `ColumnTransformer` for mixed data types, and `GridSearchCV` for tuning.

### Scenario 5: Advanced Survival Machine Learning
**User Request:** "I want to use a Survival Support Vector Machine (SVM) and a Gradient Boosting Survival model to see which gives a better Uno's C-index."
**Action:** 
Invoke the **`scikit-survival`** skill directly. It contains the specific implementation details for margin-based survival learning, ensemble survival models, and specialized metrics like `concordance_index_ipcw`.

---

## Important Rules

1. **Always Verify Data Prerequisites:**
   - Radiomics ML requires a *feature table*. Do not start ML on raw `.nii.gz` files.
   - Survival analysis requires *Time* and *Event* columns. Verify these exist before proceeding.
2. **Prioritize Scientific Rigor:** When conducting `statistical-analysis` or `radiomics`, effect sizes, confidence intervals, and strict assumption checking (e.g., multicollinearity, normality) are mandatory, not optional.