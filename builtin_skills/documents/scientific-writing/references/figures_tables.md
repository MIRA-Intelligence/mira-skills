# Figures and Tables Best Practices

Guide for creating effective data visualizations and tabular presentations for scientific manuscripts.

## 1. Core Principles

**Self-Explanatory**: Every figure and table should be understandable without referring to the main text. This requires complete titles, comprehensive legends, and clearly defined abbreviations in captions.

**Data-to-Ink Ratio**: Maximize the ratio of "data ink" to "total ink." Avoid unnecessary gridlines, borders, background shading, or decorative elements.

**Consistency**: Use the same fonts, colors, and line weights across all display items in a manuscript. Maintain consistent terminology and notation.

**Accuracy**: Ensure data plotted in figures matches the values in tables and text perfectly. Check axes scales for appropriate representation (avoid misleading truncations).

## 2. When to Use What

| Feature | Tables | Figures |
|---------|--------|---------|
| Purpose | Present precise numerical values | Show trends, patterns, relationships |
| Complexity | Handles many variables/dimensions | Best for 2-3 main variables |
| Interaction | Reader looks up specific values | Reader interprets visual patterns |
| Data Type | Summary stats, large datasets | Time series, correlations, distributions |

## 3. Designing Effective Tables

**Structure:**
- **Table Number and Title**: Descriptive title above the table.
- **Stub Head**: Label for the leftmost column (the independent variable).
- **Column Heads**: Labels for data columns with units in parentheses.
- **Body**: The actual data, logically ordered.
- **Footnotes**: Define abbreviations, statistical symbols (*p* values), and data sources below the table.

**Formatting:**
- Use horizontal lines to separate headers and totals; avoid vertical lines.
- Align numbers by decimal points.
- Use a consistent number of decimal places for similar data.
- Avoid large blocks of empty cells (use "n/a" or "-" with explanation).
- Group related rows using subheadings or whitespace.

## 4. Designing Effective Figures

**General Guidelines:**
- **Resolution**: Minimum 300 DPI for photographs, 600-1200 DPI for line art.
- **Fonts**: Use sans-serif (Arial, Helvetica) for readability; keep sizes between 8-12pt in final publication size.
- **Captions**: Positioned *below* the figure. Include a descriptive title and enough detail to interpret the figure.
- **Axes**: Label clearly with variable name and units (e.g., "Concentration (mg/dL)").
- **Accessibility**: Use high-contrast colors and patterns. Ensure figures are colorblind-friendly (avoid red-green combinations).

**Common Figure Types and Tips:**
- **Bar Graphs**: Start y-axis at zero. Use for comparing discrete categories.
- **Line Graphs**: Best for time series or continuous variables. Distinguish lines using different markers and styles.
- **Scatterplots**: Show individual data points to reveal correlations and variance. Add trend lines only if statistically justified.
- **Box Plots**: Excellent for showing distributions, medians, and outliers simultaneously.
- **Heatmaps**: Use perceptually uniform color scales (e.g., Viridis, Magma) rather than rainbow gradients.

## 5. Statistical Annotation

- **P-values**: Use standard markers (* for p < 0.05, ** for p < 0.01, *** for p < 0.001) or report exact p-values.
- **Error Bars**: Explicitly state if they represent Standard Deviation (SD), Standard Error (SEM), or Confidence Intervals (CI).
- **Sample Size**: Always report 'n' for each group in the caption or legend.

## 6. Integration Checklist

- [ ] Does the text refer to every figure and table by number (e.g., "See Table 1")?
- [ ] Are all abbreviations used in the figure/table defined in the caption?
- [ ] Do values in the text match values in the figures and tables?
- [ ] Consistent formatting across all display items?
- [ ] All display items necessary (each tells important part of story)?
- [ ] Visual style matches target journal?
- [ ] Quality comparable to published examples in journal?
