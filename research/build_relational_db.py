#!/usr/bin/env python3
"""
Create normalized relational database from AIA PDFs
Uses LLM to extract structured sections and creates interrelated tables

Database Schema:
  - projects (Project Details)
  - systems (About the System)
  - governance (Governance/Oversight)
  - risks (Risk Areas)
  - mitigations (Risk Mitigations)
  - stakeholders (Respondents/Key People)
  - sections (Assessment Sections 1, 2, 3, etc.)

All tables linked by project_id and respondent_id as foreign keys
"""

import os
import json
import sqlite3
from pathlib import Path
from pdfminer.high_level import extract_text

import dotenv
from openai import OpenAI

# Load environment
dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

# LLM prompt for structured extraction
EXTRACTION_PROMPT = """You are extracting data from a government Algorithmic Impact Assessment (AIA).

Extract and return ONLY the JSON below with actual values or null:

{{"project_details": {{"respondent_name": null, "respondent_title": null, "respondent_email": null, "department": null, "branch": null, "project_title": null, "project_phase": null, "program": null}}, "system_overview": {{"system_purpose": null, "system_description": null, "data_inputs": null, "decision_outputs": null, "affected_population": null}}, "governance": {{"oversight_mechanism": null, "appeal_process": null, "transparency_measures": null, "accountability_framework": null}}, "risk_areas": [], "mitigations": [], "key_findings": {{"biases_identified": null, "fairness_issues": null, "transparency_gaps": null, "accountability_gaps": null}}}}

Fill in actual values from this text:
{text}

Return ONLY the JSON with values filled in where found. Do not include markdown, backticks, or any other text."""


