#!/bin/bash
# Complete PostgreSQL setup script for AIA Governance Database
# Generates CSVs from PDFs and loads into PostgreSQL

set -e  # Exit on error

echo "================================================================================"
echo "PostgreSQL Setup for AIA Governance Divergence Analysis"
echo "================================================================================"
echo ""

# Step 1: Generate CSV files from PDFs
echo "Step 1: Generating CSV files from PDFs..."
echo "--------------------------------------------------------------------------------"
python3 research/pdf_to_postgres_csvs.py --folder both

if [ $? -ne 0 ]; then
    echo "❌ CSV generation failed!"
    exit 1
fi

echo ""
echo "✅ CSV generation complete"
echo ""

# Step 2: Create PostgreSQL database
echo "Step 2: Creating PostgreSQL database..."
echo "--------------------------------------------------------------------------------"

DB_NAME="aia_governance"

# Drop database if exists (optional - comment out if you want to keep existing data)
# dropdb --if-exists $DB_NAME

# Create database
createdb $DB_NAME 2>/dev/null || echo "Database $DB_NAME already exists"

echo "✅ Database created: $DB_NAME"
echo ""

# Step 3: Create tables
echo "Step 3: Creating database tables..."
echo "--------------------------------------------------------------------------------"

psql $DB_NAME << 'EOF'
-- Drop existing tables if they exist
DROP TABLE IF EXISTS mitigations CASCADE;
DROP TABLE IF EXISTS key_findings CASCADE;
DROP TABLE IF EXISTS risk_areas CASCADE;
DROP TABLE IF EXISTS stakeholders CASCADE;
DROP TABLE IF EXISTS governance CASCADE;
DROP TABLE IF EXISTS systems CASCADE;
DROP TABLE IF EXISTS projects CASCADE;

