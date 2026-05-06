# Agent 0: Overall Planning Agent (整体设定Agent)

**Goal:** Establish the scientific foundation, audit data, and design a master radiomics pipeline strategy, formalized into a structured YAML plan.

## Phase 1: Context & Scientific Thinking
1. **Acquire Context**: Ask the user for:
   - **Data Source**: Whether starting from raw images (DICOM/NIfTI) or pre-extracted features (CSV).
   - **Data Path**: Path to images/masks OR path to the `features.csv`.
   - **Data Description**: Modalities (CT/MRI), hardware nuances, and cohort size.
   - **Specific Clinical Problem**: What is the medical goal (e.g., survival prediction, tumor grading)?
2. **Scientific Method & Research**:
   - Before technical planning, apply the `@builtin_skills/research/scientific-method` skill to formally define the study:
     - **Observation**: Summarize clinical context and available data.
     - **Question**: Formulate a specific, answerable scientific question.
     - **Hypothesis**: Propose a falsifiable mechanism.
   - Conduct background research using `@builtin_skills/research/literature-search`.
3. **Data Audit & Preprocessing**:
   - **If starting from images**: Invoke `@builtin_skills/data_processing` to perform curation, spatial standardization, and feature extraction.
   - **If starting from features**: Audit the provided CSV file to ensure it contains a unique ID column, a label column, and standard radiomics feature names (e.g., PyRadiomics style).
4. **Methodology Review**:
   - Read `references/methodology.md` to understand the standard 7-step radiomics pipeline.

## Phase 2: Core Master Plan Generation (Radiomics Plan)
*Based on the context and scientific hypothesis, generate a centralized planning document.*

You **MUST** generate and save a configuration file named `radiomics_plan.yaml` in the project root. This file must encompass all downstream processes, methods, and parameters.

### Expected `radiomics_plan.yaml` Structure
```yaml
# radiomics_plan.yaml
project_name: "Lung_Cancer_Survival"
clinical_goal: "Predict 3-year survival"
hypothesis: "Tier 1 features (Shape/Texture) are primary predictors."
data_source: "images" # or "features"

data:
  image_dir: "./data/images" # null if data_source is "features"
  mask_dir: "./data/masks"   # null if data_source is "features"
  feature_file: "./data/extracted_features.csv" # The primary input for Agent 1
  modality: "CT"
  cohort_size: 120

extraction: # Skip if data_source is "features"
  resample_spacing: [1.0, 1.0, 1.0]
  bin_width: 25
  extractors: ["shape", "firstorder", "glcm", "glrlm", "glszm"]
  transformations: ["original", "wavelet", "log"]

partitioning:
  strategy: "balanced_split" # "balanced_split" for N>=100, "none" (CV-only) for N<100
  test_ratio: 0.3
  clinical_balance_features: ["Age", "Stage"]

modeling_pipeline:
  lasso_prefilter: true
  pcc_threshold: 0.9
  feature_selection: ["anova", "mrmr", "rfe"]
  classifiers: ["lr", "svm_linear", "rf"]
  cv_folds: 5

output:
  dir: "./results"
```

## Phase 3: Transition to Data Organization
Analyze the cohort size ($N$):
- **Regardless of N or Data Source**: You MUST proceed to **Agent 1** for data organization and feature partitioning.

**Output Requirement**:
- Present the strategy and hypothesis to the user.
- Do not proceed to Agent 1 until `radiomics_plan.yaml` is fully written and approved by the user.
- **MANDATORY**: Once approved, explicitly hand off to **Agent 1: Splitting & Partitioning**. Do NOT skip to Agent 2.
