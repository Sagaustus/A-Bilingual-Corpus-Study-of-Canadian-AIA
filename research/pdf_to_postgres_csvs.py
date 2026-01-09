#!/usr/bin/env python3
"""
Extract data from AIA PDFs into 7 separate CSV files for PostgreSQL import
Creates one CSV per table with proper foreign key relationships
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
from pdfminer.high_level import extract_text

import dotenv
from openai import OpenAI

# Load environment
dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

# LLM extraction prompt (same as relational DB)
EXTRACTION_PROMPT = """You are extracting data from a government Algorithmic Impact Assessment (AIA).

Extract and return ONLY the JSON below with actual values or null:

{{"project_details": {{"respondent_name": null, "respondent_title": null, "respondent_email": null, "department": null, "branch": null, "project_title": null, "project_phase": null, "program": null, "annual_decisions": null}}, "system_overview": {{"system_purpose": null, "system_description": null, "data_inputs": null, "decision_outputs": null, "affected_population": null}}, "governance": {{"oversight_mechanism": null, "appeal_process": null, "transparency_measures": null, "accountability_framework": null, "external_audit": null}}, "risk_areas": [], "mitigations": [], "key_findings": {{"biases_identified": null, "fairness_issues": null, "transparency_gaps": null, "accountability_gaps": null}}}}

Fill in actual values from this text:
{text}

