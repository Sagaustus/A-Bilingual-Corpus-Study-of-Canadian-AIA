# PostgreSQL Database Setup Guide

## Database Structure: 7 Tables

When loading into PostgreSQL, you will have **7 normalized tables** with foreign key relationships:

```
1. projects (master table)
2. systems (linked to projects)
3. governance (linked to projects) ⭐ PRIMARY FOR DIVERGENCE ANALYSIS
4. stakeholders (linked to projects)
5. risk_areas (linked to projects)
6. mitigations (linked to projects AND risk_areas)
7. key_findings (linked to projects)
```

---

## Table Schemas for PostgreSQL

### 1. PROJECTS Table

```sql
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
```

**CSV File**: `projects.csv`

**Columns**: `project_id, pdf_filename, project_title, department, branch, project_phase, program, annual_decisions, language, created_at`

---

### 2. SYSTEMS Table

```sql
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
```

**CSV File**: `systems.csv`

**Columns**: `system_id, project_id, system_purpose, system_description, data_inputs, decision_outputs, affected_population`

---

### 3. GOVERNANCE Table ⭐ **PRIMARY FOR DIVERGENCE ANALYSIS**

```sql
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
```

**CSV File**: `governance.csv`

**Columns**: `governance_id, project_id, oversight_mechanism, appeal_process, transparency_measures, accountability_framework, external_audit`

**Key for Research**: This table contains the EN vs FR governance divergences

---

### 4. STAKEHOLDERS Table

```sql
CREATE TABLE stakeholders (
    stakeholder_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    respondent_name TEXT,
    respondent_title TEXT,
    respondent_email TEXT
);

CREATE INDEX idx_stakeholders_project ON stakeholders(project_id);
```

**CSV File**: `stakeholders.csv`

**Columns**: `stakeholder_id, project_id, respondent_name, respondent_title, respondent_email`

---

### 5. RISK_AREAS Table

```sql
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
```

**CSV File**: `risk_areas.csv`

**Columns**: `risk_id, project_id, risk_area, risk_description, severity, affected_groups`

---

### 6. MITIGATIONS Table

```sql
CREATE TABLE mitigations (
    mitigation_id SERIAL PRIMARY KEY,
    risk_id INTEGER REFERENCES risk_areas(risk_id) ON DELETE SET NULL,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    mitigation_strategy TEXT,
    implementation_status TEXT
);

CREATE INDEX idx_mitigations_risk ON mitigations(risk_id);
CREATE INDEX idx_mitigations_project ON mitigations(project_id);
```

**CSV File**: `mitigations.csv`

**Columns**: `mitigation_id, risk_id, project_id, mitigation_strategy, implementation_status`

**Note**: Has TWO foreign keys (risk_id and project_id)

---

### 7. KEY_FINDINGS Table

```sql
CREATE TABLE key_findings (
    finding_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    biases_identified TEXT,
    fairness_issues TEXT,
    transparency_gaps TEXT,
    accountability_gaps TEXT
);

CREATE INDEX idx_key_findings_project ON key_findings(project_id);
```

**CSV File**: `key_findings.csv`

**Columns**: `finding_id, project_id, biases_identified, fairness_issues, transparency_gaps, accountability_gaps`

---

## Generate CSV Files from PDFs

### Quick Start

```bash
# Generate all 7 CSV files from all PDFs (English + French)
python3 research/pdf_to_postgres_csvs.py --folder both

# Output: data/postgres_csvs/
#   - projects.csv
#   - systems.csv
#   - governance.csv
#   - stakeholders.csv
#   - risk_areas.csv
#   - mitigations.csv
#   - key_findings.csv
```

### Options

```bash
# Process only English PDFs
python3 research/pdf_to_postgres_csvs.py --folder en

# Process only French PDFs
python3 research/pdf_to_postgres_csvs.py --folder fr

# Test with first 5 PDFs only
python3 research/pdf_to_postgres_csvs.py --folder both --limit 5

# Custom output directory
python3 research/pdf_to_postgres_csvs.py --folder both --output /path/to/csvs
```

---

## Import into PostgreSQL

### Step 1: Create Database and Tables

```bash
# Create database
createdb aia_governance

# Create tables
psql aia_governance < create_tables.sql
```

**create_tables.sql** (run all CREATE TABLE statements above)

---

### Step 2: Import CSV Files

