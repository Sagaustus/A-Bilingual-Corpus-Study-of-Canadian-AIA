# Relational Database System for AIA Analysis

## Quick Start

### 1. Build the Database

Process all PDFs and create normalized 7-table database:

```bash
# Process all English and French documents (full corpus)
python3 research/build_relational_db.py --folder both

# Or test with subset first
python3 research/build_relational_db.py --folder en --limit 10
```

### 2. Query the Database

Run analytical queries:

```bash
# View summary statistics
python3 research/query_aia_db.py --summary

# Find governance divergences between EN and FR versions
python3 research/query_aia_db.py --divergence

# Find systems with governance gaps
python3 research/query_aia_db.py --gaps

# Analyze risk profiles by department
python3 research/query_aia_db.py --risks

# Find unmitigated risks
python3 research/query_aia_db.py --unmitigated

# Compare EN/FR versions of specific system
python3 research/query_aia_db.py --compare "ATIP Online Request Service"
```

---

## Database Architecture

### 7 Normalized Tables

#### 1. **projects** (Master Table)
Represents each AIA document - the central hub linking all other tables.

| Column | Type | Description |
|--------|------|-------------|
| project_id | INTEGER PRIMARY KEY | Unique identifier for each project |
| pdf_filename | TEXT | Original PDF filename |
| project_title | TEXT | Name of the algorithmic system |
| department | TEXT | Government department responsible |
| branch | TEXT | Sub-branch/division |
| project_phase | TEXT | Phase of system (e.g., "Deployment") |
| program | TEXT | Program name |
| annual_decisions | INTEGER | Estimated annual decisions |
| language | TEXT | Document language (en/fr) |
| extraction_confidence | FLOAT | LLM confidence score (0-1) |
| created_at | TIMESTAMP | Extraction timestamp |

**Foreign Keys**: Referenced by all other tables via `project_id`

---

#### 2. **stakeholders** (Who/Respondents)
People making decisions about the system.

| Column | Type | Description |
|--------|------|-------------|
| stakeholder_id | INTEGER PRIMARY KEY | Unique identifier |
| project_id | INTEGER FK | Links to projects table |
| respondent_name | TEXT | Name of person responding |
| respondent_title | TEXT | Job title/role |
| respondent_email | TEXT | Contact email |

**Example Use**: Find all projects managed by Chief Information Officer

---

#### 3. **systems** (About the System)
Technical description of the algorithmic system.

| Column | Type | Description |
|--------|------|-------------|
| system_id | INTEGER PRIMARY KEY | Unique identifier |
| project_id | INTEGER FK | Links to projects table |
| system_purpose | TEXT | Why the system exists |
| system_description | TEXT | How it works |
| data_inputs | TEXT | What data feeds the system |
| decision_outputs | TEXT | What decisions it makes |
| affected_population | TEXT | Who is affected |

**Example Use**: Find all systems affecting veterans

---

#### 4. **governance** (Oversight & Accountability) ⭐
**PRIMARY TABLE FOR DIVERGENCE ANALYSIS**
- Where EN vs FR discrepancies appear most clearly
- Shows oversight mechanisms and accountability frameworks

| Column | Type | Description |
|--------|------|-------------|
| governance_id | INTEGER PRIMARY KEY | Unique identifier |
| project_id | INTEGER FK | Links to projects table |
| oversight_mechanism | TEXT | How system is monitored |
| appeal_process | TEXT | How citizens can challenge decisions |
| transparency_measures | TEXT | How transparency is ensured |
| accountability_framework | TEXT | Who is accountable |
| external_audit | TEXT | External auditing information |

**Example Use**: Compare governance claims between EN and FR versions

---

#### 5. **risk_areas** (Identified Risks)
Risks identified in the assessment.

| Column | Type | Description |
|--------|------|-------------|
| risk_id | INTEGER PRIMARY KEY | Unique identifier |
| project_id | INTEGER FK | Links to projects table |
| risk_area | TEXT | Category of risk (bias, equity, etc.) |
| risk_description | TEXT | Description of the risk |
| severity | TEXT | High/Medium/Low |
| affected_groups | TEXT | Populations affected by risk |

**Example Use**: Find all high-severity risks affecting minorities

---

#### 6. **mitigations** (Risk Mitigation Strategies)
Strategies to reduce identified risks.

