#!/usr/bin/env python3
"""
Create detailed bilingual pairing report showing exact EN-FR matches
"""

import json
from pathlib import Path
from collections import defaultdict

def create_pairing_report():
    """Generate detailed report of EN-FR document pairs."""
    
    mapping_file = Path("data/pdfs/bilingual_mapping.json")
    with open(mapping_file) as f:
        mapping_data = json.load(f)
    
    print(f"{'='*80}")
    print("DETAILED BILINGUAL PAIRING REPORT")
    print(f"{'='*80}\n")
    
    bilingual_datasets = []
    en_only_datasets = []
    fr_only_datasets = []
    
    for dataset in mapping_data['datasets']:
        title = dataset['title']
        en_files = dataset['en_files']
        fr_files = dataset['fr_files']
        
        if en_files and fr_files:
            bilingual_datasets.append(dataset)
        elif en_files:
            en_only_datasets.append(dataset)
        elif fr_files:
            fr_only_datasets.append(dataset)
    
    # Bilingual datasets
    print(f"✅ BILINGUAL DATASETS ({len(bilingual_datasets)} datasets)")
    print(f"{'='*80}\n")
    
    total_en_paired = 0
    total_fr_paired = 0
    
    for i, ds in enumerate(bilingual_datasets, 1):
        en_count = len(ds['en_files'])
        fr_count = len(ds['fr_files'])
        total_en_paired += en_count
        total_fr_paired += fr_count
        
        balance = "✓" if en_count == fr_count else "⚠️"
        
        print(f"{i}. {ds['title'][:70]}")
        print(f"   {balance} EN: {en_count} | FR: {fr_count}")
        
        # Show files if counts don't match
        if en_count != fr_count:
            print(f"   English files:")
            for ef in ds['en_files']:
                print(f"     - {Path(ef).name[:65]}")
            print(f"   French files:")
            for ff in ds['fr_files']:
                print(f"     - {Path(ff).name[:65]}")
        
        print()
    
    print(f"Subtotal: {total_en_paired} EN, {total_fr_paired} FR\n")
    
    # English-only datasets
    if en_only_datasets:
        print(f"\n⚠️  ENGLISH-ONLY DATASETS ({len(en_only_datasets)} datasets)")
        print(f"{'='*80}\n")
        
        for i, ds in enumerate(en_only_datasets, 1):
            print(f"{i}. {ds['title'][:70]}")
            print(f"   EN files: {len(ds['en_files'])}")
            for ef in ds['en_files']:
                print(f"     - {Path(ef).name[:65]}")
            print()
    
    # French-only datasets
    if fr_only_datasets:
        print(f"\n⚠️  FRENCH-ONLY DATASETS ({len(fr_only_datasets)} datasets)")
        print(f"{'='*80}\n")
        
        for i, ds in enumerate(fr_only_datasets, 1):
            print(f"{i}. {ds['title'][:70]}")
            print(f"   FR files: {len(ds['fr_files'])}")
            for ff in ds['fr_files']:
                print(f"     - {Path(ff).name[:65]}")
            print()
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY FOR BILINGUAL DIVERGENCE ANALYSIS")
    print(f"{'='*80}\n")
    
    print(f"Datasets with both EN+FR: {len(bilingual_datasets)}")
    print(f"  → Usable for LLM divergence analysis")
    print()
    print(f"Datasets EN-only: {len(en_only_datasets)}")
    print(f"  → Moved to data/pdfs/en_only/")
    print()
    print(f"Datasets FR-only: {len(fr_only_datasets)}")
    print(f"  → Keep in data/pdfs/fr/ (may be useful for FR-only analysis)")
    print()
    print(f"Document counts:")
    print(f"  Paired EN documents: {total_en_paired}")
    print(f"  Paired FR documents: {total_fr_paired}")
    print(f"  Imbalance: {abs(total_en_paired - total_fr_paired)} extra FR docs")
    print()
    
    if total_en_paired != total_fr_paired:
        print("ℹ️  Note: Some datasets have multiple document types (AIA + GBA+ + Peer Review)")
        print("   This is normal - you can analyze each document type separately or")
        print("   focus on primary AIAs only (usually 1 EN + 1 FR per dataset).")

if __name__ == "__main__":
    create_pairing_report()
