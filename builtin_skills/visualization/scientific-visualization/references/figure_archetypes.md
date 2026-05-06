# Scientific Figure Archetypes & Architecture

Use this reference to select the visual structure of your figure based on the scientific claim.

## 1. Multi-Panel Information Architecture
Each panel must answer a unique scientific question. Covering any one panel should leave a gap that cannot be recovered from the others.

### Three-Level Progressive Complexity
| Level | Question | Encoding |
|-------|----------|----------|
| **Overview** | "What is the landscape?" | Stacked bar, composition, main effect |
| **Deviation** | "What is distinctive per group?" | Z-score heatmap, diverging RdBu_r cmap |
| **Relationship** | "How do variables co-vary?" | Bubble scatter, correlation, regression |

## 2. Page Archetypes

### Archetype A: Schematic-Led Composite
Used when a workflow, mechanism, device, or experimental design must be understood first.
- **Hero Panel**: Schematic occupying 45–60% of total height.
- **Supporting Panels**: 2–4 quantitative validation plots.
- **Rule**: Reuse colors from the schematic (physical palette) in the support plots.

### Archetype B: Dark Image Plate
Used for microscopy, volume rendering, or fluorescence-heavy data.
- **Background**: Black `facecolor` ONLY inside the image region.
- **Channels**: Grayscale context + Cyan/Magenta/White accents.
- **Rule**: Labels and scale bars must be high-contrast white. No detached legends; use direct labels.

### Archetype C: Clinical Triptych
Used for longitudinal outcomes and population summaries.
- **Top Row**: Longitudinal trend lines (shared legend above).
- **Middle Row**: Forest plots (Effect sizes) with vertical dashed reference line.
- **Bottom Row**: Summary bars (e.g., binary or stacked percentage).
- **Rule**: Columns must be semantically parallel.

### Archetype D: Asymmetric Hero Layout
Used when one panel is conceptually central and should dominate.
- **Hero Panel**: Spans multiple grid cells (e.g., a large circular genome map or a central UMAP).
- **Support Plots**: Smaller plots ranked by evidence value around the hero.

## 3. Python/R Layout Snippets

### GridSpec (Python)
```python
from matplotlib import gridspec
gs = gridspec.GridSpec(2, 2, height_ratios=[1.5, 1.0])
ax_hero = fig.add_subplot(gs[0, :])
ax_b = fig.add_subplot(gs[1, 0])
```

### Patchwork (R)
```r
library(patchwork)
design <- "
  AAAA
  BCDE
"
p_hero + p_b + p_c + p_d + p_e + plot_layout(design = design)
```
