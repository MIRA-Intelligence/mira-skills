---
name: radiomics
description: End-to-end radiomics pipeline for feature extraction, selection, and modeling. Use when building radiomic signatures with hierarchical interpretability (Original -> LoG -> Wavelet), performing balanced clinical-feature splitting, or handling small-cohort cross-validation.
metadata:
  scenarios: ["Building radiomics signatures", "Evaluating clinical-radiomic combined models", "Feature extraction and selection pipeline"]
---

# Radiomics Pipeline

A specialized workflow for clinical radiomics, prioritizing model interpretability and statistical rigor.

## Autonomous Orchestration (自主编排逻辑)

When tasked with an end-to-end radiomics analysis, you MUST act as an **Autonomous Lead Scientist**:
1. **Master Scripting**: Construct comprehensive Python scripts using the `scikit-learn` skill to execute the 3-level **Pyramid Feature Selection** strategy automatically.
2. **FAE Efficiency**: Implement computational shortcuts inspired by the FAE framework (e.g., pre-calculated CV folds, lazy slicing) and use **Process-Level Parallelization** (joblib) to accelerate Level 1 sub-model evaluation.
3. **Advanced Interpretability**: For every final model, you MUST generate **SHAP Bar and Beeswarm plots** to provide clinical interpretability beyond simple coefficients.
4. **State Recovery**: Maintain a `results/execution_log.json` to track progress through the pyramid levels, enabling recovery if the process is interrupted.

## Standardized Result Preservation

For EVERY pipeline permutation evaluated, you MUST preserve all outputs in a hierarchical directory structure. Adherence to this format is critical for reproducibility and automated analysis.

- **Detailed Specification**: Refer to **[Result Preservation Guide](references/result_preservation.md)** for the mandatory directory hierarchy, naming conventions, and required artifacts (CSVs, PKLs, and Plots).
- **Directory Hierarchy Overview**: `results/<SubModel>/<Normalization>/<DimReduction>/<Selector>_<K>/<Classifier>/`
- **Mandatory Visualizations**: ROC curves MUST include shaded 95% CI areas (Bootstrap n=1000).

## Reproducibility & Version Control (可重复性与版本控制)

To ensure 100% replication of results and full traceability, you MUST adhere to these mandates:

### 1. Git Management Strategy
Except for raw/processed image data (DICOM/NIfTI), ALL artifacts MUST be managed via Git:
- **Managed Artifacts**: Python scripts, study plans (`radiomics_plan.yaml`), partition indices, performance metrics (`.csv`), and execution logs.
- **Commit Frequency**: Perform a `git commit` after the successful completion of each Agent's stage (e.g., "feat: finish data partitioning in Agent 1").
- **Branching**: Use a new branch for experimental structural changes (e.g., testing a new feature selection algorithm) to keep the `main` branch stable and reproducible.

### 2. Mandatory Random Seed Management
Randomness MUST be eliminated across the entire pipeline:
- **Global Seed**: Initialize `numpy.random.seed(42)` and `random.seed(42)` at the start of every script.
- **Scikit-Learn**: Explicitly set `random_state=42` in ALL relevant components:
  - `StratifiedKFold`
  - `TrainTestSplit`
  - `LogisticRegression`, `RandomForestClassifier`, `SVC`, etc.
  - Feature Selectors (e.g., `LASSO`, `RFE`)
- **Environment**: Document the `requirements.txt` to ensure package version consistency.

## Core Workflow

### Model Selection Principle (模型挑选原则)
When selecting the final model from the pre-experiment or optimization stages, you MUST adhere to the following statistical rigor:
- **CV AUC is the ONLY Criterion**: Always use Cross-Validation (CV) AUC on the training set to rank and select the best pipeline or model. 
- **Test AUC Prohibition**: NEVER use the Test Set performance (Test AUC) to pick or "peek" at models. This prevents data leakage and ensures the Test Set remains an unbiased evaluator of generalization.
- **Reporting Exception**: You MAY inform the user if a different model has a higher Test AUC, but you MUST NOT select it as the final recommendation based on that fact.

The pipeline is a **mandatory 4-step sequence**. Whether starting from raw images or pre-extracted features, the process must follow all steps to ensure scientific rigor and data organization.


### 0. Study Planning & Extraction
**[Agent 0: Planning](agents/agent_0_planning.md)** - Assess data source (DICOM/NIfTI or pre-extracted CSV), execute feature extraction (if starting from images), and design the study architecture. Generates `radiomics_plan.yaml`.

### 1. Data Organization & Partitioning
**[Agent 1: Splitting & Partitioning](agents/agent_1_curation_partitioning.md)** - **Mandatory for all workflows.** Organizes features into hierarchical sub-models (Original -> LoG -> Wavelet) and performs balanced cohort splitting (if sample size allows).

### 2. Feature Selection & Baseline Modeling
**[Agent 2: Modeling](agents/agent_2_modeling.md)** - Refine features per sub-model, build interpretability-focused baseline models, and handle batch effects.

### 3. Optimization & Validation
**[Agent 3: Optimization](agents/agent_3_optimization.md)** - Fine-tune baseline models using two-stage grid search and validate performance on test/external sets.

## Specialized References
- **Methodology**: [FAE Pipeline Methodology](references/methodology.md).
- **Interpretability**: Sub-model hierarchy (Shape -> Firstorder -> Texture).
- **Harmonization**: ComBat and normalization persistence for external sets.
