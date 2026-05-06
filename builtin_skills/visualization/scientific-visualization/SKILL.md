name: scientific-visualization
description: "Master orchestrator for scientific visualization and data compliance. Create submission-grade figures (Python/R) including basic plots (Line, Bar, Box, Violin) and specialized clinical plots (ROC, DCA, Nomogram). Covers Nature-tier figure archetypes, multi-panel layouts, and FAIR metadata auditing."
metadata:
  scenarios: ["Manuscript figure preparation", "Clinical prediction models (ROC/DCA/Nomogram)", "Data Availability statements", "FAIR metadata auditing"]
---

# Scientific Visualization & Data Compliance

This skill acts as a master orchestrator for creating publication-grade scientific figures and ensuring research data transparency. It follows high-impact journal standards (Nature/Science/Cell) and FAIR metadata principles.

## Core Workflow: The Figure Contract

**BEFORE writing any code, establish a "Figure Contract" with the user:**
1. **Core Conclusion**: The one-sentence claim the figure defends (e.g., "Drug X improves survival by inhibiting Y").
2. **Backend Selection (BLOCKING)**: Ask "Python or R?" and stop. Do not proceed until confirmed.
3. **Archetype**: Choose from `Schematic-Led`, `Dark Image Plate`, `Clinical Triptych`, or `Asymmetric Hero`.
4. **Evidence Chain**: Map panels (a, b, c...) to unique evidence. Remove panels that do not carry a unique scientific question.

## 1. Figure Design Standards

### Mandatory Python Configuration
Guarantees editable SVG text and Nature-style aesthetics:
```python
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none' # Editable <text> nodes
plt.rcParams['font.size'] = 7        # Nature default for dense panels
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
```

### Mandatory R Configuration
```r
library(ggplot2); library(patchwork)
theme_set(theme_classic(base_size = 7, base_family = "Arial"))
```

### Palette & Encoding Policy
- **Unified Families**: Use a coherent hue family (e.g., cool blue-greys for baselines, lilac-roses for hero method).
- **Semantic Mapping**: Consistent colors across ALL panels for the same condition.
- **Directional Cues**: Reserve green and red for gains, drops, or threshold crossings only.
- **Luminance Safety**: Ensure text inside bars/cells contrasts correctly with background colors.

## 2. Data Availability & Compliance

Draft transparent statements that link manuscript claims to accessible evidence.

- **Prefer Repositories**: Use persistent identifiers (DOI/Accession) over email-based access.
- **Source Data Mapping**: Map underlying data to exact figure panels (e.g., "Source Data for Fig. 1 is in Supplementary Table 1").
- **Bilingual Terminology**: Translate intent (`数据可用性` -> `Data Availability`; `合理请求` -> `reasonable request` with explicit route).

## 3. Interactive Visualization (Plotly)

Use Plotly for exploratory analysis, supplementary web-embeddable charts, or complex 3D meshes.

- **Plotly Express (px)**: For quick, standard charts from Pandas DataFrames.
- **Graph Objects (go)**: For fine-grained control over individual traces and 3D shapes.
- **Static Snapshots**: For publication, use `fig.write_image('fig.pdf', scale=3)` (requires `kaleido`) to convert interactive plots to high-res vector files.

## 4. Export & Resolution Policy

| Target | Format | Resolution |
|--------|--------|------------|
| **Line Art / Plots** | **SVG (Primary)** / PDF | Vector (lossless) |
| **Combined Figures**| PDF / TIFF | 600 DPI |
| **Photos / Imaging**| TIFF | 300 DPI |
| **Quick Previews**  | PNG | 300 DPI |

**Anti-Pattern**: Never save text-heavy plots as JPEG. Never use `svg.fonttype = 'path'`.

## Internal References

| Reference | Use when... |
|-----------|-----------|
| [references/figure_archetypes.md](references/figure_archetypes.md) | Designing multi-panel layouts and selecting evidence hierarchies. |
| [references/data_availability_patterns.md](references/data_availability_patterns.md) | Drafting Data Availability statements for manuscript submissions. |
| [references/data_compliance_alignment.md](references/data_compliance_alignment.md) | Aligning Chinese terms to EN or running a FAIR metadata audit. |
| [references/color_palettes.md](references/color_palettes.md) | Selecting Okabe-Ito or NMI-style colorblind-safe hex codes. |
| [references/journal_requirements.md](references/journal_requirements.md) | Checking specific column widths and DPI for Nature/Science/Cell. |
| [references/matplotlib_examples.md](references/matplotlib_examples.md) | Implementing specific plot types like heatmaps or shaded trends. |
| [references/specialized_plots.md](references/specialized_plots.md) | Creating clinical plots like ROC, DCA, Nomograms, and Calibration curves. |

## Validation Checklist
- [ ] Figure Contract established and claim is a complete sentence?
- [ ] Backend exclusivity: All visual output produced by the selected runtime?
- [ ] Font size 5-7pt for dense journal figures?
- [ ] SVG/PDF text remains selectable/editable?
- [ ] Panel labels (a, b, c) are bold lowercase?
- [ ] Data Availability statement covers both new and reused data?
