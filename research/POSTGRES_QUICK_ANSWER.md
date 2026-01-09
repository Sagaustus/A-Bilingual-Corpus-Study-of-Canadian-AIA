# PostgreSQL Quick Reference - 7 Tables for AIA Governance

## Answer: 7 Tables Total

When loading into PostgreSQL, you will have **7 normalized tables**:

```
1. projects         (master table - 1 row per PDF)
2. systems          (1 row per project)
3. governance       (1 row per project) ⭐ PRIMARY FOR DIVERGENCE
4. stakeholders     (1 row per project)
5. risk_areas       (0+ rows per project)
6. mitigations      (0+ rows per project)
7. key_findings     (1 row per project)
```

---

## Quick Setup (3 Commands)

### Option A: Generate CSVs Only

```bash
# Generate all 7 CSV files from PDFs (uses GPT-4 API)
python3 research/pdf_to_postgres_csvs.py --folder both

# Output location: data/postgres_csvs/
#   ├── projects.csv
#   ├── systems.csv
#   ├── governance.csv
#   ├── stakeholders.csv
#   ├── risk_areas.csv
#   ├── mitigations.csv
#   └── key_findings.csv
```

### Option B: Full PostgreSQL Setup

```bash
# Generate CSVs + Create database + Import everything
bash research/setup_postgres.sh

# Creates database: aia_governance
# Imports all 7 CSV files
# Verifies data
```

---

## CSV Files Generated

| File | Rows (47 docs) | Description |
|------|----------------|-------------|
| **projects.csv** | 47 | One per PDF document |
| **systems.csv** | 47 | System descriptions |
| **governance.csv** | 47 | Oversight, appeals, accountability ⭐ |
| **stakeholders.csv** | 47 | Respondent information |
| **risk_areas.csv** | ~150 | Identified risks |
| **mitigations.csv** | ~80 | Risk mitigation strategies |
| **key_findings.csv** | 47 | Assessment summaries |

---

## Table Relationships

```
          projects (master)
         /    |    |    |    \    \
        /     |    |    |     \    \
  systems  governance stakeholders risk_areas key_findings
                                    |
                                    └──> mitigations
```

**Foreign Keys**:
- All tables link to `projects` via `project_id`
- `mitigations` also links to `risk_areas` via `risk_id`

---

## CSV Column Structure

### projects.csv
```
project_id, pdf_filename, project_title, department, branch, 
project_phase, program, annual_decisions, language, created_at
```

### governance.csv ⭐
```
governance_id, project_id, oversight_mechanism, appeal_process,
transparency_measures, accountability_framework, external_audit
```

### systems.csv
```
system_id, project_id, system_purpose, system_description,
data_inputs, decision_outputs, affected_population
```

### stakeholders.csv
```
stakeholder_id, project_id, respondent_name, 
respondent_title, respondent_email
```

### risk_areas.csv
```
risk_id, project_id, risk_area, risk_description,
severity, affected_groups
```

### mitigations.csv
```
mitigation_id, risk_id, project_id, 
mitigation_strategy, implementation_status
```

### key_findings.csv
```
finding_id, project_id, biases_identified, 
fairness_issues, transparency_gaps, accountability_gaps
```

---

## Import Order (PostgreSQL)

**MUST import in this order** (respecting foreign keys):

```bash
# 1. Master table first
\COPY projects FROM 'data/postgres_csvs/projects.csv' WITH CSV HEADER

# 2. Child tables (all depend on projects)
\COPY systems FROM 'data/postgres_csvs/systems.csv' WITH CSV HEADER
\COPY governance FROM 'data/postgres_csvs/governance.csv' WITH CSV HEADER
\COPY stakeholders FROM 'data/postgres_csvs/stakeholders.csv' WITH CSV HEADER
\COPY risk_areas FROM 'data/postgres_csvs/risk_areas.csv' WITH CSV HEADER
\COPY key_findings FROM 'data/postgres_csvs/key_findings.csv' WITH CSV HEADER

# 3. Mitigations last (depends on projects AND risk_areas)
\COPY mitigations FROM 'data/postgres_csvs/mitigations.csv' WITH CSV HEADER
```

