#!/usr/bin/env python3
"""
Convert AIA PDFs to structured CSV files using LLM-powered extraction

Extracts key sections from Algorithmic Impact Assessment PDFs and converts to CSV format.
Then aggregates all CSVs into a master database.

Usage:
    python research/pdf_to_csv.py --folder en      # Process all EN PDFs
    python research/pdf_to_csv.py --folder fr      # Process all FR PDFs
    python research/pdf_to_csv.py --dry-run        # Test on first PDF
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

import dotenv
from openai import OpenAI
from pdfminer.high_level import extract_text

# Load environment
dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

# Extraction prompt
EXTRACTION_PROMPT = """
You are an expert at extracting structured information from Algorithmic Impact Assessment (AIA) documents.

Extract the following key information from the provided AIA document text and return as JSON:

{
  "metadata": {
    "department": "string - department name",
    "project_title": "string",
    "project_phase": "string - e.g., Planning, Implementation, Deployed",
    "respondent_name": "string",
    "respondent_title": "string"
  },
  "project_overview": {
    "description": "string - 100-200 word summary",
    "system_purpose": "string - what does the algorithm do?",
    "system_input": "string - what data does it use?",
    "system_output": "string - what does it decide/recommend?"
  },
  "governance": {
    "human_oversight": "string - yes/no/description of human review",
    "transparency": "string - how are decisions explained?",
    "appeals_process": "string - how can people contest decisions?",
    "accountability": "string - who is responsible?"
  },
  "risk_assessment": {
    "risks_identified": ["string", "string"],
    "mitigation_strategies": ["string", "string"],
    "highest_risk": "string"
  },
  "key_terms": {
    "bias": "string - mention of bias/fairness",
    "transparency": "string - explainability, interpretability",
    "accountability": "string - responsibility, oversight",
    "equity": "string - fairness, discrimination concerns"
  },
  "document_language": "EN or FR",
  "extraction_confidence": "high/medium/low"
}

Return ONLY valid JSON, no markdown or extra text.
If a field is not mentioned, use null.
Be concise but complete.

