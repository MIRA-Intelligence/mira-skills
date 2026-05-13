# Agent 1: Data Organization & Partitioning (数据组织与子模型划分)

**Goal:** This agent is **MANDATORY** for all workflows. It organizes raw/extracted features into hierarchical sub-models for interpretability and performs balanced cohort splitting if the sample size is sufficient.

## 1. Hierarchical Sub-model Partitioning (Mandatory)
Organize the `features.csv` (or the `feature_file` defined in Agent 0) into sub-models to prioritize interpretability. This must be done regardless of sample size to prepare the data for Agent 2.

### Tier 1: Interpretability First (Simple Features)
Separate features from **Original** images:
- `df_original_shape`: Geometric properties.
- `df_original_firstorder`: Basic intensity stats.
- `df_original_texture`: GLCM, GLRLM, GLSZM, NGTDM, GLDM.

### Tier 2: Advanced Complexity (Filtered Features)
Partition features from **Transformed** images (only if Tier 1 is insufficient):
- **LoG Partitioning**: Group by sigma values (e.g., `df_log_sigma_1_0`, `df_log_sigma_3_0`).
- **Wavelet Partitioning**: Group by sub-bands (e.g., `df_wavelet_LLL`, `df_wavelet_HHH`).

## 2. Balanced Cohort Splitting (Conditional)
Perform this step ONLY if $N \geq 100$.
- **Identify Basis**: Ask for clinical features (Age, Stage, etc.) or Labels.
- **Algorithm**: Repeated random splitting (e.g., 7:3) until the distribution of **ALL** clinical features and the Label shows no significant difference between Train and Test sets ($p > 0.05$, ideally $p > 0.10$). 
- **Tool Execution**: 
  ```bash
  python builtin_skills/ml-statistics/radiomics/scripts/cohort_split.py \
      --input <path_to_features.csv> \
      --clinical <path_to_clinical.csv> \
      --output_dir <output_directory> \
      --ratio 0.3 \
      --label <label_column_name>
  ```
- **Small Dataset Scenario**: If $N < 100$, do NOT perform splitting. Proceed with the full dataset and the hierarchical partitions created in Step 1. Agent 2 will use cross-validation on this unified dataset.

## 3. Modality Partitioning
If multiple modalities exist (e.g., T1, T2, CT), create modality-specific feature sets before merging.

## Deliverables
- **Partitioned Feature Matrices**: (e.g., `X_train_original.csv`, `X_train_wavelet_LLL.csv`). These serve as the discrete data inputs for the **Exhaustive Permutation Grid** in Agent 2.
- `train_cohort.csv` / `test_cohort.csv` (if splitting was performed).
- **Final Data Readiness Report**: A summary of available sub-models and sample sizes per cohort for **Agent 2: Feature Selection & Modeling**.

**Handoff**: Once partitioning (and optional splitting) is complete, proceed to **Agent 2**. You MUST use the partitioned matrices to evaluate every sub-model independently and in combination as part of the pre-experiment sweep.
