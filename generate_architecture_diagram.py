"""
Generate Enhanced System Architecture Diagram for Automotive Emissions Optimization Project
Student: Hrishikesh M (22BCE0422)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.lines as mlines

# Create figure with white background
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Define colors - Professional gradient
layer_colors = {
    'layer1': '#FFF3E0',  # Warm light orange
    'layer2': '#E1F5FE',  # Light cyan
    'layer3': '#F3E5F5',  # Light purple
    'layer4': '#E8F5E9',  # Light green
    'layer5': '#FCE4EC',  # Light pink
}

border_color = '#263238'
text_color = '#263238'
arrow_color = '#37474F'
accent_color = '#00897B'

# Title with project identifier
ax.text(5, 10.5, 'Five-Layer Data Processing Architecture', 
        fontsize=18, fontweight='bold', ha='center', color=text_color)
ax.text(5, 10.15, 'Automotive Emissions & Fuel Efficiency Optimization System', 
        fontsize=11, ha='center', color='#546E7A', style='italic')

# Layer 1: Data Sources
y_pos = 8.2
layer1_box = FancyBboxPatch((1, y_pos), 8, 1.2, 
                            boxstyle="round,pad=0.08", 
                            edgecolor=border_color, facecolor=layer_colors['layer1'],
                            linewidth=2.5)
ax.add_patch(layer1_box)
ax.text(5, y_pos + 0.85, 'LAYER 1: DATA SOURCES', 
        fontsize=14, fontweight='bold', ha='center', color=text_color)

# Data source boxes - Simple
datasets = [
    ('UCI Auto MPG\n398 rows', 2.5, y_pos + 0.25),
    ('EPA Fuel Economy\n1,000 rows', 5, y_pos + 0.25),
    ('Vehicle Specs\n2,000 rows', 7.5, y_pos + 0.25)
]

for name, x, y in datasets:
    box = FancyBboxPatch((x - 0.65, y), 1.3, 0.45,
                         boxstyle="round,pad=0.05",
                         edgecolor=border_color, facecolor='white',
                         linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y + 0.225, name, fontsize=9, ha='center', va='center', 
            color=text_color, linespacing=1.4, fontweight='bold')

# Data flow arrow
arrow1 = FancyArrowPatch((5, y_pos - 0.05), (5, y_pos - 0.45),
                        arrowstyle='->', mutation_scale=30, 
                        linewidth=3, color=arrow_color)
ax.add_patch(arrow1)

# Layer 2: Data Loading
y_pos = 6.5
layer2_box = FancyBboxPatch((1, y_pos), 8, 1.2,
                            boxstyle="round,pad=0.08",
                            edgecolor=border_color, facecolor=layer_colors['layer2'],
                            linewidth=2.5)
ax.add_patch(layer2_box)
ax.text(5, y_pos + 0.85, 'LAYER 2: DATA LOADING & INTEGRATION', 
        fontsize=14, fontweight='bold', ha='center', color=text_color)

# Simple feature list
ax.text(5, y_pos + 0.3, 'Multi-format parsing • Error handling • Schema standardization', 
        fontsize=10, ha='center', color=text_color)

arrow2 = FancyArrowPatch((5, y_pos - 0.05), (5, y_pos - 0.45),
                        arrowstyle='->', mutation_scale=30,
                        linewidth=3, color=arrow_color)
ax.add_patch(arrow2)

# Layer 3: Quality Assessment
y_pos = 4.8
layer3_box = FancyBboxPatch((1, y_pos), 8, 1.2,
                            boxstyle="round,pad=0.08",
                            edgecolor=border_color, facecolor=layer_colors['layer3'],
                            linewidth=2.5)
ax.add_patch(layer3_box)
ax.text(5, y_pos + 0.85, 'LAYER 3: QUALITY ASSESSMENT', 
        fontsize=14, fontweight='bold', ha='center', color=text_color)

# Three dimensions - Simple
dimensions = [
    ('Completeness\n40%', 2.8, y_pos + 0.3),
    ('Validity\n30%', 5, y_pos + 0.3),
    ('Consistency\n30%', 7.2, y_pos + 0.3)
]

for name, x, y in dimensions:
    box = FancyBboxPatch((x - 0.55, y), 1.1, 0.4,
                         boxstyle="round,pad=0.05",
                         edgecolor=border_color, facecolor='white',
                         linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y + 0.2, name, fontsize=9, ha='center', va='center', 
            color=text_color, linespacing=1.3, fontweight='bold')

arrow3 = FancyArrowPatch((5, y_pos - 0.05), (5, y_pos - 0.45),
                        arrowstyle='->', mutation_scale=30,
                        linewidth=3, color=arrow_color)
ax.add_patch(arrow3)

# Layer 4: Data Cleaning
y_pos = 5.0
layer4_box = FancyBboxPatch((0.3, y_pos), 9.4, 0.85,
                            boxstyle="round,pad=0.08",
                            edgecolor=border_color, facecolor=layer_colors['layer4'],
                            linewidth=2)
ax.add_patch(layer4_box)
ax.text(5, y_pos + 0.6, 'LAYER 4: DATA CLEANING & TREATMENT', 
        fontsize=12, fontweight='bold', ha='center', color=text_color)

# Strategy boxes - Simple
strategies = [
    ('<5%\nDeletion', 2.5, y_pos + 0.15),
    ('5-15%\nMedian/Mode', 5, y_pos + 0.15),
    ('>15%\nKNN', 7.5, y_pos + 0.15)
]

for name, x, y in strategies:
    box = FancyBboxPatch((x - 0.55, y), 1.1, 0.4,
                         boxstyle="round,pad=0.05",
                         edgecolor=border_color, facecolor='white',
                         linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y + 0.2, name, fontsize=9, ha='center', va='center', 
            color=text_color, linespacing=1.3, fontweight='bold')

arrow4 = FancyArrowPatch((5, y_pos - 0.05), (5, y_pos - 0.45),
                        arrowstyle='->', mutation_scale=30,
                        linewidth=3, color=arrow_color)
ax.add_patch(arrow4)

# Layer 5: Visualization
y_pos = 1.4
layer5_box = FancyBboxPatch((1, y_pos), 8, 1.2,
                            boxstyle="round,pad=0.08",
                            edgecolor=border_color, facecolor=layer_colors['layer5'],
                            linewidth=2.5)
ax.add_patch(layer5_box)
ax.text(5, y_pos + 0.85, 'LAYER 5: VISUALIZATION & ANALYTICS', 
        fontsize=14, fontweight='bold', ha='center', color=text_color)

# Simple description
ax.text(5, y_pos + 0.3, 'Interactive Dashboard • Plotly • Tableau Integration', 
        fontsize=10, ha='center', color=text_color)

# Footer
ax.text(5, 0.6, 'System Architecture - Automotive Emissions Optimization',
        fontsize=12, ha='center', color=text_color, fontweight='bold')
ax.text(5, 0.3, 'Hrishikesh M (22BCE0422) | Foundation of Data Science | Professor: Kumar K | VIT',
        fontsize=9, ha='center', color='#78909C', style='italic')

plt.tight_layout()
plt.savefig('system_architecture_diagram.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("✅ System Architecture Diagram saved as 'system_architecture_diagram.png'")
print(f"   Resolution: 300 DPI | Format: PNG | Size: ~4200x3600 pixels")
