#!/usr/bin/env python3
"""
Analyze AIA database to identify key governance patterns and bilingual divergences
"""

import csv
from pathlib import Path
from collections import defaultdict, Counter

def analyze_database(db_file="data/aia_database.csv"):
    """Analyze AIA database for patterns."""
    
    print(f"\n{'='*70}")
    print("AIA DATABASE ANALYSIS REPORT")
    print(f"{'='*70}\n")
    
    # Load data
    rows = []
    with open(db_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Language distribution
    en_count = sum(1 for r in rows if r['document_language'] == 'en')
    fr_count = sum(1 for r in rows if r['document_language'] == 'fr')
    
    print(f"📊 DOCUMENT DISTRIBUTION")
    print(f"{'='*70}")
    print(f"English documents: {en_count}")
    print(f"French documents: {fr_count}")
    print(f"Total documents: {len(rows)}")
    print()
    
    # Department analysis
    departments = Counter()
    for row in rows:
        dept = row.get('metadata_department', 'Unknown').strip()
        if dept and dept != 'Unknown':
            departments[dept] += 1
    
    print(f"🏛️  DEPARTMENTS INVOLVED")
    print(f"{'='*70}")
    for dept, count in departments.most_common(10):
        print(f"  {dept[:55]}: {count} documents")
    print()
    
    # Governance analysis
    en_rows = [r for r in rows if r['document_language'] == 'en']
    fr_rows = [r for r in rows if r['document_language'] == 'fr']
    
    print(f"⚖️  GOVERNANCE PATTERNS - ENGLISH")
    print(f"{'='*70}")
    en_oversight = sum(1 for r in en_rows if 'yes' in r.get('governance_human_oversight', '').lower())
    en_transparency = sum(1 for r in en_rows if 'yes' in r.get('governance_transparency', '').lower())
    print(f"  Documents mentioning human oversight: {en_oversight}/{len(en_rows)}")
    print(f"  Documents mentioning transparency: {en_transparency}/{len(en_rows)}")
    print()
    
    print(f"⚖️  GOVERNANCE PATTERNS - FRENCH")
    print(f"{'='*70}")
    fr_oversight = sum(1 for r in fr_rows if 'yes' in r.get('governance_human_oversight', '').lower())
    fr_transparency = sum(1 for r in fr_rows if 'yes' in r.get('governance_transparency', '').lower())
    print(f"  Documents mentioning human oversight: {fr_oversight}/{len(fr_rows)}")
    print(f"  Documents mentioning transparency: {fr_transparency}/{len(fr_rows)}")
    print()
    
    # Key terms analysis
    print(f"🔑 KEY TERMS MENTIONED IN DOCUMENTS")
    print(f"{'='*70}")
    
    en_bias = sum(1 for r in en_rows if r.get('key_terms_bias', 'False').lower() == 'true')
    en_transparency_term = sum(1 for r in en_rows if r.get('key_terms_transparency', 'False').lower() == 'true')
    en_accountability = sum(1 for r in en_rows if r.get('key_terms_accountability', 'False').lower() == 'true')
    en_equity = sum(1 for r in en_rows if r.get('key_terms_equity', 'False').lower() == 'true')
    
    fr_bias = sum(1 for r in fr_rows if r.get('key_terms_bias', 'False').lower() == 'true')
    fr_transparency_term = sum(1 for r in fr_rows if r.get('key_terms_transparency', 'False').lower() == 'true')
    fr_accountability = sum(1 for r in fr_rows if r.get('key_terms_accountability', 'False').lower() == 'true')
    fr_equity = sum(1 for r in fr_rows if r.get('key_terms_equity', 'False').lower() == 'true')
    
    terms = ['Bias', 'Transparency', 'Accountability', 'Equity']
    en_counts = [en_bias, en_transparency_term, en_accountability, en_equity]
    fr_counts = [fr_bias, fr_transparency_term, fr_accountability, fr_equity]
    
    print(f"  {'Term':<20} {'EN':<10} {'FR':<10} {'Divergence':<15}")
    print(f"  {'-'*55}")
    for term, en_c, fr_c in zip(terms, en_counts, fr_counts):
        divergence = abs(en_c - fr_c)
        print(f"  {term:<20} {en_c:<10} {fr_c:<10} {f'+{divergence}' if divergence > 0 else '0':<15}")
    print()
    
    # Create bilingual pairs summary
    print(f"🔗 BILINGUAL DOCUMENT PAIRS")
    print(f"{'='*70}")
    
    # Match EN and FR files by title
    en_by_title = defaultdict(list)
    fr_by_title = defaultdict(list)
    
    for row in rows:
        title = row.get('metadata_project_title', 'Unknown').strip()
        if row['document_language'] == 'en':
            en_by_title[title].append(row)
        else:
            fr_by_title[title].append(row)
    
    paired = 0
    en_only = 0
    fr_only = 0
    
    for title in set(en_by_title.keys()) | set(fr_by_title.keys()):
        en_docs = en_by_title.get(title, [])
        fr_docs = fr_by_title.get(title, [])
        
        if en_docs and fr_docs:
            paired += 1
        elif en_docs:
            en_only += 1
        else:
            fr_only += 1
    
    print(f"  Bilingual pairs (EN + FR): {paired}")
    print(f"  English-only: {en_only}")
    print(f"  French-only: {fr_only}")
    print()
    
    # Convergence/Divergence examples
    print(f"📈 BILINGUAL DIVERGENCE INDICATORS")
    print(f"{'='*70}")
    print(f"  Pairs with different governance mentions:")
    
    divergence_count = 0
    for title in sorted(set(en_by_title.keys()) & set(fr_by_title.keys())):
        en_docs = en_by_title[title]
        fr_docs = fr_by_title[title]
        
        for en_doc in en_docs:
            for fr_doc in fr_docs:
                en_oversight = en_doc.get('governance_human_oversight', '')
                fr_oversight = fr_doc.get('governance_human_oversight', '')
                
                if en_oversight.lower() != fr_oversight.lower():
                    divergence_count += 1
                    if divergence_count <= 5:
                        print(f"\n    Title: {title[:50]}")
                        print(f"      EN oversight: {en_oversight}")
                        print(f"      FR oversight: {fr_oversight}")
    
    print(f"\n  Total divergences found: {divergence_count}")
    print()
    
    print(f"{'='*70}")
    print("✅ ANALYSIS COMPLETE")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    analyze_database()
