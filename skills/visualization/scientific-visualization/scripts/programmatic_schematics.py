#!/usr/bin/env python3
"""
Programmatic Schematics & Origin-Style Plots

Demonstrates how to generate overlap-free flowcharts, neural network architectures,
and data plots using pure Python (without multimodal AI).
"""

import matplotlib.pyplot as plt
import numpy as np

def draw_consort_flowchart():
    """
    Draws a CONSORT flowchart using bbox text properties and shrink arrows.
    Guarantees perfect centering and no overlaps.
    """
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis('off')
    
    # Define styles
    blue_box = dict(boxstyle="round,pad=0.6", facecolor="#56B4E9", edgecolor="black", lw=1.5, alpha=0.9)
    orange_box = dict(boxstyle="round,pad=0.6", facecolor="#E69F00", edgecolor="black", lw=1.5, alpha=0.9)
    green_box = dict(boxstyle="round,pad=0.6", facecolor="#009E73", edgecolor="black", lw=1.5, alpha=0.9)
    
    # 1. Draw text nodes (Auto-calculates box sizes to prevent text spilling!)
    ax.text(0.5, 0.9, "Assessed for eligibility (n=500)", ha="center", va="center", bbox=blue_box, fontsize=11, fontweight='bold')
    
    # Excluded box offset to the right
    ax.text(0.8, 0.75, "Excluded (n=150)\n• Not meeting criteria (n=80)\n• Declined (n=50)\n• Other (n=20)", 
            ha="left", va="center", bbox=orange_box, fontsize=9)
            
    ax.text(0.5, 0.6, "Randomized (n=350)", ha="center", va="center", bbox=blue_box, fontsize=11, fontweight='bold')
    
    # Two arms
    ax.text(0.25, 0.4, "Treatment Arm (n=175)", ha="center", va="center", bbox=green_box, fontsize=10)
    ax.text(0.75, 0.4, "Control Arm (n=175)", ha="center", va="center", bbox=green_box, fontsize=10)
    
    ax.text(0.25, 0.2, "Analyzed (n=170)\nLost to follow-up (n=5)", ha="center", va="center", bbox=blue_box, fontsize=9)
    ax.text(0.75, 0.2, "Analyzed (n=165)\nLost to follow-up (n=10)", ha="center", va="center", bbox=blue_box, fontsize=9)

    # 2. Draw connecting arrows using shrink to avoid piercing the boxes
    arrow_kws = dict(arrowstyle="->", color="black", lw=1.5, shrinkA=20, shrinkB=20)
    
    # Vertical main flow
    ax.annotate("", xy=(0.5, 0.6), xytext=(0.5, 0.9), arrowprops=arrow_kws)
    
    # Branch to excluded (requires a right angle, we use standard connection style)
    ax.annotate("", xy=(0.78, 0.75), xytext=(0.5, 0.75), 
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5, shrinkA=0, shrinkB=10))
                
    # Branching to arms (angle A and B define the elbow path)
    ax.annotate("", xy=(0.25, 0.4), xytext=(0.5, 0.6), arrowprops=dict(arrowstyle="->", color="black", lw=1.5, shrinkA=15, shrinkB=15, connectionstyle="angle,angleA=-90,angleB=90,rad=10"))
    ax.annotate("", xy=(0.75, 0.4), xytext=(0.5, 0.6), arrowprops=dict(arrowstyle="->", color="black", lw=1.5, shrinkA=15, shrinkB=15, connectionstyle="angle,angleA=-90,angleB=90,rad=10"))
    
    # Down to analysis
    ax.annotate("", xy=(0.25, 0.2), xytext=(0.25, 0.4), arrowprops=arrow_kws)
    ax.annotate("", xy=(0.75, 0.2), xytext=(0.75, 0.4), arrowprops=arrow_kws)
    
    plt.tight_layout()
    plt.savefig('consort_programmatic.pdf', dpi=300)
    print("Saved consort_programmatic.pdf")

def draw_network_architecture():
    """
    Uses NetworkX to calculate optimal, non-overlapping coordinates for a Neural Network,
    then draws it with Matplotlib.
    """
    try:
        import networkx as nx
    except ImportError:
        print("Warning: networkx not installed. Run `pip install networkx`")
        return
        
    G = nx.DiGraph()
    # Define layers
    layers = {
        "Input\n(1x128x128)": 0,
        "Conv1\n(16)": 1,
        "Conv2\n(32)": 2,
        "Pool\n(32)": 3,
        "FC1\n(128)": 4,
        "Output\n(2)": 5
    }
    
    for node, layer in layers.items():
        G.add_node(node, layer=layer)
        
    # Connect sequentially
    nodes = list(layers.keys())
    for i in range(len(nodes)-1):
        G.add_edge(nodes[i], nodes[i+1])
        
    # Calculate non-overlapping layout automatically
    pos = nx.multipartite_layout(G, subset_key="layer")
    
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('off')
    
    box_style = dict(boxstyle="square,pad=0.5", facecolor="#E69F00", edgecolor="black", lw=1.5)
    
    # Draw nodes
    for node, coords in pos.items():
        ax.text(coords[0], coords[1], node, ha="center", va="center", bbox=box_style, fontsize=10, fontweight='bold')
        
    # Draw edges
    for edge in G.edges():
        start = pos[edge[0]]
        end = pos[edge[1]]
        ax.annotate("", xy=end, xytext=start, 
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5, shrinkA=35, shrinkB=35))

    plt.tight_layout()
    plt.savefig('architecture_programmatic.pdf', dpi=300)
    print("Saved architecture_programmatic.pdf")

def draw_origin_style_scatter():
    """
    Demonstrates OriginLab/ggplot2 style aesthetics and adjustText to prevent overlapping.
    """
    try:
        from adjustText import adjust_text
    except ImportError:
        print("Warning: adjustText not installed. Run `pip install adjustText`")
        return
        
    import seaborn as sns
    
    # Generate mock Volcano plot data
    np.random.seed(42)
    log2fc = np.random.normal(0, 2, 200)
    pval = -np.log10(np.random.uniform(0.0001, 1, 200))
    
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Plot background points
    ax.scatter(log2fc, pval, color="lightgray", alpha=0.6, edgecolors="none", s=30)
    
    # Highlight significant points
    sig_mask = (np.abs(log2fc) > 2) & (pval > 2)
    ax.scatter(log2fc[sig_mask], pval[sig_mask], color="#D55E00", alpha=0.9, edgecolors="black", lw=0.5, s=40)
    
    # Add non-overlapping labels
    texts = []
    for i in np.where(sig_mask)[0][:10]: # Label top 10
        texts.append(ax.text(log2fc[i], pval[i], f"Gene_{i}", fontsize=8, fontweight='bold'))
        
    # MAGIC: Adjust text to prevent any overlap
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black', lw=0.5), ax=ax)
    
    # Apply Origin/Prism-like aesthetics
    ax.axvline(0, color='black', linestyle='--', lw=1, alpha=0.5)
    ax.axhline(2, color='black', linestyle='--', lw=1, alpha=0.5)
    
    ax.set_xlabel("Log2 Fold Change", fontweight='bold')
    ax.set_ylabel("-Log10 P-value", fontweight='bold')
    
    # Detach spines for professional look
    sns.despine(trim=True, offset=5)
    ax.margins(0.05)
    
    plt.tight_layout()
    plt.savefig('volcano_origin_style.pdf', dpi=300)
    print("Saved volcano_origin_style.pdf")

if __name__ == "__main__":
    draw_consort_flowchart()
    draw_network_architecture()
    draw_origin_style_scatter()