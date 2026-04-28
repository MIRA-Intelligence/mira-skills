import os
import csv
import copy
import logging
import collections
import numpy as np
import SimpleITK as sitk
import pandas as pd
from radiomics.featureextractor import RadiomicsFeatureExtractor
from skimage.exposure import equalize_adapthist
from matplotlib import pyplot as plt
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeriesStringMatcher:
    """Simple utility to match files in a folder based on include/exclude keys."""
    def __init__(self, include_key=None, exclude_key=None):
        self.include_key = include_key if include_key else []
        self.exclude_key = exclude_key if exclude_key else []

    def Match(self, string_list):
        matches = []
        for s in string_list:
            # Check if all include keys are in the string
            include_match = all(k.lower() in s.lower() for k in self.include_key)
            # Check if any exclude key is in the string
            exclude_match = any(k.lower() in s.lower() for k in self.exclude_key) if self.exclude_key else False
            
            if include_match and not exclude_match:
                matches.append(s)
        return matches

def n4_bias_correction(input_image, mask_image, shrinkFactor=1):
    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    if shrinkFactor > 1:
        image = sitk.Shrink(input_image, [shrinkFactor] * input_image.GetDimension())
        mask = sitk.Shrink(mask_image, [shrinkFactor] * input_image.GetDimension())
    else:
        image = input_image
        mask = mask_image
    return corrector.Execute(image, mask)

def CLAHE(data):
    """Contrast Limited Adaptive Histogram Equalization. Data must be in range [0, 1]."""
    kernel = (data.shape[0] // 5, data.shape[1] // 5, data.shape[2] // 2)
    return equalize_adapthist(data, kernel)

class AdvancedRadiomicsExtractor:
    """
    Advanced Radiomics Extractor with preprocessing capabilities.
    """
    def __init__(
        self,
        params_file,
        if_CLAHE=False,
        if_N4=False,
        normalization='Minmax',
        if_normalize_in_roi=False,
        ignore_diagnostic=True
    ):
        self.extractor = RadiomicsFeatureExtractor(params_file)
        self.if_CLAHE = if_CLAHE
        self.if_N4 = if_N4
        self.normalization = normalization
        self.if_normalize_in_roi = if_normalize_in_roi
        self.ignore_diagnostic = ignore_diagnostic
        
        self.feature_values = []
        self.case_list = []
        self.feature_names = []
        self.errors = []

    def _preprocess_image(self, image, mask):
        # Convert to float32 for processing
        image = sitk.Cast(image, sitk.sitkFloat32)
        
        # N4 Bias Correction
        if self.if_N4:
            logger.info("Applying N4 Bias Field Correction...")
            image = n4_bias_correction(image, mask)
            
        img_arr = sitk.GetArrayFromImage(image)
        mask_arr = sitk.GetArrayFromImage(mask)
        
        # Define region for normalization
        target_arr = img_arr[mask_arr > 0] if self.if_normalize_in_roi else img_arr
        
        # Normalization
        if self.normalization == "Minmax":
            img_arr = np.clip(img_arr, np.percentile(img_arr, 0.5), np.percentile(img_arr, 99.5))
            img_arr = (img_arr - target_arr.min()) / (target_arr.max() - target_arr.min() + 1e-7)
        elif self.normalization == "Zscore":
            img_arr = (img_arr - target_arr.mean()) / (target_arr.std() + 1e-7)
            
        # CLAHE
        if self.if_CLAHE:
            logger.info("Applying CLAHE...")
            # Ensure range [0, 1] for CLAHE
            img_arr = (img_arr - img_arr.min()) / (img_arr.max() - img_arr.min() + 1e-7)
            img_arr = CLAHE(img_arr)
            
        processed_image = sitk.GetImageFromArray(img_arr)
        processed_image.CopyInformation(image)
        return processed_image

    def extract_case(self, image_path, mask_path, label_name=""):
        try:
            image = sitk.ReadImage(image_path)
            mask = sitk.ReadImage(mask_path)
            
            # Apply preprocessing
            image = self._preprocess_image(image, mask)
            
            # Execute extraction
            result = self.extractor.execute(image, mask)
            
            # Filter and rename
            case_results = {}
            for name, value in result.items():
                if self.ignore_diagnostic and 'diagnostics' in name:
                    continue
                full_name = f"{label_name}_{name}" if label_name else name
                case_results[full_name] = value
                
            return case_results
        except Exception as e:
            logger.error(f"Extraction failed for {image_path}: {e}")
            return None

    def run_cohort(self, root_dir, image_keys, mask_keys, output_path):
        image_matcher = SeriesStringMatcher(include_key=image_keys)
        mask_matcher = SeriesStringMatcher(include_key=mask_keys)
        
        patient_dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
        patient_dirs.sort()
        
        all_results = []
        
        for p_id in patient_dirs:
            p_path = os.path.join(root_dir, p_id)
            files = os.listdir(p_path)
            
            img_files = image_matcher.Match(files)
            msk_files = mask_matcher.Match(files)
            
            if not img_files or not msk_files:
                logger.warning(f"Skipping {p_id}: Missing image or mask match.")
                self.errors.append(p_id)
                continue
                
            logger.info(f"Processing patient: {p_id}")
            res = self.extract_case(
                os.path.join(p_path, img_files[0]),
                os.path.join(p_path, msk_files[0]),
                label_name="LGE" # Example label
            )
            
            if res:
                res['PatientID'] = p_id
                all_results.append(res)
            else:
                self.errors.append(p_id)
                
        if all_results:
            df = pd.DataFrame(all_results)
            # Ensure PatientID is the first column
            cols = ['PatientID'] + [c for c in df.columns if c != 'PatientID']
            df = df[cols]
            df.to_csv(output_path, index=False)
            logger.info(f"Saved {len(all_results)} cases to {output_path}")
        
        if self.errors:
            logger.warning(f"Failed cases: {self.errors}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advanced Radiomics Batch Extractor")
    parser.add_argument('--root_dir', required=True, help="Root directory containing patient folders")
    parser.add_argument('--img_key', required=True, help="Key to match image files")
    parser.add_argument('--msk_key', required=True, help="Key to match mask files")
    parser.add_argument('--out_csv', required=True, help="Output CSV path")
    parser.add_argument('--params', required=True, help="Path to PyRadiomics YAML params")
    parser.add_argument('--n4', action='store_true', help="Enable N4 Bias Correction")
    parser.add_argument('--clahe', action='store_true', help="Enable CLAHE")
    
    args = parser.parse_args()
    
    extractor = AdvancedRadiomicsExtractor(
        args.params,
        if_N4=args.n4,
        if_CLAHE=args.clahe
    )
    
    extractor.run_cohort(
        args.root_dir,
        image_keys=[args.img_key],
        mask_keys=[args.msk_key],
        output_path=args.out_csv
    )
