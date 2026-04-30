import os
import shutil
import argparse
from pathlib import Path
from typing import Sequence, Union
import numpy as np
import pandas as pd
import SimpleITK as sitk
from scipy.fft import fft2, ifft2
from tqdm import tqdm

def check_image_spacings(root: Union[str, Path], image_key: str = 'image'):
    """Analyze image spacings across the dataset to determine the optimal target spacing."""
    infos = {'spacing': [], 'fixed_path': [], 'shape': [], 'count': []}
    
    root_path = Path(root)
    for case in tqdm(root_path.iterdir(), desc='Checking Spacing'):
        if case.is_dir():
            for i in case.iterdir():
                if image_key in i.stem and not i.name.startswith('._'):
                    img = sitk.ReadImage(str(i))
                    spacing = img.GetSpacing()
                    spacing = tuple(round(v, 2) for v in spacing)
                    shape = img.GetSize()
                    
                    if spacing in infos['spacing']:
                        idx = infos['spacing'].index(spacing)
                        infos['count'][idx] += 1
                    else:
                        infos['spacing'].append(spacing)
                        infos['fixed_path'].append(str(i))
                        infos['shape'].append(shape)
                        infos['count'].append(1)
                        
    if not infos['spacing']:
        return None, None
        
    df = pd.DataFrame(infos)
    print("Found Spacings:\n", df[['spacing', 'count']])
    
    # Choose spacing that appears most frequently (mode) to minimize resampling
    most_frequent_idx = df['count'].idxmax()
    target_spacing = df.loc[most_frequent_idx, 'spacing']
    print(f"Optimal target spacing selected to minimize resampling operations: {target_spacing}")
    return infos, target_spacing

def process_frequency_domain(slice_data, target_size):
    """Frequency domain resampling (cropping/padding in K-space) for a single 2D slice."""
    h, w = slice_data.shape
    target_h, target_w = target_size
    
    f_transform = np.fft.fftshift(np.fft.fft2(slice_data))
    result_f = np.zeros(target_size, dtype=complex)
    
    # Height processing
    if h > target_h:
        h_start_src = (h - target_h) // 2
        h_slice_src = slice(h_start_src, h_start_src + target_h)
        h_start_dst = 0
        h_slice_dst = slice(0, target_h)
    else:
        h_slice_src = slice(None)
        h_start_dst = (target_h - h) // 2
        h_slice_dst = slice(h_start_dst, h_start_dst + h)
        
    # Width processing
    if w > target_w:
        w_start_src = (w - target_w) // 2
        w_slice_src = slice(w_start_src, w_start_src + target_w)
        w_start_dst = 0
        w_slice_dst = slice(0, target_w)
    else:
        w_slice_src = slice(None)
        w_start_dst = (target_w - w) // 2
        w_slice_dst = slice(w_start_dst, w_start_dst + w)
        
    result_f[h_slice_dst, w_slice_dst] = f_transform[h_slice_src, w_slice_src]
    reconstructed = np.abs(np.fft.ifft2(np.fft.ifftshift(result_f)))
    return reconstructed.astype(np.float64)

def resample_frequency_domain_3d(image: sitk.Image, target_spacing: Sequence[float]) -> sitk.Image:
    """Perform frequency domain resampling for MR images slice by slice (in-plane)."""
    image_array = sitk.GetArrayFromImage(image)
    
    original_size = image.GetSize()
    original_spacing = image.GetSpacing()
    
    target_size_x = int(original_size[0] * (original_spacing[0] / target_spacing[0]))
    target_size_y = int(original_size[1] * (original_spacing[1] / target_spacing[1]))
    target_size = (target_size_y, target_size_x) # (height, width) for numpy array
    
    num_slices = image_array.shape[0]
    result_array = np.zeros((num_slices, target_size[0], target_size[1]), dtype=np.float64)
    
    for slice_idx in range(num_slices):
        slice_data = image_array[slice_idx, :, :].astype(np.float64)
        result_array[slice_idx, :, :] = process_frequency_domain(slice_data, target_size)
        
    result_image = sitk.GetImageFromArray(result_array)
    result_image.SetOrigin(image.GetOrigin())
    result_image.SetDirection(image.GetDirection())
    
    new_spacing = (
        original_spacing[0] * (original_size[0] / target_size_x),
        original_spacing[1] * (original_size[1] / target_size_y),
        original_spacing[2] # Z axis unchanged
    )
    result_image.SetSpacing(new_spacing)
    return result_image

