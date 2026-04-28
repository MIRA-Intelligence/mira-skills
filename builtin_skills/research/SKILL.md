---
name: research-orchestrator
description: "Master orchestrator for the entire scientific research lifecycle. Guides the iterative process from literature search and review, to hypothesis generation and experimental design (scientific method), manuscript writing, and rigorous peer review. Orchestrates tools like visualization for plotting."
---

# Scientific Research Orchestrator (科研全流程统筹)

This skill acts as the central orchestrator for the entire scientific research lifecycle in MedPilot. It enforces a highly rigorous, cyclical, and iterative process designed to produce high-quality, innovative academic outcomes.

## The Iterative Scientific Lifecycle

The research process is never linear. It is a continuous loop of discovery, validation, and refinement. When executing a research project, follow this 5-stage lifecycle.

### 1. Discovery & Gap Identification (Literature Search & Review)
* **Objective**: Understand the state-of-the-art and identify meaningful knowledge gaps.
* **Skills Used**: 
  - **`literature-search`**: Gather papers across PubMed, ArXiv, Zotero, and general web search engines.
  - **`literature-review`**: Synthesize the gathered literature into a structured review or deep-dive report. Identify controversies, consensus, and missing links.

### 2. Hypothesis & Experimental Design (Scientific Method)
* **Objective**: Transform a knowledge gap into a testable, falsifiable hypothesis and plan the experiment.
* **Skill Used**: **`scientific-method`**
* **Workflow**: 
  - *Observe* the literature/data → *Question* the phenomenon → *Hypothesize* a mechanism → *Predict* specific outcomes → *Design* a controlled experiment (variables, baselines, metrics).

### 3. Execution & Analysis (Scientific Method + Visualization)
* **Objective**: Run the experiment, analyze the data, and visualize the findings.
* **Skill Used**: **`scientific-method`** (for analysis) + **`medpilot/skills/visualization`** (for plotting).
* **Workflow**: 
  - Compare empirical results against the predictions.
  - Call the `visualization` skill to generate necessary data plots, histograms, and statistical charts to make sense of the results.
  - *Iterate*: If results are unexpected, go back to step 2 to revise the hypothesis.

### 4. Manuscript Drafting (Scientific Writing)
* **Objective**: Document the finalized research in a publication-ready format.
* **Skill Used**: **`scientific-writing`**
* **Workflow**: 
  - Write in flowing prose using the standard **IMRAD** structure (Introduction, Methods, Results, And Discussion).
  - Apply proper citation styles (e.g., APA, AMA).
  - Use `visualization` to generate a **Graphical Abstract** and conceptual schematics.

### 5. Quality Control & Refinement (Peer Review)
* **Objective**: Stress-test the manuscript before actual submission to identify flaws in logic, statistics, or presentation.
* **Skill Used**: **`peer-review`**
* **Workflow**: 
  - Act as a harsh, critical reviewer. Assess methodological rigor, statistical assumptions, and potential data leakage.
  - Output a structured review report with Major and Minor comments.
  - *Iterate*: Use this feedback to return to Stage 4 (Writing), Stage 3 (More experiments), or Stage 2 (Refine hypothesis).

---

## Consolidated Skills Inventory

To reduce homogenization and improve efficiency, the research skills are categorized into the following core modules:

1. **`literature-search`** *(Merged from pubmed-search & multi-search-engine)*: The foundational tool for retrieving academic papers, guidelines, and general web knowledge without API keys.
2. **`literature-review`** *(Merged from deep-research & medical-imaging-review)*: The analytical engine that reads full texts and synthesizes systematic reviews or deep research reports using a rigorous 7-phase workflow.
3. **`scientific-method`**: The core logic engine driving the research loop (Observe → Question → Hypothesize → Predict → Test → Analyze → Iterate).
4. **`scientific-writing`**: The writing engine enforcing IMRAD, reporting guidelines (CONSORT/STROBE), and academic prose.
5. **`peer-review`**: The evaluation engine for rigorous quality assurance, checking ethics, statistics, and reporting standards.

## Cross-Skill Interaction (Important Rules)
- **Visualization is Mandatory**: Whenever data needs to be interpreted in Stage 3, or when drafting the paper in Stage 4, you MUST invoke the `medpilot/skills/visualization` skill to create high-quality plots and graphical abstracts.
- **Never Skip the Hypothesis**: Do not jump from Literature Review directly to running models. You must explicitly use the `scientific-method` skill to state the *Why* and the *Prediction* before executing code.
- **Cyclical Feedback**: If `peer-review` identifies a critical flaw (e.g., missing a baseline), you must loop back to `scientific-method` to design the new baseline experiment, execute it, and update the manuscript via `scientific-writing`.