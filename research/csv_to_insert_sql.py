#!/usr/bin/env python3
"""
Convert CSV files to INSERT SQL statements for DataGrip.
Generates one SQL file per CSV with INSERT statements.
"""

import csv
import os
from pathlib import Path

def escape_sql_string(value):
    """Escape single quotes and handle NULL values for SQL."""
    if value is None or value == '':
        return 'NULL'
    # Escape single quotes by doubling them
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"

def csv_to_insert_sql(csv_path, table_name, output_dir):
    """Convert a CSV file to INSERT SQL statements."""
    
    print(f"Processing {csv_path.name} → {table_name}...")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if not rows:
            print(f"  ⚠️  No data found in {csv_path.name}")
            return
        
        # Get column names from CSV header
        columns = list(rows[0].keys())
        column_list = ', '.join(columns)
        
        # Generate SQL file
        output_file = output_dir / f"{table_name}_insert.sql"
        
        with open(output_file, 'w', encoding='utf-8') as sql_file:
            # Header comment
            sql_file.write(f"-- INSERT statements for {table_name}\n")
            sql_file.write(f"-- Generated from {csv_path.name}\n")
            sql_file.write(f"-- Total rows: {len(rows)}\n")
            sql_file.write(f"-- Run in DataGrip SQL console\n\n")
            
            # Generate INSERT for each row
            for i, row in enumerate(rows, 1):
                values = []
                for col in columns:
                    value = row.get(col, '')
                    values.append(escape_sql_string(value))
                
                values_list = ', '.join(values)
                sql_file.write(f"INSERT INTO {table_name} ({column_list})\n")
                sql_file.write(f"VALUES ({values_list});\n\n")
            
            # Footer
            sql_file.write(f"-- {len(rows)} rows inserted into {table_name}\n")
        
        print(f"  ✅ Generated {output_file.name} ({len(rows)} INSERT statements)")

def main():
    """Main function to convert all CSV files."""
    
    # Paths
    csv_dir = Path('/workspaces/aia-eia-js/data/postgres_csvs')
    output_dir = Path('/workspaces/aia-eia-js/data/postgres_sql_inserts')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Table definitions (CSV filename → table name)
    # Order matters! (foreign key dependencies)
    csv_tables = [
        ('projects.csv', 'projects'),
        ('systems.csv', 'systems'),
        ('governance.csv', 'governance'),
        ('stakeholders.csv', 'stakeholders'),
        ('risk_areas.csv', 'risk_areas'),
        ('key_findings.csv', 'key_findings'),
        ('mitigations.csv', 'mitigations'),
    ]
    
    print("=" * 80)
    print("📝 CSV to INSERT SQL Converter")
    print("=" * 80)
    print(f"Input:  {csv_dir}")
    print(f"Output: {output_dir}")
    print()
    
    # Convert each CSV
    for csv_file, table_name in csv_tables:
        csv_path = csv_dir / csv_file
        
        if not csv_path.exists():
            print(f"  ⚠️  {csv_file} not found, skipping...")
            continue
        
        csv_to_insert_sql(csv_path, table_name, output_dir)
    
    print()
    print("=" * 80)
    print("✅ Conversion complete!")
    print("=" * 80)
    print()
    print("📁 SQL files created in: data/postgres_sql_inserts/")
    print()
    print("🔄 Load order in DataGrip (copy/paste each file):")
    print()
    for i, (csv_file, table_name) in enumerate(csv_tables, 1):
        print(f"  {i}. {table_name}_insert.sql")
    print()
    print("💡 In DataGrip:")
    print("   1. Open SQL console connected to aia_governance database")
    print("   2. Open each .sql file in order above")
    print("   3. Execute entire file (Ctrl+Enter or Cmd+Enter)")
    print("   4. Check console for success messages")
    print()

if __name__ == '__main__':
    main()
