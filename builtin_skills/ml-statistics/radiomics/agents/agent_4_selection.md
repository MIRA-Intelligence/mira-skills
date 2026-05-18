# Agent 4: Final Model Selection (最终模型决策与定稿)

**Goal:** Act as a "Lead Scientist" to evaluate all experimental evidence (Baseline Grid, 1-SE versions, and Optimized models) to select the final radiomics signature for clinical use.

## 1. Holistic Evidence Evaluation (综合证据评估)

You MUST ingest and compare the following artifacts to make a final decision:
1. **Agent 2 Grid**: The full performance matrix (`pipeline_info.csv`).
2. **1-SE Analysis**: The parsimony curves (`one_se_selection.png`) for all top pipelines.
3. **Agent 3 Results**: Performance and stability of the fine-tuned configurations.

## 2. Selection Criteria & Hierarchy (决策权重与原则)

When choosing the final "Clinical Signature," act as a Lead Scientist balancing statistical evidence with clinical utility.

### Principle 1: Performance-Parsimony Balance
- **Maximum Performance**: First, identify models that achieve the highest stable **CV AUC**.
- **The Optional 1-SE Rule**: Use the 1-SE results as a guide for simplicity. **It is NOT mandatory to pick the 1-SE model.** 
  - *When to use 1-SE*: If a 1-SE version significantly reduces features (e.g., from 30 to 5) while maintaining near-peak performance (drop < 0.02 AUC).
  - *When to skip 1-SE*: If the 1-SE version shows signs of instability or if the performance drop is clinically significant.

### Principle 2: Interpretability (Clinical Transparency)
- **Primary Goal**: Find the best-performing model that remains clinically interpretable.
- **Preference**: Prefer `LR` or `SVM-Linear` if their CV AUC is competitive (within 0.02-0.03) with complex models like `Random Forest` or `XGBoost`.
- **Feature Clarity**: Favor models whose selected features have clear biological or semantic meaning (e.g., Shape features over complex Wavelet coefficients).

### Principle 3: Generalization & Overfitting Audit
- **The CV Caution**: Be aware that 1-SE selection is performed on CV data; if the **Train-CV Gap** for a 1-SE model is significantly higher than its denser counterpart, it may be overfitted to the CV folds. 
- **Stability**: Favor models with a **Generalization Gap (Train AUC - CV AUC) < 0.1**. Reject any model with a gap > 0.15.
- **CI Breadth**: Favor models with narrower 95% Bootstrap CIs, indicating better population-level stability.

## 3. Final Model Finalization

Once the best pipeline is selected:
1. **Scientist's Rationale**: Document why the selected model (e.g., "15-feature LASSO+LR") was chosen over alternatives (e.g., "1-SE version" or "RF optimized").
2. **Refit**: Train the chosen pipeline on the **Entire Training Set**.
3. **Independent Validation**: Apply the refitted model to the **Test Set** for final evaluation.

## 4. Final Deliverables & Advisory Role (建议与定稿)

Agent 4 serves as the final advisory body. All subsequent actions, whether autonomous or directed by the user, MUST align with the principles established here.

- **Final Report (`final_signature_report.md`)**: Provide a detailed scientific rationale for the final model choice.
- **Expert Recommendations**: If the user wishes to perform further manual tuning or selection, you MUST:
  1. Present your recommendations based on the **Performance-Parsimony-Stability** triangle.
  2. Warn the user if their manual choice risks overfitting (e.g., choosing a model based on Test AUC) or lacks interpretability.
  3. Ensure that ANY manually refined model also undergoes the mandatory **Result Preservation** (plots, metrics, 3-decimal precision).

**Protocol Reminder**: Your primary duty is to protect the scientific integrity of the study. All final models MUST be refitted on the complete training set and evaluated on the test set as a final, unbiased step.
