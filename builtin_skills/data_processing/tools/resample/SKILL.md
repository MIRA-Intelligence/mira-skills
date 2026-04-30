---
name: resample
description: Unify spatial resolution of medical images prior to feature extraction using optimal domain operations (Image vs. Frequency).
---

# Resample Skill

Provides an optimal methodology for uniform spatial resampling across heterogeneous medical imaging datasets before quantitative feature extraction (e.g., Radiomics).

## Best Practices
1. **Adaptive Target Spacing**: Always survey the dataset to select a target spacing that covers the majority of the distribution, minimizing unnecessary interpolation artifacts.
2. **Tolerance Thresholds**: Skip resampling if the image spacing matches the target spacing within a tight tolerance (e.g., `0.05 mm` margin like `0.6` vs `0.61`).
3. **Thick-Slice Handling**: If the image is anisotropic with a significantly thick slice dimension (e.g. `z > 1.5 * max(x, y)`), limit resampling to the in-plane axes (`x, y`) only, leaving the slice thickness alone.
4. **Modality-Specific Strategy**:
   - **MR Continuous Images**: Resample using zero-padding or cropping in the Frequency Domain (K-space) to avoid smoothing out high-frequency features in standard interpolation.
   - **CT/PET Continuous Images**: Resample in the Image Domain using Tricubic (B-Spline) interpolation.
   - **Binary Images (Labels/Masks)**: Resample in the Image Domain exclusively using Nearest-Neighbor interpolation, regardless of the underlying modality.

## Scripts Provided

- `scripts/resample.py`: Python CLI tool for batch processing and uniforming the resolution across medical imaging datasets based on the best practices mentioned above.

## Usage
Run the script over a directory containing structured patient cases:

```bash
python builtin_skills/data_processing/resample/scripts/resample.py \
    --input_dir /path/to/raw \
    --output_dir /path/to/resampled \
    --modality MR \
    --image_key image \
    --label_key label
```
