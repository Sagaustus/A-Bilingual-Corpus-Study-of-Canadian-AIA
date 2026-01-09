#!/usr/bin/env python3
"""
Convert AIA PDFs to structured CSV files using hybrid parsing
- LLM-powered extraction (with API key)
- Rule-based extraction (fallback)

Usage:
    python research/pdf_to_csv_v2.py --folder en      # Process all EN PDFs
    python research/pdf_to_csv_v2.py --folder fr      # Process all FR PDFs
"""

import argparse
import csv
import json
import os
import re
from pathlib import Path

import dotenv
from pdfminer.high_level import extract_text

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Load environment
dotenv.load_dotenv()

if HAS_OPENAI:
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
        HAS_API_KEY = bool(os.getenv("OPENAI_API_KEY"))
        MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    except:
        HAS_API_KEY = False
else:
    HAS_API_KEY = False


def extract_pdf_text(pdf_path, max_pages=10):
    """Extract text from PDF."""
    try:
        text = extract_text(str(pdf_path), maxpages=max_pages)
        return text[:10000]  # Limit for efficiency
    except Exception as e:
        return None


def extract_with_regex(text, lang='en'):
    """Rule-based extraction of AIA fields."""
    
    data = {
        "metadata": {},
        "project_overview": {},
        "governance": {},
        "risk_assessment": {},
        "key_terms": {},
        "document_language": lang,
        "extraction_confidence": "medium"
    }
    
    # Extract department (various patterns)
    dept_patterns = [
        r"(?:Department|Ministère)[:\s]+([^\n]+)",
        r"(?:Department Name|Nom du ministère)[:\s]+([^\n]+)"
    ]
    for pattern in dept_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["metadata"]["department"] = match.group(1).strip()
            break
    
    # Extract project title
    title_patterns = [
        r"Project Title[:\s]+([^\n]+)",
        r"Titre du projet[:\s]+([^\n]+)"
    ]
    for pattern in title_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["metadata"]["project_title"] = match.group(1).strip()
            break
    
    # Extract project phase
    phase_patterns = [
        r"Project Phase[:\s]+([^\n]+)",
        r"Phase du projet[:\s]+([^\n]+)"
    ]
    for pattern in phase_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["metadata"]["project_phase"] = match.group(1).strip()
            break
    
    # Extract project description (first 300 chars after description header)
    desc_patterns = [
        r"(?:project description|description du projet)[:\s]*([^.]+\.)",
        r"project description[:\s]*\n*([^(\n]+)"
    ]
    for pattern in desc_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            desc = match.group(1).strip()[:300]
            data["project_overview"]["description"] = desc
            break
    
    # Key term extraction (count mentions)
    data["key_terms"]["bias"] = "bias" in text.lower() or "discrimination" in text.lower()
    data["key_terms"]["transparency"] = "transparent" in text.lower() or "explainable" in text.lower()
    data["key_terms"]["accountability"] = "account" in text.lower() or "oversight" in text.lower()
    data["key_terms"]["equity"] = "equit" in text.lower() or "fairness" in text.lower()
    
    # Governance indicators
    data["governance"]["human_oversight"] = "yes" if "human review" in text.lower() or "oversight" in text.lower() else "not mentioned"
    data["governance"]["transparency"] = "yes" if "transparent" in text.lower() or "explainable" in text.lower() else "not mentioned"
    
    return data


def process_pdf_to_row(pdf_path, lang='en'):
    """Process single PDF to data row."""
    
    # Extract text
    text = extract_pdf_text(pdf_path)
    if not text:
        return None
    
    # Extract data (regex-based)
    data = extract_with_regex(text, lang=lang)
    
    # Flatten to row
    row = {"pdf_filename": pdf_path.name}
    
    for key, val in data.items():
        if isinstance(val, dict):
            for subkey, subval in val.items():
                row[f"{key}_{subkey}"] = subval
        elif isinstance(val, list):
            row[key] = "; ".join(val)
        else:
            row[key] = val
    
    return row


def process_folder(folder_path, output_dir="data/csv", limit=None):
    """Process all PDFs in folder."""
    
    folder = Path(folder_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdfs = sorted(folder.glob("*.pdf"))
    if limit:
        pdfs = pdfs[:limit]
    
    lang = "en" if "en" in folder.name else "fr"
    
    print(f"\n{'='*70}")
    print(f"Processing {len(pdfs)} PDFs from: {folder.name}")
    print(f"{'='*70}\n")
    
    all_rows = []
    fieldnames = set()
    
    for i, pdf_path in enumerate(pdfs, 1):
        print(f"[{i}/{len(pdfs)}] {pdf_path.name[:55]}", end=" ")
        
        row = process_pdf_to_row(pdf_path, lang=lang)
        if row:
            all_rows.append(row)
            fieldnames.update(row.keys())
            print("✓")
        else:
            print("✗")
    
    # Write master CSV
    fieldnames = sorted(list(fieldnames))
    master_csv = output_dir / f"{folder.name}_master.csv"
    
    try:
        with open(master_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in all_rows:
                writer.writerow(row)
        
        print(f"\n✅ Saved: {master_csv}")
        print(f"   Documents: {len(all_rows)}")
        print(f"   Fields: {len(fieldnames)}")
    
    except Exception as e:
        print(f"✗ Error writing CSV: {e}")
    
    return all_rows, fieldnames


def create_unified_database(csv_dir="data/csv", output_file="data/aia_database.csv"):
    """Combine EN and FR master CSVs into unified database."""
    
    csv_dir = Path(csv_dir)
    all_rows = []
    fieldnames = set()
    
    # Find master CSVs
    master_files = list(csv_dir.glob("*_master.csv"))
    
    print(f"\n{'='*70}")
    print(f"Creating unified database from {len(master_files)} CSV files")
    print(f"{'='*70}\n")
    
    for master_file in sorted(master_files):
        print(f"  Reading: {master_file.name}")
        try:
            with open(master_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_rows.append(row)
                    fieldnames.update(row.keys())
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    # Write unified database
    fieldnames = sorted(list(fieldnames))
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in all_rows:
                writer.writerow(row)
        
        print(f"\n✅ Unified database: {output_path}")
        print(f"   Total documents: {len(all_rows)}")
        print(f"   Total fields: {len(fieldnames)}")
        print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert AIA PDFs to CSV database")
    parser.add_argument('--folder', choices=['en', 'fr', 'both'], default='both')
    parser.add_argument('--output', default='data/csv')
    parser.add_argument('--limit', type=int, help='Limit PDFs per folder')
    parser.add_argument('--skip-database', action='store_true')
    
    args = parser.parse_args()
    
    if args.folder in ['en', 'both']:
        process_folder('data/pdfs/en', output_dir=args.output, limit=args.limit)
    
    if args.folder in ['fr', 'both']:
        process_folder('data/pdfs/fr', output_dir=args.output, limit=args.limit)
    
    if not args.skip_database:
        create_unified_database(csv_dir=args.output, output_file="data/aia_database.csv")
    
    print(f"\n{'='*70}\n✅ DONE\n{'='*70}\n")


if __name__ == "__main__":
    main()
