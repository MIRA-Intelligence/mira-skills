# Agent 3: Two-Stage Optimization (两阶段超参数优化)

**Goal:** Fine-tune the promising baseline configurations identified in Agent 2 to maximize performance while maintaining model stability.

## 1. Candidate Identification

Based on the baseline results from Agent 2 (`pipeline_info.csv`), select the Top-N (default 20) configurations based on their **Maximum CV AUC**. 

## 2. Fine-Tuning Strategy

For each candidate configuration, perform an expanded hyperparameter search.

### Expanded Search Space
- **Classifiers**:
  - `LR`: Deep-tune `C` (logspace), `penalty` (l1, l2, elasticnet), and `solver`.
  - `SVM-Linear`: Deep-tune `C` and `intercept_scaling`.
  - **Advanced Models**: If baseline performance is low (CV AUC < 0.70), introduce and tune `Random Forest` or `XGBoost`.
- **Reference**: Follow the ranges in **[Two-Stage Optimization Guide](../references/two_stage_optimization.md)**.

### Generalization Focus
- Adjust hyperparameters to ensure the **Gap (Train AUC - CV AUC) < 0.1**. 
- Increase regularization if the gap is too large.

## 3. Deliverables & Result Preservation (调优结果全量保存)

You MUST treat the results of the optimization process with the same rigor as the baseline grid. 

- **Hierarchical Storage**: Save the artifacts for EVERY fine-tuned pipeline in the directory structure defined in **[Result Preservation Guide](../references/result_preservation.md)**.
  - *Note*: Use the `<Classifier>` name with an `_optimized` suffix if necessary (e.g., `.../LR_optimized/`) to distinguish from baseline results.
- **Mandatory Artifacts**: For every optimized configuration, you MUST generate and save:
  - `metrics.csv`: Performance table (3 decimal places).
  - `roc_combined.png`: Updated Train/CV/Test plot with 95% Bootstrap CI.
  - `feature_importance.png`: Updated weight/importance bar chart.
  - `optimized_model.pkl`: The fine-tuned pipeline object.
  - `tuning_log.json`: A record of the hyperparameter search space and the best parameters found.

**Handoff**: Provide the user with a summary of the improvements gained through optimization and hand off to **Agent 4** for the final selection advice.

## 4. Tuning Redlines (调优警戒线)

During the fine-tuning process, you MUST adhere to the following empirical rules to prevent "hyperparameter overfitting":

- **Stability Check**: If the Standard Deviation of the CV AUC increases by > 50% compared to the baseline model, REJECT the optimization even if the mean CV AUC is higher. Consistency is more important than peak performance.
- **Boundary Warning**: If the optimal hyperparameter found is at the absolute upper or lower boundary of your defined search grid (e.g., `C=1000` when the range was `[0.001, 1000]`), you MUST expand the grid further in that direction and re-run to ensure you haven't missed the true peak.
- **Complexity Penalty**: If two sets of hyperparameters yield a CV AUC within an insignificant margin (e.g., delta < 0.005), ALWAYS choose the configuration with higher regularization (e.g., lower `C` in SVM/LR, smaller `max_depth` in RF) to enforce model simplicity.
- **Sensitivity/Specificity Balance**: Do not accept an optimization that achieves high AUC solely by predicting the majority class correctly. Monitor Class Weights and ensure a balanced Sensitivity and Specificity.