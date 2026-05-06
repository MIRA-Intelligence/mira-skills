import pandas as pd
import numpy as np
import argparse
import os
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import StandardScaler

def lasso_prefilter(input_csv, output_csv, label_col='label', alpha_range=[0.0001, 0.001, 0.01, 0.1, 1.0], retain_fraction=0.3, cv_folds=5):
    df = pd.read_csv(input_csv, index_col=0)
    
    # Separate features and label
    if label_col not in df.columns:
        # Try case-insensitive
        cols = {c.lower(): c for c in df.columns}
        if label_col.lower() in cols:
            label_col = cols[label_col.lower()]
        else:
            raise ValueError(f"Label column '{label_col}' not found in {input_csv}")
            
    y = df[label_col]
    X = df.drop(columns=[label_col])
    
    # Drop non-numeric columns
    X = X.select_dtypes(include=[np.number])
    feature_names = X.columns
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Lasso CV
    # Cs is the inverse of regularization strength; 1/alpha
    Cs = [1.0/a for a in alpha_range]
    lasso = LogisticRegressionCV(
        Cs=Cs, cv=cv_folds, penalty='l1', solver='liblinear', 
        scoring='roc_auc', max_iter=10000, random_state=42
    )
    lasso.fit(X_scaled, y)
    
    # Identify best alpha (C)
    best_C = lasso.C_[0]
    coef = lasso.coef_[0]
    
    selected_indices = np.where(np.abs(coef) > 1e-6)[0]
    selected_features = feature_names[selected_indices].tolist()
    
    # Enforce retain_fraction if too many features selected
    max_features = int(len(feature_names) * retain_fraction)
    if len(selected_features) > max_features:
        print(f"Lasso selected {len(selected_features)} features, which exceeds retain_fraction {retain_fraction}. Sorting by coefficient magnitude.")
        # Sort by coefficient magnitude
        abs_coef = np.abs(coef[selected_indices])
        sorted_indices = np.argsort(abs_coef)[::-1][:max_features]
        selected_features = [selected_features[i] for i in sorted_indices]
        
    print(f"Lasso pre-filter: {len(feature_names)} -> {len(selected_features)} features.")
    
    # Save results
    output_df = df[[label_col] + selected_features]
    output_df.to_csv(output_csv)
    
    # Save report
    report_path = output_csv.replace('.csv', '_report.json')
    import json
    with open(report_path, 'w') as f:
        json.dump({
            "best_alpha": 1.0/best_C,
            "n_original": len(feature_names),
            "n_selected": len(selected_features),
            "selected_features": selected_features
        }, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="LASSO Pre-filter for Radiomics")
    parser.add_argument("--input", required=True, help="Input features CSV (with labels)")
    parser.add_argument("--output", required=True, help="Output features CSV")
    parser.add_argument("--label", default="label", help="Label column name")
    parser.add_argument("--retain", type=float, default=0.3, help="Max fraction of features to retain")
    
    args = parser.parse_args()
    lasso_prefilter(args.input, args.output, label_col=args.label, retain_fraction=args.retain)

if __name__ == "__main__":
    main()
