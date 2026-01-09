#!/usr/bin/env python3
"""
Identify and separate English PDFs that don't have French counterparts
"""

import json
import shutil
from pathlib import Path
from collections import defaultdict

def identify_unpaired_documents():
    """Find English PDFs without French pairs and move to separate folder."""
    
    # Load mapping
    mapping_file = Path("data/pdfs/bilingual_mapping.json")
    with open(mapping_file) as f:
        mapping_data = json.load(f)
    
    # Create folder for unpaired English docs
    en_only_dir = Path("data/pdfs/en_only")
    en_only_dir.mkdir(parents=True, exist_ok=True)
    
    # Track all English files in mapping
    paired_en_files = set()
    unpaired_datasets = []
    
    for dataset in mapping_data['datasets']:
        title = dataset['title']
        en_files = dataset['en_files']
        fr_files = dataset['fr_files']
        
        if en_files and fr_files:
            # Both languages present - these are paired
            for en_file in en_files:
                filename = Path(en_file).name
                paired_en_files.add(filename)
        elif en_files and not fr_files:
            # English only - unpaired
            unpaired_datasets.append({
                'title': title,
                'en_files': en_files
            })
    
    # Get all actual English PDF files
    en_dir = Path("data/pdfs/en")
    all_en_files = {f.name for f in en_dir.glob("*.pdf")}
    
    # Find unpaired files (in directory but not in paired set)
    unpaired_files = all_en_files - paired_en_files
    
    print(f"{'='*70}")
    print("BILINGUAL PAIRING ANALYSIS")
    print(f"{'='*70}")
    print(f"Total EN files: {len(all_en_files)}")
    print(f"Paired EN files: {len(paired_en_files)}")
    print(f"Unpaired EN files: {len(unpaired_files)}")
    print()
    
    if unpaired_files:
        print("📂 Moving unpaired English documents to: data/pdfs/en_only/")
        print()
        
        for filename in sorted(unpaired_files):
            source = en_dir / filename
            dest = en_only_dir / filename
            
            # Find which dataset this belongs to
            dataset_title = "Unknown"
            for dataset in mapping_data['datasets']:
                for en_file in dataset['en_files']:
                    if Path(en_file).name == filename:
                        dataset_title = dataset['title']
                        break
            
            # Also check unpaired datasets
            for unpaired_ds in unpaired_datasets:
                for en_file in unpaired_ds['en_files']:
                    if Path(en_file).name == filename:
                        dataset_title = unpaired_ds['title']
                        break
            
            shutil.move(str(source), str(dest))
            print(f"  ✓ {filename[:60]}")
            print(f"    Dataset: {dataset_title[:60]}")
            print()
    
    # Show datasets without French versions
    if unpaired_datasets:
        print(f"\n{'='*70}")
        print("DATASETS WITHOUT FRENCH VERSIONS:")
        print(f"{'='*70}")
        for ds in unpaired_datasets:
            print(f"\n📄 {ds['title']}")
            for en_file in ds['en_files']:
                print(f"   - {Path(en_file).name}")
    
    # Final count
    print(f"\n{'='*70}")
    print("FINAL CORPUS STRUCTURE")
    print(f"{'='*70}")
    
    paired_en_count = len(list(en_dir.glob("*.pdf")))
    fr_count = len(list(Path("data/pdfs/fr").glob("*.pdf")))
    unpaired_count = len(list(en_only_dir.glob("*.pdf")))
    
    print(f"✅ Bilingual pairs (for divergence analysis):")
    print(f"   EN: {paired_en_count} documents")
    print(f"   FR: {fr_count} documents")
    print()
    print(f"⚠️  English-only (excluded from bilingual analysis):")
    print(f"   EN: {unpaired_count} documents")
    print()
    print(f"Total corpus: {paired_en_count + fr_count + unpaired_count} PDFs")
    
    if paired_en_count != fr_count:
        print(f"\n⚠️  Warning: EN ({paired_en_count}) and FR ({fr_count}) counts don't match!")
        print("   Some documents may need manual pairing review.")

if __name__ == "__main__":
    identify_unpaired_documents()
