---
name: FAE-Methodology
description: Core methodology reference based on the FAE (FeAture Explorer) open-source radiomics framework
---

# FAE Pipeline Methodology

## Source
Based on https://github.com/salan668/FAE.git (East China Normal University & Siemens Healthineers, PLoS One 2020)

## Core Pipeline Architecture

FAE implements a combinatorial grid search over six pipeline stages:

```
Balance × Normalizer × DimensionReduction × FeatureSelector × FeatureCount × Classifier
```

Each combination is evaluated via cross-validation, producing an ensemble of models ranked by AUC.

### Pipeline Components

#### 1. Data Balancing
Handles class imbalance in binary classification:
- **None**: No balancing
- **DownSampling**: Random under-sampling of majority class
- **UpSampling**: Random over-sampling of minority class
- **SMOTE**: Synthetic Minority Over-sampling Technique (generates synthetic samples via interpolation)
- **SMOTE+Tomek**: SMOTE followed by Tomek links cleanup (removes borderline samples)

Uses `imbalanced-learn` library.

#### 2. Normalization
Feature scaling applied to training data, then transformed to validation/test:
- **None**: Identity transform
- **MinMax**: Scale to [0, 1] range
- **ZScore**: Standardize to zero mean, unit variance (`StandardScaler`)
- **Mean**: Mean-subtract and range-divide

#### 3. Dimension Reduction
Reduce feature collinearity before selection:
- **None**: No reduction
- **PCC**: Remove one of each pair with Pearson |r| > threshold (default 0.99). Greedy: start from highest correlation, remove feature with lower variance, iterate
- **PCA**: Principal Component Analysis, retain components explaining 95% of variance

#### 4. Feature Selection
Select top-K features by relevance to outcome:
- **ANOVA**: F-test for feature-class relationship (parametric)
- **ReliefF**: Distance-based, weighs features by how well they distinguish nearest neighbors of same/different class
- **RFE**: Recursive Feature Elimination using linear SVM — iteratively remove worst coefficient
- **mRMR**: Minimum Redundancy Maximum Relevance — maximize mutual information with class while minimizing feature-feature redundancy
- **Kruskal-Wallis**: Non-parametric alternative to ANOVA (H-test)

All selectors take `n_features` parameter specifying how many to retain.

#### 5. Classifiers (Coarse Stage)
- **SVM**: Support Vector Machine (linear kernel only in coarse stage)
- **LDA**: Linear Discriminant Analysis
- **RF**: Random Forest
- **MLP**: Multi-Layer Perceptron (neural network)
- **LR**: Logistic Regression
- **AdaBoost**: Adaptive boosting with decision tree base

Fine stage expands to: RBF/poly/sigmoid SVM kernels, GP, NaiveBayes, DecisionTree, LRLasso.

#### 6. Cross-Validation
- **5-fold stratified**: Default, good balance of bias/variance
- **10-fold stratified**: More estimates, higher variance per fold
- **LOO**: Leave-One-Out (useful for very small datasets <30 samples)
- **Arbitrary K**: User-specified number of folds

#### 7. Evaluation Metrics
- **AUC**: Area Under ROC Curve, with 1000-bootstrap 95% CI (Delong method)
- **Accuracy**: Overall correct classification rate
- **Sensitivity (Recall)**: True positive rate
- **Specificity**: True negative rate
- **PPV**: Positive Predictive Value (precision)
- **NPV**: Negative Predictive Value
- **MCC**: Matthews Correlation Coefficient (balanced measure for imbalanced classes)
- **Youden Index**: Sensitivity + Specificity - 1
- **PR-AUC**: Area Under Precision-Recall Curve (informative for imbalanced data)

## Limitations of Original FAE
1. SVM only uses linear kernel — no RBF/polynomial/sigmoid
2. No LASSO as a feature pre-filter step
3. Hyperparameters fixed in JSON files — not dynamically tuned
4. No two-stage optimization (coarse → fine)
5. GUI-only — no headless CLI scripting

## Our Enhancements
1. **LASSO pre-filter**: Reduce ~1000 PyRadiomics features to ~50-100 before grid search
2. **Two-stage pipeline**: Coarse grid (9000 combos) → fine-tune top-N with expanded hyperparams
3. **Nonlinear SVM**: RBF, polynomial, sigmoid kernels with auto-tuned C and gamma
4. **Auto-iteration**: Continue fine-tuning until AUC target reached or max iterations
5. **Headless CLI**: Full command-line interface, no GUI dependency
