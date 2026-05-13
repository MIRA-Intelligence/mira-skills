# Agent 3: Two-Stage Optimization (两阶段超参数优化)

**Goal:** Fine-tune the baseline models established by Agent 2 using a coarse-to-fine two-stage pipeline optimization. The ultimate objective is to achieve **maximal predictive performance with the minimum number of highly interpretable features**.
**Goal:** Fine-tune the baseline models established by Agent 2 using a coarse-to-fine two-stage pipeline optimization. The ultimate objective is to achieve **maximal predictive performance with the minimum number of highly interpretable features**.

*Reference*: [Two-Stage Optimization Methodology](../references/two_stage_optimization.md)

## Stage 1: Coarse Permutation Sweep
Performed by agent_2_modeling(`agents/agent_2_modeling.md`). 
## Stage 1: Coarse Permutation Sweep
Performed by agent_2_modeling(`agents/agent_2_modeling.md`). 

### Output Analysis
- **Ranking**: Sort all pre-experiment combinations by **CV AUC**.
- **Model Selection**: Select the **Top-N** (e.g., Top 20) configurations based strictly on CV performance. 
- **Anti-Leakage**: Do NOT use Test AUC for ranking or selection at this stage. You may note models with high Test AUC for the user's information only.
- **Interpretability Check**: Compare the performance of Tier 1 (Simple) vs. Tier 2 (Advanced) pipelines. If the performance gap is negligible (< 0.02 AUC), prioritize the Tier 1 pipeline to maintain better interpretability.

## Stage 2: Fine-Tuning with Auto-Iteration & Algorithm Migration

Deep-tune the Top-N configurations using an expanded hyperparameter space and explore advanced classifier variants.
Deep-tune the Top-N configurations using an expanded hyperparameter space and explore advanced classifier variants.

### Expanded Hyperparameter Space & Algorithm Migration
- **SVM Migration**: If **Random Forest** or other non-linear ensembles showed strong baseline results in Agent 2, you MUST prioritize fine-tuning **Non-Linear SVM (RBF/Poly kernels)** to capture these complex patterns in a more geometrically constrained model.
  - `kernel ∈ {linear, rbf, poly, sigmoid}`, `C = logspace(-3, 3, 20)`, `gamma = logspace(-4, 2, 12)`, `degree ∈ {2, 3, 4, 5}`
- **RF Tuning**: `n_estimators ∈ {50, 100, 200, 500}`, `max_depth ∈ {3, 5, 10, None}`, `min_samples_split ∈ {2, 5, 10}`, `class_weight ∈ {None, balanced}`
- **LR (Parsimony Focus)**: Optimize `C = logspace(-4, 4, 20)` with `penalty='l1'` or `penalty='elasticnet'` to further prune features during the modeling phase.
- **Other Classifiers**:
  - **MLP**: `hidden ∈ {[10], [30], [50], [100], [100,50]}`, `alpha = logspace(-5, -2, 10)`
  - **LDA**: `solver ∈ {lsqr, eigh}`, `shrinkage ∈ {None, auto, 0.1, 0.5}`
  - **AdaBoost/Gradients**: `n_estimators ∈ {50, 100, 200, 500}`, `learning_rate ∈ {0.01, 0.1, 0.5, 1.0}`

### Optimization Objectives
Your tuning strategy MUST balance these three pillars:
1. **Parsimony**: Favor models with fewer features (refer back to the 1-SE models from Agent 2).
2. **Interpretability**: Favor linear models or models with clear feature importance rankings.
3. **Performance**: Maximize CV AUC while ensuring the gap between Train and CV AUC is minimized (to prevent overfitting).

## Deliverables
- **Optimized Model Pipeline**: The best combination of balancing, normalization, selection, and classifier with its fine-tuned hyperparameters.
- **Artifacts**: You MUST preserve all optimization results (CSVs, models, plots) according to the **[Result Preservation Guide](../references/result_preservation.md)**.
- **Final Performance Metrics**: Updated performance table showing the improvement over the baseline models (reported to **3 decimal places**).