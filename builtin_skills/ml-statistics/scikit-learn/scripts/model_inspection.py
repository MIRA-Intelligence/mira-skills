"""
Model Inspection and Visualization Pipeline Example.

Demonstrates how to interpret a trained model using Partial Dependence Plots (PDP),
Individual Conditional Expectation (ICE), Permutation Importance, and modern Plotting APIs.
"""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import fetch_california_cancer # using breast cancer as proxy
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
from sklearn.metrics import RocCurveDisplay, ConfusionMatrixDisplay, classification_report
import warnings
warnings.filterwarnings('ignore')

def run_inspection_pipeline():
    print("="*60)
    print("Model Inspection & Interpretability Example")
    print("="*60)

    # 1. Load Data
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 2. Train a modern, fast ensemble model
    print("Training HistGradientBoostingClassifier...")
    model = HistGradientBoostingClassifier(max_iter=100, random_state=42)
    model.fit(X_train, y_train)

    print("\nTest Set Evaluation:")
    print(classification_report(y_test, model.predict(X_test)))

    # 3. Permutation Feature Importance
    print("\nCalculating Permutation Feature Importance (on Test Set)...")
    result = permutation_importance(
        model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=-1
    )
    
    importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance Mean': result.importances_mean,
        'Importance Std': result.importances_std
    }).sort_values(by='Importance Mean', ascending=False)

    print("\nTop 5 Most Important Features:")
    print(importance_df.head(5).to_string(index=False))

    # Plot Permutation Importance
    plt.figure(figsize=(10, 6))
    importance_df.head(10).plot.barh(x='Feature', y='Importance Mean', xerr='Importance Std', ax=plt.gca())
    plt.title("Top 10 Features - Permutation Importance (Test Set)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('permutation_importance.png', dpi=300)
    print("Saved: permutation_importance.png")
    plt.close()

    # 4. Partial Dependence Plots (PDP) & ICE
    top_2_features = importance_df['Feature'].iloc[:2].tolist()
    print(f"\nGenerating PDP and ICE plots for top features: {top_2_features}...")

    fig, ax = plt.subplots(figsize=(12, 5))
    display = PartialDependenceDisplay.from_estimator(
        model,
        X_test,
        features=top_2_features,
        kind='both', # ICE + PDP
        feature_names=X.columns,
        ax=ax,
        n_jobs=-1
    )
    plt.suptitle("Partial Dependence and ICE Plots")
    plt.tight_layout()
    plt.savefig('pdp_ice_plots.png', dpi=300)
    print("Saved: pdp_ice_plots.png")
    plt.close()

    # 5. Diagnostic Visualizations
    print("\nGenerating Diagnostic Visualizations (ROC & Confusion Matrix)...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax1)
    ax1.set_title("ROC Curve")

    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap='Blues', normalize='true', ax=ax2)
    ax2.set_title("Normalized Confusion Matrix")

    plt.tight_layout()
    plt.savefig('diagnostic_plots.png', dpi=300)
    print("Saved: diagnostic_plots.png")
    plt.close()

    print("\nInspection pipeline complete. Check the generated PNG files.")

if __name__ == "__main__":
    run_inspection_pipeline()
