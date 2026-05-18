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
- **Directory Hierarchy Overview**: `results/<SubModel>/<Normalization>/PCC_0.99/<Selector>_<K>/<Classifier>/`
- **Mandatory Visualizations**: ROC curves MUST include shaded 95% CI areas (Bootstrap n=1000) for Train, CV, and Test.

## Reproducibility & Version Control (可重复性与版本控制)

To ensure 100% replication of results and full traceability, you MUST adhere to these mandates:

### 1. Git Management Strategy
Except for raw/processed image data (DICOM/NIfTI), ALL artifacts MUST be managed via Git:
- **Managed Artifacts**: Python scripts, study plans (`radiomics_plan.yaml`), partition indices, performance metrics (`.csv`), and execution logs.
- **Commit Frequency**: Perform a `git commit` after the successful completion of each Agent's stage (e.g., "feat: finish data partitioning in Agent 1").

### 2. Mandatory Random Seed Management
Randomness MUST be eliminated across the entire pipeline:
- **Global Seed**: Initialize `numpy.random.seed(42)` and `random.seed(42)` at the start of every script.
- **Scikit-Learn**: Explicitly set `random_state=42` in ALL relevant components (Splitters, Selectors, Classifiers).

## Core Workflow

### Model Selection Principle (模型挑选原则)
When selecting the final model, you MUST adhere to the following scientific mindset:
- **Performance & Interpretability**: Prioritize models that combine high CV AUC with clinical transparency. Favor linear models and fewer features.
- **Optional 1-SE Rule**: The 1-SE rule is a tool for finding the simplest robust model, but its application is **optional** and should be balanced against potential performance loss or CV-related overfitting.
- **Test Set Protection**: NEVER use the Test Set performance to select or tune models. The Test Set is for final evaluation only.

The pipeline is a **mandatory 4-step sequence**:

### 0. Study Planning & Extraction
**[Agent 0: Planning](agents/agent_0_planning.md)** - Assess data source, design study architecture, and define the scientific hypothesis. Generates `radiomics_plan.yaml`.

### 1. Data Organization & Partitioning
**[Agent 1: Splitting & Partitioning](agents/agent_1_curation_partitioning.md)** - Organizes features into sub-models and performs balanced cohort splitting.

### 2. Baseline Modeling Grid
**[Agent 2: Modeling](agents/agent_2_modeling.md)** - Execute an exhaustive grid search using interpretable models (LR, SVM), standardized normalization (Z-score, Minmax), and PCC (0.99). Saves results for EVERY permutation.

### 3. Hyperparameter Optimization
**[Agent 3: Optimization](agents/agent_3_optimization.md)** - Perform fine-tuning of top baseline configurations to maximize stability and performance. **Exhaustive Result Preservation**: All tuning results and plots are saved in the hierarchical results folder.

### 4. Final Model Selection
**[Agent 4: Selection](agents/agent_4_selection.md)** - Ingest all evidence (Baseline, 1-SE, Optimized) to select the final clinical signature based on parsimony and interpretability. **Authoritative Guidance**: Agents 3 and 4 provide the definitive scientific recommendations for any final model choice or manual refinement by the user.

## Specialized References
- **Methodology**: [FAE Pipeline Methodology](references/methodology.md).
- **Implementation Standards**: [Implementation Quality Check](references/implementation_check.md).
- **Interpretability**: Sub-model hierarchy (Shape -> Firstorder -> Texture).
- **Harmonization**: ComBat and normalization persistence for external sets.

---

## Compliance Checklist (执行自查清单)
At the end of every response, you MUST verify your compliance:
- [ ] **Current State**: (Agent 0/1/2/3/4)
- [ ] **Random Seed**: 42 applied globally and in all SKLearn components.
- [ ] **Selection Criterion**: CV AUC + 1-SE Rule (decided in Agent 4).
- [ ] **Bootstrap**: ROC plots include 95% CI (n=1000) for Train, CV, and Test.
- [ ] **Full Matrix**: Results and plots saved for EVERY pipeline permutation.
- [ ] **Structure**: Hierarchical results folder per `result_preservation.md`.
- [ ] **Precision**: All reported metrics are formatted to 3 decimal places.
