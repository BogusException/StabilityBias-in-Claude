#!/usr/bin/env python3
"""
Generate visualization graphs for the Stability Bias experiment results.
Outputs PNG files to the same directory.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Create results directory if needed
results_dir = Path(__file__).parent.parent / "results"
results_dir.mkdir(exist_ok=True)

# ============================================================================
# GRAPH 1: Success Rate - With vs Without Active Signaling
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

conditions = ['With Active\nSignaling\n(Phase 1)', 'Without Signaling\n(Solution 1 Test)']
success_rates = [100, 0]
colors = ['#2ecc71', '#e74c3c']

bars = ax.bar(conditions, success_rates, color=colors, width=0.5, edgecolor='black', linewidth=2)

# Add value labels on bars
for bar, rate in zip(bars, success_rates):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{rate}%\n({int(rate/100 * 15)}/15)' if rate > 0 else '0%\n(0/10)',
            ha='center', va='bottom', fontsize=14, fontweight='bold')

ax.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Stability Bias: Active Signaling vs Passive Reminders', fontsize=14, fontweight='bold')
ax.set_ylim(0, 120)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig(results_dir.parent / 'graph_1_signaling_impact.png', dpi=300, bbox_inches='tight')
print("✓ Graph 1: graph_1_signaling_impact.png")

# ============================================================================
# GRAPH 2: Solution Effectiveness Ranking (10 Solutions)
# ============================================================================
solutions_data = [
    {'name': '1: Hook\nReminder', 'effectiveness': 0, 'category': 'Passive', 'color': '#e74c3c'},
    {'name': '2: Background\nAgent', 'effectiveness': 20, 'category': 'Passive', 'color': '#e74c3c'},
    {'name': '3: Skill\nWrapper', 'effectiveness': 60, 'category': 'Enforcement', 'color': '#3498db'},
    {'name': '4: Context\nInflation', 'effectiveness': 10, 'category': 'Passive', 'color': '#e74c3c'},
    {'name': '5: Scheduled\nCheck-ins', 'effectiveness': 15, 'category': 'Passive', 'color': '#e74c3c'},
    {'name': '6: MCP State\nTracking', 'effectiveness': 25, 'category': 'Passive', 'color': '#e74c3c'},
    {'name': '7: File\nWatcher', 'effectiveness': 20, 'category': 'Passive', 'color': '#e74c3c'},
    {'name': '8: Token Cost\nVisibility', 'effectiveness': 75, 'category': 'Passive', 'color': '#f39c12'},
    {'name': '9: Git\nValidation', 'effectiveness': 99, 'category': 'Enforcement', 'color': '#2ecc71'},
    {'name': '10: Behavioral\nFraming', 'effectiveness': 30, 'category': 'Passive', 'color': '#e74c3c'},
]

fig, ax = plt.subplots(figsize=(14, 7))

solutions = [s['name'] for s in reversed(solutions_data)]
effectiveness = [s['effectiveness'] for s in reversed(solutions_data)]
colors = [s['color'] for s in reversed(solutions_data)]

bars = ax.barh(solutions, effectiveness, color=colors, edgecolor='black', linewidth=1.5)

# Add value labels
for i, (bar, eff) in enumerate(zip(bars, effectiveness)):
    ax.text(eff + 2, i, f'{eff}%', va='center', fontsize=11, fontweight='bold')

ax.set_xlabel('Estimated Effectiveness (%)', fontsize=12, fontweight='bold')
ax.set_title('Solution Effectiveness Ranking (Phase 2 Analysis)', fontsize=14, fontweight='bold')
ax.set_xlim(0, 110)
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add legend
enforcement_patch = mpatches.Patch(color='#2ecc71', label='Enforcement', edgecolor='black', linewidth=1)
high_passive_patch = mpatches.Patch(color='#f39c12', label='High Passive', edgecolor='black', linewidth=1)
low_passive_patch = mpatches.Patch(color='#e74c3c', label='Low Passive', edgecolor='black', linewidth=1)
ax.legend(handles=[enforcement_patch, high_passive_patch, low_passive_patch], loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig(results_dir.parent / 'graph_2_solution_ranking.png', dpi=300, bbox_inches='tight')
print("✓ Graph 2: graph_2_solution_ranking.png")

# ============================================================================
# GRAPH 3: Cost vs Effectiveness (Top 3 Solutions)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 7))

top_solutions = [
    {'name': 'Solution A:\nCLAUDE.md', 'cost': 0.00023, 'effectiveness': 75},
    {'name': 'Solution B:\nGit Validation', 'cost': 0.62, 'effectiveness': 99},
    {'name': 'Solution C:\nToken Visibility', 'cost': 0.47, 'effectiveness': 85},
]

names = [s['name'] for s in top_solutions]
costs = [s['cost'] for s in top_solutions]
effectiveness = [s['effectiveness'] for s in top_solutions]
colors_scatter = ['#3498db', '#2ecc71', '#f39c12']

scatter = ax.scatter(costs, effectiveness, s=800, c=colors_scatter, edgecolor='black', linewidth=2, alpha=0.7)

# Add labels to points
for i, (name, cost, eff) in enumerate(zip(names, costs, effectiveness)):
    ax.annotate(name, (cost, eff), fontsize=11, fontweight='bold',
                ha='center', va='center')

ax.set_xlabel('Annual Cost (USD)', fontsize=12, fontweight='bold')
ax.set_ylabel('Estimated Effectiveness (%)', fontsize=12, fontweight='bold')
ax.set_title('Cost-Effectiveness Trade-off: Top 3 Solutions', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Log scale for cost axis makes more sense given the range
ax.set_xscale('log')

plt.tight_layout()
plt.savefig(results_dir.parent / 'graph_3_cost_effectiveness.png', dpi=300, bbox_inches='tight')
print("✓ Graph 3: graph_3_cost_effectiveness.png")

# ============================================================================
# GRAPH 4: Annual Cost Breakdown (Token Usage)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

top_solutions_detailed = [
    {'name': 'Solution A:\nCLAUDE.md', 'setup': 50, 'annual': 0.00023, 'overhead': 0},
    {'name': 'Solution B:\nGit Validation', 'setup': 200, 'annual': 0.62, 'per_change': 80},
    {'name': 'Solution C:\nToken Cost\nVisibility', 'setup': 25, 'annual': 0.47, 'per_display': 50},
]

names_detail = [s['name'] for s in top_solutions_detailed]
annual_costs = [s['annual'] for s in top_solutions_detailed]
colors_bar = ['#3498db', '#2ecc71', '#f39c12']

bars = ax.bar(names_detail, annual_costs, color=colors_bar, edgecolor='black', linewidth=2, width=0.6)

# Add value labels
for bar, cost in zip(bars, annual_costs):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'${cost:.5f}/yr',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Annual Cost (USD)', fontsize=12, fontweight='bold')
ax.set_title('Annual Token Cost for Top 3 Solutions\n(Assuming 100 changes/week = 5,200/year)',
             fontsize=13, fontweight='bold')
ax.set_ylim(0, max(annual_costs) * 1.15)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add reference line for forgotten commit cost
forgotten_cost = 0.54
ax.axhline(y=forgotten_cost, color='red', linestyle='--', linewidth=2, alpha=0.7, label=f'Annual Forgetting Cost: ${forgotten_cost:.2f}')
ax.legend(fontsize=10, loc='upper left')

plt.tight_layout()
plt.savefig(results_dir.parent / 'graph_4_annual_costs.png', dpi=300, bbox_inches='tight')
print("✓ Graph 4: graph_4_annual_costs.png")

# ============================================================================
# GRAPH 5: Phase 1 Success Timeline (15 Changes)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 5))

changes = list(range(1, 16))
results = [1] * 15  # All successful

colors_timeline = ['#2ecc71' if r == 1 else '#e74c3c' for r in results]
bars = ax.bar(changes, results, color=colors_timeline, edgecolor='black', linewidth=1.5, width=0.8)

# Add checkmarks
for i, (change, result) in enumerate(zip(changes, results)):
    ax.text(change, 0.5, '✓', ha='center', va='center', fontsize=16, fontweight='bold', color='white')

ax.set_xlabel('Sequential File Changes', fontsize=12, fontweight='bold')
ax.set_ylabel('Status', fontsize=12, fontweight='bold')
ax.set_title('Phase 1 Baseline: 15 Sequential Changes with Active Signaling\nResult: 100% Success (15/15)',
             fontsize=13, fontweight='bold')
ax.set_ylim(0, 1.2)
ax.set_xticks(changes)
ax.set_yticks([])

plt.tight_layout()
plt.savefig(results_dir.parent / 'graph_5_phase1_timeline.png', dpi=300, bbox_inches='tight')
print("✓ Graph 5: graph_5_phase1_timeline.png")

# ============================================================================
# GRAPH 6: Solution Category Distribution
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 7))

categories = ['Enforcement\n(2)', 'High Passive\n(1)', 'Low Passive\n(7)']
counts = [2, 1, 7]
colors_cat = ['#2ecc71', '#f39c12', '#e74c3c']
explode = (0.05, 0.1, 0)

wedges, texts, autotexts = ax.pie(counts, labels=categories, autopct='%1.0f%%',
                                     colors=colors_cat, explode=explode,
                                     startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'},
                                     wedgeprops={'edgecolor': 'black', 'linewidth': 2})

ax.set_title('Solution Distribution by Category\n(10 Solutions Analyzed)',
             fontsize=14, fontweight='bold')

# Add legend with descriptions
enforcement_desc = 'Solutions 3, 9\nForce action at tool level'
high_passive_desc = 'Solution 8\nFinancial transparency'
low_passive_desc = 'Solutions 1,2,4,5,6,7,10\nReminders & suggestions'

legend_labels = [f'{categories[0].split(chr(10))[0]}\n{enforcement_desc}',
                 f'{categories[1].split(chr(10))[0]}\n{high_passive_desc}',
                 f'{categories[2].split(chr(10))[0]}\n{low_passive_desc}']

ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(0.85, 1), fontsize=9)

plt.tight_layout()
plt.savefig(results_dir.parent / 'graph_6_category_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Graph 6: graph_6_category_distribution.png")

print("\n" + "="*60)
print("All graphs generated successfully!")
print("="*60)
print(f"\nOutput location: {results_dir.parent}/")
print("\nGenerated files:")
print("  - graph_1_signaling_impact.png")
print("  - graph_2_solution_ranking.png")
print("  - graph_3_cost_effectiveness.png")
print("  - graph_4_annual_costs.png")
print("  - graph_5_phase1_timeline.png")
print("  - graph_6_category_distribution.png")
