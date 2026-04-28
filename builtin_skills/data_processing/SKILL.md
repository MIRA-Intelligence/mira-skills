---
name: data-processing
description: Orchestrator skill for medical image data processing. Triggers when users ask to curate, format, convert (e.g., DICOM to NIfTI), or extract radiomics features from medical datasets.
metadata:
  aliases: ["dicom conversion", "radiomics extraction", "data preprocessing", "nifti formatting", "medical image curation", "特征提取", "dicom转换", "数据预处理", "nifti格式化", "医学图像整理"]
---

# Medical Image Data Processing

This skill orchestrates medical image data processing tasks. The following operations have no strict sequential order (except feature extraction, which requires curated data). They can be executed concurrently or as independent steps. 

When executing these tasks, you MUST load and delegate to the specialized tool skills provided in the `tools/` directory (e.g., `tools/dicom2nifti/SKILL.md`, `tools/pydicom/SKILL.md`, `tools/nibabel/SKILL.md`, `tools/pyradiomics/SKILL.md`).

## 1. Data Curation (数据整理)

When the user provides a data path, perform the following steps:
- **Scan & Audit**: Recursively scan the data folder to determine the total number of cases and the data modalities present. If the modality is MRI, identify and list the specific sequences available.
- **Reorganize**: Reorganize the required data into a new, cleanly structured target directory based on the user's needs.
- **Format Conversion**: If the raw data is in DICOM format, invoke the `tools/dicom2nifti` skill to convert it to NIfTI.
- **Metadata Extraction**: During the conversion step, extract and save relevant metadata (e.g., modality, sequence, acquisition parameters, window level, window center, orientation, e.g.) into a JSON file for each case. This metadata will be crucial for downstream processing and analysis.
- **MRI Preprocessing**: Consider performing N4 bias field correction on MRI data during the conversion step to improve image quality for downstream tasks.
- **Naming Conventions**:
  - Single Modality: Name the converted file `image.nii.gz`.
  - Multi-Modality: Name the files by their modality or sequence (e.g., `t1.nii.gz`, `t2.nii.gz`, `flair.nii.gz`).
  - eg. For a patient with T1 and T2 MRI sequences, the folder structure would be:
    ```
    patient_001/
      t1.nii.gz
      t2.nii.gz
    ```
- **Task-Specific Label Handling**:
  - **Segmentation**: Store the image and its corresponding label mask in the same folder, named according to the patient or image ID.
  - **Classification**: Save all case IDs and their corresponding class labels into a unified JSON file.
  - **Other Tasks**: Do not save labels by default; you may ask the user for clarification on how they want the targets organized.

## 2. Anonymization & Spatial Statistics (匿名化与图像方位统计)

During the data curation process, you must pay attention to data privacy and spatial consistency:
- **Anonymization**: Ensure Protected Health Information (PHI) is handled appropriately.
- **Metadata Gathering**: Read the images (invoking the `tools/pydicom` skill for DICOMs or the `tools/nibabel` skill for NIfTIs) to extract spatial metadata.
- **Statistical Summary**: Extract and compile the `orientation`, `shape`, and `spacing` across all cases in the dataset. Save this aggregated summary into a JSON file for easy review.

## 3. Radiomics Feature Extraction (特征提取)

Data MUST be fully curated and spatially standardized before feature extraction begins.
- **Tool Delegation**: Invoke the `tools/pyradiomics` skill to perform the actual extraction.
- **Mandatory Preprocessing**: You MUST perform image preprocessing (such as MinMax scaling or Z-score normalization) before extracting features. Choose the appropriate method based on the imaging modality and user requirements.
- **CT Specifics (CT 窗宽窗位)**: CT values (Hounsfield Units) have absolute physical meaning. Before applying any normalization to CT data, you must first apply a unified Window Width and Window Level (窗宽窗位) clipping across all data.
- **ROI-Specific Normalization**: For segmentations/masks with highly specific or unusual shapes, consider performing intensity normalization *only within the Region of Interest (ROI)* rather than globally across the entire image volume.

## 4. Spatial Validation (空间一致性校验)

When curating data for radiomics, image-mask pairs must be spatially consistent:

```python
import os
import json
import glob
import SimpleITK as sitk
from pathlib import Path

def validate_and_index(image_dir, mask_dir, output_json="dataset.json"):
    image_files = sorted(glob.glob(os.path.join(image_dir, "*")))
    mask_files = {Path(m).stem: m for m in glob.glob(os.path.join(mask_dir, "*"))}

    dataset = []
    mismatches = []

    for img_path in image_files:
        stem = Path(img_path).stem
        mask_path = mask_files.get(stem)
        if not mask_path:
            mismatches.append(f"No mask for {stem}")
            continue

        img = sitk.ReadImage(img_path)
        msk = sitk.ReadImage(mask_path)

        if img.GetOrigin() != msk.GetOrigin():
            mismatches.append(f"{stem}: Origin mismatch")
        if img.GetSpacing() != msk.GetSpacing():
            mismatches.append(f"{stem}: Spacing mismatch")
        if img.GetDirection() != msk.GetDirection():
            mismatches.append(f"{stem}: Direction mismatch")
        if img.GetSize() != msk.GetSize():
            mismatches.append(f"{stem}: Size mismatch")

        dataset.append({
            "image": os.path.abspath(img_path),
            "mask": os.path.abspath(mask_path),
            "label": stem
        })

    with open(output_json, "w") as f:
        json.dump(dataset, f, indent=2)

    if mismatches:
        print(f"WARNING: {len(mismatches)} mismatches found:")
        for m in mismatches:
            print(f"  - {m}")

    return dataset, mismatches
```

## 5. PyRadiomics Configuration (PyRadiomics参数配置)

Generate a `pyradiomics_params.yaml` with explicit filter settings for reproducibility:

```yaml
extraction:
  resample_spacing: [1, 1, 1]
  bin_width: 25
  dimensionality: 3

  imageType:
    Original: {}
    LoG:
      sigma: [1.0, 2.0, 3.0]
    LoG+Wavelet:
      sigma: [1.0, 2.0]
    Wavelet: {}

  featureClass:
    shape: true
    firstorder: true
    glcm: true
    glrlm: true
    glszm: true
    glnm: true
    ngtdm: true
    gldm: true
```

### Modality-Specific Parameters

| Modality | Recommended `bin_width` | Recommended `resample_spacing` |
|----------|------------------------|-------------------------------|
| CT | 25 HU | [1, 1, 1] mm |
| T1-MRI | 5 or dynamic | [1.5, 1.5, 1.5] mm (isotropic) |
| T2-MRI | 5 or dynamic | [1.5, 1.5, 1.5] mm (isotropic) |
| PET | 50–60 SUV | Depends on acquisition, usually [2, 2, 2] mm |

> For MRI, consider using `bin_width: auto` (dynamic) since signal intensity is not standardized across scanners.

### 2D vs 3D Extraction

The choice depends primarily on **inter-slice resolution** (层间分辨率) and **mask coverage**:

- **3D extraction** (default): Use when the image is **isotropic** (层内分辨率 ≈ 层间分辨率, e.g., spacing `[1, 1, 1]`). Enables shape, first-order, and 3D texture features (GLCM, GLRLM, NGTDM, SGLDM) across all voxels.
- **2D extraction**: Use when the **inter-slice spacing is significantly larger** than in-plane spacing (e.g., spacing `[0.5, 0.5, 5]`). Set `dimensionality: 2`. Also use 2D when the **mask has only one slice** or **all masks have the same number of slices** (slice-level ROI). Note: 3D texture features (NGTDM, SGLDM) will be unavailable.

## 6. Batch Extraction (批量提取)

For batch processing over cohorts, you SHOULD delegate to the high-performance scripts provided in the `tools/pyradiomics` skill. These scripts handle logging, error recovery, and data consolidation automatically.

### Option A: Basic Batch Extraction
Use `tools/pyradiomics/scripts/batch_extract.py` when images and masks are stored in two matching directories.

```bash
python tools/pyradiomics/scripts/batch_extract.py \
  --image_dir ./data/images \
  --mask_dir ./data/masks \
  --out_csv features.csv \
  --params pyradiomics_params.yaml
```

### Option B: Advanced Extraction (Preprocessing)
Use `tools/pyradiomics/scripts/advanced_extract.py` when data is organized in patient-specific folders or requires advanced preprocessing (N4 correction, CLAHE).

```bash
python tools/pyradiomics/scripts/advanced_extract.py \
  --root_dir ./data/patients \
  --img_key "T1" \
  --msk_key "mask" \
  --out_csv features_advanced.csv \
  --params pyradiomics_params.yaml \
  --n4 --clahe
```

### Common Extraction Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `Empty label` | Mask has no voxels in ROI | Remove sample or check segmentation threshold |
| `Dimension mismatch` | Image/mask spacing differ | Re-resample mask in curation step |
| `NaN in firstorder` | All voxel values are zero/NaN | Check DICOM windowing or HU rescaling |