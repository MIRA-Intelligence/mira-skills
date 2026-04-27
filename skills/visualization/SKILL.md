---
name: visualization-orchestrator
description: "Master orchestrator for publication-quality scientific visualization. Guides the creation of both experimental result plots and academic flowcharts/architectures. Enforces top-tier journal aesthetics (comparable to Origin or R/ggplot2) using matplotlib and seaborn."
---

# Scientific Visualization Orchestrator (科研绘图与可视化统筹)

This skill acts as the central hub for all plotting, diagramming, and data visualization tasks in MedPilot. It ensures that every figure generated meets the rigorous aesthetic and technical standards of top-tier academic journals (e.g., Nature, Science, Cell), rivaling the output quality of professional software like OriginLab or R's `ggplot2`.

## The Visualization Philosophy (Top-Tier Journal Standards)
To achieve "Origin/R-level" aesthetics using Python (`matplotlib`/`seaborn`), you MUST adhere to the following principles across all plotting tasks:

1. **Clean & Minimalist Design (Data-to-Ink Ratio)**: 
   - Remove top and right spines (`sns.despine()`).
   - Avoid unnecessary grid lines, 3D effects, and background colors.
   - Use clean, white backgrounds with high-contrast elements.
2. **Professional Typography**: 
   - Use sans-serif fonts (Arial, Helvetica) for maximum legibility.
   - Ensure font sizes are readable at the final print size (e.g., 8-10pt for labels, 6-8pt for ticks).
3. **Colorblind-Safe Palettes**: 
   - Never use the `jet` or rainbow colormap.
   - Always use perceptually uniform sequential maps (e.g., `viridis`, `plasma`) or colorblind-safe categorical palettes (e.g., the Okabe-Ito palette, Paul Tol).
4. **Statistical Rigor**:
   - Always include error bars (clearly stating whether they are SD, SEM, or 95% CI).
   - Mark statistical significance correctly (e.g., `* p < 0.05`, `** p < 0.01`).
   - For small sample sizes, overlay individual data points (e.g., using `sns.stripplot` over boxplots).
5. **Vector Formats**: 
   - Always export plots in vector formats (`.pdf`, `.svg`, or `.eps`) for manuscripts, alongside high-DPI (300+) raster formats (`.png`) for quick previews.

---

## The Two Core Visualization Tracks

Scientific papers generally require two types of figures. Depending on the user's request, delegate the task to the appropriate sub-skill:

### Track 1: Experimental Data Plots (实验结果图)
* **Objective**: Visualize empirical data, statistical relationships, distributions, and comparisons.
* **Primary Skill**: **`scientific-visualization`** (Built heavily on `matplotlib` and `seaborn`).
* **Use Cases**:
  - Bar charts with error bars and significance brackets.
  - Kaplan-Meier survival curves.
  - Heatmaps for correlation matrices or gene expression (RNA-seq).
  - Multi-panel figures (e.g., Figure 1A, 1B, 1C) combined seamlessly.
* **Workflow**: 
  - Load data via `pandas`.
  - Apply publication styles (e.g., `style_presets.py`).
  - Plot using `seaborn` for statistical aggregations or `matplotlib` for fine-grained control.
  - Export using `figure_export.py`.

### Track 2: Academic Flowcharts & Architectures (学术流程图/网络结构图)
* **Objective**: Visually explain study designs, clinical workflows, algorithm pipelines, or deep learning network architectures.
* **Primary Skill**: **`scientific-schematics`** (For AI generation) OR **`scientific-visualization`** (For strict programmatic control).
* **Implementation Strategy**:
  - **Programmatic Drawing (No-AI, Zero Overlap Guarantee)**: When drawing pure Python flowcharts via `matplotlib`, NEVER manually place `Rectangle` patches. Read `scientific-visualization/references/layout_and_overlap_optimization.md`. 
    - Use `ax.text(..., bbox=dict(...))` which mathematically guarantees text is perfectly centered within an auto-scaling box.
    - Use `ax.annotate('', xy=..., xytext=..., arrowprops=dict(shrinkA=15, shrinkB=15))` so arrows automatically maintain a perfect distance from the boxes without piercing them.
    - For Deep Learning architectures, use `networkx.multipartite_layout()` to compute collision-free x/y coordinates before drawing the boxes.
  - **AI Generation (For Conceptual Rapid Prototyping)**: Use the AI-driven `scientific-schematics` generation scripts (Nano Banana 2) for highly complex, organic, or conceptual biological pathways where programmatic drawing is too tedious.

---

## Sub-Skills & Toolkits Reference

1. **`scientific-visualization`**: The main pipeline for formatting and exporting data plots. Contains journal-specific templates (Nature, Science, Cell), helper scripts for multi-panel assembly, and **the `adjustText` toolkit** to algorithmically prevent text labels from overlapping on scatter plots (like Volcano plots).
2. **`scientific-schematics`**: The pipeline for generating workflow diagrams, CONSORT flowcharts, and neural network architectures.
3. **`matplotlib`**: The foundational low-level engine. Used when absolute pixel-perfect control is needed over subplots, custom legends, or non-standard visual layouts.
4. **`seaborn`**: The high-level statistical plotting engine. Highly recommended for distributions (violin, box, KDE) and relational data, as it inherently aligns with R/ggplot2's declarative syntax and aesthetic defaults.

## Task-to-Skill Mapping Examples

- **User**: "Plot a boxplot of tumor volumes between the control and treatment groups, and add p-value stars."
  - **Action**: Use **`scientific-visualization`** (via `seaborn`). Apply Okabe-Ito colors, overlay a stripplot to show individual points, and draw significance lines using matplotlib.
- **User**: "I need a figure showing the UNet architecture we used for the segmentation task."
  - **Action**: Use **`scientific-schematics`**. Write a Python script using matplotlib patches to draw the encoder-decoder blocks with skip connections, or call the AI generation tool for a quick graphical abstract.
- **User**: "Combine my ROC curve, Confusion Matrix, and Calibration plot into a single Figure 1."
  - **Action**: Use **`matplotlib`**'s `GridSpec` or `subplot_mosaic` to assemble the multi-panel figure, labeling them A, B, and C with bold sans-serif fonts, and export to PDF.