```bash
# Import in order (respecting foreign key dependencies)

# 1. Import projects first (master table, no dependencies)
psql aia_governance -c "\COPY projects FROM 'data/postgres_csvs/projects.csv' WITH CSV HEADER"

# 2. Import child tables (all depend on projects)
psql aia_governance -c "\COPY systems FROM 'data/postgres_csvs/systems.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY governance FROM 'data/postgres_csvs/governance.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY stakeholders FROM 'data/postgres_csvs/stakeholders.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY risk_areas FROM 'data/postgres_csvs/risk_areas.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY key_findings FROM 'data/postgres_csvs/key_findings.csv' WITH CSV HEADER"

# 3. Import mitigations last (depends on projects AND risk_areas)
psql aia_governance -c "\COPY mitigations FROM 'data/postgres_csvs/mitigations.csv' WITH CSV HEADER"
```

---

### Step 3: Verify Import

```sql
-- Check row counts
SELECT 'projects' AS table_name, COUNT(*) FROM projects
UNION ALL
SELECT 'systems', COUNT(*) FROM systems
UNION ALL
SELECT 'governance', COUNT(*) FROM governance
UNION ALL
SELECT 'stakeholders', COUNT(*) FROM stakeholders
UNION ALL
SELECT 'risk_areas', COUNT(*) FROM risk_areas
UNION ALL
SELECT 'mitigations', COUNT(*) FROM mitigations
UNION ALL
SELECT 'key_findings', COUNT(*) FROM key_findings;
```

Expected output (after processing 47 documents):
```
 table_name   | count 
--------------+-------
 projects     |    47
 systems      |    47
 governance   |    47
 stakeholders |    47
 risk_areas   |   ~150
 mitigations  |   ~80
 key_findings |    47
```

---

## PostgreSQL Analysis Queries

### Query 1: Find Governance Divergences (EN vs FR)

```sql
SELECT 
    COALESCE(p_en.project_title, p_fr.project_title) AS system,
    p_en.department,
    g_en.oversight_mechanism AS en_oversight,
    g_fr.oversight_mechanism AS fr_oversight,
    CASE 
        WHEN g_en.oversight_mechanism != g_fr.oversight_mechanism THEN '⚠️ DIVERGENCE'
        ELSE '✓ Aligned'
    END AS status
FROM projects p_en
FULL OUTER JOIN projects p_fr 
    ON LOWER(p_en.project_title) = LOWER(p_fr.project_title)
    AND p_en.language = 'en' 
    AND p_fr.language = 'fr'
LEFT JOIN governance g_en ON p_en.project_id = g_en.project_id
LEFT JOIN governance g_fr ON p_fr.project_id = g_fr.project_id
WHERE (p_en.language = 'en' OR p_en.language IS NULL)
  AND (p_fr.language = 'fr' OR p_fr.language IS NULL)
ORDER BY status DESC, system;
```

---

### Query 2: Systems with Governance Gaps

```sql
SELECT 
    p.project_title,
    p.department,
    p.language,
    g.oversight_mechanism,
    g.appeal_process
FROM projects p
LEFT JOIN governance g ON p.project_id = g.project_id
WHERE (g.oversight_mechanism IS NULL OR g.oversight_mechanism = '')
  AND (g.appeal_process IS NULL OR g.appeal_process = '')
ORDER BY p.department, p.project_title;
```

---

### Query 3: Risk Profile by Department

```sql
SELECT 
    p.department,
    COUNT(DISTINCT p.project_id) AS num_systems,
    COUNT(CASE WHEN r.severity = 'High' THEN 1 END) AS high_risks,
    COUNT(CASE WHEN r.severity = 'Medium' THEN 1 END) AS medium_risks,
    COUNT(CASE WHEN r.severity = 'Low' THEN 1 END) AS low_risks
FROM projects p
LEFT JOIN risk_areas r ON p.project_id = r.project_id
GROUP BY p.department
ORDER BY high_risks DESC;
```

---

### Query 4: Unmitigated Risks

```sql
SELECT 
    p.project_title,
    p.department,
    r.risk_area,
    r.severity,
    r.risk_description
FROM risk_areas r
LEFT JOIN mitigations m ON r.risk_id = m.risk_id
JOIN projects p ON r.project_id = p.project_id
WHERE m.mitigation_id IS NULL
ORDER BY 
    CASE r.severity 
        WHEN 'High' THEN 1 
        WHEN 'Medium' THEN 2 
        WHEN 'Low' THEN 3 
    END,
    p.department;
```

---

### Query 5: Bilingual Systems Comparison

```sql
SELECT 
    p.project_title,
    p.language,
    g.oversight_mechanism,
    g.appeal_process,
    g.accountability_framework
FROM projects p
JOIN governance g ON p.project_id = g.project_id
WHERE p.project_title IN (
    SELECT project_title 
    FROM projects 
    GROUP BY project_title 
    HAVING COUNT(DISTINCT language) = 2
)
ORDER BY p.project_title, p.language;
```

