import pandas as pd
import numpy as np
import argparse
import os
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

def select_features(input_csv, output_dir, n_features=10, method='anova', label='label', pcc_threshold=0.9):
    df = pd.read_csv(input_csv, index_col=0)
    y = df[label]
    X = df.drop(columns=[label])
    
    # 1. 移除低方差特征
    X = X.loc[:, X.std() > 0]
    
    # 2. 相关性过滤 (PCC)
    if pcc_threshold < 1.0:
        corr_matrix = X.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > pcc_threshold)]
        X = X.drop(columns=to_drop)
        print(f"PCC dropped {len(to_drop)} redundant features.")

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. 特征筛选
    if method == 'anova':
        selector = SelectKBest(f_classif, k=n_features)
        selector.fit(X_scaled, y)
        selected_cols = X.columns[selector.get_support()].tolist()
    elif method == 'rfe':
        svc = SVC(kernel="linear", C=1)
        selector = RFE(estimator=svc, n_features_to_select=n_features, step=0.1)
        selector.fit(X_scaled, y)
        selected_cols = X.columns[selector.get_support()].tolist()
    else:
        raise ValueError(f"Method {method} not supported in this script.")

    print(f"Selected {len(selected_cols)} features using {method}.")
    
    # 保存
    os.makedirs(output_dir, exist_ok=True)
    df_selected = df[[label] + selected_cols]
    df_selected.to_csv(os.path.join(output_dir, "selected_features.csv"))
    
    with open(os.path.join(output_dir, "feature_list.txt"), "w") as f:
        f.write("\n".join(selected_cols))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--n_features", type=int, default=10)
    parser.add_argument("--method", choices=['anova', 'rfe'], default='anova')
    parser.add_argument("--pcc", type=float, default=0.9)
    parser.add_argument("--label", default="label")
    args = parser.parse_args()
    select_features(args.input, args.output_dir, args.n_features, args.method, label=args.label, pcc_threshold=args.pcc)
