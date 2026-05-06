import pandas as pd
import numpy as np
import argparse
from sklearn.model_selection import train_test_split
from scipy.stats import mannwhitneyu, chi2_contingency

def compare_groups(df1, df2, features):
    """检查两组之间特征分布是否有显著差异 (p < 0.05 则有差异)"""
    p_values = {}
    for feat in features:
        if df1[feat].dtype in [np.float64, np.int64] and df1[feat].nunique() > 10:
            # 连续变量使用 Mann-Whitney U 检验
            _, p = mannwhitneyu(df1[feat], df2[feat], alternative='two-sided')
        else:
            # 分类变量使用卡方检验
            contingency = pd.concat([
                df1[feat].value_counts(),
                df2[feat].value_counts()
            ], axis=1).fillna(0)
            _, p, _, _ = chi2_contingency(contingency)
        p_values[feat] = p
    return p_values

def balanced_split(input_csv, clinical_csv, output_dir, ratio=0.3, max_loop=100, label='label'):
    features_df = pd.read_csv(input_csv, index_col=0)
    clinical_df = pd.read_csv(clinical_csv, index_col=0)
    
    # 合并数据
    combined = features_df.join(clinical_df, how='inner')
    clinical_cols = clinical_df.columns.tolist()
    
    best_p_min = -1
    best_train, best_test = None, None
    
    print(f"Starting balanced split (max {max_loop} loops)...")
    for i in range(max_loop):
        train, test = train_test_split(combined, test_size=ratio, stratify=combined[label])
        p_vals = compare_groups(train, test, clinical_cols + [label])
        min_p = min(p_vals.values())
        
        if min_p > best_p_min:
            best_p_min = min_p
            best_train, best_test = train, test
            
        if min_p > 0.1: # 理想状态：所有特征 p > 0.1
            break
            
    print(f"Best minimum p-value: {best_p_min:.4f}")
    
    # 保存结果
    import os
    os.makedirs(output_dir, exist_ok=True)
    best_train.to_csv(os.path.join(output_dir, "train_features.csv"))
    best_test.to_csv(os.path.join(output_dir, "test_features.csv"))
    
    # 保存统计报告
    p_vals_final = compare_groups(best_train, best_test, clinical_cols + [label])
    pd.Series(p_vals_final).to_json(os.path.join(output_dir, "split_stats.json"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--clinical", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--ratio", type=float, default=0.3)
    parser.add_argument("--label", default="label")
    args = parser.parse_args()
    balanced_split(args.input, args.clinical, args.output_dir, args.ratio, label=args.label)
