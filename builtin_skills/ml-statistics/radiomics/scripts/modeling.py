import pandas as pd
import numpy as np
import argparse
import os
import joblib
import shap
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, recall_score, precision_score
from sklearn.model_selection import StratifiedKFold, cross_val_score

from data_container import DataContainer

def run_pipeline(train_dc, test_dc, output_dir, classifier_name='lr', n_features=10):
    """
    使用严格的 Pipeline (Scaler -> Selector -> Classifier)
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. 定义分类器
    if classifier_name == 'lr':
        clf = LogisticRegression(max_iter=1000, solver='liblinear')
    elif classifier_name == 'svm':
        clf = SVC(probability=True, kernel='linear')
    elif classifier_name == 'rf':
        clf = RandomForestClassifier(n_estimators=100)
    else:
        raise ValueError(f"Unsupported classifier: {classifier_name}")

    # 2. 构建 Pipeline (严格防止 CV 过程中的数据泄露)
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('selector', SelectKBest(f_classif, k=n_features)),
        ('classifier', clf)
    ])

    # 3. 交叉验证 (使用固定 Seed 保证可重复性)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, train_dc.data, train_dc.label, cv=cv, scoring='roc_auc')
    print(f"5-Fold CV AUC: {np.mean(cv_scores):.3f} +/- {np.std(cv_scores):.3f}")

    # 4. 训练最终模型
    pipeline.fit(train_dc.data, train_dc.label)
    joblib.dump(pipeline, os.path.join(output_dir, "pipeline_model.pkl"))

    # 5. 验证
    results = {}
    for name, dc in [('train', train_dc), ('test', test_dc)]:
        if dc is None or dc.label is None: continue
        
        y_prob = pipeline.predict_proba(dc.data)[:, 1]
        y_pred = pipeline.predict(dc.data)
        
        results[name] = {
            'auc': roc_auc_score(dc.label, y_prob),
            'accuracy': accuracy_score(dc.label, y_pred),
            'sensitivity': recall_score(dc.label, y_pred),
            'specificity': recall_score(dc.label, y_pred, pos_label=0)
        }
        
        # 保存预测结果
        pred_df = pd.DataFrame({'Prob': y_prob, 'Label': dc.label}, index=dc.case_names)
        pred_df.to_csv(os.path.join(output_dir, f"{name}_predictions.csv"))

    pd.DataFrame(results).T.to_csv(os.path.join(output_dir, "performance_metrics.csv"))

    # 6. SHAP 可解释性分析
    try:
        # 获取筛选后的特征名
        selector_mask = pipeline.named_steps['selector'].get_support()
        selected_feature_names = [f for i, f in enumerate(train_dc.feature_names) if selector_mask[i]]
        X_train_scaled = pipeline.named_steps['scaler'].transform(train_dc.data)[:, selector_mask]
        final_clf = pipeline.named_steps['classifier']

        # 根据分类器类型选择 Explainer
        if classifier_name in ['lr', 'svm']:
            explainer = shap.LinearExplainer(final_clf, X_train_scaled)
        else:
            explainer = shap.TreeExplainer(final_clf)
        
        shap_values = explainer.shap_values(X_train_scaled)

        # 绘图
        plt.figure()
        shap.summary_plot(shap_values, X_train_scaled, feature_names=selected_feature_names, plot_type="bar", show=False)
        plt.savefig(os.path.join(output_dir, "SHAP_BarPlot.png"), bbox_inches='tight')
        plt.close()

        plt.figure()
        shap.summary_plot(shap_values, X_train_scaled, feature_names=selected_feature_names, show=False)
        plt.savefig(os.path.join(output_dir, "SHAP_Beeswarm.png"), bbox_inches='tight')
        plt.close()
        print("SHAP plots saved.")
    except Exception as e:
        print(f"SHAP analysis failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True)
    parser.add_argument("--test")
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--classifier", default="lr")
    parser.add_argument("--k", type=int, default=10)
    args = parser.parse_args()

    train_dc = DataContainer.from_csv(args.train)
    test_dc = DataContainer.from_csv(args.test) if args.test else None
    
    run_pipeline(train_dc, test_dc, args.output_dir, classifier_name=args.classifier, n_features=args.k)