Or simply run: `bash research/setup_postgres.sh`

---

## Example: What the CSVs Look Like

**projects.csv** (sample):
```csv
project_id,pdf_filename,project_title,department,branch,project_phase,program,annual_decisions,language,created_at
1,ATIP_Online_Request_Service_en_1.pdf,ATIP Digital Services,Treasury Board Secretariat,CIOB,Implementation,,,en,2026-01-09T10:54:43
2,ATIP_Online_Request_Service_en_2.pdf,ATIP Digital Services,Treasury Board Secretariat,CIOB,Implementation,,,en,2026-01-09T10:54:52
```

**governance.csv** (sample):
```csv
governance_id,project_id,oversight_mechanism,appeal_process,transparency_measures,accountability_framework,external_audit
1,1,,,,,
2,2,A data and automation advisory board specified by Treasury Board Secretariat,Yes,"Plain language notice posted through all service delivery channels in use (Internet, in person, mail or telephone)",,
```

---

## Analysis Queries (PostgreSQL)

### Find EN vs FR Divergences

```sql
SELECT 
    p_en.project_title,
    g_en.oversight_mechanism AS en_oversight,
    g_fr.oversight_mechanism AS fr_oversight
FROM projects p_en
JOIN projects p_fr ON LOWER(p_en.project_title) = LOWER(p_fr.project_title)
LEFT JOIN governance g_en ON p_en.project_id = g_en.project_id
LEFT JOIN governance g_fr ON p_fr.project_id = g_fr.project_id
WHERE p_en.language = 'en' AND p_fr.language = 'fr'
  AND g_en.oversight_mechanism != g_fr.oversight_mechanism;
```

### Count Rows by Table

```sql
SELECT 'projects' AS table_name, COUNT(*) FROM projects
UNION ALL SELECT 'governance', COUNT(*) FROM governance
UNION ALL SELECT 'risk_areas', COUNT(*) FROM risk_areas;
```

---

## Options & Variations

### Process Subset of PDFs

```bash
# Test with 5 PDFs only
python3 research/pdf_to_postgres_csvs.py --folder both --limit 5

# English only
python3 research/pdf_to_postgres_csvs.py --folder en

# French only
python3 research/pdf_to_postgres_csvs.py --folder fr

# Custom output directory
python3 research/pdf_to_postgres_csvs.py --folder both --output /tmp/csvs
```

---

## Cost & Time

| Operation | Time | Cost |
|-----------|------|------|
| Generate 47 CSVs | 5-10 min | ~$20-30 (GPT-4 API) |
| Create PostgreSQL tables | <5 sec | Free |
| Import CSVs to PostgreSQL | <10 sec | Free |
| **Total** | **~10 min** | **~$20-30** |

---

## Files Created

After running the script:

```
data/postgres_csvs/
├── projects.csv         ✅ Ready for import
├── systems.csv          ✅ Ready for import
├── governance.csv       ✅ Ready for import (divergence analysis)
├── stakeholders.csv     ✅ Ready for import
├── risk_areas.csv       ✅ Ready for import
├── mitigations.csv      ✅ Ready for import
└── key_findings.csv     ✅ Ready for import
```

---

## Documentation

- **Full Guide**: [POSTGRESQL_SETUP_GUIDE.md](POSTGRESQL_SETUP_GUIDE.md)
- **Table Schemas**: See POSTGRESQL_SETUP_GUIDE.md (CREATE TABLE statements)
- **Example Queries**: See POSTGRESQL_SETUP_GUIDE.md (5+ analytical queries)
- **Setup Script**: [setup_postgres.sh](setup_postgres.sh)

---

## Summary

✅ **7 tables total** for PostgreSQL
✅ **1 CSV file per table** with proper headers
✅ **Foreign key relationships** via project_id and risk_id
✅ **Ready for \COPY import** into PostgreSQL
✅ **Automated script** generates all CSVs from PDFs using GPT-4

**Next Step**: Run `python3 research/pdf_to_postgres_csvs.py --folder both`
