# Radiomics Utility Scripts

These scripts provide standalone implementations of common radiomics pipeline steps. They are provided as **supplements** and do not replace the core agent-led workflow.

## Scripts Overview

### 1. `cohort_split.py`
- **Purpose**: Performs balanced cohort splitting.
- **Logic**: Randomly splits data and verifies that clinical features and labels have similar distributions in train/test sets (using Mann-Whitney U and Chi-Square tests).
- **Usage**:
  ```bash
  python cohort_split.py --input features.csv --clinical clinical.csv --output_dir ./split
  ```

### 2. `lasso_filter.py`
- **Purpose**: High-dimensional feature pre-filtering.
- **Logic**: Uses `LogisticRegressionCV` with L1 (LASSO) penalty to identify a sparse set of predictive features.
- **Usage**:
  ```bash
  python lasso_filter.py --input train.csv --output lasso_filtered.csv
  ```

### 3. `feature_selection.py`
- **Purpose**: Dimension reduction and feature selection.
- **Logic**: 
  - Removes zero-variance features.
  - Applies **PCC** (Pearson Correlation) to remove redundant features ($|r| > 0.9$).
  - Performs **ANOVA** or **RFE** to select top-K features.
- **Usage**:
  ```bash
  python feature_selection.py --input lasso_filtered.csv --method anova --n_features 10 --output_dir ./selected
  ```

### 4. `modeling.py`
- **Purpose**: Model training, CV, and validation.
- **Logic**:
  - Scales features (fit on train, transform on test).
  - Performs 5-fold Stratified Cross-Validation on the training set.
  - Trains a final model (LR, SVM, or RF).
  - Evaluates on the independent test set (AUC, Acc, Precision, Recall).
- **Usage**:
  ```bash
  python modeling.py --train train_selected.csv --test test_selected.csv --classifier lr --output_dir ./results
  ```

## Extensibility
These scripts can be used as lightweight wrappers or logic references when building custom radiomics pipelines.
