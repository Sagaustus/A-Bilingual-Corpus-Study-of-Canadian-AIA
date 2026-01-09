# Relational AIA Database Schema

## Overview

Instead of a flat CSV, the relational database stores AIA data in **7 interconnected tables**, normalized to eliminate redundancy and support complex queries.

**Primary Key**: `project_id` (unique identifier for each AIA)  
**Foreign Keys**: Link child tables back to projects

## Database Tables

### 1. **projects** (Main Table)
Stores metadata about each AIA document

| Column | Type | Description |
|--------|------|-------------|
| `project_id` | INTEGER (PK) | Unique identifier for this project/AIA |
| `pdf_filename` | TEXT (UNIQUE) | Source PDF filename |
| `project_title` | TEXT | Name of the algorithmic system |
| `department` | TEXT | Government department |
| `branch` | TEXT | Specific branch/division |
| `project_phase` | TEXT | Planning \| Implementation \| Deployed |
| `program` | TEXT | Departmental program area |
| `annual_decisions` | INTEGER | Estimated decisions/year |
| `language` | TEXT | en \| fr |
| `created_at` | TIMESTAMP | When entered into database |

**Purpose**: Central hub connecting all other tables

---

### 2. **stakeholders**
Information about respondents/decision-makers

| Column | Type | Description |
|--------|------|-------------|
| `stakeholder_id` | INTEGER (PK) | |
| `project_id` | INTEGER (FK) | Links to projects table |
| `respondent_name` | TEXT | Name of survey respondent |
| `respondent_title` | TEXT | Their job title |
| `respondent_email` | TEXT | Contact information |

**Purpose**: Track who is responsible for the system

**Query Example**: Find all systems managed by specific person
```sql
SELECT p.project_title, p.department 
FROM projects p
JOIN stakeholders s ON p.project_id = s.project_id
WHERE s.respondent_name = 'John Smith'
```

---

### 3. **systems**
Describes what the algorithmic system does

| Column | Type | Description |
|--------|------|-------------|
| `system_id` | INTEGER (PK) | |
| `project_id` | INTEGER (FK, UNIQUE) | One system per project |
| `system_purpose` | TEXT | What is it designed to do? |
| `system_description` | TEXT | How does it work? (detailed) |
| `data_inputs` | TEXT | What data feeds in? |
| `decision_outputs` | TEXT | What decisions/recommendations? |
| `affected_population` | TEXT | Who does it impact? |

**Purpose**: Technical description of the algorithm

**Query Example**: Find all systems that use specific type of data
```sql
SELECT p.project_title, s.system_purpose 
FROM systems s
JOIN projects p ON s.project_id = p.project_id
WHERE s.data_inputs LIKE '%criminal%'
```

---

### 4. **governance**
Oversight and accountability mechanisms

| Column | Type | Description |
|--------|------|-------------|
| `governance_id` | INTEGER (PK) | |
| `project_id` | INTEGER (FK, UNIQUE) | One governance record per project |
| `oversight_mechanism` | TEXT | How is it supervised? |
| `appeal_process` | TEXT | How can decisions be challenged? |
| `transparency_measures` | TEXT | How is it explained to the public? |
| `accountability_framework` | TEXT | Who is responsible if something goes wrong? |
| `external_audit` | TEXT | Is it audited externally? |

**Purpose**: Governance claims - **THIS IS WHERE BILINGUAL DIVERGENCE APPEARS**

**Query Example**: Compare governance between EN and FR versions
```sql
SELECT p1.project_title, 
       p1.language, p1.oversight_mechanism,
       p2.language, p2.oversight_mechanism
FROM governance g1
JOIN projects p1 ON g1.project_id = p1.project_id
JOIN projects p2 ON p1.project_title = p2.project_title 
AND p1.language != p2.language
WHERE p1.language = 'en' AND p2.language = 'fr'
```

---

### 5. **risk_areas**
Identified algorithmic risks

| Column | Type | Description |
|--------|------|-------------|
| `risk_id` | INTEGER (PK) | |
| `project_id` | INTEGER (FK) | Which project/system |
| `risk_area` | TEXT | Type of risk (bias, fairness, etc.) |
| `risk_description` | TEXT | Detailed description |
| `severity` | TEXT | Low \| Medium \| High |
| `affected_groups` | TEXT | Which populations at risk? |

**Purpose**: Store identified risks

**Query Example**: Find all high-severity risks
```sql
SELECT p.project_title, r.risk_area, r.affected_groups
FROM risk_areas r
JOIN projects p ON r.project_id = p.project_id
WHERE r.severity = 'High'
ORDER BY p.department
```

---

### 6. **mitigations**
How risks are addressed

| Column | Type | Description |
|--------|------|-------------|
| `mitigation_id` | INTEGER (PK) | |
| `risk_id` | INTEGER (FK) | Which risk does this address? |
| `project_id` | INTEGER (FK) | Which project |
| `mitigation_strategy` | TEXT | How is it being addressed? |
| `implementation_status` | TEXT | Implemented \| Planned \| In-progress |

**Purpose**: Track risk mitigation strategies

**Query Example**: Find risks without mitigations
```sql
SELECT r.risk_area, p.project_title
FROM risk_areas r
LEFT JOIN mitigations m ON r.risk_id = m.risk_id
JOIN projects p ON r.project_id = p.project_id
WHERE m.mitigation_id IS NULL
```

---

### 7. **key_findings**
Summary of assessment findings

