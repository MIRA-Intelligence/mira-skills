# Agent 0: Overall Planning Agent (整体设定Agent)

**Goal:** Establish the scientific foundation, audit data, and design a master radiomics pipeline strategy, formalized into a structured YAML plan.

## Phase 1: Context & Scientific Thinking
1. **Acquire Context**: Ask the user for:
   - **Data Path**: Where the images and masks reside.
   - **Data Description**: Modalities (CT/MRI), patient cohorts, hardware nuances.
   - **Specific Clinical Problem**: What is the medical goal (e.g., survival prediction, tumor grading)?
2. **Scientific Method & Research**:
   - Before technical planning, apply the `@builtin_skills/research/scientific-method` skill to formally define the study:
     - **Observation**: Summarize clinical context and available data.
     - **Question**: Formulate a specific, answerable scientific question.
     - **Hypothesis**: Propose a falsifiable mechanism (e.g., "Texture features in the peritumoral region correlate with lymph node metastasis").
   - Conduct background research using `@builtin_skills/research/literature-search` to see how previous studies have tackled this specific clinical problem and what feature sets were most predictive.
3. **Data Audit & Preprocessing**:
   - Invoke `@builtin_skills/data_processing` to perform data curation, spatial standardization (resampling), and radiomics feature extraction.
4. **Methodology Review**:
   - Before generating the technical master plan, read `references/methodology.md` to understand the standard 7-step radiomics pipeline (based on FAE). Incorporate principles like balanced cohort splitting, parameter migration for normalization, PCC dimension reduction, and rigorous feature selection into the pipeline design.

## Phase 2: Core Master Plan Generation (Radiomics Plan)
*Based on the context and scientific hypothesis, generate a centralized planning document. This is the SINGLE SOURCE OF TRUTH for all subsequent agents.*

You **MUST** generate and save a configuration file named `radiomics_plan.yaml` in the project root. This file must encompass all downstream processes, methods, and parameters.

### Expected `radiomics_plan.yaml` Structure
```yaml
# radiomics_plan.yaml
project_name: "Lung_Cancer_Survival"
clinical_goal: "Predict 3-year survival"
hypothesis: "Tier 1 features (Shape/Texture) are primary predictors."

data:
  image_dir: "./data/images"
  mask_dir: "./data/masks"
  modality: "CT"
  cohort_size: 120

extraction:
  resample_spacing: [1.0, 1.0, 1.0]
  bin_width: 25
  extractors: ["shape", "firstorder", "glcm", "glrlm", "glszm"]
  transformations: ["original", "wavelet", "log"] # Hierarchy: Original -> Transformed

partitioning:
  strategy: "balanced_split" # "balanced_split" for N>=100, "5-fold-cv" for N<100
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

## Phase 3: Strategy Branching & Sample Power
Analyze the cohort size ($N$):
- **Small Cohort ($N < 100$)**: Explicitly set `partitioning.strategy: "5-fold-cv"` in the YAML. Skip independent split.
- **Large Cohort ($N \geq 100$)**: Explicitly set `partitioning.strategy: "balanced_split"`.

## Constraints & Optimization
- **Max Features**: $N_{train} / 10$.
- **Boundary Optimization**: If peak performance is at $MaxFeatures$, try $MaxFeatures + 1, 2$.

**Output Requirement**:
- Present the strategy and hypothesis to the user.
- Emphasize to the user that they can manually edit `radiomics_plan.yaml`.
- Do not proceed to Agent 1 until `radiomics_plan.yaml` is fully written and approved by the user.
