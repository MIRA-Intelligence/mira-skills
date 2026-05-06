---
name: medical-image-dl-pipeline
description: End-to-end deep learning pipeline for medical image analysis. Make sure to use this skill whenever the user asks to build, train, evaluate, or optimize a deep learning model for medical image data (like MRI, CT, X-ray) or solve a specific medical imaging problem. It covers data organization, preprocessing, architecture design, training, testing, and iterative improvement.
metadata:
  scenarios: ["Training 3D CNNs for tumor segmentation", "Evaluating classification networks on medical scans", "Optimizing deep learning pipelines for clinical images", "Building MONAI-based workflows for medical imaging", "Deep learning for medical image analysis"]
---

# Medical Image Deep Learning Pipeline

This skill guides the construction and iterative improvement of deep learning pipelines for medical imaging problems.

## Workflow & Independent Agents

**The Iterative Cycle**: This pipeline is deeply iterative and centered around a single source of truth: `pipeline_plan.yaml`. Agent 0 generates this plan. Agents 1-3 act strictly according to this plan. Agent 4 reviews the results; if the results fail, Agent 4 MUST immediately overwrite `pipeline_plan.yaml` with better strategies and re-trigger Agents 1-3. The user can also manually edit this file to steer the AI.


When the user asks to solve a medical imaging problem or build a deep learning pipeline, follow these steps by sequentially adopting the persona of the specialized agents below. Read the corresponding agent file for detailed instructions when you reach that step.

### [Agent 0: Overall Planning Agent (整体设定Agent)](agents/agent_0_planning.md)
Establish the foundation of the pipeline, assess feasibility, and explicitly define network inputs and labels.

### [Agent 1: Data Preprocessing Agent (数据预处理Agent)](agents/agent_1_data_preprocessing.md)
Perform robust data splitting and design a MONAI-based preprocessing pipeline tailored to the data characteristics.

### [Agent 2: Architecture Design Agent (模型架构Agent)](agents/agent_2_architecture.md)
Select and define the core learning components parameters.

### [Agent 3: Training & Validation Agent (模型训练Agent)](agents/agent_3_training.md)
Build, execute, and monitor the training loop (handles VRAM, Imbalance, and 5-Fold CV).

### [Agent 4: Testing & Iteration Agent (模型测试和迭代Agent)](agents/agent_4_testing.md)
Analyze real-world capability and trigger feedback loops.

## Coding Guidelines
- **MONAI First Paradigm**: You MUST utilize `MONAI` for ALL stages of the deep learning pipeline. This includes using MONAI for data loading (`monai.data.DataLoader`), dataset caching (`monai.data.CacheDataset`, `PersistentDataset`), preprocessing and augmentations (dictionary-based `*d` transforms in `monai.transforms`), network architectures (`monai.networks.nets`), loss functions (`monai.losses`), evaluation metrics (`monai.metrics`), and inference (`monai.inferers.sliding_window_inference`). Do not write custom raw PyTorch implementations for these components if a MONAI equivalent exists.
- Always ensure reproducible code by setting random seeds.
- Provide clear and modular code structure.

## External Tool Invocation
If raw medical data (like DICOMs) needs conversion or advanced preprocessing before it enters the pipeline, you **MUST** delegate these low-level operations to the specialized tool skills found in `@/skills/data_processing/tools/`. 
For instance, load and read `@/skills/data_processing/tools/dicom2nifti/SKILL.md` when DICOM formatting is required, rather than attempting to write custom parsing scripts from scratch.
