#!/usr/bin/env python3
"""
Query the relational AIA database for analysis and insights
Provides common research queries for governance divergence analysis
"""

import sqlite3
import sys
from pathlib import Path
from tabulate import tabulate

class AIAQueryTool:
    """Query interface for AIA relational database."""
    
    def __init__(self, db_path="data/aia_relational.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
    
    def query(self, sql):
        """Execute SQL query and return results as list of dicts."""
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    
    def print_results(self, results, headers=None):
        """Pretty print query results."""
        if not results:
            print("No results found.")
            return
        
        if headers is None:
            headers = [description[0] for description in results[0].keys()]
        
        data = [list(row) for row in results]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    
    def governance_divergence_analysis(self):
        """Analyze EN vs FR governance divergences."""
        print("\n" + "="*80)
        print("GOVERNANCE DIVERGENCE ANALYSIS")
        print("="*80 + "\n")
        
        sql = '''
            SELECT 
                COALESCE(p_en.project_title, p_fr.project_title) as system,
                p_en.language as en_lang, g_en.oversight_mechanism as en_oversight,
                p_fr.language as fr_lang, g_fr.oversight_mechanism as fr_oversight
            FROM projects p_en
            FULL OUTER JOIN projects p_fr 
                ON LOWER(p_en.project_title) = LOWER(p_fr.project_title)
            LEFT JOIN governance g_en ON p_en.project_id = g_en.project_id AND p_en.language = 'en'
            LEFT JOIN governance g_fr ON p_fr.project_id = g_fr.project_id AND p_fr.language = 'fr'
            WHERE p_en.language = 'en' AND p_fr.language = 'fr'
        '''
        
        results = self.query(sql)
        
        print(f"Found {len(results)} bilingual system pairs\n")
        
        divergences = 0
        for row in results:
            en_oversight = row[2] or "Not mentioned"
            fr_oversight = row[4] or "Not mentioned"
            
            if en_oversight != fr_oversight:
                divergences += 1
                print(f"DIVERGENCE: {row[0]}")
                print(f"  EN: {en_oversight[:70]}")
                print(f"  FR: {fr_oversight[:70]}")
                print()
        
        print(f"Total divergences: {divergences}/{len(results)}")
    
    def governance_gaps(self):
        """Find systems with governance gaps."""
        print("\n" + "="*80)
        print("GOVERNANCE GAPS (No Oversight + No Appeals)")
        print("="*80 + "\n")
        
        sql = '''
            SELECT p.project_title, p.department, g.oversight_mechanism, g.appeal_process
            FROM projects p
            LEFT JOIN governance g ON p.project_id = g.project_id
            WHERE (g.oversight_mechanism IS NULL OR g.oversight_mechanism = '')
              AND (g.appeal_process IS NULL OR g.appeal_process = '')
        '''
        
        results = self.query(sql)
        
        if results:
            data = [
                [r[0][:50], r[1][:40], r[2] or "None", r[3] or "None"]
                for r in results
            ]
            print(tabulate(data, 
                headers=["System", "Department", "Oversight", "Appeals"],
                tablefmt="grid"))
        else:
            print("No governance gaps found.")
        
        print(f"\nTotal: {len(results)} systems")
    
    def risk_profile_by_department(self):
        """Analyze risk profiles by department."""
        print("\n" + "="*80)
        print("RISK PROFILE BY DEPARTMENT")
        print("="*80 + "\n")
        
        sql = '''
            SELECT 
                p.department,
                COUNT(DISTINCT p.project_id) as num_systems,
                COUNT(CASE WHEN r.severity = 'High' THEN 1 END) as high_risks,
                COUNT(CASE WHEN r.severity = 'Medium' THEN 1 END) as medium_risks,
                COUNT(CASE WHEN r.severity = 'Low' THEN 1 END) as low_risks
            FROM projects p
            LEFT JOIN risk_areas r ON p.project_id = r.project_id
            GROUP BY p.department
            ORDER BY high_risks DESC
        '''
        
        results = self.query(sql)
        
        data = [[r[0], r[1], r[2], r[3], r[4]] for r in results]
        print(tabulate(data,
            headers=["Department", "Systems", "High Risk", "Medium Risk", "Low Risk"],
            tablefmt="grid"))
    
    def unmitigated_risks(self):
        """Find risks without mitigations."""
        print("\n" + "="*80)
        print("UNMITIGATED RISKS (No Mitigation Strategy)")
        print("="*80 + "\n")
        
        sql = '''
            SELECT p.project_title, p.department, r.risk_area, r.severity
            FROM risk_areas r
            LEFT JOIN mitigations m ON r.risk_id = m.risk_id
            JOIN projects p ON r.project_id = p.project_id
            WHERE m.mitigation_id IS NULL
            ORDER BY r.severity DESC
        '''
        
        results = self.query(sql)
        
        if results:
            data = [[r[0][:50], r[1][:30], r[2][:40], r[3]] for r in results]
            print(tabulate(data,
                headers=["System", "Department", "Risk", "Severity"],
                tablefmt="grid"))
        else:
            print("No unmitigated risks found.")
        
        print(f"\nTotal: {len(results)} unmitigated risks")
    
    def system_comparison(self, system_name=None):
        """Compare EN and FR versions of same system."""
        print("\n" + "="*80)
        print("SYSTEM COMPARISON: ENGLISH vs FRENCH")
        print("="*80 + "\n")
        
        if system_name is None:
            # List all systems with both EN and FR versions
            sql = '''
                SELECT DISTINCT LOWER(p.project_title) as title, COUNT(*) as versions
                FROM projects p
                GROUP BY LOWER(p.project_title)
                HAVING COUNT(*) > 1
                ORDER BY title
            '''
            results = self.query(sql)
            
            print("Systems available in both languages:\n")
            for i, row in enumerate(results, 1):
                print(f"  {i}. {row[0]}")
            return
        
        # Compare specific system
        sql = f'''
            SELECT 
                p.language,
                p.project_title,
                s.system_purpose,
                g.oversight_mechanism,
                g.accountability_framework
            FROM projects p
            LEFT JOIN systems s ON p.project_id = s.project_id
            LEFT JOIN governance g ON p.project_id = g.project_id
            WHERE LOWER(p.project_title) = LOWER('{system_name}')
        '''
        
        results = self.query(sql)
        
        if len(results) == 2:
            r_en = results[0]
            r_fr = results[1]
            
            print(f"System: {r_en[1]}\n")
            print(f"{'Aspect':<25} {'English':<35} {'French':<35}")
            print("-" * 95)
            print(f"{'Purpose':<25} {str(r_en[2])[:35]:<35} {str(r_fr[2])[:35]:<35}")
            print(f"{'Oversight':<25} {str(r_en[3])[:35]:<35} {str(r_fr[3])[:35]:<35}")
            print(f"{'Accountability':<25} {str(r_en[4])[:35]:<35} {str(r_fr[4])[:35]:<35}")
        else:
            print(f"System '{system_name}' not found or doesn't have both versions.")
    
    def summary_statistics(self):
        """Print summary statistics."""
        print("\n" + "="*80)
        print("DATABASE SUMMARY STATISTICS")
        print("="*80 + "\n")
        
        # Total documents
        sql = "SELECT COUNT(*) FROM projects"
        total = self.query(sql)[0][0]
        
        # Language breakdown
        sql = "SELECT language, COUNT(*) FROM projects GROUP BY language"
        lang_results = self.query(sql)
        
        # Total risks
        sql = "SELECT COUNT(*) FROM risk_areas"
        total_risks = self.query(sql)[0][0]
        
        # Total mitigations
        sql = "SELECT COUNT(*) FROM mitigations"
        total_mitigations = self.query(sql)[0][0]
        
        print(f"Total Projects: {total}")
        for row in lang_results:
            print(f"  {row[0].upper()}: {row[1]}")
        
        print(f"\nTotal Risk Areas: {total_risks}")
        print(f"Total Mitigations: {total_mitigations}")
        
        # Systems with oversight
        sql = "SELECT COUNT(*) FROM governance WHERE oversight_mechanism IS NOT NULL AND oversight_mechanism != ''"
        oversight_count = self.query(sql)[0][0]
        print(f"\nSystems with Oversight: {oversight_count}/{total}")
        
        # Systems with appeals
        sql = "SELECT COUNT(*) FROM governance WHERE appeal_process IS NOT NULL AND appeal_process != ''"
        appeals_count = self.query(sql)[0][0]
        print(f"Systems with Appeal Process: {appeals_count}/{total}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Query AIA relational database")
    parser.add_argument('--db', default='data/aia_relational.db', help='Database path')
    parser.add_argument('--divergence', action='store_true', help='Show governance divergences')
    parser.add_argument('--gaps', action='store_true', help='Show governance gaps')
    parser.add_argument('--risks', action='store_true', help='Show department risk profiles')
    parser.add_argument('--unmitigated', action='store_true', help='Show unmitigated risks')
    parser.add_argument('--compare', help='Compare EN/FR versions of system')
    parser.add_argument('--summary', action='store_true', help='Show summary statistics')
    
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"Database not found: {args.db}")
        print("Run: python3 research/build_relational_db.py --folder both")
        return
    
    tool = AIAQueryTool(args.db)
    
    if args.divergence:
        tool.governance_divergence_analysis()
    elif args.gaps:
        tool.governance_gaps()
    elif args.risks:
        tool.risk_profile_by_department()
    elif args.unmitigated:
        tool.unmitigated_risks()
    elif args.compare:
        tool.system_comparison(args.compare)
    elif args.summary:
        tool.summary_statistics()
    else:
        # Show all
        tool.summary_statistics()
        tool.governance_gaps()
        tool.risk_profile_by_department()


if __name__ == "__main__":
    main()
