import pandas as pd
import numpy as np
import argparse
import os
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from data_container import DataContainer

def select_features(train_dc, output_dir, n_features=10, method='anova', pcc_threshold=0.95):
    """
    参考 FAE 逻辑：特征筛选函数，支持 PCC 和 并列的选择器 (ANOVA, LASSO, RFE)
    """
    os.makedirs(output_dir, exist_ok=True)
    X = train_dc.data
    y = train_dc.label
    feature_names = train_dc.feature_names

    # 1. 相关性过滤 (PCC) - 矩阵缓存逻辑由 Agent 实现，这里提供基础过滤
    df_temp = pd.DataFrame(X, columns=feature_names)
    if pcc_threshold < 1.0:
        corr_matrix = df_temp.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > pcc_threshold)]
        df_temp = df_temp.drop(columns=to_drop)
        print(f"PCC dropped {len(to_drop)} features.")

    # 更新特征名和数据
    remaining_features = df_temp.columns.tolist()
    X_remaining = df_temp.values

    # 2. 特征筛选 (并列互斥逻辑)
    if method == 'anova':
        selector = SelectKBest(f_classif, k=min(n_features, X_remaining.shape[1]))
        selector.fit(X_remaining, y)
        support = selector.get_support()
    elif method == 'lasso':
        # LASSO 逻辑：使用 L1 惩罚的 LogisticRegression
        clf = LogisticRegression(penalty='l1', C=0.1, solver='liblinear', random_state=42)
        clf.fit(X_remaining, y)
        # 获取非零系数的特征，如果超过 n_features 则按绝对值排序
        coef = np.abs(clf.coef_[0])
        if np.sum(coef > 0) > n_features:
            threshold = np.sort(coef[coef > 0])[-n_features]
            support = coef >= threshold
        else:
            support = coef > 0
    elif method == 'rfe':
        # NOTE: RFE estimator MUST match the final classifier of the pipeline.
        # For this standalone script, we default to LogisticRegression, but
        # Agent 2 will dynamically pass the correct estimator.
        base_estimator = LogisticRegression(max_iter=1000, solver='liblinear')
        selector = RFE(estimator=base_estimator, n_features_to_select=min(n_features, X_remaining.shape[1]), step=0.05)
        selector.fit(X_remaining, y)
        support = selector.get_support()
    else:
        raise ValueError(f"Method {method} not supported.")

    selected_feature_names = [f for i, f in enumerate(remaining_features) if support[i]]
    print(f"Selected {len(selected_feature_names)} features using {method}.")

    # 3. 保存结果 (FAE 风格)
    selected_dc = train_dc.get_subset(selected_feature_names)
    selected_dc.save(os.path.join(output_dir, "selected_features.csv"))
    
    with open(os.path.join(output_dir, "feature_list.txt"), "w") as f:
        f.write("\n".join(selected_feature_names))
    
    return selected_feature_names

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--n_features", type=int, default=10)
    parser.add_argument("--method", choices=['anova', 'lasso', 'rfe'], default='anova')
    parser.add_argument("--pcc", type=float, default=0.95)
    args = parser.parse_args()

    train_dc = DataContainer.from_csv(args.input)
    select_features(train_dc, args.output_dir, n_features=args.n_features, method=args.method, pcc_threshold=args.pcc)
