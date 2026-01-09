#!/usr/bin/env python3
"""
Classify unknown PDFs by analyzing first page content
"""

import shutil
from pathlib import Path
from pdfminer.high_level import extract_text

def detect_language_from_text(text):
    """Detect if text is English or French based on linguistic markers."""
    text_lower = text.lower()
    
    # Count French markers
    fr_score = 0
    fr_score += text_lower.count(' de la ') * 3
    fr_score += text_lower.count(' du ') * 3
    fr_score += text_lower.count(' des ') * 2
    fr_score += text_lower.count(' le ') * 2
    fr_score += text_lower.count(' la ') * 2
    fr_score += text_lower.count('évaluation') * 5
    fr_score += text_lower.count('résumé') * 5
    fr_score += text_lower.count('français') * 5
    fr_score += text_lower.count('algorithmique') * 5
    fr_score += text_lower.count(' en ') * 1  # "in" in French
    fr_score += text_lower.count('sur le') * 3
    fr_score += text_lower.count('pour le') * 3
    
    # Count English markers
    en_score = 0
    en_score += text_lower.count(' the ') * 3
    en_score += text_lower.count(' of ') * 2
    en_score += text_lower.count('assessment') * 5
    en_score += text_lower.count('summary') * 5
    en_score += text_lower.count('english') * 5
    en_score += text_lower.count('algorithmic') * 5
    en_score += text_lower.count(' on ') * 1
    en_score += text_lower.count('for the') * 3
    
    return 'fr' if fr_score > en_score else 'en'


def classify_unknown_pdfs():
    unknown_dir = Path("data/pdfs/unknown")
    en_dir = Path("data/pdfs/en")
    fr_dir = Path("data/pdfs/fr")
    
    if not unknown_dir.exists():
        print("No unknown folder found")
        return
    
    results = {'en': [], 'fr': [], 'error': []}
    
    for pdf_file in sorted(unknown_dir.glob("*.pdf")):
        try:
            # Extract first 2 pages of text
            text = extract_text(str(pdf_file), maxpages=2)
            
            # Detect language
            lang = detect_language_from_text(text)
            
            # Generate new filename (remove UNKNOWN markers)
            new_name = pdf_file.name
            for pattern in ['_UNKNOWN_1', '_UNKNOWN_2', '_UNKNOWN_3', '_UNKNOWN_4', 
                           'UNKNOWN_1_', 'UNKNOWN_2_', 'UNKNOWN_3_', 'UNKNOWN_4_']:
                new_name = new_name.replace(pattern, '')
            new_name = new_name.replace('__', '_')  # Clean up double underscores
            
            # Append language suffix if not present
            if not (new_name.endswith('_en.pdf') or new_name.endswith('_fr.pdf')):
                new_name = new_name.replace('.pdf', f'_{lang}.pdf')
            
            # Move to appropriate folder
            target_dir = en_dir if lang == 'en' else fr_dir
            
            # Handle duplicate names
            target_path = target_dir / new_name
            counter = 1
            while target_path.exists():
                new_name = new_name.replace('.pdf', f'_{counter}.pdf').replace(f'_{counter-1}.pdf', f'_{counter}.pdf')
                target_path = target_dir / new_name
                counter += 1
            
            shutil.move(str(pdf_file), str(target_path))
            results[lang].append(pdf_file.name)
            print(f"✓ {lang.upper()}: {pdf_file.name[:70]}")
            
        except Exception as e:
            results['error'].append(pdf_file.name)
            print(f"✗ ERROR: {pdf_file.name[:70]} - {str(e)[:40]}")
    
    print(f"\n{'='*70}")
    print("CLASSIFICATION SUMMARY")
    print(f"{'='*70}")
    print(f"Moved to EN: {len(results['en'])}")
    print(f"Moved to FR: {len(results['fr'])}")
    print(f"Errors: {len(results['error'])}")
    
    if results['error']:
        print(f"\nFiles with errors:")
        for f in results['error']:
            print(f"  - {f}")

if __name__ == "__main__":
    classify_unknown_pdfs()
