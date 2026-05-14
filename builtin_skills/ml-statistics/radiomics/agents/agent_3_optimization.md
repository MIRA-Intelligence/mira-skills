# Agent 3: Two-Stage Optimization (两阶段超参数优化)

**Goal:** Fine-tune the baseline models established by Agent 2 using a coarse-to-fine two-stage pipeline optimization. The ultimate objective is to achieve **maximal predictive performance with the minimum number of highly interpretable features**.

*Reference*: [Two-Stage Optimization Methodology](../references/two_stage_optimization.md)

## Stage 1: Coarse Permutation Sweep
Performed by agent_2_modeling(`agents/agent_2_modeling.md`). 

### Output Analysis & 1-SE Application (模型横向PK与1-SE检验)
Instead of blindly forcing 1-SE on every pipeline, you MUST follow this comparative logic to avoid over-penalizing already-sparse models:
1. **Absolute Ranking**: First, sort ALL pre-experiment pipelines by their **Absolute Maximum CV AUC** (ignoring feature counts temporarily).
2. **Select Top-K Candidates**: Pick the top-performing pipelines (e.g., Top 10-20) from this absolute ranking.
3. **1-SE Verification**: For EACH of these Top-K pipelines, find its corresponding "1-SE version" (the version with the fewest features whose CV AUC is within one standard error of its absolute maximum).
4. **Parsimony Check**: Compare the 1-SE version against the absolute version. Did 1-SE actually reduce the feature count? If a model's absolute best version already uses very few features (e.g., $\le 5$), the 1-SE version might unnecessarily degrade performance without significantly improving interpretability.
5. **Final Stage 1 Selection**: Re-rank these Top-K candidates using the CV AUC of their **1-SE versions** (or their absolute version if 1-SE degraded performance without a meaningful reduction in features). Select the final configurations for deep optimization. 
- **Anti-Leakage**: Do NOT use Test AUC for ranking or selection at this stage. You may note models with high Test AUC for the user's information only.
- **Interpretability Check**: If the performance gap between a Tier 1 (Simple) pipeline and a Tier 2 (Advanced) pipeline is negligible (< 0.02 AUC), prioritize the Tier 1 pipeline.

## Stage 2: Fine-Tuning & Hyperparameter Strategy

Deep-tune the Top-K configurations using an expanded hyperparameter space. You MUST refer to the following scenarios to decide which parameters to prioritize.

### 1. Feature Selector Optimization (特征选择器调优)

| Selector | Tunable Parameters | Tuning Scenario (适用场景) |
| :--- | :--- | :--- |
| **K-Best (ANOVA/KW)** | `k` (Number of features) | **Dimension Bottleneck**: If CV AUC fluctuates wildly, narrow `k` to find the plateau. Usually $1 \leq k \leq N_{cases}/10$. |
| **RFE** | `step` (float/int), `estimator` params | **Interaction Sensitivity**: Use small `step` (e.g., 0.05) if features are highly synergistic; adjust the base estimator (e.g., SVC `C`) to change selection strictness. |
| **LASSO (Embedded)** | `C` (Inverse regularization) | **Sparsity Control**: Use smaller `C` (high penalty) when features are extremely redundant; larger `C` when signal is sparse and distributed. |
| **ReliefF** | `n_neighbors` | **Local Interaction**: Increase `n_neighbors` if data has high noise/outliers; decrease if data is clean and local clusters are tight. |

### 2. Classifier Optimization (分类器调优)

| Classifier | Expanded Hyperparameter Space | Tuning Scenario (适用场景) |
| :--- | :--- | :--- |
| **LR** | `C`: logspace(-4, 4, 20)<br>`penalty`: ['l1', 'l2', 'elasticnet']<br>`solver`: ['liblinear', 'saga'] | **Linear Parsimony**: Use `l1` or `elasticnet` when you need the model to force coefficients of redundant features to exactly zero for better interpretability. |
| **SVM** | `C`: logspace(-3, 3, 20)<br>`kernel`: ['linear', 'rbf', 'poly']<br>`gamma`: logspace(-4, 2, 12)<br>`degree`: [2, 3, 4] | **Complexity Scaling**: If linear SVM underperforms, migrate to `rbf` (captures non-linear blobs) or `poly` (captures feature interactions). Adjust `gamma` to control the "reach" of a single training instance. |
| **Random Forest** | `n_estimators`: [50, 100, 200, 500]<br>`max_depth`: [3, 5, 10, None]<br>`min_samples_split`: [2, 5, 10]<br>`class_weight`: ['balanced', None] | **Ensemble Stability**: Decrease `max_depth` and increase `n_estimators` to fight overfitting on small cohorts. Use `class_weight='balanced'` if the label distribution is skewed (> 1:2). |
| **MLP (NN)** | `hidden_layer_sizes`: [(10,), (50,), (100,), (50, 25)]<br>`alpha`: logspace(-5, -2, 10)<br>`learning_rate`: ['constant', 'adaptive'] | **Non-Linear Depth**: Use smaller `alpha` (less regularization) if the model is underfitting; increase `hidden_layer_sizes` only if simpler classifiers fail to reach target AUC. |
| **LDA** | `solver`: ['lsqr', 'eigen']<br>`shrinkage`: ['auto', 0.1, 0.5, None] | **Small Sample Adjustment**: Use `shrinkage='auto'` or a float value when the number of features is large relative to the number of samples ($k > N_{train}$) to stabilize the covariance matrix. |
| **AdaBoost** | `n_estimators`: [50, 100, 200, 500]<br>`learning_rate`: [0.01, 0.1, 0.5, 1.0] | **Boosting Precision**: Use smaller `learning_rate` with larger `n_estimators` for a more robust but slower convergence to the optimal decision boundary. |

### 3. Optimization Objectives & Logic
Your tuning strategy MUST balance these three pillars:
1. **Parsimony**: Favor models with fewer features (refer back to the 1-SE models from Agent 2).
2. **Interpretability**: Favor linear models or models with clear feature importance rankings (like SVM-linear coefficients or RF importances).
3. **Generalization**: Maximize CV AUC while ensuring the **Gap (Train AUC - CV AUC) < 0.1**. If the gap is larger, increase regularization (e.g., smaller `C`, larger `alpha`, or smaller `max_depth`).

- **Optimized Model Pipeline**: The best combination of balancing, normalization, selection, and classifier with its fine-tuned hyperparameters.
- **Artifacts**: You MUST preserve all optimization results (CSVs, models, plots) according to the **[Result Preservation Guide](../references/result_preservation.md)**.
- **Final Performance Metrics**: Updated performance table showing the improvement over the baseline models (reported to **3 decimal places**).