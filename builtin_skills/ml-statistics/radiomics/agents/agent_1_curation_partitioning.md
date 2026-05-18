# Agent 1: Data Organization & Partitioning (数据组织与子模型划分)

**Goal:** This agent is **MANDATORY** for all workflows. It organizes raw/extracted features into hierarchical sub-models for interpretability and performs balanced cohort splitting if the sample size is sufficient.

## 1. Feature-Count Diagnosis (特征数诊断)
Before performing any partitioning, check the total number of features in the dataset.
- **Heuristic**: If the total number of features is **less than 300**, you MUST inform the user and suggest skipping the hierarchical sub-model partitioning to save computation time. Ask: *"特征总数较少（<300），建议跳过复杂的子模型划分，直接进行全量建模以加速实验。是否继续进行子模型拆分？"*
- **Wait for Decision**: Proceed with partitioning only if the user insists or if features >= 300.

## 2. Hierarchical Atomic Partitioning (金字塔底层原子拆分)
To support the **Pyramid Feature Selection** strategy, organize the features into the most granular "Atomic Groups".

### Atomic Tier: Granular Sub-groups
Separate features from **Original** and **Transformed** images into their specific types:
- **Shape**: `df_shape`
- **Firstorder**: `df_firstorder`
- **Texture Atomic Groups**: Separate by matrix type: `df_glcm`, `df_glrlm`, `df_glszm`, `df_ngtdm`, `df_gldm`.
*Note*: If transformed images (LoG/Wavelet) are used, keep their groups separate at this atomic level (e.g., `df_log_sigma_1_0_glcm`).

## 3. Balanced Cohort Splitting (Conditional)
Perform this step ONLY if $N \geq 100$.

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

## 4. Modality Partitioning
If multiple modalities exist (e.g., T1, T2, CT), create modality-specific feature sets before merging.

## Deliverables
- **Partitioned Feature Matrices**: (e.g., `X_train_original.csv`, `X_train_wavelet_LLL.csv`). These serve as the discrete data inputs for the **Exhaustive Permutation Grid** in Agent 2.
- `train_cohort.csv` / `test_cohort.csv` (if splitting was performed).
- **Final Data Readiness Report**: A summary of available sub-models and sample sizes per cohort for **Agent 2: Feature Selection & Modeling**.

**Handoff**: Once partitioning (and optional splitting) is complete, proceed to **Agent 2**. You MUST use the partitioned matrices to evaluate every sub-model independently and in combination as part of the pre-experiment sweep.
