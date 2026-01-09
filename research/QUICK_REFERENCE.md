# Quick Reference: Commands & Tools

## 🚀 Quick Start (Copy & Paste)

### 1. Build the database (first time only, ~5-10 minutes)
```bash
cd /workspaces/aia-eia-js
python3 research/build_relational_db.py --folder both
```

### 2. Analyze divergences
```bash
python3 research/query_aia_db.py --divergence
```

### 3. Generate all reports
```bash
python3 research/export_divergence_reports.py --all
```

### 4. View the text report
```bash
cat data/divergence_analysis.txt
```

---

## 📋 All Available Commands

### Database Builder

#### Build full database
```bash
python3 research/build_relational_db.py --folder both
```
**Time**: 5-10 minutes | **Cost**: ~$20-30 (API calls)

#### Build English only
```bash
python3 research/build_relational_db.py --folder en
```

#### Build French only
```bash
python3 research/build_relational_db.py --folder fr
```

#### Test with small sample
```bash
python3 research/build_relational_db.py --folder both --limit 5
```

#### View database schema report
```bash
python3 research/build_relational_db.py --report
```

#### Rebuild fresh (delete old database)
```bash
rm data/aia_relational.db
python3 research/build_relational_db.py --folder both
```

---

### Query Tool

#### View summary statistics
```bash
python3 research/query_aia_db.py --summary
```

**Output**:
- Total documents by language
- Records per table
- Governance pattern percentages

#### Find governance divergences (EN vs FR) ⭐
```bash
python3 research/query_aia_db.py --divergence
```

**Output**:
- List of systems with different governance claims
- EN vs FR comparison for oversight, appeals, accountability
- Divergence count summary

#### Find governance gaps
```bash
python3 research/query_aia_db.py --gaps
```

**Output**:
- Systems with no oversight mechanism AND no appeal process
- Department and system name

#### Analyze risks by department
```bash
python3 research/query_aia_db.py --risks
```

**Output**:
- Department breakdown
- High/Medium/Low risk counts

#### Find unmitigated risks
```bash
python3 research/query_aia_db.py --unmitigated
```

**Output**:
- Risks with no mitigation strategy
- Severity levels

#### Compare specific system (EN vs FR)
```bash
python3 research/query_aia_db.py --compare "System Name"
```

**Example**:
```bash
python3 research/query_aia_db.py --compare "CRES"
```

**Output**:
- Side-by-side comparison of same system in both languages
- Shows differences in purpose, oversight, accountability

---

### Report Export Tool

#### Generate all reports (recommended)
```bash
python3 research/export_divergence_reports.py --all
```

**Creates 3 files**:
- `data/governance_divergences.csv` - For Excel/Tableau
- `data/divergence_analysis.txt` - For reading/paper
- `data/divergence_statistics.txt` - Summary stats

#### Generate only statistics
```bash
python3 research/export_divergence_reports.py --stats
```

#### Generate only text report
```bash
python3 research/export_divergence_reports.py --text
```

#### Generate only CSV
```bash
python3 research/export_divergence_reports.py --csv
```

#### View generated reports
```bash
# Detailed text report
cat data/divergence_analysis.txt

# Statistics summary
cat data/divergence_statistics.txt

# CSV for spreadsheet
cat data/governance_divergences.csv
```

---

## 🔧 Advanced: Direct SQL Queries

### Access database via Python
```python
from research.query_aia_db import AIAQueryTool

tool = AIAQueryTool("data/aia_relational.db")

# Run custom SQL
results = tool.query("""
    SELECT p.project_title, p.language, g.oversight_mechanism
    FROM projects p
    LEFT JOIN governance g ON p.project_id = g.project_id
    WHERE p.department = 'Treasury Board Secretariat'
""")

# Pretty print results
tool.print_results(results)
```

### Direct SQLite command line
```bash
sqlite3 data/aia_relational.db << 'EOF'
.headers on
.mode column

-- Show all projects
SELECT project_title, department, language FROM projects;

-- Show governance patterns
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN oversight_mechanism IS NOT NULL THEN 1 ELSE 0 END) as with_oversight
FROM governance;

-- Find specific divergence
SELECT p.project_title, g.oversight_mechanism
FROM projects p
JOIN governance g ON p.project_id = g.project_id
WHERE p.language = 'en' AND p.project_title LIKE '%CRES%';
EOF
```

---

## 📊 Export to Other Formats

### Export to JSON
```bash
python3 << 'EOF'
import sqlite3, json

conn = sqlite3.connect('data/aia_relational.db')
conn.row_factory = sqlite3.Row

# Export projects table
cursor = conn.cursor()
cursor.execute('SELECT * FROM projects')
data = [dict(row) for row in cursor.fetchall()]

with open('data/projects.json', 'w') as f:
    json.dump(data, f, indent=2)

print('✅ Exported to data/projects.json')
conn.close()
EOF
```

### Export to Excel (requires pandas)
```bash
python3 -m pip install pandas openpyxl -q

python3 << 'EOF'
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/aia_relational.db')

# Export governance table
df = pd.read_sql_query("SELECT * FROM governance", conn)
df.to_excel('data/governance.xlsx', index=False)

print('✅ Exported to data/governance.xlsx')
conn.close()
EOF
```

### Export multiple tables
```bash
python3 << 'EOF'
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/aia_relational.db')

tables = ['projects', 'governance', 'risk_areas', 'mitigations']

with pd.ExcelWriter('data/aia_complete.xlsx') as writer:
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        df.to_excel(writer, sheet_name=table, index=False)

print('✅ Exported all tables to data/aia_complete.xlsx')
conn.close()
EOF
```

---

## 🔍 Useful Queries for Your Paper