| Column | Type | Description |
|--------|------|-------------|
| `finding_id` | INTEGER (PK) | |
| `project_id` | INTEGER (FK, UNIQUE) | One findings record per project |
| `biases_identified` | TEXT | Any bias concerns mentioned? |
| `fairness_issues` | TEXT | Equity/fairness problems? |
| `transparency_gaps` | TEXT | Explainability issues? |
| `accountability_gaps` | TEXT | Oversight weaknesses? |

**Purpose**: High-level summary of concerns

---

## Database Relationships Diagram

```
                    ┌─────────────┐
                    │  projects   │  ← Central table
                    │ (project_id)│
                    └─────────────┘
                          │
            ┌─────────────┼─────────────┐
            │             │             │
       ┌────▼────┐   ┌────▼────┐  ┌───▼──────┐
       │ stakeh. │   │ systems  │  │governance│
       │(respondent) │         │  │ (rules)  │
       └─────────┘   └─────────┘  └──────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼────┐     ┌─────▼──────┐    ┌───▼──┐
    │  risks  │─┐   │ key_findings│   │mitigation│
    │ (hazards)│ └──▶│ (summary)  │   │(solutions)
    └─────────┘     └────────────┘    └────────┘
```

## Example Queries

### Query 1: Find all systems with NO oversight mechanisms

```sql
SELECT p.project_title, p.department, g.oversight_mechanism
FROM projects p
LEFT JOIN governance g ON p.project_id = g.project_id
WHERE g.oversight_mechanism IS NULL 
   OR g.oversight_mechanism = '';
```

### Query 2: Compare accountability between EN and FR versions

```sql
SELECT 
    p_en.project_title,
    g_en.accountability_framework AS EN_accountability,
    g_fr.accountability_framework AS FR_accountability,
    CASE 
        WHEN g_en.accountability_framework = g_fr.accountability_framework THEN 'Same'
        ELSE 'DIVERGENT'
    END AS convergence
FROM projects p_en
JOIN projects p_fr ON p_en.project_title = p_fr.project_title
JOIN governance g_en ON p_en.project_id = g_en.project_id
JOIN governance g_fr ON p_fr.project_id = g_fr.project_id
WHERE p_en.language = 'en' AND p_fr.language = 'fr'
  AND g_en.accountability_framework != g_fr.accountability_framework;
```

### Query 3: Department risk profile

```sql
SELECT 
    p.department,
    COUNT(DISTINCT p.project_id) AS num_systems,
    COUNT(CASE WHEN r.severity = 'High' THEN 1 END) AS high_risks,
    COUNT(CASE WHEN r.severity = 'Medium' THEN 1 END) AS medium_risks,
    COUNT(CASE WHEN m.mitigation_id IS NULL THEN 1 END) AS unmitigated_risks
FROM projects p
LEFT JOIN risk_areas r ON p.project_id = r.project_id
LEFT JOIN mitigations m ON r.risk_id = m.risk_id
GROUP BY p.department
ORDER BY high_risks DESC;
```

### Query 4: Systems with governance gaps (no oversight + no appeals)

```sql
SELECT p.project_title, p.department
FROM projects p
JOIN governance g ON p.project_id = g.project_id
WHERE (g.oversight_mechanism IS NULL OR g.oversight_mechanism = '')
  AND (g.appeal_process IS NULL OR g.appeal_process = '');
```

### Query 5: All risks affecting specific population

```sql
SELECT 
    p.project_title,
    r.risk_area,
    r.risk_description,
    m.mitigation_strategy
FROM risk_areas r
JOIN projects p ON r.project_id = p.project_id
LEFT JOIN mitigations m ON r.risk_id = m.risk_id
WHERE r.affected_groups LIKE '%women%'
   OR r.affected_groups LIKE '%racialized%'
   OR r.affected_groups LIKE '%indigenous%';
```

## Data Types & Capacity

| Metric | Value |
|--------|-------|
| Max text field size | 4 GB |
| Max rows per table | 2 billion |
| Max database size | Unlimited (SQLite expandable) |
| Query performance | Indexed lookups <10ms for 1000+ documents |

## Benefits of Relational Schema

✅ **Eliminates redundancy**: Department names stored once, referenced many times  
✅ **Enables complex queries**: Join tables to find patterns across systems  
✅ **Supports bilingual comparison**: Query EN vs FR versions of same system  
✅ **Flexible analysis**: Extract slices of data for specific research questions  
✅ **Scalable**: Easily add new tables or fields without restructuring existing data  
✅ **Normalized**: Reduces errors and maintains data integrity  

## Usage

### Create database from PDFs:
```bash
python3 research/build_relational_db.py --folder both --limit 10
```

### Query the database:
```python
import sqlite3

conn = sqlite3.connect('data/aia_relational.db')
cursor = conn.cursor()

# Find all systems with accountability mechanisms
cursor.execute('''
    SELECT p.project_title, g.accountability_framework
    FROM projects p
    JOIN governance g ON p.project_id = g.project_id
    WHERE g.accountability_framework IS NOT NULL
''')

for row in cursor.fetchall():
    print(row)
```

### Export specific query to CSV:
```bash
sqlite3 data/aia_relational.db \
".mode csv" \
".output results.csv" \
"SELECT p.project_title, p.department, r.risk_area 
 FROM risk_areas r 
 JOIN projects p ON r.project_id = p.project_id;"
```

---

**Generated**: January 9, 2026  
**Schema Version**: 1.0  
**Tables**: 7  
**Foreign Keys**: 8  
**Ready for**: Multi-dimensional analysis and CSDH 2026 research