| Column | Type | Description |
|--------|------|-------------|
| mitigation_id | INTEGER PRIMARY KEY | Unique identifier |
| risk_id | INTEGER FK | Links to risk_areas table |
| project_id | INTEGER FK | Links to projects table |
| mitigation_strategy | TEXT | How risk will be reduced |
| implementation_status | TEXT | Planned/In Progress/Complete |

**Note**: Dual FKs allow querying at both risk and project level

**Example Use**: Find unmitigated risks

---

#### 7. **key_findings** (Summary Findings)
Summary assessment findings.

| Column | Type | Description |
|--------|------|-------------|
| finding_id | INTEGER PRIMARY KEY | Unique identifier |
| project_id | INTEGER FK | Links to projects table |
| biases_identified | TEXT | Potential biases found |
| fairness_issues | TEXT | Fairness concerns |
| transparency_gaps | TEXT | Transparency shortcomings |
| accountability_gaps | TEXT | Accountability gaps |

**Example Use**: Find all systems with identified bias

---

## Relationship Diagram

```
                    projects (Master Table)
                  /    |    |    |    \    \
                 /     |    |    |     \    \
           systems  stakeholders governance risk_areas key_findings
                                |
                                |
                          mitigations
```

**Foreign Key Relationships**:
- `systems.project_id` → `projects.project_id`
- `stakeholders.project_id` → `projects.project_id`
- `governance.project_id` → `projects.project_id`
- `risk_areas.project_id` → `projects.project_id`
- `mitigations.project_id` → `projects.project_id`
- `mitigations.risk_id` → `risk_areas.risk_id`
- `key_findings.project_id` → `projects.project_id`

---

## Example SQL Queries for Research

### Query 1: Systems with No Oversight

Find systems where oversight mechanism is missing:

```sql
SELECT p.project_title, p.department, p.language
FROM projects p
LEFT JOIN governance g ON p.project_id = g.project_id
WHERE g.oversight_mechanism IS NULL OR g.oversight_mechanism = '';
```

**Use Case**: Identifying governance gaps

---

### Query 2: Bilingual Governance Divergence ⭐ **KEY FOR CSDH PAPER**

Compare oversight mechanisms between EN and FR versions of same system:

```sql
SELECT 
    COALESCE(p_en.project_title, p_fr.project_title) as system,
    g_en.oversight_mechanism as EN_oversight,
    g_fr.oversight_mechanism as FR_oversight,
    CASE WHEN g_en.oversight_mechanism != g_fr.oversight_mechanism THEN '⚠️ DIVERGENCE' ELSE '✓ Aligned' END as status
FROM projects p_en
FULL OUTER JOIN projects p_fr 
    ON LOWER(p_en.project_title) = LOWER(p_fr.project_title)
LEFT JOIN governance g_en ON p_en.project_id = g_en.project_id AND p_en.language = 'en'
LEFT JOIN governance g_fr ON p_fr.project_id = g_fr.project_id AND p_fr.language = 'fr'
WHERE p_en.language = 'en' AND p_fr.language = 'fr'
ORDER BY status DESC;
```

**Expected Output**:
```
System          | EN Oversight              | FR Oversight      | Status
CRES            | Board review required     | TBS oversight     | ⚠️ DIVERGENCE
ATIP System     | Annual audit              | Annual audit      | ✓ Aligned
```

---

### Query 3: Department Risk Profile

Summarize risks by department:

```sql
SELECT 
    p.department,
    COUNT(DISTINCT p.project_id) as num_systems,
    COUNT(CASE WHEN r.severity = 'High' THEN 1 END) as high_risks,
    COUNT(CASE WHEN r.severity = 'Medium' THEN 1 END) as medium_risks,
    COUNT(CASE WHEN r.severity = 'Low' THEN 1 END) as low_risks
FROM projects p
LEFT JOIN risk_areas r ON p.project_id = r.project_id
GROUP BY p.department
ORDER BY high_risks DESC;
```

---

### Query 4: Governance Gaps (No Oversight + No Appeals)

Systems with both missing oversight AND missing appeal process:

```sql
SELECT p.project_title, p.department, p.language, g.oversight_mechanism, g.appeal_process
FROM projects p
LEFT JOIN governance g ON p.project_id = g.project_id
WHERE (g.oversight_mechanism IS NULL OR g.oversight_mechanism = '')
  AND (g.appeal_process IS NULL OR g.appeal_process = '')
ORDER BY p.department;
```

---

### Query 5: Risks Affecting Specific Populations

Find all risks that affect a particular group:

