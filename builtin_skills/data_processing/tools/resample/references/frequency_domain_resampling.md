# Frequency Domain Resampling for MR Images

When preparing Magnetic Resonance (MR) images for quantitative analysis (such as Radiomics), preserving the original texture and high-frequency details is critical. Standard image domain interpolation methods (like linear or cubic) calculate new pixel values based on weighted averages of neighboring pixels. This process acts as a low-pass filter, inherently smoothing the image and potentially blurring fine textural features.

## Why Resample in the Frequency Domain?

MR images are fundamentally acquired in the spatial frequency domain, known as **K-space**. The mathematical relationship between K-space and the final image domain is a Fourier Transform. Because of this direct relationship, we can perform spatial operations, like changing the image resolution (matrix size), entirely within the frequency domain.

### Zero-Padding (Increasing Resolution)

To increase the spatial resolution (i.e., decrease the pixel spacing while keeping the physical field of view constant), we must increase the matrix size of the image. 

In the frequency domain, this is achieved by **Zero-Padding**:
1. Apply a 2D or 3D Fast Fourier Transform (FFT) to the image to move it into the frequency domain.
2. Place the original frequency data in the center of a larger, empty (zero-filled) matrix. The original data represents the low and mid frequencies.
3. The newly added zeros represent high frequencies that were not acquired.
4. Apply the Inverse Fast Fourier Transform (IFFT).

**Result:** The resulting image in the spatial domain has a larger matrix size and smaller pixel spacing. Because we only added zeros (no new information) and did not alter the acquired frequencies, the original contrast and texture are perfectly preserved without the smoothing artifacts caused by spatial interpolation.

### Cropping (Decreasing Resolution)

To decrease the spatial resolution (i.e., increase the pixel spacing), we must reduce the matrix size.

In the frequency domain, this is achieved by **Cropping**:
1. Apply the FFT to move the image into the frequency domain.
2. Crop the outer edges of the frequency matrix, retaining only the central region. The central region contains the low frequencies (general contrast and shape).
3. The cropped outer edges represent the highest spatial frequencies (fine details and noise).
4. Apply the IFFT to the smaller, central matrix.

**Result:** The resulting image has a smaller matrix size. While high-frequency details are lost (which is inevitable when reducing resolution), this method mathematically avoids aliasing (Moire patterns) that can occur if spatial domain downsampling is performed without proper pre-filtering.

## Summary

Resampling MR images via Fourier Transform (zero-padding or cropping in K-space) is mathematically elegant and preserves the integrity of the acquired signal better than spatial interpolation. It is the preferred method for standardizing MR image resolution prior to sensitive feature extraction tasks.