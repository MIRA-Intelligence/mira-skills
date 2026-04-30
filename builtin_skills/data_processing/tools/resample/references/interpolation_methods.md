# Interpolation Methods in Image Domain Resampling

When resampling medical images in the spatial domain (e.g., CT, PET, or when frequency domain resampling is not applicable), selecting the correct interpolation algorithm is crucial. The choice depends entirely on the nature of the data being resampled.

## 1. Binary Images (Labels, Masks, ROIs)

Binary images or segmentation masks represent discrete categories (e.g., 0 = background, 1 = tumor, 2 = organ). 

### Required Method: Nearest-Neighbor Interpolation
*   **How it works:** When a new pixel is created, it takes the exact value of the closest original pixel.
*   **Why it is mandatory:** Nearest-neighbor is the *only* interpolation method that does not create new, intermediate values. If you use linear interpolation between a background pixel (0) and a tumor pixel (1), you might get a pixel value of 0.5. A value of 0.5 is meaningless in a discrete label map and will break downstream analysis or rendering.
*   **Drawback:** It can create jagged, "stair-step" edges on curves, but preserving the discrete integer values is paramount.

## 2. Continuous Images (CT, PET)

Continuous images represent physical measurements (e.g., Hounsfield Units in CT, standardized uptake values in PET). The goal is to estimate the value at a new coordinate as accurately as possible while maintaining smooth gradients.

### Trilinear Interpolation
*   **How it works:** Estimates the new pixel value using a weighted average of the 8 closest neighboring pixels (in 3D). The weights are proportional to the distance from the new coordinate.
*   **Pros:** Computationally fast; prevents the creation of values outside the original range of the neighbors.
*   **Cons:** Acts as a low-pass filter, slightly smoothing the image. It can blunt sharp edges and reduce high-frequency noise/texture.

### Tricubic (B-Spline) Interpolation
*   **How it works:** Fits a cubic polynomial (or B-spline curve) using a larger neighborhood of pixels (typically 64 in 3D: 4x4x4).
*   **Pros:** Produces smoother, more continuous gradients than trilinear interpolation. It is generally considered more accurate for modeling continuous physical phenomena and preserves edges better.
*   **Cons:** Computationally more expensive. More importantly, cubic interpolation can suffer from **overshoot** (ringing artifacts). Near very sharp transitions (like bone to air in CT), the interpolated value might slightly exceed the maximum or minimum values of the original pixels. 

## Recommendation

*   **Always** use Nearest-Neighbor for any mask, label, or Region of Interest (ROI).
*   For continuous volumetric data (CT, PET) destined for Radiomics or deep learning, **Tricubic (B-Spline) interpolation** is generally preferred due to its superior preservation of gradients and edges, provided that minor ringing artifacts at extreme boundaries are acceptable for the specific task. If strict adherence to the original intensity bounds is required, Trilinear is the safer fallback.