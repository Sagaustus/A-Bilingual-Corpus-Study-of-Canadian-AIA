#!/usr/bin/env python3
"""
Classify unknown PDFs based on filename patterns
"""

import os
import shutil
import re
from pathlib import Path

def classify_unknown_pdfs():
    unknown_dir = Path("data/pdfs/unknown")
    en_dir = Path("data/pdfs/en")
    fr_dir = Path("data/pdfs/fr")
    
    if not unknown_dir.exists():
        print("No unknown folder found")
        return
    
    classifications = {'en': [], 'fr': [], 'still_unknown': []}
    
    for pdf_file in unknown_dir.glob("*.pdf"):
        filename = pdf_file.name.lower()
        
        # Check for language patterns
        is_en = False
        is_fr = False
        
        # Strong patterns
        if any(p in filename for p in ['_en.pdf', '-en.pdf', '_en_', '-en-', 'english']):
            is_en = True
        if any(p in filename for p in ['_fr.pdf', '-fr.pdf', '_fr_', '-fr-', 'french', 'francais', 'français']):
            is_fr = True
        
        # Check if filename contains French/English indicators
        if '_fre.pdf' in filename or 'fre_' in filename or '-fre-' in filename:
            is_fr = True
        if '_eng.pdf' in filename or 'eng_' in filename or '-eng-' in filename:
            is_en = True
            
        # Peer review pattern (usually has "english" or "frenc" in name)
        if 'peer-review' in filename:
            if 'english' in filename or 'engli' in filename:
                is_en = True
            if 'french' in filename or 'frenc' in filename:
                is_fr = True
        
        # GBA+ pattern
        if 'gba' in filename or 'gender' in filename:
            # Check URL patterns from original downloads
            # Many GBA+ files have summary-en or summary-fr
            if '-en' in filename or '_en' in filename:
                is_en = True
            if '-fr' in filename or '_fr' in filename:
                is_fr = True
        
        # Specific filename patterns we saw
        if 'aia_roec_en' in filename or 'aia_roec_eng' in filename:
            is_en = True
        if 'aia_roec_fr' in filename or 'aia_roec_fra' in filename:
            is_fr = True
            
        if 'oas_eav_acc_final.pdf' in filename and 'fr' not in filename:
            is_en = True
        if 'oas_eav_acc_finalfr' in filename:
            is_fr = True
            
        if 'tfwp_aia_en' in filename:
            is_en = True
        if 'tfwp_aia_fr' in filename:
            is_fr = True
            
        if 'trv-aia-en' in filename:
            is_en = True
        if 'trv-aia-fr' in filename:
            is_fr = True
            
        if 'rap-evm_aia_en' in filename:
            is_en = True
        if 'rap-evm_aia_fr' in filename:
            is_fr = True
            
        if 'aia-fr-' in filename or 'aia_fr' in filename:
            is_fr = True
        if 'aia-en-' in filename or 'aia_en' in filename:
            is_en = True
            
        # Decide classification
        if is_en and not is_fr:
            new_path = en_dir / pdf_file.name.replace('_UNKNOWN', '').replace('UNKNOWN_', '')
            shutil.move(str(pdf_file), str(new_path))
            classifications['en'].append(pdf_file.name)
            print(f"✓ EN: {pdf_file.name}")
        elif is_fr and not is_en:
            new_path = fr_dir / pdf_file.name.replace('_UNKNOWN', '').replace('UNKNOWN_', '')
            shutil.move(str(pdf_file), str(new_path))
            classifications['fr'].append(pdf_file.name)
            print(f"✓ FR: {pdf_file.name}")
        else:
            classifications['still_unknown'].append(pdf_file.name)
            print(f"⚠️  Still unknown: {pdf_file.name}")
    
    print(f"\n{'='*60}")
    print(f"CLASSIFICATION SUMMARY")
    print(f"{'='*60}")
    print(f"Moved to EN: {len(classifications['en'])}")
    print(f"Moved to FR: {len(classifications['fr'])}")
    print(f"Still unknown: {len(classifications['still_unknown'])}")
    
    if classifications['still_unknown']:
        print(f"\nFiles needing manual review:")
        for f in classifications['still_unknown']:
            print(f"  - {f}")

if __name__ == "__main__":
    classify_unknown_pdfs()
