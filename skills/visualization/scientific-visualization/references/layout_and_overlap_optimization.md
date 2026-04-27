# Layout and Overlap Optimization (Origin/R Aesthetics)

When generating programmatic diagrams and data plots without multimodal AI feedback, pure Python code can easily result in overlapping text, misaligned boxes, and ugly arrows. Follow these strict rules to achieve pixel-perfect, Origin/ggplot2-level aesthetics automatically.

## 1. Fixing Misaligned Flowcharts (Academic Diagrams)

**Problem:** Drawing a `matplotlib.patches.Rectangle` and then trying to place `ax.text()` inside it requires manual coordinate guessing, which always fails when text length changes, leading to text spilling out of boxes.
**Solution:** NEVER draw boxes manually. Use the `bbox` property of `ax.text`. Matplotlib will automatically calculate the exact dimensions to perfectly center the text, no matter how long the string is.

```python
# THE WRONG WAY (Will misalign and overlap):
# ax.add_patch(Rectangle((0,0), width=2, height=1))
# ax.text(1, 0.5, "My Long Text Here", ha='center', va='center')

# THE RIGHT WAY (Perfectly centered and auto-scaled):
box_style = dict(boxstyle="round,pad=0.6", facecolor="#E69F00", edgecolor="black", linewidth=1.5)
ax.text(0.5, 0.8, "Assessed for eligibility (n=500)", 
        ha="center", va="center", fontsize=12, bbox=box_style)
```

## 2. Fixing Arrow Penetration and Distances

**Problem:** Arrows overlap with the text or pierce into the boxes, making the diagram look sloppy.
**Solution:** Use `ax.annotate` with `shrinkA` and `shrinkB`. This automatically pulls the start and end points of the arrow back by a specified number of points, leaving a clean, professional gap between the box and the arrow.

```python
# Shrink pulls the arrow back by 20 points from the start (shrinkA) and end (shrinkB)
ax.annotate("", xy=(0.5, 0.5), xytext=(0.5, 0.8),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5, 
                            shrinkA=20, shrinkB=20))
```

## 3. Fixing Text Overlap in Data Plots (e.g., Volcano Plots, PCA)

**Problem:** When labeling specific points in scatter plots, labels overlap with each other and obscure the data points.
**Solution:** Use the **`adjustText`** library. It implements a force-directed layout algorithm to push text apart, completely eliminating overlap.

```python
from adjustText import adjust_text

texts = []
for i, txt in enumerate(labels):
    texts.append(ax.text(x[i], y[i], txt, fontsize=9))

# Magically repels texts from each other and draws lines to their original points
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
```

## 4. Drawing Deep Learning Architectures cleanly

**Problem:** Calculating x, y coordinates for UNet or ResNet layers is tedious and prone to severe overlap.
**Solution:** Use `networkx` to calculate the mathematical layout (`multipartite_layout` for layered networks), and then draw it using Matplotlib.

```python
import networkx as nx

G = nx.DiGraph()
# Add nodes with a 'layer' attribute
G.add_node("Input", layer=0)
G.add_node("Conv1", layer=1)
G.add_node("Output", layer=2)
G.add_edge("Input", "Conv1")

# NetworkX calculates perfect non-overlapping coordinates!
pos = nx.multipartite_layout(G, subset_key="layer")

# Now use the pos dictionary to place ax.text() boxes in matplotlib...
```

## 5. Achieving OriginLab / GraphPad Prism Aesthetics

To make your statistical plots look like they came from high-end software:

1. **Detached Spines**:
   Instead of just `sns.despine()`, use `sns.despine(trim=True, offset=5)`. This creates a small gap between the axes and the data, which is a hallmark of professional GraphPad/Origin plots.
2. **Axis Margins**:
   Call `ax.margins(0.05)` to ensure data points don't clip the edges of the plot.
3. **Thick Ticks, Clean Lines**:
   Set `ax.tick_params(width=1.5, length=5, direction='out')` and ensure `axes.linewidth: 1.5`.
4. **Avoid Legends Occluding Data**:
   Use `bbox_to_anchor=(1.05, 1), loc='upper left'` to move legends outside the plot.
