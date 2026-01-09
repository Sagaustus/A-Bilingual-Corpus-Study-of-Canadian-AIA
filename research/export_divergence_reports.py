#!/usr/bin/env python3
"""
Export divergence findings from relational database to research-ready reports
Designed for CSDH 2026 CFP integration
"""

import sqlite3
import csv
from pathlib import Path
from datetime import datetime

class DivergenceReportGenerator:
    """Generate divergence evidence reports for academic papers."""
    
    def __init__(self, db_path="data/aia_relational.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
    
    def export_governance_divergences(self, output_csv="data/governance_divergences.csv"):
        """Export all governance divergences to CSV."""
        sql = '''
            SELECT 
                COALESCE(p_en.project_title, p_fr.project_title) as system,
                p_en.department,
                p_en.project_phase,
                g_en.oversight_mechanism as EN_oversight,
                g_fr.oversight_mechanism as FR_oversight,
                g_en.appeal_process as EN_appeal,
                g_fr.appeal_process as FR_appeal,
                g_en.accountability_framework as EN_accountability,
                g_fr.accountability_framework as FR_accountability,
                CASE 
                    WHEN g_en.oversight_mechanism != g_fr.oversight_mechanism THEN 'Oversight'
                    WHEN g_en.appeal_process != g_fr.appeal_process THEN 'Appeals'
                    WHEN g_en.accountability_framework != g_fr.accountability_framework THEN 'Accountability'
                    ELSE 'Other'
                END as divergence_type
            FROM projects p_en
            FULL OUTER JOIN projects p_fr 
                ON LOWER(p_en.project_title) = LOWER(p_fr.project_title)
            LEFT JOIN governance g_en ON p_en.project_id = g_en.project_id AND p_en.language = 'en'
            LEFT JOIN governance g_fr ON p_fr.project_id = g_fr.project_id AND p_fr.language = 'fr'
            WHERE p_en.language = 'en' AND p_fr.language = 'fr'
            ORDER BY divergence_type DESC, system
        '''
        
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # Write to CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'System', 'Department', 'Phase',
                'EN Oversight', 'FR Oversight', 'Divergence',
                'EN Appeals', 'FR Appeals',
                'EN Accountability', 'FR Accountability',
                'Divergence Type'
            ])
            
            divergence_count = 0
            for row in results:
                # Only write if there's actual divergence
                if row[3] != row[4]:  # EN vs FR oversight
                    divergence_count += 1
                    writer.writerow([
                        row[0], row[1], row[2],
                        row[3] or '', row[4] or '', '⚠️' if row[3] != row[4] else '✓',
                        row[5] or '', row[6] or '',
                        row[7] or '', row[8] or '',
                        row[9]
                    ])
        
        return output_csv, divergence_count
    
    def generate_text_report(self, output_file="data/divergence_analysis.txt"):
        """Generate human-readable divergence report."""
        sql = '''
            SELECT 
                COALESCE(p_en.project_title, p_fr.project_title) as system,
                p_en.department,
                g_en.oversight_mechanism as EN_oversight,
                g_fr.oversight_mechanism as FR_oversight,
                g_en.appeal_process as EN_appeal,
                g_fr.appeal_process as FR_appeal,
                g_en.accountability_framework as EN_accountability,
                g_fr.accountability_framework as FR_accountability,
                g_en.transparency_measures as EN_transparency,
                g_fr.transparency_measures as FR_transparency
            FROM projects p_en
            FULL OUTER JOIN projects p_fr 
                ON LOWER(p_en.project_title) = LOWER(p_fr.project_title)
            LEFT JOIN governance g_en ON p_en.project_id = g_en.project_id AND p_en.language = 'en'
            LEFT JOIN governance g_fr ON p_fr.project_id = g_fr.project_id AND p_fr.language = 'fr'
            WHERE p_en.language = 'en' AND p_fr.language = 'fr'
            ORDER BY system
        '''
        
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # Generate report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*100 + "\n")
            f.write("GOVERNANCE DIVERGENCE ANALYSIS: BILINGUAL AIA DOCUMENTS\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*100 + "\n\n")
            
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-"*100 + "\n")
            
            divergence_count = 0
            oversight_divergences = 0
            appeal_divergences = 0
            accountability_divergences = 0
            transparency_divergences = 0
            
            for row in results:
                if row[2] != row[3]:  # EN vs FR oversight
                    oversight_divergences += 1
                    divergence_count += 1
                if row[4] != row[5]:  # EN vs FR appeal
                    appeal_divergences += 1
                    divergence_count += 1
                if row[6] != row[7]:  # EN vs FR accountability
                    accountability_divergences += 1
                    divergence_count += 1
                if row[8] != row[9]:  # EN vs FR transparency
                    transparency_divergences += 1
                    divergence_count += 1
            
            f.write(f"Total Bilingual Systems: {len(results)}\n")
            f.write(f"Systems with Governance Divergences: {divergence_count}\n")
            f.write(f"Divergence Rate: {(divergence_count/len(results)*100):.1f}%\n\n")
            
            f.write("Divergence Breakdown:\n")
            f.write(f"  - Oversight Mechanisms: {oversight_divergences}\n")
            f.write(f"  - Appeal Processes: {appeal_divergences}\n")
            f.write(f"  - Accountability Frameworks: {accountability_divergences}\n")
            f.write(f"  - Transparency Measures: {transparency_divergences}\n\n")
            
            f.write("="*100 + "\n")
            f.write("DETAILED DIVERGENCES BY SYSTEM\n")
            f.write("="*100 + "\n\n")
            
            for row in results:
                has_divergence = (
                    row[2] != row[3] or row[4] != row[5] or 
                    row[6] != row[7] or row[8] != row[9]
                )
                
                if has_divergence:
                    f.write(f"\n📋 SYSTEM: {row[0]}\n")
                    f.write(f"   Department: {row[1]}\n")
                    f.write("-"*100 + "\n")
                    
                    if row[2] != row[3]:
                        f.write(f"\n   ⚠️  OVERSIGHT MECHANISM DIVERGENCE\n")
                        f.write(f"       English: {row[2] or 'Not mentioned'}\n")
                        f.write(f"       French:  {row[3] or 'Not mentioned'}\n")
                    
                    if row[4] != row[5]:
                        f.write(f"\n   ⚠️  APPEAL PROCESS DIVERGENCE\n")
                        f.write(f"       English: {row[4] or 'Not mentioned'}\n")
                        f.write(f"       French:  {row[5] or 'Not mentioned'}\n")
                    
                    if row[6] != row[7]:
                        f.write(f"\n   ⚠️  ACCOUNTABILITY FRAMEWORK DIVERGENCE\n")
                        f.write(f"       English: {row[6] or 'Not mentioned'}\n")
                        f.write(f"       French:  {row[7] or 'Not mentioned'}\n")
                    
                    if row[8] != row[9]:
                        f.write(f"\n   ⚠️  TRANSPARENCY MEASURES DIVERGENCE\n")
                        f.write(f"       English: {row[8] or 'Not mentioned'}\n")
                        f.write(f"       French:  {row[9] or 'Not mentioned'}\n")
                    
                    f.write("\n")
            
            # Methodology section
            f.write("\n" + "="*100 + "\n")
            f.write("METHODOLOGY\n")
            f.write("="*100 + "\n")
            f.write("""
This analysis compares governance descriptions across bilingual Algorithmic Impact Assessment (AIA) 
documents for the same algorithmic systems implemented by Canadian government departments.

Data Source: Paired English/French AIA documents from government Open Data portal
Analysis Method: Relational database comparison of governance fields
Comparison Fields: 
  - Oversight mechanisms (how systems are monitored)
  - Appeal processes (how citizens can challenge decisions)
  - Accountability frameworks (who is accountable)
  - Transparency measures (how information is disclosed)

A "divergence" is recorded when the English and French versions of the same system contain 
different information about any governance field, indicating potential untranslatable governance concepts.
""")
        
        return output_file
    
    def generate_summary_statistics(self, output_file="data/divergence_statistics.txt"):
        """Generate summary statistics file."""
        
        sql_total = "SELECT COUNT(*) FROM projects"
        sql_en = "SELECT COUNT(*) FROM projects WHERE language = 'en'"
        sql_fr = "SELECT COUNT(*) FROM projects WHERE language = 'fr'"
        
        cursor = self.conn.cursor()
        
        cursor.execute(sql_total)
        total = cursor.fetchone()[0]
        cursor.execute(sql_en)
        en_count = cursor.fetchone()[0]
        cursor.execute(sql_fr)
        fr_count = cursor.fetchone()[0]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("RELATIONAL DATABASE STATISTICS\n")
            f.write("="*50 + "\n\n")
            
            f.write("DOCUMENT COUNTS\n")
            f.write("-"*50 + "\n")
            f.write(f"Total Documents: {total}\n")
            f.write(f"English Documents: {en_count}\n")
            f.write(f"French Documents: {fr_count}\n\n")
            
            # Table statistics
            sql_tables = [
                ("projects", "SELECT COUNT(*) FROM projects"),
                ("systems", "SELECT COUNT(*) FROM systems"),
                ("stakeholders", "SELECT COUNT(*) FROM stakeholders"),
                ("governance", "SELECT COUNT(*) FROM governance"),
                ("risk_areas", "SELECT COUNT(*) FROM risk_areas"),
                ("mitigations", "SELECT COUNT(*) FROM mitigations"),
                ("key_findings", "SELECT COUNT(*) FROM key_findings"),
            ]
            
            f.write("TABLE STATISTICS\n")
            f.write("-"*50 + "\n")
            
            for table_name, sql in sql_tables:
                cursor.execute(sql)
                count = cursor.fetchone()[0]
                f.write(f"{table_name}: {count} records\n")
            
            # Governance patterns
            f.write("\n\nGOVERNANCE PATTERNS\n")
            f.write("-"*50 + "\n")
            
            cursor.execute("""
                SELECT COUNT(*) FROM governance 
                WHERE oversight_mechanism IS NOT NULL AND oversight_mechanism != ''
            """)
            oversight = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM governance 
                WHERE appeal_process IS NOT NULL AND appeal_process != ''
            """)
            appeals = cursor.fetchone()[0]
            
            f.write(f"Projects with Oversight: {oversight}/{total}\n")
            f.write(f"Projects with Appeal Process: {appeals}/{total}\n")
            f.write(f"Projects with Both: {min(oversight, appeals)}/{total}\n")
        
        return output_file
    
    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate divergence research reports")
    parser.add_argument('--db', default='data/aia_relational.db', help='Database path')
    parser.add_argument('--all', action='store_true', help='Generate all reports')
    parser.add_argument('--csv', action='store_true', help='Export divergences as CSV')
    parser.add_argument('--text', action='store_true', help='Generate text report')
    parser.add_argument('--stats', action='store_true', help='Generate statistics')
    
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"Database not found: {args.db}")
        return
    
    generator = DivergenceReportGenerator(args.db)
    
    print("Generating reports...\n")
    
    if args.all or args.csv:
        output, count = generator.export_governance_divergences()
        print(f"✅ CSV Report: {output}")
        print(f"   {count} divergences found\n")
    
    if args.all or args.text:
        output = generator.generate_text_report()
        print(f"✅ Text Report: {output}\n")
    
    if args.all or args.stats:
        output = generator.generate_summary_statistics()
        print(f"✅ Statistics: {output}\n")
    
    generator.close()
    
    if not (args.all or args.csv or args.text or args.stats):
        # Default: all
        generator = DivergenceReportGenerator(args.db)
        generator.export_governance_divergences()
        generator.generate_text_report()
        generator.generate_summary_statistics()
        generator.close()
        print("✅ All reports generated")


if __name__ == "__main__":
    main()
