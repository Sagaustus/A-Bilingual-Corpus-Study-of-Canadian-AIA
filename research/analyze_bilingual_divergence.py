#!/usr/bin/env python3
"""
Analyze bilingual divergence: Find entries that are pure translations vs. divergent.
"""

import csv
from collections import defaultdict
import json

def load_csv(filepath):
    """Load CSV and return list of dicts."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def normalize_title(title):
    """Normalize project title for matching."""
    return title.lower().strip() if title else ""

def main():
    print("=" * 80)
    print("🔍 BILINGUAL DIVERGENCE ANALYSIS")
    print("=" * 80)
    
    # Load all tables
    projects = load_csv('data/postgres_csvs/projects.csv')
    governance = load_csv('data/postgres_csvs/governance.csv')
    systems = load_csv('data/postgres_csvs/systems.csv')
    stakeholders = load_csv('data/postgres_csvs/stakeholders.csv')
    risk_areas = load_csv('data/postgres_csvs/risk_areas.csv')
    key_findings = load_csv('data/postgres_csvs/key_findings.csv')
    
    # Organize by language and normalized title
    en_projects = {normalize_title(p['project_title']): p for p in projects if p['language'] == 'en'}
    fr_projects = {normalize_title(p['project_title']): p for p in projects if p['language'] == 'fr'}
    
    # Create lookup maps
    gov_by_project_id = {g['project_id']: g for g in governance}
    sys_by_project_id = {s['project_id']: s for s in systems}
    find_by_project_id = {f['project_id']: f for f in key_findings}
    
    # Find bilingual pairs
    en_titles = set(en_projects.keys())
    fr_titles = set(fr_projects.keys())
    
    paired_titles = en_titles & fr_titles
    en_only = en_titles - fr_titles
    fr_only = fr_titles - en_titles
    
    print(f"\n📊 PAIRING STATISTICS")
    print(f"  English-only projects:     {len(en_only)}")
    print(f"  French-only projects:      {len(fr_only)}")
    print(f"  Bilingual pairs:           {len(paired_titles)}")
    print(f"  Total projects:            {len(projects)}")
    
    # Analyze each bilingual pair
    print(f"\n" + "=" * 80)
    print("🔄 BILINGUAL PAIR ANALYSIS")
    print("=" * 80)
    
    pure_translations = []
    divergent_pairs = []
    
    for norm_title in sorted(paired_titles):
        en_proj = en_projects[norm_title]
        fr_proj = fr_projects[norm_title]
        en_proj_id = en_proj['project_id']
        fr_proj_id = fr_proj['project_id']
        
        # Get related data
        en_gov = gov_by_project_id.get(en_proj_id, {})
        fr_gov = gov_by_project_id.get(fr_proj_id, {})
        en_sys = sys_by_project_id.get(en_proj_id, {})
        fr_sys = sys_by_project_id.get(fr_proj_id, {})
        en_find = find_by_project_id.get(en_proj_id, {})
        fr_find = find_by_project_id.get(fr_proj_id, {})
        
        # Compare key fields
        differences = []
        
        # Governance comparison
        for field in ['oversight_mechanism', 'appeal_process', 'transparency_measures', 
                      'accountability_framework', 'external_audit']:
            en_val = en_gov.get(field, '').strip()
            fr_val = fr_gov.get(field, '').strip()
            if en_val and fr_val and en_val != fr_val:
                differences.append({
                    'table': 'governance',
                    'field': field,
                    'en': en_val[:60],
                    'fr': fr_val[:60]
                })
        
        # Systems comparison
        for field in ['system_description', 'data_inputs', 'decision_outputs']:
            en_val = en_sys.get(field, '').strip()
            fr_val = fr_sys.get(field, '').strip()
            if en_val and fr_val and en_val != fr_val:
                differences.append({
                    'table': 'systems',
                    'field': field,
                    'en': en_val[:60],
                    'fr': fr_val[:60]
                })
        
        # Key findings comparison
        for field in ['biases_identified', 'fairness_issues', 'transparency_gaps']:
            en_val = en_find.get(field, '').strip()
            fr_val = fr_find.get(field, '').strip()
            if en_val and fr_val and en_val != fr_val:
                differences.append({
                    'table': 'key_findings',
                    'field': field,
                    'en': en_val[:60],
                    'fr': fr_val[:60]
                })
        
        pair_info = {
            'title': en_proj['project_title'],
            'en_proj_id': en_proj_id,
            'fr_proj_id': fr_proj_id,
            'en_file': en_proj['pdf_filename'],
            'fr_file': fr_proj['pdf_filename'],
            'differences': differences
        }
        
        if differences:
            divergent_pairs.append(pair_info)
        else:
            pure_translations.append(pair_info)
    
    # Report pure translations
    print(f"\n✅ PURE TRANSLATIONS ({len(pure_translations)} pairs)")
    print("   (Same values in EN and FR - just translated or empty)")
    print("-" * 80)
    for pair in pure_translations[:10]:  # Show first 10
        print(f"  • {pair['title']}")
        print(f"    EN: {pair['en_file']}")
        print(f"    FR: {pair['fr_file']}")
    
    if len(pure_translations) > 10:
        print(f"  ... and {len(pure_translations) - 10} more")
    
    # Report divergent pairs
    print(f"\n⚠️  DIVERGENT PAIRS ({len(divergent_pairs)} pairs)")
    print("   (Different values between EN and FR)")
    print("-" * 80)
    for pair in divergent_pairs:
        print(f"\n  📌 {pair['title']}")
        print(f"     EN File: {pair['en_file']}")
        print(f"     FR File: {pair['fr_file']}")
        
        for diff in pair['differences']:
            print(f"\n     [{diff['table']}] {diff['field']}:")
            print(f"       EN: {diff['en']}")
            print(f"       FR: {diff['fr']}")
    
    # Summary statistics
    print(f"\n" + "=" * 80)
    print("📈 DIVERGENCE SUMMARY")
    print("=" * 80)
    print(f"  Total bilingual pairs:        {len(paired_titles)}")
    print(f"  Pure translations:            {len(pure_translations)} ({100*len(pure_translations)//len(paired_titles)}%)")
    print(f"  Divergent pairs:              {len(divergent_pairs)} ({100*len(divergent_pairs)//len(paired_titles)}%)")
    print(f"  Total divergence points:      {sum(len(p['differences']) for p in divergent_pairs)}")
    
    # Export JSON
    export_data = {
        'statistics': {
            'total_projects': len(projects),
            'bilingual_pairs': len(paired_titles),
            'en_only': len(en_only),
            'fr_only': len(fr_only),
            'pure_translations': len(pure_translations),
            'divergent_pairs': len(divergent_pairs),
            'total_divergence_points': sum(len(p['differences']) for p in divergent_pairs)
        },
        'pure_translations': pure_translations,
        'divergent_pairs': divergent_pairs
    }
    
    with open('research/bilingual_divergence_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Analysis exported to: research/bilingual_divergence_analysis.json")
    print("=" * 80)

if __name__ == '__main__':
    main()
