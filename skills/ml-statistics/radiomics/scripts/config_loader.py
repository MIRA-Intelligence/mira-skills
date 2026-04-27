import yaml
import json
import os


def load_config(path):
    with open(path, 'r') as f:
        if path.endswith(('.yaml', '.yml')):
            return yaml.safe_load(f)
        else:
            return json.load(f)


def merge_config(config, overrides):
    """Deep merge overrides into config. None values in overrides are skipped."""
    merged = config.copy()
    for k, v in overrides.items():
        if v is None:
            continue
        if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
            merged[k] = merge_config(merged[k], v)
        else:
            merged[k] = v
    return merged


def save_config(config, path):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w') as f:
        if path.endswith(('.yaml', '.yml')):
            yaml.dump(config, f, default_flow_style=False)
        else:
            json.dump(config, f, indent=2)


DEFAULT_CONFIG = {
    'pipeline': 'radiomics',
    'modality': 'CT',
    'paths': {'images': './data/images', 'masks': './data/masks'},
    'extraction': {
        'resample_spacing': [1, 1, 1],
        'bin_width': 25,
        'dimensionality': 3,
    },
    'lasso_prefilter': {
        'alpha_range': [0.0001, 0.001, 0.01, 0.1, 1.0],
        'retain_fraction': 0.3,
        'cv_folds': 5,
    },
    'grid_search': {
        'top_n': 20,
        'cv_folds': 5,
        'cv_strategy': 'stratified_kfold',
        'feature_counts': [5, 10, 15, 20, 30],
    },
    'fine_tuning': {
        'auc_target': 0.90,
        'max_iterations': 10,
        'min_improvement': 0.005,
        'shrink_factor': 0.5,
        'svm_kernels': ['linear', 'rbf', 'poly', 'sigmoid'],
    },
    'output': {
        'results_dir': './results',
        'headless': True,
    },
}


def get_config(path=None, overrides=None):
    config = DEFAULT_CONFIG.copy()
    if path and os.path.exists(path):
        config = merge_config(config, load_config(path))
    if overrides:
        config = merge_config(config, overrides)
    return config
