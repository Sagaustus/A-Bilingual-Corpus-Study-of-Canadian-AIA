#!/usr/bin/env python3
"""
Create publication-quality visualizations of EN/FR governance terminology disparities.
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Set style for publication
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

def load_data():
    """Load terminology analysis data."""
    with open('research/governance_terminology/full_terminology_analysis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def create_comparative_bar_chart(data, output_dir):
    """Create comparative bar chart of top governance terms."""
    
    en_totals = data['summary']['en_term_totals']
    fr_totals = data['summary']['fr_term_totals']
    
    # Key term mappings (EN -> FR equivalents)
    term_pairs = {
        'accountability': 'responsabilité',
        'oversight': 'surveillance',
        'transparency': 'transparence',
        'fairness': 'équité',
        'bias': 'biais',
        'audit': 'audit',
        'review': 'révision',
        'monitoring': 'contrôle',
        'assessment': 'évaluation',
        'explanation': 'explication'
    }
    
    # Prepare data
    categories = []
    en_counts = []
    fr_counts = []
    
    for en_term, fr_term in term_pairs.items():
        categories.append(en_term.capitalize())
        en_counts.append(en_totals.get(en_term, 0))
        fr_counts.append(fr_totals.get(fr_term, 0))
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, en_counts, width, label='English', color='#2E86AB', alpha=0.8)
    bars2 = ax.bar(x + width/2, fr_counts, width, label='French', color='#A23B72', alpha=0.8)
    
    ax.set_ylabel('Occurrences', fontweight='bold')
    ax.set_xlabel('Governance Terms', fontweight='bold')
    ax.set_title('Governance Terminology: English vs. French\nAcross 16 Bilingual AI Impact Assessments', 
                 fontweight='bold', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend(frameon=True, shadow=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    output_file = output_dir / 'fig1_comparative_terms.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Created: {output_file}")

def create_divergence_chart(data, output_dir):
    """Create chart showing largest EN/FR disparities."""
    
    en_totals = data['summary']['en_term_totals']
    fr_totals = data['summary']['fr_term_totals']
    
    # Calculate divergence ratios
    term_pairs = {
        'accountability': ('responsabilité', 'imputabilité'),
        'monitoring': ('contrôle', 'suivi'),
        'bias': ('biais', 'préjugé'),
        'fairness': ('équité',),
        'oversight': ('surveillance',),
        'transparency': ('transparence',),
        'review': ('révision', 'examen')
    }
    
    divergences = []
    for en_term, fr_terms in term_pairs.items():
        en_count = en_totals.get(en_term, 0)
        fr_count = sum(fr_totals.get(fr_term, 0) for fr_term in fr_terms)
        
        if en_count > 0 or fr_count > 0:
            # Calculate log ratio to show divergence direction
            if en_count == 0:
                ratio = -fr_count  # Negative = FR-heavy
            elif fr_count == 0:
                ratio = en_count  # Positive = EN-heavy
            else:
                ratio = (en_count - fr_count) / (en_count + fr_count) * 100
            
            divergences.append({
                'term': en_term.capitalize(),
                'ratio': ratio,
                'en_count': en_count,
                'fr_count': fr_count
            })
    
    # Sort by absolute divergence
    divergences.sort(key=lambda x: abs(x['ratio']), reverse=True)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    terms = [d['term'] for d in divergences]
    ratios = [d['ratio'] for d in divergences]
    colors = ['#2E86AB' if r > 0 else '#A23B72' for r in ratios]
    
    bars = ax.barh(terms, ratios, color=colors, alpha=0.8)
    
    ax.set_xlabel('Divergence Score (% difference)', fontweight='bold')
    ax.set_title('Terminology Divergence: English vs. French\nPositive = EN-dominant | Negative = FR-dominant', 
                 fontweight='bold', fontsize=12)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add annotations
    for i, (bar, div) in enumerate(zip(bars, divergences)):
        if div['ratio'] > 0:
            label = f"EN: {div['en_count']} | FR: {div['fr_count']}"
            x_pos = bar.get_width() + 2
            ha = 'left'
        else:
            label = f"EN: {div['en_count']} | FR: {div['fr_count']}"
            x_pos = bar.get_width() - 2
            ha = 'right'
        
        ax.text(x_pos, bar.get_y() + bar.get_height()/2, label,
               ha=ha, va='center', fontsize=8, style='italic')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2E86AB', label='English-dominant'),
        Patch(facecolor='#A23B72', label='French-dominant')
    ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True, shadow=True)
    
    plt.tight_layout()
    output_file = output_dir / 'fig2_divergence_analysis.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Created: {output_file}")

def create_category_comparison(data, output_dir):
    """Create grouped bar chart by governance category."""
    
    en_totals = data['summary']['en_term_totals']
    fr_totals = data['summary']['fr_term_totals']
    
    categories = {
        'Accountability': {
            'en': ['accountability', 'responsibility', 'liable', 'accountable'],
            'fr': ['responsabilité', 'imputabilité', 'redevabilité']
        },
        'Oversight': {
            'en': ['oversight', 'supervision', 'monitoring', 'surveillance'],
            'fr': ['surveillance', 'supervision', 'contrôle', 'suivi']
        },
        'Transparency': {
            'en': ['transparency', 'openness', 'disclosure'],
            'fr': ['transparence', 'ouverture', 'divulgation']
        },
        'Fairness': {
            'en': ['fairness', 'equity', 'justice', 'bias', 'discrimination'],
            'fr': ['équité', 'justice', 'biais', 'discrimination', 'préjugé']
        },
        'Human Review': {
            'en': ['human review', 'human oversight', 'human judgment'],
            'fr': ['examen humain', 'surveillance humaine', 'jugement humain']
        },
        'Verification': {
            'en': ['audit', 'evaluation', 'assessment'],
            'fr': ['audit', 'évaluation', 'vérification']
        }
    }
    
    cat_names = []
    en_sums = []
    fr_sums = []
    
    for cat_name, terms in categories.items():
        cat_names.append(cat_name)
        en_sum = sum(en_totals.get(t, 0) for t in terms['en'])
        fr_sum = sum(fr_totals.get(t, 0) for t in terms['fr'])
        en_sums.append(en_sum)
        fr_sums.append(fr_sum)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(cat_names))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, en_sums, width, label='English', color='#2E86AB', alpha=0.8)
    bars2 = ax.bar(x + width/2, fr_sums, width, label='French', color='#A23B72', alpha=0.8)
    
    ax.set_ylabel('Total Occurrences', fontweight='bold')
    ax.set_xlabel('Governance Category', fontweight='bold')
    ax.set_title('Governance Categories: English vs. French\nAggregated Term Frequencies', 
                 fontweight='bold', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_names, rotation=30, ha='right')
    ax.legend(frameon=True, shadow=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    plt.tight_layout()
    output_file = output_dir / 'fig3_category_comparison.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Created: {output_file}")

def create_heatmap(data, output_dir):
    """Create heatmap showing term usage across all 16 pairs."""
    
    # Prepare data matrix
    key_terms = ['accountability', 'oversight', 'transparency', 'fairness', 
                 'bias', 'audit', 'review', 'monitoring', 'assessment']
    
    en_matrix = []
    fr_matrix = []
    pair_labels = []
    
    for i, pair in enumerate(data['pair_analyses'][:16], 1):  # Limit to 16 for readability
        en_row = []
        fr_row = []
        
        for term in key_terms:
            en_count = pair['term_analysis']['en_frequencies'].get(term, 0)
            fr_count = pair['term_analysis']['fr_frequencies'].get(term, 0)
            en_row.append(en_count)
            fr_row.append(fr_count)
        
        en_matrix.append(en_row)
        fr_matrix.append(fr_row)
        
        # Short label
        title = pair['en_project']['title'][:30]
        pair_labels.append(f"P{i}: {title}...")
    
    # Create side-by-side heatmaps
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    # English heatmap
    sns.heatmap(en_matrix, annot=True, fmt='d', cmap='Blues', 
                xticklabels=[t.capitalize() for t in key_terms],
                yticklabels=pair_labels, cbar_kws={'label': 'Occurrences'},
                ax=ax1)
    ax1.set_title('English Terminology Distribution', fontweight='bold', fontsize=12)
    ax1.set_xlabel('Governance Terms', fontweight='bold')
    ax1.set_ylabel('Document Pairs', fontweight='bold')
    
    # French heatmap
    sns.heatmap(fr_matrix, annot=True, fmt='d', cmap='Purples',
                xticklabels=[t.capitalize() for t in key_terms],
                yticklabels=pair_labels, cbar_kws={'label': 'Occurrences'},
                ax=ax2)
    ax2.set_title('French Terminology Distribution', fontweight='bold', fontsize=12)
    ax2.set_xlabel('Governance Terms', fontweight='bold')
    ax2.set_ylabel('')
    
    plt.suptitle('Governance Term Distribution Across 16 Bilingual Document Pairs', 
                 fontweight='bold', fontsize=14, y=0.995)
    
    plt.tight_layout()
    output_file = output_dir / 'fig4_heatmap_distribution.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Created: {output_file}")

def create_accountability_focus(data, output_dir):
    """Create focused visualization on accountability gap."""
    
    en_totals = data['summary']['en_term_totals']
    fr_totals = data['summary']['fr_term_totals']
    
    # Accountability-related terms
    accountability_terms = {
        'EN': {
            'accountability': en_totals.get('accountability', 0),
            'accountable': en_totals.get('accountable', 0),
            'responsibility': en_totals.get('responsibility', 0),
            'liable': en_totals.get('liable', 0)
        },
        'FR': {
            'responsabilité': fr_totals.get('responsabilité', 0),
            'imputabilité': fr_totals.get('imputabilité', 0),
            'redevabilité': fr_totals.get('redevabilité', 0)
        }
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # English pie chart
    en_labels = list(accountability_terms['EN'].keys())
    en_sizes = list(accountability_terms['EN'].values())
    en_colors = ['#2E86AB', '#5AA9C7', '#8BCCE3', '#BDE5F8']
    
    if sum(en_sizes) > 0:
        wedges1, texts1, autotexts1 = ax1.pie(en_sizes, labels=en_labels, autopct='%1.0f%%',
                                               colors=en_colors, startangle=90)
        for autotext in autotexts1:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    ax1.set_title('English: Accountability Terms\nTotal: {}'.format(sum(en_sizes)), 
                  fontweight='bold')
    
    # French pie chart
    fr_labels = list(accountability_terms['FR'].keys())
    fr_sizes = list(accountability_terms['FR'].values())
    fr_colors = ['#A23B72', '#C76DA2', '#E89EC3']
    
    if sum(fr_sizes) > 0:
        wedges2, texts2, autotexts2 = ax2.pie(fr_sizes, labels=fr_labels, autopct='%1.0f%%',
                                               colors=fr_colors, startangle=90)
        for autotext in autotexts2:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    else:
        ax2.text(0.5, 0.5, 'NO ACCOUNTABILITY\nTERMS FOUND', 
                ha='center', va='center', fontsize=16, fontweight='bold',
                color='#A23B72', transform=ax2.transAxes)
        ax2.set_xlim(-1, 1)
        ax2.set_ylim(-1, 1)
    
    ax2.set_title('French: Accountability Terms\nTotal: {}'.format(sum(fr_sizes)),
                  fontweight='bold')
    
    plt.suptitle('The "Accountability Gap": English vs. French\nAcross 16 Bilingual AI Impact Assessments', 
                 fontweight='bold', fontsize=13)
    
    plt.tight_layout()
    output_file = output_dir / 'fig5_accountability_gap.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Created: {output_file}")

def create_summary_stats_table(data, output_dir):
    """Create publication-ready summary statistics table."""
    
    en_totals = data['summary']['en_term_totals']
    fr_totals = data['summary']['fr_term_totals']
    
    # Create summary data
    summary = []
    
    key_pairs = [
        ('accountability', 'responsabilité'),
        ('oversight', 'surveillance'),
        ('monitoring', 'contrôle'),
        ('transparency', 'transparence'),
        ('fairness', 'équité'),
        ('bias', 'biais'),
        ('assessment', 'évaluation'),
        ('audit', 'audit'),
        ('review', 'révision')
    ]
    
    for en_term, fr_term in key_pairs:
        en_count = en_totals.get(en_term, 0)
        fr_count = fr_totals.get(fr_term, 0)
        total = en_count + fr_count
        
        if total > 0:
            en_pct = (en_count / total) * 100
            fr_pct = (fr_count / total) * 100
            ratio = en_count / max(fr_count, 1) if fr_count > 0 else float('inf')
        else:
            en_pct = fr_pct = 0
            ratio = 0
        
        summary.append({
            'EN Term': en_term,
            'EN Count': en_count,
            'FR Term': fr_term,
            'FR Count': fr_count,
            'Total': total,
            'EN %': f"{en_pct:.1f}%",
            'FR %': f"{fr_pct:.1f}%",
            'Ratio': f"{ratio:.2f}" if ratio != float('inf') else "∞"
        })
    
    df = pd.DataFrame(summary)
    
    # Create table visualization
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=df.values, colLabels=df.columns,
                    cellLoc='center', loc='center',
                    colWidths=[0.15, 0.1, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1])
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Style header
    for i in range(len(df.columns)):
        table[(0, i)].set_facecolor('#2E86AB')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#F0F0F0')
    
    plt.title('Governance Terminology Summary Statistics\n16 Bilingual AI Impact Assessment Pairs',
             fontweight='bold', fontsize=13, pad=20)
    
    output_file = output_dir / 'fig6_summary_table.png'
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"  ✅ Created: {output_file}")

def main():
    print("=" * 80)
    print("📊 CREATING GOVERNANCE TERMINOLOGY VISUALIZATIONS")
    print("=" * 80)
    
    # Load data
    data = load_data()
    
    # Create output directory
    output_dir = Path('research/governance_terminology/figures')
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n📈 Generating visualizations...\n")
    
    # Create all visualizations
    create_comparative_bar_chart(data, output_dir)
    create_divergence_chart(data, output_dir)
    create_category_comparison(data, output_dir)
    create_heatmap(data, output_dir)
    create_accountability_focus(data, output_dir)
    create_summary_stats_table(data, output_dir)
    
    print(f"\n" + "=" * 80)
    print("✅ ALL VISUALIZATIONS CREATED")
    print("=" * 80)
    print(f"\n📁 Output directory: {output_dir}")
    print(f"\nFiles created:")
    print(f"  1. fig1_comparative_terms.png - EN/FR term comparison")
    print(f"  2. fig2_divergence_analysis.png - Divergence scores")
    print(f"  3. fig3_category_comparison.png - Category-level analysis")
    print(f"  4. fig4_heatmap_distribution.png - Term distribution heatmap")
    print(f"  5. fig5_accountability_gap.png - Accountability focus")
    print(f"  6. fig6_summary_table.png - Summary statistics table")
    print("\n💡 All figures are publication-ready (300 DPI)")
    print("=" * 80)

if __name__ == '__main__':
    main()