-- Create projects table (master table)
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    pdf_filename TEXT NOT NULL,
    project_title TEXT,
    department TEXT,
    branch TEXT,
    project_phase TEXT,
    program TEXT,
    annual_decisions INTEGER,
    language VARCHAR(2) CHECK (language IN ('en', 'fr')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_language ON projects(language);
CREATE INDEX idx_projects_department ON projects(department);
CREATE INDEX idx_projects_title ON projects(project_title);

-- Create systems table
CREATE TABLE systems (
    system_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    system_purpose TEXT,
    system_description TEXT,
    data_inputs TEXT,
    decision_outputs TEXT,
    affected_population TEXT
);

CREATE INDEX idx_systems_project ON systems(project_id);

-- Create governance table (PRIMARY FOR DIVERGENCE ANALYSIS)
CREATE TABLE governance (
    governance_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    oversight_mechanism TEXT,
    appeal_process TEXT,
    transparency_measures TEXT,
    accountability_framework TEXT,
    external_audit TEXT
);

CREATE INDEX idx_governance_project ON governance(project_id);

-- Create stakeholders table
CREATE TABLE stakeholders (
    stakeholder_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    respondent_name TEXT,
    respondent_title TEXT,
    respondent_email TEXT
);

CREATE INDEX idx_stakeholders_project ON stakeholders(project_id);

-- Create risk_areas table
CREATE TABLE risk_areas (
    risk_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    risk_area TEXT,
    risk_description TEXT,
    severity TEXT,
    affected_groups TEXT
);

CREATE INDEX idx_risk_areas_project ON risk_areas(project_id);
CREATE INDEX idx_risk_areas_severity ON risk_areas(severity);

-- Create mitigations table
CREATE TABLE mitigations (
    mitigation_id SERIAL PRIMARY KEY,
    risk_id INTEGER REFERENCES risk_areas(risk_id) ON DELETE SET NULL,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    mitigation_strategy TEXT,
    implementation_status TEXT
);

CREATE INDEX idx_mitigations_risk ON mitigations(risk_id);
CREATE INDEX idx_mitigations_project ON mitigations(project_id);

-- Create key_findings table
CREATE TABLE key_findings (
    finding_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    biases_identified TEXT,
    fairness_issues TEXT,
    transparency_gaps TEXT,
    accountability_gaps TEXT
);

CREATE INDEX idx_key_findings_project ON key_findings(project_id);

\echo '✅ Tables created successfully'
EOF

echo ""
echo "✅ Tables created"
echo ""

# Step 4: Import CSV files
echo "Step 4: Importing CSV files into PostgreSQL..."
echo "--------------------------------------------------------------------------------"

CSV_DIR="data/postgres_csvs"

# Import in order (respecting foreign key dependencies)
echo "  Importing projects.csv..."
psql $DB_NAME -c "\COPY projects(project_id, pdf_filename, project_title, department, branch, project_phase, program, annual_decisions, language, created_at) FROM '$CSV_DIR/projects.csv' WITH CSV HEADER"

echo "  Importing systems.csv..."
psql $DB_NAME -c "\COPY systems(system_id, project_id, system_purpose, system_description, data_inputs, decision_outputs, affected_population) FROM '$CSV_DIR/systems.csv' WITH CSV HEADER"

echo "  Importing governance.csv..."
psql $DB_NAME -c "\COPY governance(governance_id, project_id, oversight_mechanism, appeal_process, transparency_measures, accountability_framework, external_audit) FROM '$CSV_DIR/governance.csv' WITH CSV HEADER"

echo "  Importing stakeholders.csv..."
psql $DB_NAME -c "\COPY stakeholders(stakeholder_id, project_id, respondent_name, respondent_title, respondent_email) FROM '$CSV_DIR/stakeholders.csv' WITH CSV HEADER"

echo "  Importing risk_areas.csv..."
psql $DB_NAME -c "\COPY risk_areas(risk_id, project_id, risk_area, risk_description, severity, affected_groups) FROM '$CSV_DIR/risk_areas.csv' WITH CSV HEADER"

echo "  Importing key_findings.csv..."
psql $DB_NAME -c "\COPY key_findings(finding_id, project_id, biases_identified, fairness_issues, transparency_gaps, accountability_gaps) FROM '$CSV_DIR/key_findings.csv' WITH CSV HEADER"

echo "  Importing mitigations.csv..."
psql $DB_NAME -c "\COPY mitigations(mitigation_id, risk_id, project_id, mitigation_strategy, implementation_status) FROM '$CSV_DIR/mitigations.csv' WITH CSV HEADER"

echo ""
echo "✅ CSV files imported"
echo ""

# Step 5: Update sequences
echo "Step 5: Updating ID sequences..."
echo "--------------------------------------------------------------------------------"

psql $DB_NAME << 'EOF'
-- Update sequences to continue from max ID
SELECT setval('projects_project_id_seq', COALESCE((SELECT MAX(project_id) FROM projects), 1));
SELECT setval('systems_system_id_seq', COALESCE((SELECT MAX(system_id) FROM systems), 1));
SELECT setval('governance_governance_id_seq', COALESCE((SELECT MAX(governance_id) FROM governance), 1));
SELECT setval('stakeholders_stakeholder_id_seq', COALESCE((SELECT MAX(stakeholder_id) FROM stakeholders), 1));
SELECT setval('risk_areas_risk_id_seq', COALESCE((SELECT MAX(risk_id) FROM risk_areas), 1));
SELECT setval('mitigations_mitigation_id_seq', COALESCE((SELECT MAX(mitigation_id) FROM mitigations), 1));
SELECT setval('key_findings_finding_id_seq', COALESCE((SELECT MAX(finding_id) FROM key_findings), 1));
EOF

echo "✅ Sequences updated"
echo ""

# Step 6: Verify import
echo "Step 6: Verifying data import..."
echo "--------------------------------------------------------------------------------"

psql $DB_NAME << 'EOF'
\echo ''
\echo '📊 ROW COUNTS BY TABLE'
\echo '----------------------'
SELECT 
    'projects' AS table_name, 
    COUNT(*) AS rows,
    COUNT(CASE WHEN language = 'en' THEN 1 END) AS en_count,
    COUNT(CASE WHEN language = 'fr' THEN 1 END) AS fr_count
FROM projects
UNION ALL
SELECT 'systems', COUNT(*), NULL, NULL FROM systems
UNION ALL
SELECT 'governance', COUNT(*), NULL, NULL FROM governance
UNION ALL
SELECT 'stakeholders', COUNT(*), NULL, NULL FROM stakeholders
UNION ALL
SELECT 'risk_areas', COUNT(*), NULL, NULL FROM risk_areas
UNION ALL
SELECT 'mitigations', COUNT(*), NULL, NULL FROM mitigations
UNION ALL
SELECT 'key_findings', COUNT(*), NULL, NULL FROM key_findings;

\echo ''
\echo '📋 SAMPLE DATA FROM PROJECTS'
\echo '-----------------------------'
SELECT project_id, project_title, department, language 
FROM projects 
LIMIT 5;

\echo ''
\echo '📋 GOVERNANCE PATTERNS'
\echo '----------------------'
SELECT 
    COUNT(*) AS total_projects,
    COUNT(CASE WHEN oversight_mechanism IS NOT NULL AND oversight_mechanism != '' THEN 1 END) AS with_oversight,
    COUNT(CASE WHEN appeal_process IS NOT NULL AND appeal_process != '' THEN 1 END) AS with_appeals
FROM governance;
EOF

echo ""
echo "================================================================================"
echo "✅ PostgreSQL Setup Complete!"
echo "================================================================================"
echo ""
echo "Database: $DB_NAME"
echo "Tables: 7 (projects, systems, governance, stakeholders, risk_areas, mitigations, key_findings)"
echo ""
echo "Connect: psql $DB_NAME"
echo ""
echo "Example queries available in: research/POSTGRESQL_SETUP_GUIDE.md"
echo ""
echo "================================================================================"