Return ONLY the JSON with values filled in where found. Do not include markdown, backticks, or any other text."""


class PostgresCSVGenerator:
    """Generate 7 separate CSV files for PostgreSQL import."""
    
    def __init__(self, output_dir="data/postgres_csvs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # CSV file paths
        self.csv_files = {
            'projects': self.output_dir / 'projects.csv',
            'systems': self.output_dir / 'systems.csv',
            'governance': self.output_dir / 'governance.csv',
            'stakeholders': self.output_dir / 'stakeholders.csv',
            'risk_areas': self.output_dir / 'risk_areas.csv',
            'mitigations': self.output_dir / 'mitigations.csv',
            'key_findings': self.output_dir / 'key_findings.csv',
        }
        
        # CSV writers and files
        self.csv_writers = {}
        self.csv_file_handles = {}
        
        # Counters for IDs
        self.project_id_counter = 1
        self.system_id_counter = 1
        self.governance_id_counter = 1
        self.stakeholder_id_counter = 1
        self.risk_id_counter = 1
        self.mitigation_id_counter = 1
        self.finding_id_counter = 1
        
        self.initialize_csv_files()
    
    def initialize_csv_files(self):
        """Create CSV files with headers."""
        
        # Projects CSV
        self.csv_file_handles['projects'] = open(self.csv_files['projects'], 'w', newline='', encoding='utf-8')
        self.csv_writers['projects'] = csv.writer(self.csv_file_handles['projects'])
        self.csv_writers['projects'].writerow([
            'project_id', 'pdf_filename', 'project_title', 'department', 
            'branch', 'project_phase', 'program', 'annual_decisions', 
            'language', 'created_at'
        ])
        
        # Systems CSV
        self.csv_file_handles['systems'] = open(self.csv_files['systems'], 'w', newline='', encoding='utf-8')
        self.csv_writers['systems'] = csv.writer(self.csv_file_handles['systems'])
        self.csv_writers['systems'].writerow([
            'system_id', 'project_id', 'system_purpose', 'system_description',
            'data_inputs', 'decision_outputs', 'affected_population'
        ])
        
        # Governance CSV
        self.csv_file_handles['governance'] = open(self.csv_files['governance'], 'w', newline='', encoding='utf-8')
        self.csv_writers['governance'] = csv.writer(self.csv_file_handles['governance'])
        self.csv_writers['governance'].writerow([
            'governance_id', 'project_id', 'oversight_mechanism', 'appeal_process',
            'transparency_measures', 'accountability_framework', 'external_audit'
        ])
        
        # Stakeholders CSV
        self.csv_file_handles['stakeholders'] = open(self.csv_files['stakeholders'], 'w', newline='', encoding='utf-8')
        self.csv_writers['stakeholders'] = csv.writer(self.csv_file_handles['stakeholders'])
        self.csv_writers['stakeholders'].writerow([
            'stakeholder_id', 'project_id', 'respondent_name', 
            'respondent_title', 'respondent_email'
        ])
        
        # Risk Areas CSV
        self.csv_file_handles['risk_areas'] = open(self.csv_files['risk_areas'], 'w', newline='', encoding='utf-8')
        self.csv_writers['risk_areas'] = csv.writer(self.csv_file_handles['risk_areas'])
        self.csv_writers['risk_areas'].writerow([
            'risk_id', 'project_id', 'risk_area', 'risk_description',
            'severity', 'affected_groups'
        ])
        
        # Mitigations CSV
        self.csv_file_handles['mitigations'] = open(self.csv_files['mitigations'], 'w', newline='', encoding='utf-8')
        self.csv_writers['mitigations'] = csv.writer(self.csv_file_handles['mitigations'])
        self.csv_writers['mitigations'].writerow([
            'mitigation_id', 'risk_id', 'project_id', 
            'mitigation_strategy', 'implementation_status'
        ])
        
        # Key Findings CSV
        self.csv_file_handles['key_findings'] = open(self.csv_files['key_findings'], 'w', newline='', encoding='utf-8')
        self.csv_writers['key_findings'] = csv.writer(self.csv_file_handles['key_findings'])
        self.csv_writers['key_findings'].writerow([
            'finding_id', 'project_id', 'biases_identified', 
            'fairness_issues', 'transparency_gaps', 'accountability_gaps'
        ])
        
        print(f"✅ Created 7 CSV files in {self.output_dir}/")
    
    def extract_with_llm(self, text):
        """Extract structured data from PDF text using LLM."""
        try:
            # Truncate text if too long
            max_chars = 15000
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
            
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You extract structured data from government documents."},
                    {"role": "user", "content": EXTRACTION_PROMPT.format(text=text)}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("\n", 1)[1]
                content = content.rsplit("```", 1)[0]
            
            data = json.loads(content)
            return data
            
        except json.JSONDecodeError as e:
            print(f"  ⚠️  LLM extraction error: {str(e)[:50]}")
            return None
        except Exception as e:
            print(f"  ⚠️  Error: {str(e)[:50]}")
            return None
    
    def process_pdf(self, pdf_path, language='en'):
        """Process a single PDF and write to all relevant CSV files."""
        
        # Extract text
        try:
            text = extract_text(str(pdf_path))
        except Exception as e:
            print(f"  ⚠️  Failed to extract text: {e}")
            return False
        
        # Extract structured data with LLM
        data = self.extract_with_llm(text)
        if not data:
            return False
        
        # Get current project ID
        project_id = self.project_id_counter
        
        # Write to PROJECTS CSV
        project_details = data.get('project_details', {})
        self.csv_writers['projects'].writerow([
            project_id,
            pdf_path.name,
            project_details.get('project_title') or '',
            project_details.get('department') or '',
            project_details.get('branch') or '',
            project_details.get('project_phase') or '',
            project_details.get('program') or '',
            project_details.get('annual_decisions') or '',
            language,
            datetime.now().isoformat()
        ])
        
        # Write to SYSTEMS CSV
        system_overview = data.get('system_overview', {})
        self.csv_writers['systems'].writerow([
            self.system_id_counter,
            project_id,
            system_overview.get('system_purpose') or '',
            system_overview.get('system_description') or '',
            system_overview.get('data_inputs') or '',
            system_overview.get('decision_outputs') or '',
            system_overview.get('affected_population') or ''
        ])
        self.system_id_counter += 1
        
        # Write to GOVERNANCE CSV
        governance = data.get('governance', {})
        self.csv_writers['governance'].writerow([
            self.governance_id_counter,
            project_id,
            governance.get('oversight_mechanism') or '',
            governance.get('appeal_process') or '',
            governance.get('transparency_measures') or '',
            governance.get('accountability_framework') or '',
            governance.get('external_audit') or ''
        ])
        self.governance_id_counter += 1
        
        # Write to STAKEHOLDERS CSV
        self.csv_writers['stakeholders'].writerow([
            self.stakeholder_id_counter,
            project_id,
            project_details.get('respondent_name') or '',
            project_details.get('respondent_title') or '',
            project_details.get('respondent_email') or ''
        ])
        self.stakeholder_id_counter += 1
        
        # Write to RISK_AREAS CSV
        risk_areas = data.get('risk_areas', [])
        risk_id_map = {}
        for risk in risk_areas:
            risk_id = self.risk_id_counter
            risk_id_map[risk.get('risk_area', '')] = risk_id
            
            self.csv_writers['risk_areas'].writerow([
                risk_id,
                project_id,
                risk.get('risk_area') or '',
                risk.get('risk_description') or '',
                risk.get('severity') or '',
                risk.get('affected_groups') or ''
            ])
            self.risk_id_counter += 1
        
        # Write to MITIGATIONS CSV
        mitigations = data.get('mitigations', [])
        for mitigation in mitigations:
            # Try to link to risk_area
            risk_area_name = mitigation.get('risk_area', '')
            risk_id = risk_id_map.get(risk_area_name, '')
            
            self.csv_writers['mitigations'].writerow([
                self.mitigation_id_counter,
                risk_id,
                project_id,
                mitigation.get('mitigation_strategy') or '',
                mitigation.get('implementation_status') or ''
            ])
            self.mitigation_id_counter += 1
        
        # Write to KEY_FINDINGS CSV
        key_findings = data.get('key_findings', {})
        self.csv_writers['key_findings'].writerow([
            self.finding_id_counter,
            project_id,
            key_findings.get('biases_identified') or '',
            key_findings.get('fairness_issues') or '',
            key_findings.get('transparency_gaps') or '',
            key_findings.get('accountability_gaps') or ''
        ])
        self.finding_id_counter += 1
        
        # Increment project ID
        self.project_id_counter += 1
        
        return True
    
    def process_folder(self, folder_path, language='en', limit=None):
        """Process all PDFs in a folder."""
        folder = Path(folder_path)
        pdf_files = sorted(folder.glob("*.pdf"))
        
        if limit:
            pdf_files = pdf_files[:limit]
        
        print(f"\n{'='*70}")
        print(f"Processing {len(pdf_files)} PDFs from {folder} ({language.upper()})")
        print(f"{'='*70}\n")
        
        success_count = 0
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"[{i}/{len(pdf_files)}] {pdf_path.name}", end=" ... ")
            
            if self.process_pdf(pdf_path, language):
                print("✓")
                success_count += 1
            else:
                print("✗ Failed")
        
        print(f"\n{'='*70}")
        print(f"✅ Successfully processed: {success_count}/{len(pdf_files)}")
        print(f"{'='*70}\n")
        
        return success_count
    
    def close(self):
        """Close all CSV files."""
        for handle in self.csv_file_handles.values():
            handle.close()
        
        print(f"\n{'='*70}")
        print("CSV FILES SUMMARY")
        print(f"{'='*70}")
        
        for name, path in self.csv_files.items():
            size = path.stat().st_size if path.exists() else 0
            rows = sum(1 for _ in open(path)) - 1  # Subtract header
            print(f"  {name:20} {rows:5} rows  ({size/1024:.1f} KB)")
        
        print(f"\n📁 All files saved to: {self.output_dir}/")
        print(f"{'='*70}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate PostgreSQL CSV files from AIA PDFs")
    parser.add_argument('--folder', choices=['en', 'fr', 'both'], default='both',
                        help='Which PDFs to process')
    parser.add_argument('--limit', type=int, help='Limit number of PDFs per folder')
    parser.add_argument('--output', default='data/postgres_csvs',
                        help='Output directory for CSV files')
    
    args = parser.parse_args()
    
    generator = PostgresCSVGenerator(args.output)
    
    total_processed = 0
    
    if args.folder in ['en', 'both']:
        count = generator.process_folder('data/pdfs/en', language='en', limit=args.limit)
        total_processed += count
    
    if args.folder in ['fr', 'both']:
        count = generator.process_folder('data/pdfs/fr', language='fr', limit=args.limit)
        total_processed += count
    
    generator.close()
    
    print(f"\n✅ Total PDFs processed: {total_processed}")
    print(f"✅ Ready for PostgreSQL import")


if __name__ == "__main__":
    main()