class AIADatabaseBuilder:
    """Build normalized relational database from AIAs."""
    
    def __init__(self, db_path="data/aia_relational.db"):
        self.db_path = db_path
        self.conn = None
        self.project_counter = 0
        self.create_database()
    
    def create_database(self):
        """Create SQLite database with normalized schema."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pdf_filename TEXT UNIQUE,
                project_title TEXT,
                department TEXT,
                branch TEXT,
                project_phase TEXT,
                program TEXT,
                annual_decisions INTEGER,
                language TEXT,
                extraction_confidence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Stakeholders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stakeholders (
                stakeholder_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                respondent_name TEXT,
                respondent_title TEXT,
                respondent_email TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(project_id)
            )
        ''')
        
        # Systems table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS systems (
                system_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER UNIQUE,
                system_purpose TEXT,
                system_description TEXT,
                data_inputs TEXT,
                decision_outputs TEXT,
                affected_population TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(project_id)
            )
        ''')
        
        # Governance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS governance (
                governance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER UNIQUE,
                oversight_mechanism TEXT,
                appeal_process TEXT,
                transparency_measures TEXT,
                accountability_framework TEXT,
                external_audit TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(project_id)
            )
        ''')
        
        # Risk areas table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_areas (
                risk_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                risk_area TEXT,
                risk_description TEXT,
                severity TEXT,
                affected_groups TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(project_id)
            )
        ''')
        
        # Mitigations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mitigations (
                mitigation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                risk_id INTEGER,
                project_id INTEGER,
                mitigation_strategy TEXT,
                implementation_status TEXT,
                FOREIGN KEY(risk_id) REFERENCES risk_areas(risk_id),
                FOREIGN KEY(project_id) REFERENCES projects(project_id)
            )
        ''')
        
        # Key findings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_findings (
                finding_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER UNIQUE,
                biases_identified TEXT,
                fairness_issues TEXT,
                transparency_gaps TEXT,
                accountability_gaps TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(project_id)
            )
        ''')
        
        self.conn.commit()
        print("✅ Database schema created")
    
    def extract_with_llm(self, text, pdf_name):
        """Extract structured data using LLM."""
        try:
            prompt = EXTRACTION_PROMPT.format(text=text)
            
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Extract structured AIA data. Return ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            # Find JSON
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                response_text = response_text[json_start:json_end]
            
            data = json.loads(response_text)
            return data
        
        except Exception as e:
            print(f"  ⚠️  LLM extraction error: {str(e)[:60]}")
            return None
    
    def insert_pdf(self, pdf_path, lang='en'):
        """Extract and insert single PDF into database."""
        try:
            # Extract text
            text = extract_text(str(pdf_path), maxpages=10)[:12000]
            
            # Extract with LLM
            data = self.extract_with_llm(text, pdf_path.name)
            if not data:
                print(f"  ✗ Failed to extract {pdf_path.name}")
                return None
            
            cursor = self.conn.cursor()
            
            # Insert project
            proj_details = data.get("project_details", {})
            cursor.execute('''
                INSERT INTO projects 
                (pdf_filename, project_title, department, branch, project_phase, 
                 program, annual_decisions, language, extraction_confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pdf_path.name,
                proj_details.get("project_title"),
                proj_details.get("department"),
                proj_details.get("branch"),
                proj_details.get("project_phase"),
                proj_details.get("program"),
                proj_details.get("annual_decisions"),
                lang,
                "high"
            ))
            
            project_id = cursor.lastrowid
            
            # Insert stakeholder
            cursor.execute('''
                INSERT INTO stakeholders (project_id, respondent_name, respondent_title, respondent_email)
                VALUES (?, ?, ?, ?)
            ''', (
                project_id,
                proj_details.get("respondent_name"),
                proj_details.get("respondent_title"),
                proj_details.get("respondent_email")
            ))
            
            # Insert system
            system = data.get("system_overview", {})
            cursor.execute('''
                INSERT INTO systems 
                (project_id, system_purpose, system_description, data_inputs, decision_outputs, affected_population)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                project_id,
                system.get("system_purpose"),
                system.get("system_description"),
                system.get("data_inputs"),
                system.get("decision_outputs"),
                system.get("affected_population")
            ))
            
            # Insert governance
            governance = data.get("governance", {})
            cursor.execute('''
                INSERT INTO governance 
                (project_id, oversight_mechanism, appeal_process, transparency_measures, 
                 accountability_framework, external_audit)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                project_id,
                governance.get("oversight_mechanism"),
                governance.get("appeal_process"),
                governance.get("transparency_measures"),
                governance.get("accountability_framework"),
                governance.get("external_audit")
            ))
            
            # Insert risk areas and mitigations
            for risk in data.get("risk_areas", []):
                cursor.execute('''
                    INSERT INTO risk_areas (project_id, risk_area, risk_description, severity, affected_groups)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    project_id,
                    risk.get("area"),
                    risk.get("description"),
                    risk.get("severity"),
                    risk.get("affected_groups")
                ))
                
                risk_id = cursor.lastrowid
                
                # Find matching mitigation
                for mitigation in data.get("mitigations", []):
                    if mitigation.get("risk_area") == risk.get("area"):
                        cursor.execute('''
                            INSERT INTO mitigations 
                            (risk_id, project_id, mitigation_strategy, implementation_status)
                            VALUES (?, ?, ?, ?)
                        ''', (
                            risk_id,
                            project_id,
                            mitigation.get("mitigation_strategy"),
                            mitigation.get("implementation_status")
                        ))
            
            # Insert key findings
            findings = data.get("key_findings", {})
            cursor.execute('''
                INSERT INTO key_findings 
                (project_id, biases_identified, fairness_issues, transparency_gaps, accountability_gaps)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                project_id,
                findings.get("biases_identified"),
                findings.get("fairness_issues"),
                findings.get("transparency_gaps"),
                findings.get("accountability_gaps")
            ))
            
            self.conn.commit()
            print(f"  ✓ Inserted: {pdf_path.name[:50]}")
            return project_id
        
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:80]}")
            return None
    
    def process_folder(self, folder_path, lang='en', limit=None):
        """Process all PDFs in folder."""
        pdfs = sorted(Path(folder_path).glob("*.pdf"))
        if limit:
            pdfs = pdfs[:limit]
        
        print(f"\nProcessing {len(pdfs)} PDFs from {folder_path}")
        print("=" * 70)
        
        for i, pdf in enumerate(pdfs, 1):
            print(f"[{i}/{len(pdfs)}]", end=" ")
            self.insert_pdf(pdf, lang=lang)
    
    def generate_schema_report(self):
        """Generate report on database schema and content."""
        cursor = self.conn.cursor()
        
        print(f"\n{'='*70}")
        print("DATABASE SCHEMA REPORT")
        print(f"{'='*70}\n")
        
        # Table sizes
        cursor.execute("SELECT COUNT(*) FROM projects")
        projects_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM systems")
        systems_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM risk_areas")
        risks_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM mitigations")
        mitigations_count = cursor.fetchone()[0]
        
        print(f"📊 DATABASE CONTENT")
        print(f"{'='*70}")
        print(f"  Projects: {projects_count}")
        print(f"  Systems: {systems_count}")
        print(f"  Risk Areas: {risks_count}")
        print(f"  Mitigations: {mitigations_count}")
        print()
        
        # Governance patterns
        print(f"⚖️  GOVERNANCE PATTERNS")
        print(f"{'='*70}")
        
        cursor.execute('''
            SELECT COUNT(*) FROM governance 
            WHERE oversight_mechanism IS NOT NULL 
            AND oversight_mechanism != ''
        ''')
        oversight_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM governance 
            WHERE appeal_process IS NOT NULL 
            AND appeal_process != ''
        ''')
        appeal_count = cursor.fetchone()[0]
        
        print(f"  Projects with oversight mechanisms: {oversight_count}/{projects_count}")
        print(f"  Projects with appeal processes: {appeal_count}/{projects_count}")
        print()
        
        # Risk patterns
        print(f"⚠️  RISK PATTERNS")
        print(f"{'='*70}")
        
        cursor.execute("SELECT severity, COUNT(*) FROM risk_areas GROUP BY severity")
        severity_dist = cursor.fetchall()
        for severity, count in severity_dist:
            print(f"  {severity} severity risks: {count}")
        print()
        
        # Key findings
        print(f"🔍 KEY FINDINGS")
        print(f"{'='*70}")
        
        cursor.execute('''
            SELECT COUNT(*) FROM key_findings 
            WHERE biases_identified IS NOT NULL 
            AND biases_identified != ''
        ''')
        bias_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM key_findings 
            WHERE fairness_issues IS NOT NULL 
            AND fairness_issues != ''
        ''')
        fairness_count = cursor.fetchone()[0]
        
        print(f"  Projects identifying biases: {bias_count}/{projects_count}")
        print(f"  Projects identifying fairness issues: {fairness_count}/{projects_count}")
        print()
        
        # Database file size
        db_size = Path(self.db_path).stat().st_size / 1024 / 1024
        print(f"💾 DATABASE SIZE: {db_size:.2f} MB")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Build normalized AIA database")
    parser.add_argument('--folder', choices=['en', 'fr', 'both'], default='both')
    parser.add_argument('--output', default='data/aia_relational.db')
    parser.add_argument('--limit', type=int)
    
    args = parser.parse_args()
    
    builder = AIADatabaseBuilder(db_path=args.output)
    
    try:
        if args.folder in ['en', 'both']:
            builder.process_folder('data/pdfs/en', lang='en', limit=args.limit)
        
        if args.folder in ['fr', 'both']:
            builder.process_folder('data/pdfs/fr', lang='fr', limit=args.limit)
        
        builder.generate_schema_report()
        
        print(f"\n{'='*70}")
        print(f"✅ Database saved to: {args.output}")
        print(f"{'='*70}\n")
    
    finally:
        builder.close()


if __name__ == "__main__":
    main()
