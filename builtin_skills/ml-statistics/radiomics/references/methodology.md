---
name: FAE-Methodology
description: Core methodology reference based on the FAE (FeAture Explorer) open-source radiomics framework
---

# Radiomics Pipeline Methodology (FAE Inspired)

This methodology is based on the **FeAture Explorer (FAE)** framework (PLoS One 2020), optimized for clinical radiomics studies.

## Core Architecture: The 7-Step Pipeline

FAE implements a structured workflow to ensure reproducibility and statistical rigor.

### 1. Data Containerization
All features, labels, and case IDs are encapsulated in a `DataContainer`. This ensures that during any transformation (splitting, scaling, selection), the correspondence between feature values and their respective cases remains synchronized.

### 2. Balanced Cohort Splitting
Unlike simple random splitting, FAE emphasizes **clinical balance**:
- **Mechanism**: Iteratively performs random splits (e.g., 7:3) until the distribution of clinical features (age, stage, etc.) and the outcome labels shows no significant difference between the training and testing sets.
- **Verification**: Uses `Mann-Whitney U` for continuous variables and `Chi-Square` for categorical variables. A split is accepted typically when all $p > 0.10$.

### 3. Normalization (Parameter Migration)
Features are scaled to ensure stability.
- **Methods**: Z-Score (Zero-Center) or MinMax.
- **Strict Rule**: Scaling parameters (mean, std) must be calculated on the **Training Set only** and then applied (migrated) to the Testing and External sets to prevent data leakage.

### 4. Dimension Reduction (PCC)
High-dimensional radiomic data (often 1000+ features) contains significant redundancy.
- **Pearson Correlation Coefficient (PCC)**: If two features have a correlation $|r| > 0.9$ (default), the one with lower variance or less clinical relevance is removed.

### 5. Feature Selection
Selection reduces the feature set to a "signature" (typically top 5-15 features).
- **ANOVA**: Filters features based on univariate relationship with the label.
- **RFE (Recursive Feature Elimination)**: Iteratively removes features with the lowest importance using a linear SVM.
- **mRMR (Min-Redundancy Max-Relevance)**: Optimizes for features that are highly predictive but complementary to each oth

### 6. Modeling & Hyper-parameter Tuning
- **Classifiers**: Support for LR, SVM (Linear/RBF), Random Forest, LDA, and MLP.
- **GridSearch**: Automated cross-validation over a parameter grid (e.g., C, gamma, n_estimators) to find the optimal configuration.

### 7. Evaluation & Interpretability
- **Metrics**: AUC (with Delong test for significance), Accuracy, Sensitivity, Specificity.
- **SHAP Integration**: Provides local and global interpretability, explaining how much each feature contributes to a specific prediction.
- **Clinical Utility**: DCA (Decision Curve Analysis) and Calibration Curves to assess the model's reliability in a clinical setting.

## Enhanced Features in this Skill
1. **LASSO Pre-filter**: Added as a sparsity-inducing step before the combinatorial grid search.
2. **Two-Stage Optimization**: Coarse search for pipeline components followed by fine-tuning of top configurations.
3. **External Set Harmonization**: ComBat integration for handling multi-center batch effects.
