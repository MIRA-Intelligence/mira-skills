# Configuration and Parameter Tuning

pyradiomics behaviour is highly customizable. The best practice for keeping experiments reproducible is storing extraction parameters in a YAML configuration file.

## Essential Settings

### 1. Discretization (`binWidth` vs `binCount`)
Before computing texture matrices (GLCM, GLRLM, etc.), image intensities must be discretized.
*   **`binWidth`** (Recommended): Specifies the width of the bins. This ensures that the relationship between pixel intensities and actual physical/biological meaning remains consistent (critical for CT scans in Hounsfield Units, HU).
    *   *CT Example*: `binWidth: 25` (Standard for CT radiomics).
*   **`binCount`**: Specifies a fixed number of bins. Often preferred for MRI, where absolute intensity values are not strictly standardized.

### 2. Resampling (`resampledPixelSpacing`)
Medical images vary in voxel spacing. Resampling ensures that texture features are comparable across different scans.
*   **`resampledPixelSpacing: [1, 1, 1]`**: Resamples the image and mask to isotropic 1x1x1 mm resolution.
*   **`interpolator`**: Determines how voxel values are interpolated.
    *   Images: `sitkBSpline` (default)
    *   Masks: Always forced to `sitkNearestNeighbor` by pyradiomics internally to preserve categorical label values.

### 3. Normalization (Primarily for MRI)
Because MRI intensities are relative, normalization is highly recommended.
*   **`normalize: true`**
*   **`normalizeScale: 100`**: Scales the normalized values.

## Modality-Specific Recommendations

### CT (Computed Tomography)
*   Use `binWidth` (usually 25).
*   Do **NOT** use normalization.

### MRI (Magnetic Resonance Imaging)
*   Use Normalization.
*   Consider using `binCount` or strict Z-score normalization followed by `binWidth`.

## Example YAML Configurations
```yaml
# This is an example of a parameters file
# It is written according to the YAML-convention (www.yaml.org) and is checked by the code for consistency.
# Three types of parameters are possible and reflected in the structure of the document:
#
# Parameter category:
#   Setting Name: <value>
#
# The three parameter categories are:
# - setting: Setting to use for preprocessing and class specific settings. if no <value> is specified, the value for
#   this setting is set to None.
# - featureClass: Feature class to enable, <value> is list of strings representing enabled features. If no <value> is
#   specified or <value> is an empty list ('[]'), all features for this class are enabled.
# - imageType: image types to calculate features on. <value> is custom kwarg settings (dictionary). if <value> is an
#   empty dictionary ('{}'), no custom settings are added for this input image.
#
# Some parameters have a limited list of possible values. Where this is the case, possible values are listed in the
# package documentation

# Settings to use, possible settings are listed in the documentation (section "Customizing the extraction").
setting:
  # binWidth: 0.1
  binCount: 20
  label: 1
  interpolator: 'sitkBSpline' # This is an enumerated value, here None is not allowed
  resampledPixelSpacing: # This disables resampling, as it is interpreted as None, to enable it, specify spacing in x, y, z as [x, y , z]
  weightingNorm: # If no value is specified, it is interpreted as None
  geometryTolerance: 0.01
  normalize: False
  force2D: True
  # force2Ddimension: 0


# Image types to use: "Original" for unfiltered image, for possible filters, see documentation.
imageType:
  Original: {}
  LoG:
    sigma: [1.0, 3.0, 5.0]
  Wavelet: {}
  
# Featureclasses, from which features must be calculated. If a featureclass is not mentioned, no features are calculated
# for that class. Otherwise, the specified features are calculated, or, if none are specified, all are calculated.
featureClass:
  shape:   # disable redundant Compactness 1 and Compactness 2 features by specifying all other shape features
  firstorder: 
  glcm:
  glrlm: # for lists none values are allowed, in this case, all features are enabled
  glszm:
  ngtdm:
  gldm:

```