def resample_image_domain(image: sitk.Image, target_spacing: Sequence[float], is_binary: bool) -> sitk.Image:
    """Image domain resampling using SimpleITK for non-MR images or masks."""
    original_size = image.GetSize()
    original_spacing = image.GetSpacing()
    
    target_size = [
        int(round(orig_size * (orig_spacing / tgt_spacing)))
        for orig_size, orig_spacing, tgt_spacing in zip(original_size, original_spacing, target_spacing)
    ]
    
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(image)
    resampler.SetSize(target_size)
    resampler.SetOutputSpacing(target_spacing)
    resampler.SetOutputOrigin(image.GetOrigin())
    resampler.SetOutputDirection(image.GetDirection())
    
    if is_binary:
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)
        resampler.SetOutputPixelType(sitk.sitkUInt8)
    else:
        # Tricubic (sitkBSpline) or Trilinear (sitkLinear)
        resampler.SetInterpolator(sitk.sitkBSpline)
        resampler.SetOutputPixelType(sitk.sitkFloat32)
        
    resampler.SetTransform(sitk.Transform(3, sitk.sitkIdentity))
    return resampler.Execute(image)

def process_file(input_path: Union[str, Path], output_path: Union[str, Path], 
                 target_spacing: Sequence[float], modality: str, is_binary: bool):
    """Main processing logic for a single file."""
    image = sitk.ReadImage(str(input_path))
    original_spacing = image.GetSpacing()
    
    # Check if we can skip resampling (e.g. 0.6 vs 0.61 -> close enough)
    if np.allclose(original_spacing, target_spacing, atol=0.05):
        print(f"Skipping {input_path.name} - spacing {original_spacing} is close to target {target_spacing}")
        shutil.copy(str(input_path), str(output_path))
        return
        
    # Check for thick-slice data vs isotropic
    # If thick slice (e.g., z is much larger than x and y), we might only resample in-plane
    actual_target_spacing = list(target_spacing)
    is_thick_slice = original_spacing[2] > 1.5 * max(original_spacing[0], original_spacing[1])
    
    if is_thick_slice:
        # Keep original Z spacing
        actual_target_spacing[2] = original_spacing[2]
        
    print(f"Resampling {input_path.name} from {original_spacing} to {actual_target_spacing}")
    
    if modality.upper() == 'MR' and not is_binary:
        # Frequency domain for continuous MR images
        resampled_image = resample_frequency_domain_3d(image, actual_target_spacing)
    else:
        # Image domain for CT/PET or binary masks
        resampled_image = resample_image_domain(image, actual_target_spacing, is_binary)
        
    sitk.WriteImage(resampled_image, str(output_path))

def main():
    parser = argparse.ArgumentParser(description="Unify Spacing / Resampling Script")
    parser.add_argument('--input_dir', type=str, required=True, help='Root directory containing dataset')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory for resampled dataset')
    parser.add_argument('--modality', type=str, choices=['CT', 'MR', 'PET'], required=True, help='Imaging modality (CT, MR, PET)')
    parser.add_argument('--image_key', type=str, default='image', help='Keyword to identify main image files')
    parser.add_argument('--label_key', type=str, default='label', help='Keyword to identify mask/label files')
    parser.add_argument('--target_spacing', type=float, nargs=3, default=None, help='Target spacing (x, y, z)')
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Determine Target Spacing
    target_spacing = args.target_spacing
    if target_spacing is None:
        _, target_spacing = check_image_spacings(input_dir, args.image_key)
        if target_spacing is None:
            print("Could not determine target spacing. Exiting.")
            return
            
    # 2. Process Files
    for case in tqdm(input_dir.iterdir(), desc='Processing Cases'):
        if not case.is_dir():
            continue
            
        case_out_dir = output_dir / case.name
        case_out_dir.mkdir(exist_ok=True)
        
        for file_path in case.iterdir():
            if file_path.name.startswith('._') or file_path.name == '.DS_Store':
                continue
                
            out_file_path = case_out_dir / file_path.name
            
            is_binary = args.label_key in file_path.stem.lower() or 'mask' in file_path.stem.lower()
            
            process_file(file_path, out_file_path, target_spacing, args.modality, is_binary)

if __name__ == '__main__':
    main()
