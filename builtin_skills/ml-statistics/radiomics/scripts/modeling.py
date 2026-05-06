import pandas as pd
import numpy as np
import argparse
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler

def train_and_validate(train_csv, test_csv, output_dir, classifier='lr', label='label'):
    train_df = pd.read_csv(train_csv, index_col=0)
    y_train = train_df[label]
    X_train = train_df.drop(columns=[label])
    
    # 标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # 选择分类器
    if classifier == 'lr':
        clf = LogisticRegression(max_iter=1000)
    elif classifier == 'svm':
        clf = SVC(probability=True, kernel='linear')
    elif classifier == 'rf':
        clf = RandomForestClassifier(n_estimators=100)
    else:
        raise ValueError(f"Classifier {classifier} not supported.")
        
    # 交叉验证
    cv = StratifiedKFold(n_splits=5)
    cv_scores = cross_val_score(clf, X_train_scaled, y_train, cv=cv, scoring='roc_auc')
    print(f"5-Fold CV AUC: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores):.4f})")
    
    # 训练最终模型
    clf.fit(X_train_scaled, y_train)
    
    # 保存模型和标准化器
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(clf, os.path.join(output_dir, "model.pkl"))
    joblib.dump(scaler, os.path.join(output_dir, "scaler.pkl"))
    
    # 测试集验证
    if test_csv:
        test_df = pd.read_csv(test_csv, index_col=0)
        y_test = test_df[label]
        X_test = test_df.drop(columns=[label])
        X_test_scaled = scaler.transform(X_test)
        
        y_prob = clf.predict_proba(X_test_scaled)[:, 1]
        y_pred = clf.predict(X_test_scaled)
        
        metrics = {
            "auc": roc_auc_score(y_test, y_prob),
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred)
        }
        
        print("Test Set Performance:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")
            
        pd.Series(metrics).to_json(os.path.join(output_dir, "test_metrics.json"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True)
    parser.add_argument("--test")
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--classifier", choices=['lr', 'svm', 'rf'], default='lr')
    parser.add_argument("--label", default="label")
    args = parser.parse_args()
    train_and_validate(args.train, args.test, args.output_dir, args.classifier, label=args.label)