```sql
SELECT p.project_title, r.risk_area, r.risk_description, r.severity, m.mitigation_strategy
FROM risk_areas r
JOIN projects p ON r.project_id = p.project_id
LEFT JOIN mitigations m ON r.risk_id = m.risk_id
WHERE r.affected_groups LIKE '%Indigenous%'
ORDER BY r.severity DESC;
```

---

## Python Workflow

### Build Database (One-time)

```python
from research.build_relational_db import AIADatabaseBuilder

builder = AIADatabaseBuilder("data/aia_relational.db")
builder.create_database()
builder.process_folder("data/pdfs/en")  # Process English documents
builder.process_folder("data/pdfs/fr")  # Process French documents
builder.generate_schema_report()
builder.close()
```

### Query Database (Reusable)

```python
from research.query_aia_db import AIAQueryTool

tool = AIAQueryTool("data/aia_relational.db")

# Summary statistics
tool.summary_statistics()

# Find divergences
tool.governance_divergence_analysis()

# Find governance gaps
tool.governance_gaps()

# Compare specific systems
tool.system_comparison("CRES")
```

---

## Data Integrity Features

### Foreign Key Constraints

All tables enforce foreign key relationships:

```python
conn.execute("PRAGMA foreign_keys = ON")
```

- Prevents orphaned records
- Maintains referential integrity
- Enables cascading operations

---

### Extraction Confidence Scores

Each project has `extraction_confidence` (0-1) indicating LLM extraction quality:

```sql
-- Find low-confidence extractions that need review
SELECT project_title, extraction_confidence 
FROM projects 
WHERE extraction_confidence < 0.7;
```

---

## Database Capabilities

| Feature | Capability | Limit |
|---------|-----------|-------|
| **Max rows per table** | 2 billion | Practical: 1M+ |
| **Database size** | Unlimited | Practical: <10GB |
| **Tables** | Unlimited | Currently: 7 |
| **Foreign keys per table** | Unlimited | Currently: 1-3 each |
| **Query complexity** | Full SQL92+ | Supports complex JOINs |
| **Transaction support** | ACID compliant | Yes |

---

## Benefits of Relational Design

✅ **Eliminates Data Redundancy**: Department info stored once in projects table
✅ **Supports Complex Queries**: Find patterns across multiple dimensions (e.g., "High-risk systems in Justice Department with no appeal process")
✅ **Enables Divergence Analysis**: Side-by-side EN/FR comparison via JOINs
✅ **Scalable**: Add new documents without schema changes
✅ **Auditable**: Extraction timestamps and confidence scores track data quality
✅ **Integrable**: Export to CSV, JSON, or Power BI for analysis

---

## Usage Examples for CSDH Paper

### Example 1: Quantify Divergence

```bash
# Count systems with different governance claims
python3 research/query_aia_db.py --divergence | grep "DIVERGENCE"
```

**Output for paper**: "Of 47 bilingual systems, 12 (26%) show governance divergences"

---

### Example 2: Specific Evidence

```sql
-- Extract actual divergence examples
SELECT p_en.project_title, g_en.oversight_mechanism, g_fr.oversight_mechanism
FROM projects p_en
JOIN projects p_fr ON LOWER(p_en.project_title) = LOWER(p_fr.project_title)
LEFT JOIN governance g_en ON p_en.project_id = g_en.project_id
LEFT JOIN governance g_fr ON p_fr.project_id = g_fr.project_id
WHERE p_en.language = 'en' AND g_en.oversight_mechanism != g_fr.oversight_mechanism;
```

**Output for paper**: Specific systems and how governance differs by language

---

### Example 3: Risk Comparison

```bash
# Compare which risks appear in EN vs FR versions
python3 research/query_aia_db.py --risks
```

**Output for paper**: Risk severity patterns by department/language

---

## Troubleshooting

### Database Not Found
```bash
# Rebuild:
rm data/aia_relational.db
python3 research/build_relational_db.py --folder both
```

### Query Returns No Results
```bash
# Check what's in database:
python3 research/query_aia_db.py --summary
```

### LLM Extraction Issues
- Check `.env` file has `OPENAI_API_KEY`
- Verify API key is valid (active account, credits)
- Check internet connectivity

---

## Next Steps

1. **Build full database**: `python3 research/build_relational_db.py --folder both`
2. **Run divergence analysis**: `python3 research/query_aia_db.py --divergence`
3. **Generate evidence tables**: Export query results as CSV for paper
4. **Create visualizations**: Import into Tableau/Power BI using database connection

