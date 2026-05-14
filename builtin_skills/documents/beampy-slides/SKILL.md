---
name: beampy-slides
description: LaTeX-powered presentation engine for scientific and research presentations using beampy.
---

# Scientific Beampy: High-Precision Research Presentations

`beampy-slides` is a LaTeX-powered presentation engine designed for scientists and researchers. It combines the typographic excellence of LaTeX with the flexibility of Python and the ubiquity of PowerPoint.

## Core Design Philosophy

Scientific presentations should be **VISUALLY ENGAGING** and **RESEARCH-BACKED**.
- **Compelling Visuals**: Use high-quality figures, diagrams, and plots. Avoid text-heavy slides.
- **Research Context**: Always include proper citations (use `literature-search` or web search).
- **Minimal Text**: Use text as prompts; you provide the explanation verbally.
- **Story-Driven**: Follow a clear narrative arc (Hook -> Context -> Problem -> Approach -> Results -> Implications).

## Quick Start

```python
import sys
from pathlib import Path
from beampy import document, slide, text, figure
from beampy_adapter import export_beampy_to_editable_pptx

# Setup Document (Default 16:9 is 1280x720 in the adapter)
doc = document(width=800, height=450, cache=True)

with slide("Scientific Methodology"):
    text(r"Our model uses the Navier-Stokes equations:", x=50, y=50, size=24)
    text(r"$\rho \left( \frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} \right) = -\nabla p + \mu \nabla^2 \mathbf{u} + \mathbf{f}$",
         x='center', y=150, size=30, color='DarkBlue')
    
    # Add a citation (found via literature-search)
    text(r"(Source: Smith et al., Nature 2024)", x=50, y=400, size=14, color='gray')

# Export to Hybrid PPTX (Native Shapes for Math/Graphics, Editable Textboxes for Text)
export_beampy_to_editable_pptx("presentation.pptx")
```

## Scientific Workflow

### 1. Data-Driven Figures
Use the `visualization` skill to create professional plots. `beampy` natively supports Matplotlib figures.

```python
import matplotlib.pyplot as plt
import pandas as pd

# Load data from CSV
df = pd.read_csv("results.csv")

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(df['x'], df['y'], label='Experimental Data', color='red', linewidth=2)
ax.set_title("Result Comparison")
ax.legend()

with slide("Results Analysis"):
    figure(fig, x=400, y=100, width=350)
    text("Key Finding: Observed 15% increase in efficiency.", x=50, y=150, width=300)
```

### 2. Extracting Context from PDFs
Use PDF tools to extract text or images from your papers to include as background or reference material.

### 3. Literature-Backed Content
Before writing slides, use the `literature-search` skill to:
- Find 5-10 key papers for context.
- Identify knowledge gaps.
- Gather supporting citations.
- Find comparison studies.

## Technical Reference

### Beampy Basics
- `text(string, x, y, size, color, width, align)`: LaTeX-enabled text. Use `r"..."`.
- `figure(mpl_fig, x, y, width, height)`: Embed Matplotlib plots.
- `latex2svg(latex_str)`: Render raw LaTeX to SVG.
- `rectangle(x, y, width, height, color)`: Draw shapes.
- `position(x, y)`: Relative positioning using `x='center'`, `y='center'`, or relative to other elements.

### LaTeX Character Escaping & Text Handling
Because `beampy` uses a LaTeX engine, special characters must be escaped even in plain text strings to prevent compilation errors or incorrect "math" detection.

- **Always use raw strings**: `text(r"Content...", ...)`
- **Escape Special Characters**: Use `\&`, `\%`, `\_`, `\#` for their respective symbols.
- **Editable Text vs. Math**:
  - The adapter is smart: basic escapes (like `\&`) and formatting (like `\textbf{...}`) are treated as **Plain Text** and exported as **Editable PPTX Textboxes**.
  - Complex math (containing `$`, `\frac`, `\sum`, etc.) is treated as **Vector Math** and exported as **High-Precision Shapes**.
- **Automatic Cleanup**: The adapter automatically unescapes these characters (e.g., `\&` becomes `&`) in the final PowerPoint textboxes, so your slides look professional and stay editable.

### Advanced Layout
Use relative units and anchors to ensure elements stay aligned even if content changes.
```python
t1 = text("Primary Goal", x=50, y=50)
t2 = text("Secondary Goal", x=50, y=t1.y + 50) # Relative Y
```

## Export Options
- `export_beampy_to_editable_pptx(filename)`: The recommended "Smart Hybrid" export.
  - **Math/Equations**: Converted to high-quality native PowerPoint Shapes (Vector).
  - **Text**: Converted to native PowerPoint Textboxes (Editable).
  - **Images/Plots**: Embedded as high-res images.

## Scientific Guides
Refer to these guides (moved from scientific-slides) for deeper insights:
- `references/presentation_structure.md`: How to structure different talk types.
- `references/slide_design_principles.md`: Typography, color, and layout for science.
- `references/data_visualization_slides.md`: How to simplify journal figures for slides.
- `references/talk_types_guide.md`: Guidance for conferences, seminars, and defenses.
- `references/visual_review_workflow.md`: Systematic way to check your slides.

## Debugging & Intermediate Files

If you encounter layout issues, you can inspect the intermediate SVG files generated in the `beampy_debug_svgs/` directory:

- **`native_pXX.svg`**: The original, full-vector SVG produced by Beampy. This contains the "ground truth" layout, including all text rendered as vector paths. Use this to verify if Beampy itself rendered the slide correctly.
- **`wrapped_pXX.svg`**: The "headless" version used for PowerPoint injection. It has plain text removed (because it's replaced by editable textboxes) and optimized grouping.

### System Requirements
Ensure `latex` and `dvisvgm` are in your PATH. If math symbols are missing, check if the required TeX packages are installed.

## Alternative: Pure LaTeX Beamer Workflow
If you prefer writing raw LaTeX Beamer instead of Python, use the high-quality templates in `assets/`:
- `assets/beamer_template_conference.tex`: 15-minute conference talk.
- `assets/beamer_template_seminar.tex`: 45-minute academic seminar.
- `assets/beamer_template_defense.tex`: Dissertation defense.

See `references/beamer_guide.md` for full documentation on Beamer themes and compilation.
