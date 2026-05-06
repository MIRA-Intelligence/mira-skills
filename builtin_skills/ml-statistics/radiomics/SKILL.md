---
name: radiomics
description: End-to-end radiomics pipeline for feature extraction, selection, and modeling. Use when building radiomic signatures with hierarchical interpretability (Original -> LoG -> Wavelet), performing balanced clinical-feature splitting, or handling small-cohort cross-validation.
metadata:
  scenarios: ["Building radiomics signatures", "Evaluating clinical-radiomic combined models", "Feature extraction and selection pipeline"]
---

# Radiomics Pipeline

A specialized workflow for clinical radiomics, prioritizing model interpretability and statistical rigor.

## Core Workflow

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