Document text:
---
{text}
---
"""


def extract_pdf_text(pdf_path, max_pages=10):
    """Extract text from PDF."""
    try:
        text = extract_text(str(pdf_path), maxpages=max_pages)
        return text[:8000]  # Limit to first 8000 chars for token efficiency
    except Exception as e:
        print(f"  ✗ Error extracting text: {e}")
        return None


def parse_aia_with_llm(text, pdf_name):
    """Use LLM to extract structured information from AIA text."""
    if not client.api_key:
        print(f"  ⚠️  No OpenAI API key - skipping LLM parsing for {pdf_name}")
        return None
    
    try:
        prompt = EXTRACTION_PROMPT.format(text=text)
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert at extracting structured data from government documents. Return ONLY valid JSON, no markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON, handling markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        # Find JSON object if wrapped in text
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            response_text = response_text[json_start:json_end]
        
        data = json.loads(response_text)
        return data
    
    except json.JSONDecodeError as e:
        print(f"  ⚠️  JSON parse error: {str(e)[:60]}")
        return None
    except Exception as e:
        print(f"  ⚠️  Error in LLM parsing: {str(e)[:80]}")
        return None


def flatten_aia_data(data):
    """Flatten nested JSON to CSV row."""
    if not data:
        return {}
    
    row = {}
    
    # Flatten metadata
    if "metadata" in data:
        for k, v in data["metadata"].items():
            row[f"metadata_{k}"] = v
    
    # Flatten project overview
    if "project_overview" in data:
        for k, v in data["project_overview"].items():
            row[f"project_{k}"] = v
    
    # Flatten governance
    if "governance" in data:
        for k, v in data["governance"].items():
            row[f"governance_{k}"] = v
    
    # Flatten risk assessment
    if "risk_assessment" in data:
        risk_data = data["risk_assessment"]
        row["risk_identified"] = "; ".join(risk_data.get("risks_identified", []))
        row["risk_mitigation"] = "; ".join(risk_data.get("mitigation_strategies", []))
        row["risk_highest"] = risk_data.get("highest_risk")
    
    # Flatten key terms
    if "key_terms" in data:
        for k, v in data["key_terms"].items():
            row[f"terms_{k}"] = v
    
    # Add document info
    row["document_language"] = data.get("document_language", "UNKNOWN")
    row["extraction_confidence"] = data.get("extraction_confidence", "unknown")
    
    return row


def process_pdf_folder(folder_path, output_dir="data/csv", dry_run=False, limit=None):
    """Process all PDFs in a folder and create CSV files."""
    
    folder = Path(folder_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdfs = sorted(folder.glob("*.pdf"))
    if limit:
        pdfs = pdfs[:limit]
    
    print(f"\n{'='*70}")
    print(f"Processing {len(pdfs)} PDFs from: {folder}")
    print(f"{'='*70}\n")
    
    processed = 0
    failed = 0
    all_rows = []
    fieldnames = set()
    
    for i, pdf_path in enumerate(pdfs, 1):
        print(f"[{i}/{len(pdfs)}] {pdf_path.name[:60]}")
        
        # Extract text
        text = extract_pdf_text(pdf_path)
        if not text:
            print(f"  ✗ Failed to extract text")
            failed += 1
            continue
        
        # Parse with LLM
        structured_data = parse_aia_with_llm(text, pdf_path.name)
        if not structured_data and not dry_run:
            print(f"  ⚠️  LLM parsing failed")
            failed += 1
            continue
        
        # Flatten to CSV row
        row = flatten_aia_data(structured_data)
        row["pdf_filename"] = pdf_path.name
        row["pdf_folder"] = folder.name
        
        # Track fieldnames for CSV
        fieldnames.update(row.keys())
        
        all_rows.append(row)
        processed += 1
        print(f"  ✓ Processed")
    
    # Write individual CSV files (one per PDF)
    print(f"\n{'='*70}")
    print("Writing CSV files...")
    print(f"{'='*70}\n")
    
    fieldnames = sorted(list(fieldnames))
    
    for row in all_rows:
        pdf_name = row["pdf_filename"].replace(".pdf", ".csv")
        csv_path = output_dir / folder.name / pdf_name
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(row)
            print(f"  ✓ {csv_path.name}")
        except Exception as e:
            print(f"  ✗ Error writing {pdf_name}: {e}")
    
    # Write master CSV (all PDFs)
    master_csv = output_dir / f"{folder.name}_master.csv"
    try:
        with open(master_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in all_rows:
                writer.writerow(row)
        print(f"\n✅ Master CSV: {master_csv}")
    except Exception as e:
        print(f"✗ Error writing master CSV: {e}")
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Processed: {processed} PDFs")
    print(f"Failed: {failed} PDFs")
    print(f"Total rows: {len(all_rows)}")
    print(f"Total fields: {len(fieldnames)}")
    
    return all_rows, fieldnames


def create_master_database(csv_dir="data/csv", output_file="data/pdfs/master_database.csv"):
    """Combine all master CSVs into a single database."""
    
    csv_dir = Path(csv_dir)
    all_rows = []
    fieldnames = set()
    
    # Find all master CSVs
    master_files = list(csv_dir.glob("*_master.csv"))
    
    print(f"\n{'='*70}")
    print(f"Creating master database from {len(master_files)} CSV files")
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
    
    # Write master database
    fieldnames = sorted(list(fieldnames))
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in all_rows:
                writer.writerow(row)
        
        print(f"\n✅ Master database created: {output_path}")
        print(f"   Total documents: {len(all_rows)}")
        print(f"   Total fields: {len(fieldnames)}")
        print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
    
    except Exception as e:
        print(f"✗ Error writing master database: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert AIA PDFs to CSV")
    parser.add_argument(
        '--folder',
        choices=['en', 'fr', 'both'],
        default='both',
        help='Which folder to process'
    )
    parser.add_argument(
        '--output',
        default='data/csv',
        help='Output directory for CSV files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test without LLM calls'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of PDFs to process (for testing)'
    )
    parser.add_argument(
        '--skip-database',
        action='store_true',
        help='Skip creating master database'
    )
    
    args = parser.parse_args()
    
    # Process folders
    if args.folder in ['en', 'both']:
        process_pdf_folder(
            'data/pdfs/en',
            output_dir=args.output,
            dry_run=args.dry_run,
            limit=args.limit
        )
    
    if args.folder in ['fr', 'both']:
        process_pdf_folder(
            'data/pdfs/fr',
            output_dir=args.output,
            dry_run=args.dry_run,
            limit=args.limit
        )
    
    # Create master database
    if not args.skip_database:
        create_master_database(
            csv_dir=args.output,
            output_file=f"{args.output}/complete_aia_database.csv"
        )
    
    print(f"\n{'='*70}")
    print("✅ DONE")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