---

## Database Diagram

```
┌─────────────────┐
│    PROJECTS     │  (Master table)
│  PK: project_id │
│  - pdf_filename │
│  - title        │
│  - department   │
│  - language     │
└────────┬────────┘
         │
    ┌────┴────┬─────────┬──────────┬──────────┐
    │         │         │          │          │
    ▼         ▼         ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌─────────┐ ┌────────────┐
│SYSTEMS │ │GOVERN  │ │STAKEH  │ │RISK_    │ │KEY_        │
│        │ │ANCE ⭐ │ │OLDERS  │ │AREAS    │ │FINDINGS    │
│FK: proj│ │FK: proj│ │FK: proj│ │FK: proj │ │FK: proj_id │
│_id     │ │_id     │ │_id     │ │_id      │ │            │
└────────┘ └────────┘ └────────┘ └────┬────┘ └────────────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │ MITIGATIONS  │
                               │ FK: risk_id  │
                               │ FK: proj_id  │
                               └──────────────┘
```

---

## Benefits of PostgreSQL vs SQLite

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Concurrent writes** | Single writer | Multiple writers |
| **Max database size** | 281 TB | Unlimited |
| **Network access** | No | Yes (remote clients) |
| **User permissions** | No | Yes (role-based) |
| **Full-text search** | Limited | Advanced (GIN indexes) |
| **JSON support** | Basic | Advanced (JSONB) |
| **Replication** | No | Yes (streaming, logical) |
| **Performance (large)** | Good | Excellent |

**When to use PostgreSQL**:
- Multi-user access needed
- Remote access required
- Large dataset (1M+ rows)
- Production deployment
- Advanced analytics

**When SQLite is sufficient**:
- Single-user analysis
- Local development
- Dataset < 100K rows
- Prototyping

---

## Complete PostgreSQL Setup Script

Create `setup_postgres.sh`:

```bash
#!/bin/bash

# Step 1: Generate CSV files from PDFs
echo "Generating CSV files from PDFs..."
python3 research/pdf_to_postgres_csvs.py --folder both

# Step 2: Create database
echo "Creating PostgreSQL database..."
createdb aia_governance

# Step 3: Create tables
echo "Creating tables..."
psql aia_governance << 'EOF'
-- (paste all CREATE TABLE statements from above)
EOF

# Step 4: Import CSV files
echo "Importing CSV files..."
psql aia_governance -c "\COPY projects FROM 'data/postgres_csvs/projects.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY systems FROM 'data/postgres_csvs/systems.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY governance FROM 'data/postgres_csvs/governance.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY stakeholders FROM 'data/postgres_csvs/stakeholders.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY risk_areas FROM 'data/postgres_csvs/risk_areas.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY key_findings FROM 'data/postgres_csvs/key_findings.csv' WITH CSV HEADER"
psql aia_governance -c "\COPY mitigations FROM 'data/postgres_csvs/mitigations.csv' WITH CSV HEADER"

# Step 5: Verify
echo "Verifying import..."
psql aia_governance -c "
SELECT 'projects' AS table_name, COUNT(*) FROM projects
UNION ALL SELECT 'systems', COUNT(*) FROM systems
UNION ALL SELECT 'governance', COUNT(*) FROM governance
UNION ALL SELECT 'stakeholders', COUNT(*) FROM stakeholders
UNION ALL SELECT 'risk_areas', COUNT(*) FROM risk_areas
UNION ALL SELECT 'mitigations', COUNT(*) FROM mitigations
UNION ALL SELECT 'key_findings', COUNT(*) FROM key_findings;
"

echo "✅ PostgreSQL database setup complete!"
```

---

## Expected Output

After running `python3 research/pdf_to_postgres_csvs.py --folder both`:

```
data/postgres_csvs/
├── projects.csv        (47 rows)
├── systems.csv         (47 rows)
├── governance.csv      (47 rows)
├── stakeholders.csv    (47 rows)
├── risk_areas.csv      (~150 rows)
├── mitigations.csv     (~80 rows)
└── key_findings.csv    (47 rows)
```

Each CSV has proper column headers and is ready for PostgreSQL `\COPY` import.

---

## Summary

**7 Tables for PostgreSQL**:
1. ✅ projects (master)
2. ✅ systems
3. ✅ governance (divergence analysis)
4. ✅ stakeholders
5. ✅ risk_areas
6. ✅ mitigations
7. ✅ key_findings

**CSV Generation**: `python3 research/pdf_to_postgres_csvs.py --folder both`

**Import Order**: projects → systems, governance, stakeholders, risk_areas, key_findings → mitigations

**Ready for**: Divergence analysis, governance gap detection, risk profiling
