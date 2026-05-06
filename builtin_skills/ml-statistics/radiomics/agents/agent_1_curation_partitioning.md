# Agent 1: Splitting & Partitioning (队列拆分与子模型划分)

**Goal:** Perform balanced cohort splitting and organize features into hierarchical sub-models for interpretability.

## 1. Balanced Cohort Splitting
Perform this step if $N \geq 100$.
- **Identify Basis**: Ask for clinical features (Age, Stage, etc.) or Labels.
- **Algorithm**: Repeated random splitting (e.g., 7:3) until the distribution of **ALL** clinical features and the Label shows no significant difference between Train and Test sets ($p > 0.05$, ideally $p > 0.10$). 
- **Tool Execution**: You MUST execute the provided script using the `run_shell_command` tool to perform this splitting:
  ```bash
  python builtin_skills/ml-statistics/radiomics/scripts/cohort_split.py \
      --input <path_to_features.csv> \
      --clinical <path_to_clinical.csv> \
      --output_dir <output_directory> \
      --ratio 0.3 \
      --label <label_column_name>
  ```
  **`Random Seed` should be set to ensure that the results are reductive.**
- **Small Dataset Exception**: If $N < 100$, skip splitting. Use the full dataset for 5-fold cross-validation in Agent 2.

## 2. Hierarchical Sub-model Partitioning
Organize the extracted `features.csv` into sub-models to prioritize interpretability:

### Tier 1: Interpretability First (Simple Features)
Separate features from **Original** images:
- `df_original_shape`: Geometric properties.
- `df_original_firstorder`: Basic intensity stats.
- `df_original_texture`: GLCM, GLRLM, GLSZM, NGTDM, GLDM.

### Tier 2: Advanced Complexity (Filtered Features)
Partition features from **Transformed** images (only if Tier 1 is insufficient):
- **LoG Partitioning**: Group by sigma values (e.g., `df_log_sigma_1_0`, `df_log_sigma_3_0`).
- **Wavelet Partitioning**: Group by sub-bands (e.g., `df_wavelet_LLL`, `df_wavelet_HHH`).

## 3. Modality Partitioning
If multiple modalities exist (e.g., T1, T2, CT), create modality-specific feature sets before merging.

## Deliverables
- `train_cohort.csv` / `test_cohort.csv`.
- Partitioned feature matrices (e.g., `X_train_original.csv`, `X_train_wavelet.csv`).
