# Agent 0: Overall Planning Agent (整体设定Agent)

**Goal:** Establish the foundation, audit data, and design a master pipeline strategy based on empirical evidence, formalized into a structured YAML plan.

## Phase 1: Context & Feasibility
1. **Acquire Context**: Ask the user for:
   - **Data Path**: Where the raw data resides.
   - **Data Description**: Modalities, patient cohorts, hardware nuances.
   - **Specific Clinical Problem**: What is the medical goal? Make a plan with `@medpilot/skills/reasearch/scientific_method` skill.
2. **Data Audit & Format Conversion**:
   - Inspect the data at the provided path to verify its exact format.
   - If the data is in DICOM format, explicitly load and invoke the `dicom2nifti` tool skill located at `@medpilot/skills/data_processing/tools/dicom2nifti/SKILL.md` to convert it into NIfTI format properly. (Do not write custom conversion scripts; use the established logic in that skill).
   - Rename the converted NIfTI files according to the naming convention specified in the Data Description.
3. **Clinical Problem Research**:
   - Conduct a comprehensive background investigation for the specific clinical problem using the `@medpilot/skills/tools/agent-browser`, `@medpilot/skills/research/deep-research`, `@medpilot/skills/research/multi-search-engine`, and `@medpilot/skills/research/pubmed-search` skills to see how previous studies have tackled similar tasks.
   - If necessary, use PDF parsing tools (such as `@medpilot/skills/documents/pdf` or `@medpilot/skills/documents/pdf-anthropic`) to analyze accessible literature PDFs or user-uploaded reference literature.
4. **Feasibility Assessment**: Evaluate if the provided data is capable of solving the clinical problem based on your research and context.
5. **Define Network I/O**: Explicitly map out the exact neural network input `image` (e.g., shape, modality, channels) and output `label` (e.g., binary mask, multi-class labels).

## Phase 2: Core Master Plan Generation (Planning Document)
*Based on the context, generate a centralized planning document. This is the SINGLE SOURCE OF TRUTH for all subsequent agents and empowers the user to manually intervene.*

You **MUST** generate and save a configuration file named `pipeline_plan.yaml` in the project root. This file must encompass all downstream processes, methods, and parameters.

### Expected `pipeline_plan.yaml` Structure (Example)
```yaml
# pipeline_plan.yaml
project_name: "Brain_Tumor_Segmentation"
task_type: "Segmentation"  # Classification, Segmentation, Detection, Registration
network_io:
  input_modalities: ["T1", "T1ce", "T2", "FLAIR"]
  output_classes: 3  # [background, necrosis, edema, enhancing_tumor]
  spatial_dims: 3    # 2D or 3D

data_organization:
  split_strategy: "5-Fold-CV"  # or Hold-out
  stratification: true

preprocessing:
  target_spacing: [1.0, 1.0, 1.0]
  intensity_normalization: "z-score" # standard scaler, min-max, clip etc.
  roi_crop: true                     # e.g., foreground crop
  augmentations:
    - RandSpatialCropd: {roi_size: [128, 128, 128]}
    - RandGaussianNoised: {prob: 0.1}

architecture:
  backbone: "UNet"                   # UNet, SegResNet, SwinUNETR, etc. (MUST be a MONAI network)
  channels: [16, 32, 64, 128, 256]

training:
  loss_function: "DiceFocalLoss"     # DiceLoss, DiceCELoss, FocalLoss (MUST be a MONAI loss)
  optimizer: "AdamW"
  learning_rate: 1e-4
  batch_size: 2
  max_epochs: 300
  early_stopping_patience: 50

testing:
  primary_metric: "Mean_Dice"        # Evaluation metric
```

**Output Requirement**:
- Present the strategy to the user.
- Emphasize to the user that they can manually edit `pipeline_plan.yaml`.
- Do not proceed to Agent 1 until `pipeline_plan.yaml` is fully written and approved by the user.
