---
name: radiomics
description: End-to-end radiomics pipeline for feature extraction, selection, and modeling. Use when building radiomic signatures with hierarchical interpretability (Original -> LoG -> Wavelet), performing balanced clinical-feature splitting, or handling small-cohort cross-validation.
---

# Radiomics Pipeline

A specialized workflow for clinical radiomics, prioritizing model interpretability and statistical rigor.

## Core Workflow

The pipeline is driven by specialized agents. The process adapts dynamically based on cohort size and data availability.

### 0. Study Planning & Extraction
**[Agent 0: Planning](agents/agent_0_planning.md)** - Assess data source (DICOM/NIfTI/CSV), execute feature extraction via `@skills/data_processing`, and design study architecture.

### 1. Splitting & Partitioning
**[Agent 1: Splitting & Partitioning](agents/agent_1_curation_partitioning.md)** - Perform balanced cohort splitting (clinical features/labels) and organize features into hierarchical sub-models (Original -> LoG -> Wavelet).

### 2. Baseline Modeling & Feature Selection
**[Agent 2: Baseline Modeling](agents/agent_2_modeling.md)** - Refine features per sub-model, eliminate noise, and build interpretability-focused baseline sub-models (LR/SVM/RF). Handle batch effects (ComBat).

### 3. Two-Stage Optimization
**[Agent 3: Optimization](agents/agent_3_optimization.md)** - Fine-tune baseline models using coarse-to-fine two-stage grid search and auto-iteration to maximize performance.

## Specialized References
- **Methodology**: [FAE Pipeline Methodology](references/methodology.md).
- **Interpretability**: Sub-model hierarchy (Shape -> Firstorder -> Texture).
- **Harmonization**: ComBat and normalization persistence for external sets.