### Count divergences by type
```bash
python3 << 'EOF'
import sqlite3

conn = sqlite3.connect('data/aia_relational.db')
cursor = conn.cursor()

sql = '''
SELECT 
    COUNT(*) as total_systems,
    SUM(CASE WHEN g_en.oversight_mechanism != g_fr.oversight_mechanism THEN 1 ELSE 0 END) as oversight_divergence,
    SUM(CASE WHEN g_en.appeal_process != g_fr.appeal_process THEN 1 ELSE 0 END) as appeal_divergence,
    SUM(CASE WHEN g_en.accountability_framework != g_fr.accountability_framework THEN 1 ELSE 0 END) as accountability_divergence
FROM projects p_en
FULL OUTER JOIN projects p_fr ON LOWER(p_en.project_title) = LOWER(p_fr.project_title)
LEFT JOIN governance g_en ON p_en.project_id = g_en.project_id AND p_en.language = 'en'
LEFT JOIN governance g_fr ON p_fr.project_id = g_fr.project_id AND p_fr.language = 'fr'
WHERE p_en.language = 'en' AND p_fr.language = 'fr'
'''

cursor.execute(sql)
results = cursor.fetchone()
print(f"Total Systems: {results[0]}")
print(f"Oversight Divergences: {results[1]}")
print(f"Appeal Divergences: {results[2]}")
print(f"Accountability Divergences: {results[3]}")

conn.close()
EOF
```

### Show specific divergence examples
```bash
python3 << 'EOF'
import sqlite3

conn = sqlite3.connect('data/aia_relational.db')
conn.row_factory = sqlite3.Row

sql = '''
SELECT 
    p_en.project_title,
    g_en.oversight_mechanism as EN_oversight,
    g_fr.oversight_mechanism as FR_oversight
FROM projects p_en
JOIN projects p_fr ON LOWER(p_en.project_title) = LOWER(p_fr.project_title)
LEFT JOIN governance g_en ON p_en.project_id = g_en.project_id
LEFT JOIN governance g_fr ON p_fr.project_id = g_fr.project_id
WHERE p_en.language = 'en' 
  AND p_fr.language = 'fr'
  AND g_en.oversight_mechanism != g_fr.oversight_mechanism
LIMIT 5
'''

for row in conn.execute(sql):
    print(f"\n📋 {row[0]}")
    print(f"   EN: {row[1]}")
    print(f"   FR: {row[2]}")

conn.close()
EOF
```

---

## 🛠️ Troubleshooting

### Check database exists and has data
```bash
# Check file exists
ls -lh data/aia_relational.db

# Check row counts
sqlite3 data/aia_relational.db "SELECT COUNT(*) FROM projects"
```

### Verify API key
```bash
# Check if .env has key
cat .env | grep OPENAI_API_KEY

# Test if key is valid
python3 << 'EOF'
from openai import OpenAI
try:
    client = OpenAI()
    print("✅ API key is valid")
except Exception as e:
    print(f"❌ API key error: {e}")
EOF
```

### Clear and rebuild database
```bash
# Back up old database
cp data/aia_relational.db data/aia_relational.db.backup

# Delete old
rm data/aia_relational.db

# Rebuild
python3 research/build_relational_db.py --folder both
```

### Test with small sample
```bash
# Verify scripts work with just 2 documents
python3 research/build_relational_db.py --folder en --limit 2

# Then query
python3 research/query_aia_db.py --summary
```

---

## 📚 File Reference

### Main Scripts
| File | Purpose | Usage |
|------|---------|-------|
| `research/build_relational_db.py` | Create database | `python3 research/build_relational_db.py --folder both` |
| `research/query_aia_db.py` | Query database | `python3 research/query_aia_db.py --divergence` |
| `research/export_divergence_reports.py` | Generate reports | `python3 research/export_divergence_reports.py --all` |

### Documentation
| File | Content |
|------|---------|
| `research/README_RELATIONAL_DB.md` | Overview & quick start |
| `research/RELATIONAL_DATABASE_GUIDE.md` | Full schema documentation |
| `research/SYSTEM_ARCHITECTURE.md` | Visual diagrams & flows |
| `research/DATABASE_SCHEMA.md` | Previous schema docs (still valid) |

### Database Files
| File | Content |
|------|---------|
| `data/aia_relational.db` | SQLite database (main) |
| `data/governance_divergences.csv` | Generated: divergences as CSV |
| `data/divergence_analysis.txt` | Generated: detailed text report |
| `data/divergence_statistics.txt` | Generated: summary statistics |

---

## ⏱️ Timeline for CSDH Paper

```
Day 1:   Build database              python3 research/build_relational_db.py --folder both
Day 2:   Query & export reports      python3 research/query_aia_db.py --divergence
                                     python3 research/export_divergence_reports.py --all
Day 3:   Review divergence_analysis.txt
Day 4:   Extract key findings
Day 5-9: Write results section
Day 10:  Finalize & submit
```

---

## 💡 Tips

1. **Start small**: Test with `--limit 5` first to verify setup
2. **Use all reports**: CSV for data, text for narrative, stats for numbers
3. **Keep backups**: `cp data/aia_relational.db data/aia_relational.db.backup`
4. **Review regularly**: Check `divergence_analysis.txt` for insights
5. **Cite the database**: Note in paper that analysis is based on relational database of 47 bilingual AIAs

---

## 🎯 Success Criteria

✅ Database builds without errors
✅ Queries return results (at minimum: divergence analysis)
✅ Reports generate successfully
✅ Can identify specific EN/FR divergence examples
✅ Can quantify divergence rate (e.g., "26% of systems show divergences")
✅ Have concrete evidence for CSDH paper

---

**All tools are ready to use. Start with:**
```bash
python3 research/build_relational_db.py --folder both
```
