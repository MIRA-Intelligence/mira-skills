# Agent 3: Two-Stage Optimization (两阶段超参数优化)

**Goal:** Fine-tune the baseline models established by Agent 2 using a coarse-to-fine two-stage pipeline optimization to achieve maximal model performance.

*Reference*: [Two-Stage Optimization Methodology](../references/two_stage_optimization.md)

## Stage 1: Coarse Grid Search
Performed by agent_2_modeling(`agents/agent_2_modeling.md`)

### Output
Sort all combinations by CV AUC and select the Top-N (e.g., Top 20) configurations for fine-tuning.

## Stage 2: Fine-Tuning with Auto-Iteration

Deep-tune the Top-N configurations using an expanded hyperparameter space and auto-iteration to convergence.

### Expanded Hyperparameter Space
- **SVM**: `kernel ∈ {linear, rbf, poly, sigmoid}`, `C = logspace(-3, 3, 20)`, `gamma = logspace(-4, 2, 12)`, `degree ∈ {2, 3, 4, 5}`
- **RF**: `n_estimators ∈ {50, 100, 200, 500}`, `max_depth ∈ {3, 5, 10, None}`, `min_samples_split ∈ {2, 5, 10}`, `class_weight ∈ {None, balanced}`
- **LR**: `C = logspace(-4, 4, 20)`, `solver ∈ {liblinear, saga, lbfgs}`, `class_weight ∈ {None, balanced}`
- **MLP**: `hidden ∈ {[10], [30], [50], [100], [100,50]}`, `alpha = logspace(-5, -2, 10)`, `learning_rate ∈ {constant, adaptive, invscaling}`
- **LDA**: `solver ∈ {lsqr, eigh}`, `shrinkage ∈ {None, auto, 0.1, 0.5}`
- **AdaBoost**: `n_estimators ∈ {50, 100, 200, 500}`, `learning_rate ∈ {0.01, 0.1, 0.5, 1.0}`

### Auto-Iteration Algorithm
1. First iteration uses the expanded grid.
2. Subsequent iterations narrow the parameter grid around the best-found parameters (log space for numeric, fallback to coarse if over-narrowed).
3. Stop when reaching `auc_target` (e.g., 0.90) or when improvement falls below `min_improvement` (e.g., 0.005).

*Efficiency Mandate*: To maximize performance during this intensive fine-tuning process, you MUST enable parallel computing by setting `n_jobs=-1` in all `GridSearchCV` instances and capable classifiers (e.g., `RandomForestClassifier`).

## Deliverables
- **Optimized Model Pipeline**: The best combination of balancing, normalization, selection, and classifier with its fine-tuned hyperparameters.
- **Final Performance Metrics**: Updated performance table showing the improvement over the baseline models.