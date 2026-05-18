# Implementation Quality & Compliance Check

To ensure scientific rigor and adherence to the Radiomics Pipeline standards, every script and execution MUST pass the following checks. Failure to comply with these rules results in an invalid scientific study.

## 1. Statistical Rigor (Hard Requirements)

- **Bootstrap Resampling**: ALL ROC curves MUST be generated using **n=1000 Bootstrap samples**. A single-run ROC curve is unacceptable.
- **Random State Integrity**: `random_state=42` MUST be hardcoded into every stochastic component (Splitters, Selectors, Classifiers).
- **Metric Precision**: Every numerical result reported to the user or saved in CSVs MUST be formatted to **3 decimal places** (e.g., `0.852`).

## 2. Anti-Leakage & Selection (Zero Tolerance)

- **The "No Peeking" Rule**: You MUST NOT use the Test Set performance (Test AUC) to:
  - Rank pipelines.
  - Select features.
  - Tune hyperparameters.
- **Selection Criterion**: Only **Cross-Validation (CV) AUC** on the training set is a valid criterion for model selection.
- **Parameter Migration**: Preprocessing parameters (Mean, Std, Min, Max) MUST be fitted on the **Training Set only** and then applied to the Test Set.

## 3. Structural Compliance

- **Directory Nesting**: Artifacts MUST be stored in the exact hierarchy defined in `result_preservation.md`. Do not flatten the directory structure.
- **Mandatory Plots**: EVERY pipeline evaluation directory MUST contain:
  - `roc_combined.png` (Train, CV, and Test with shaded 95% CI).
  - `feature_importance.png` (Sorted horizontal bar chart).
  - `one_se_selection.png` (CV AUC vs. K with error bars and 1-SE thresholds).
- **Final Model Only**:
  - `SHAP_Global.png` and `SHAP_Local.png`.

## 4. Code Execution Standard

- **Process-Level Parallelization**: Use `joblib` for Level 1 atomic evaluations. Sequential loops for dozens of sub-models are prohibited.
- **Data Encapsulation**: Use a `DataContainer` or similar class to manage feature names and cohort indices, preventing index mismatch errors.

**Warning**: If your implementation skips these steps, you are instructed to immediately stop, admit the non-compliance, and rewrite the logic to meet these standards.
