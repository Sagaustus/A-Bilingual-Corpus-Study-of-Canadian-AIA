# AIA Bilingual Corpus — Pipeline Documentation

> From open-government metadata to a fully normalized relational database of Canadian federal Algorithmic Impact Assessments.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Background — The AIA Form](#2-background--the-aia-form)
3. [Stage 1 — Clean & Normalize AIA.csv](#3-stage-1--clean--normalize-aiacsv)
4. [Stage 2 — Download Source Files](#4-stage-2--download-source-files)
5. [Stage 3 — Structured Text Extraction](#5-stage-3--structured-text-extraction)
6. [Stage 4 — Form Tables & Question Catalog](#6-stage-4--form-tables--question-catalog)
7. [Stage 5 — Section Tables](#7-stage-5--section-tables)
8. [Stage 6 — LLM Semantic Interpretations](#8-stage-6--llm-semantic-interpretations)
9. [Relational Schema](#9-relational-schema)
10. [Repository Structure](#10-repository-structure)
11. [Reproducing the Pipeline](#11-reproducing-the-pipeline)
12. [Research Notes](#12-research-notes)

---

## 1. Project Overview

This project builds a structured, bilingual research corpus from all publicly available Canadian federal **Algorithmic Impact Assessments (AIAs)** — the mandatory risk-disclosure forms required under the Treasury Board Secretariat's *Directive on Automated Decision-Making* before any federal department deploys an automated decision system.

The pipeline runs in six stages:

```
AIA.csv (open.canada.ca)
    │
    ├─ Stage 1  Clean & normalize metadata → relational CSVs
    ├─ Stage 2  Download all 137 source files (PDF, JSON, HTML, CSV, XLSX)
    ├─ Stage 3  Extract structured text from each file
    ├─ Stage 4  Build question catalog + form submission table
    ├─ Stage 5  Build 12 semantically-focused section tables
    └─ Stage 6  LLM semantic interpretations → 4 derived tables + thematic patterns
```

**End result:** a fully normalized relational database covering 32 unique AIA datasets, 114 form submissions, 103 catalogued questions, 30 fully structured assessments, and LLM-generated semantic interpretations — in both English and French — ready for bilingual corpus analysis, LLM-driven semantic research, or quantitative policy comparison.

---

## 2. Background — The AIA Form

The AIA questionnaire is published as an open-source tool at [canada-ca/aia-eia-js](https://github.com/canada-ca/aia-eia-js) and is scored in two parts:

**Section 3.1 — Impact Questions** → *Raw Impact Score*
Questions assess the inherent risk of the automated system across dimensions including: scope of decisions, data sensitivity, reversibility of outcomes, and whether the system is used by a different organization than the one that built it.

**Section 3.2 — Mitigation Questions** → *Mitigation Score*
Questions assess safeguards in place: audit trails, bias testing, GBA+ analysis, privacy impact assessments, recourse processes, and human override capability.

Together these produce an **Impact Level (1–4)** which mandates specific compliance requirements:

| Level | Score range | Key requirements |
|---|---|---|
| 1 | Low | Plain-language explanation |
| 2 | Moderate | Peer review + GBA+ + notice to clients |
| 3 | High | Algorithmic transparency + ongoing monitoring |
| 4 | Very high | Full external audit |

All 32 assessments in this corpus are Level 1 or Level 2. No federal department has publicly disclosed a Level 3 or 4 system.

---

## 3. Stage 1 — Clean & Normalize `AIA.csv`

**Script:** [etl/normalize_aia.py](etl/normalize_aia.py)

### Source data problems

The source file `AIA.csv` (downloaded from open.canada.ca) contained:

| Problem | Detail |
|---|---|
| Duplicate rows | Each dataset repeated **4× identically** (128 rows → 32 unique) |
| Always-null columns | 8 columns with no values in any row |
| Constant columns | 5 columns with the same value in every row |
| Duplicate columns | `Name` = `ID`; `Formats` = `Format`; `Organization` = `Publisher name` |
| Multi-value packing | Subjects, keywords, formats, languages, URLs all comma-packed into single cells |

### Columns dropped

| Column | Reason |
|---|---|
| `Automated translation fields` | Always null |
| `Spatial Representation Type` | Always null |
| `Maintainer` | Always null |
| `Relationship Type` | Always null |
| `Data Includes URIs and Links` | Always null |
| `Spatial` | Always null |
| `Time Period Coverage End` | Always null |
| `Topic category` | Always null |
| `Name` | Duplicate of `ID` |
| `Formats` | Duplicate of `Format` |
| `Organization` | Duplicate of `Publisher - Organization Name at Publication` |

### Constants (documented, not stored as columns)

| Field | Uniform value |
|---|---|
| `Collection Type` | Algorithmic Impact Assessment |
| `Jurisdiction` | Federal |
| `Licence` | Open Government Licence - Canada |
| `Access Restrictions` | unrestricted |
| `Portal Type` | Open Information |

### Output — Dataset layer

| File | Rows | Description |
|---|---|---|
| `etl/output/organizations.csv` | 10 | Federal departments |
| `etl/output/subjects.csv` | 9 | Thematic categories |
| `etl/output/keywords.csv` | 121 | Free-form tags |
| `etl/output/resource_types.csv` | 6 | Assessment, Dataset, Report, Tool, Guide, Risk Assessment |
| `etl/output/languages.csv` | 3 | English, French, No linguistic content |
| `etl/output/formats.csv` | 5 | CSV, HTML, JSON, PDF, XLS |
| `etl/output/datasets.csv` | 32 | Core dataset records |
| `etl/output/resources.csv` | 137 | Individual download URLs |
| `etl/output/dataset_subjects.csv` | 47 | Junction: dataset ↔ subject |
| `etl/output/dataset_keywords.csv` | 222 | Junction: dataset ↔ keyword |
| `etl/output/dataset_resource_types.csv` | 46 | Junction: dataset ↔ resource type |
| `etl/output/dataset_languages.csv` | 67 | Junction: dataset ↔ language |
| `etl/output/dataset_formats.csv` | 61 | Junction: dataset ↔ format |

---

## 4. Stage 2 — Download Source Files

**Script:** [etl/download_resources.py](etl/download_resources.py)

Downloads every URL from `resources.csv` into `resources/{dataset_uuid}/{filename}`, organized by dataset GUID.

### Features

- **Resume-safe:** skips already-downloaded files; retries only failures
- **Polite:** 0.5-second delay between requests
- **Logged:** full outcome written to `etl/output/download_log.csv`
- **Filename handling:** derives safe local filenames from URL path; falls back to `page_en.html` / `page_fr.html` for URL-only resources

### Results

| Status | Count |
|---|---|
| Downloaded | 121 |
| Skipped (already exists) | 6 |
| Failed (SSL — GoC internal CA) | 10 |

The 10 failures are all from `donnees-data.tpsgc-pwgsc.gc.ca` (Public Services and Procurement Canada), which uses a Government of Canada internal certificate authority not trusted by standard environments. Those 10 files must be downloaded manually and placed in `resources/061ee9d1-a04a-4590-a381-df8527390f68/`.

### Files downloaded by type

| Format | Count | Notes |
|---|---|---|
| PDF | 84 | AIA result sheets, peer reviews, GBA+ analyses, annexes |
| JSON | 30 | Raw form data with item codes and bilingual translations |
| CSV | 3 | ATIP data dictionaries |
| HTML | 2 | Web-rendered AIA forms |
| XLSX | 2 | Spreadsheet versions |

---

## 5. Stage 3 — Structured Text Extraction

**Script:** [etl/extract_aia.py](etl/extract_aia.py)

Extracts structured data from each downloaded file according to its format. All PDFs in this corpus have embedded text (no image-based scanning), so OCR was not required — `pdfplumber` extracts clean text directly.

### Extraction methods by format

| Format | Library | Extraction approach |
|---|---|---|
| **JSON** | stdlib `json` | Direct key-value parse; item codes decoded to scores; bilingual field pairs extracted |
| **PDF** | `pdfplumber` | Full text extraction; regex patterns for scored fields; section-delimited Q&A parsing |
| **HTML** | `beautifulsoup4` | DOM parsing after stripping nav/script/footer; same regex patterns as PDF |
| **CSV** | stdlib `csv` | Column names, row count, 5-row preview |
| **XLSX** | `openpyxl` | Sheet names, row count, 5-row preview per sheet |

### Key fields extracted from PDFs (via regex)

| Field | Pattern matched |
|---|---|
| `impact_level` | `Impact Level : N` |
| `current_score` | `Current Score: N` |
| `raw_impact_score` | `Raw Impact Score: N` |
| `mitigation_score` | `Mitigation Score: N` |
| `version` | `Version: N.N.N` |
| `project_title_en` | Text following `5. Project Title` |
| `department` | Text following `3. Department` |
| `description` | Block following `Please provide a project description` |
| `qa_section_text` | Full text of `Section 3: Questions and Answers` |

### Output

- `etl/output/aia_structured.csv` — 121 rows × 40 columns (flat summary, one row per source file)
- `etl/output/extracted/{dataset_uuid}/{filename}.json` — per-file JSON with full parsed content including raw text
- `etl/output/extraction_log.csv` — status per file

### Coverage

| Metric | Count |
|---|---|
| Files processed | 121 |
| Errors | 0 |
| PDFs with impact level extracted | 30 (AIA result sheets only) |
| JSON submissions with full structured data | 30 |

---

## 6. Stage 4 — Form Tables & Question Catalog

### Question Catalog

**Script:** [etl/build_question_catalog.py](etl/build_question_catalog.py)
**Output:** `etl/output/questions.csv` (103 rows)

Maps every AIA form question to a stable `question_id`, with its section, subsection, answer type, corresponding JSON field key, and maximum score contribution.

#### Question ID scheme

```
PD-01  →  Project Details, question 1
IA-13  →  Impact Assessment, question 13 (public scrutiny score)
MQ-09  →  Mitigation Questions, question 9 (GBA+ conducted)
```

#### Section breakdown

| Section | Code | Subsections | Questions |
|---|---|---|---|
| Project Details | PD | Admin, System capabilities | 10 |
| Impact Assessment | IA | Reasons for Automation (12), Risk Profile (5), Project Authority (1), About the Algorithm (2), About the Decision (12), Individual Impacts (8), About the Data (13) | 53 |
| Mitigation Questions | MQ | Consultation (6), Data Quality & Bias (10), Fairness (17), Privacy & Security (7) | 40 |

#### Answer types

| Type | Description | Example fields |
|---|---|---|
| `scored` | Single item code; trailing digit = score | `riskProfile1`, `impact22` |
| `boolean` | Scored with 0 = No, >0 = Yes | `aboutAlgorithm1`, `privacyImplementation1` |
| `text` | Free-text narrative | `projectDetailsDescription`, `impact12` |
| `multi` | List of item codes | `businessDrivers1`, `consultationImplementation2` |

### Form Submissions Table

**Script:** [etl/build_form_tables.py](etl/build_form_tables.py)
**Output:** `etl/output/form_submissions.csv` (114 rows)

One row per source file, linked to `datasets` via `dataset_id`. Carries:
- Computed scores from PDFs (`impact_level`, `current_score`, `raw_impact_score`, `mitigation_score`)
- Form version from JSONs
- Language detection from filename patterns and content heuristics

---

## 7. Stage 5 — Section Tables

**Script:** [etl/build_section_tables.py](etl/build_section_tables.py)
**Output:** `etl/output/section/` (12 CSV files, 30 rows each)

Produces 12 semantically-focused tables — one per AIA form section — each with one row per JSON form submission. These are the primary tables for corpus analysis and LLM-driven semantic research.

All 12 section tables join to `form_submissions` on `submission_id`.

### Column conventions

| Convention | Meaning |
|---|---|
| `_score` suffix | Integer extracted from item code (0–4 scale) |
| `_en` suffix | English text from `data.*` |
| `_fr` suffix | French text from `translationsOnResult.*` |
| `_list` suffix | Comma-joined multi-select item codes |
| `_types` suffix | Comma-joined multi-select codes (categories) |

### Section table details

| # | Table | Key columns | Fill rate |
|---|---|---|---|
| 1 | `project_details` | `project_title_en/fr`, `department`, `phase`, `description_en/fr`, `system_capabilities` | 77% |
| 2 | `reasons_for_automation` | `motivation_types`, `client_needs_en/fr`, `public_benefits_en/fr`, `effectiveness_score`, `trade_offs_en/fr` | 46% |
| 3 | `risk_profile` | `public_scrutiny_score`, `vulnerable_clients_score`, `high_stakes_score`, `staff_impact_score`, `disability_barriers_score`, `risk_total` | 93% |
| 4 | `project_authority` | `new_policy_authority_score` | 100% |
| 5 | `about_the_algorithm` | `is_trade_secret_score`, `is_hard_to_explain_score` | 100% |
| 6 | `about_the_decision` | `decision_description_en/fr`, `decision_sectors`, `automation_type_score`, `system_role_en/fr`, `impacts_reversible_score` | 58% |
| 7 | `individual_impacts` | `rights_freedoms_score/en/fr`, `equality_dignity_score/en/fr`, `health_wellbeing_score/en/fr`, `economic_interests_score/en/fr` | 76% |
| 8 | `about_the_data` | `uses_personal_info`, `security_classification_score`, `data_controller_score`, `data_description_en/fr`, `uses_unstructured_data` | 82% |
| 9 | `consultation` | `internal_stakeholders_engaged/list`, `external_stakeholders_engaged/list`, `*_other_en/fr` | 65% |
| 10 | `data_quality_bias` | 10 binary safeguard flags: bias testing, GBA+, accountability, open data | 100% |
| 11 | `fairness` | 17 binary audit trail flags: authority, override, recourse, EARB | 100% |
| 12 | `privacy_security` | `pia_conducted`, `pia_description_en/fr`, `privacy_by_design`, `de_identification_applied` | 59% |

---

## 8. Stage 6 — LLM Semantic Interpretations

**Script:** [etl/llm_semantic_etl.py](etl/llm_semantic_etl.py)
**Schema:** [etl/schema_interpretations.sql](etl/schema_interpretations.sql)
**Model:** `meta-llama/Llama-3.3-70B-Instruct` via IONOS inference API

Sends respondent answers from the 12 section tables to an LLM with structured prompts and writes derived interpretation rows back into PostgreSQL. All outputs include the raw LLM response, model ID, and prompt version for reproducibility.

### Analysis types

| # | Table | Sources | What it produces |
|---|---|---|---|
| 1 | `interp_automation_justification` | project_details, reasons_for_automation, about_the_decision | Justification theme, strength score (1-5), public benefit clarity, trade-off adequacy, confinement assessment |
| 2 | `interp_risk_rights_impact` | risk_profile, individual_impacts, about_the_decision | Risk level label, dominant risk dimension, rights concern summary, proportionality assessment |
| 3 | `interp_bilingual_divergence` | All tables with _en/_fr field pairs (19 bilingual pairs per submission) | Divergence detection, divergent field details, fidelity score (0-5), untranslatable concepts |
| 4 | `interp_safeguard_compliance` | consultation, data_quality_bias, fairness, privacy_security | Compliance label/score, per-domain assessments, gap identification |
| 5 | `interp_thematic_patterns` | All 4 interpretation tables above | Cross-submission recurring themes with prevalence and outliers |

### Key results

| Analysis | Key finding |
|---|---|
| **Justification** | 57% of submissions cite efficiency as primary theme; client service and compliance are secondary |
| **Risk** | Public scrutiny and high-stakes decision-making are the dominant risk dimensions |
| **Divergence** | 97% of submissions show bilingual divergence; median fidelity score is 4/5 |
| **Safeguard** | Most submissions score "adequate" (3/5); bias testing transparency and stakeholder engagement are the most common gaps |
| **Themes** | 22 cross-submission themes identified across all four dimensions |

### Features

- **Idempotent:** skips already-processed submissions at the current prompt version
- **Rate-limited:** configurable delay between API calls (default 1.5s)
- **Versioned prompts:** each prompt template has a version string; re-running with a new version processes all submissions again
- **Auditable:** every row stores `raw_llm_response` (JSONB), `model_id`, and `prompt_version`
- **CLI interface:** `--analysis`, `--limit`, `--dry-run` flags

### Usage

```bash
# Run all analyses
python3 etl/llm_semantic_etl.py --analysis all

# Run a single analysis type
python3 etl/llm_semantic_etl.py --analysis divergence

# Test with 3 submissions, no API calls
python3 etl/llm_semantic_etl.py --analysis justification --limit 3 --dry-run
```

---

## 9. Relational Schema

**Files:**
- [etl/schema.sql](etl/schema.sql) — PostgreSQL DDL (source tables)
- [etl/schema_interpretations.sql](etl/schema_interpretations.sql) — PostgreSQL DDL (interpretation tables)
- [etl/schema.dbml](etl/schema.dbml) — dbdiagram.io visualization (paste at dbdiagram.io/d)

### Full table inventory

```
Lookup tables
  organizations        (10 rows)
  subjects             (9 rows)
  keywords             (121 rows)
  resource_types       (6 rows)
  languages            (3 rows)
  formats              (5 rows)

Dataset layer
  datasets             (32 rows)   ← core open.canada.ca metadata
  resources            (137 rows)  ← individual download URLs
  dataset_subjects     (47 rows)   ← junction
  dataset_keywords     (222 rows)  ← junction
  dataset_resource_types (46 rows) ← junction
  dataset_languages    (67 rows)   ← junction
  dataset_formats      (61 rows)   ← junction

Form layer
  questions            (103 rows)  ← AIA question catalog
  form_submissions     (114 rows)  ← one per source file

Section tables (30 rows each, from JSON submissions)
  project_details
  reasons_for_automation
  risk_profile
  project_authority
  about_the_algorithm
  about_the_decision
  individual_impacts
  about_the_data
  consultation
  data_quality_bias
  fairness
  privacy_security

LLM interpretation layer (Stage 6)
  interp_automation_justification (30 rows)
  interp_risk_rights_impact       (30 rows)
  interp_bilingual_divergence     (30 rows)
  interp_safeguard_compliance     (30 rows)
  interp_thematic_patterns        (22 rows)
  interp_run_log                  (tracking)
```

### Entity relationships

```
organizations ←─ datasets ─→ dataset_subjects      → subjects
                    │    └──→ dataset_keywords       → keywords
                    │    └──→ dataset_resource_types → resource_types
                    │    └──→ dataset_languages      → languages
                    │    └──→ dataset_formats        → formats
                    │
                    └──→ resources
                    │
                    └──→ form_submissions ──→ questions
                              │
                              ├──→ project_details        (1:1)
                              ├──→ reasons_for_automation (1:1)
                              ├──→ risk_profile           (1:1)
                              ├──→ project_authority      (1:1)
                              ├──→ about_the_algorithm    (1:1)
                              ├──→ about_the_decision     (1:1)
                              ├──→ individual_impacts     (1:1)
                              ├──→ about_the_data         (1:1)
                              ├──→ consultation           (1:1)
                              ├──→ data_quality_bias      (1:1)
                              ├──→ fairness               (1:1)
                              ├──→ privacy_security       (1:1)
                              │
                              │  LLM-derived (Stage 6)
                              ├──→ interp_automation_justification (1:1)
                              ├──→ interp_risk_rights_impact       (1:1)
                              ├──→ interp_bilingual_divergence     (1:1)
                              └──→ interp_safeguard_compliance     (1:1)
                                        │
                                        └──→ interp_thematic_patterns (cross-submission)
```

---

## 10. Repository Structure

```
.
├── AIA.csv                               # Source: open.canada.ca metadata export
├── CORPUS_PIPELINE.md                    # This document
│
├── resources/                            # Stage 2 output: downloaded source files
│   └── {dataset_uuid}/
│       ├── aia-english.pdf
│       ├── aia-results-bilingual.json
│       └── ...
│
└── etl/
    ├── normalize_aia.py                  # Stage 1
    ├── download_resources.py             # Stage 2
    ├── extract_aia.py                    # Stage 3
    ├── build_question_catalog.py         # Stage 4a
    ├── build_form_tables.py              # Stage 4b
    ├── build_section_tables.py           # Stage 5
    ├── llm_semantic_etl.py              # Stage 6 — LLM interpretations
    ├── schema.sql                        # PostgreSQL DDL (source tables)
    ├── schema_interpretations.sql        # PostgreSQL DDL (LLM-derived tables)
    ├── schema.dbml                       # dbdiagram.io schema
    │
    └── output/
        ├── organizations.csv             } Dataset layer
        ├── subjects.csv                  }
        ├── keywords.csv                  }
        ├── resource_types.csv            }
        ├── languages.csv                 }
        ├── formats.csv                   }
        ├── datasets.csv                  }
        ├── resources.csv                 }
        ├── dataset_subjects.csv          }
        ├── dataset_keywords.csv          }
        ├── dataset_resource_types.csv    }
        ├── dataset_languages.csv         }
        ├── dataset_formats.csv           }
        │
        ├── questions.csv                 } Form layer
        ├── form_submissions.csv          }
        ├── aia_structured.csv            } Flat extraction summary
        │
        ├── download_log.csv              } Operational logs
        ├── extraction_log.csv            }
        │
        ├── extracted/                    Stage 3 per-file JSON output
        │   └── {dataset_uuid}/
        │       └── {filename}.json
        │
        └── section/                      Stage 5: 12 section tables
            ├── project_details.csv
            ├── reasons_for_automation.csv
            ├── risk_profile.csv
            ├── project_authority.csv
            ├── about_the_algorithm.csv
            ├── about_the_decision.csv
            ├── individual_impacts.csv
            ├── about_the_data.csv
            ├── consultation.csv
            ├── data_quality_bias.csv
            ├── fairness.csv
            └── privacy_security.csv
```

---

## 11. Reproducing the Pipeline

### Requirements

```bash
pip install pdfplumber openpyxl pandas beautifulsoup4 requests psycopg2-binary python-dotenv openai
```

### Run stages in order

```bash
# Stage 1 — Clean and normalize AIA.csv
python3 etl/normalize_aia.py

# Stage 2 — Download all source files (resume-safe; re-run safely)
python3 etl/download_resources.py

# Stage 3 — Extract structured data from all downloaded files
python3 etl/extract_aia.py

# Stage 4 — Build question catalog and form submissions
python3 etl/build_question_catalog.py
python3 etl/build_form_tables.py

# Stage 5 — Build 12 section-specific tables
python3 etl/build_section_tables.py
```

### Load into PostgreSQL

The local database is named **`aia_corpus`**. It contains 27 source tables, 6 interpretation tables, and 1 view.

```bash
# Create the database (one-time)
psql -d postgres -c "CREATE DATABASE aia_corpus;"

# Create schema (tables, indexes, views)
psql -d aia_corpus -f etl/schema.sql

# Load in dependency order: lookups → core → junctions → form layer → sections
for table in organizations subjects keywords resource_types languages formats; do
  psql -d aia_corpus -c "\COPY $table FROM 'etl/output/$table.csv' CSV HEADER"
done

psql -d aia_corpus -c "\COPY datasets FROM 'etl/output/datasets.csv' CSV HEADER"
psql -d aia_corpus -c "\COPY resources FROM 'etl/output/resources.csv' CSV HEADER"

for table in dataset_subjects dataset_keywords dataset_resource_types dataset_languages dataset_formats; do
  psql -d aia_corpus -c "\COPY $table FROM 'etl/output/$table.csv' CSV HEADER"
done

psql -d aia_corpus -c "\COPY questions FROM 'etl/output/questions.csv' CSV HEADER"
psql -d aia_corpus -c "\COPY form_submissions FROM 'etl/output/form_submissions.csv' CSV HEADER"

for table in project_details reasons_for_automation risk_profile project_authority \
             about_the_algorithm about_the_decision individual_impacts about_the_data \
             consultation data_quality_bias fairness privacy_security; do
  psql -d aia_corpus -c "\COPY $table FROM 'etl/output/section/$table.csv' CSV HEADER"
done
```

### Verify the database

```bash
psql -d aia_corpus -c "
SELECT relname AS table_name, n_live_tup AS row_count
FROM pg_stat_user_tables ORDER BY relname;"
```

Expected row counts:

| Category | Tables | Rows |
|---|---|---|
| Lookup tables | organizations, subjects, keywords, resource_types, languages, formats | 10, 9, 121, 6, 3, 5 |
| Core | datasets | 32 |
| Junction (M2M) | dataset_subjects, dataset_keywords, dataset_resource_types, dataset_languages, dataset_formats | 47, 222, 46, 67, 61 |
| Resources | resources | 137 |
| Form structure | questions, form_submissions | 103, 114 |
| Section tables (12) | project_details through privacy_security | 30 each |
| **Source total** | **27 tables** | **1,178 rows** |

### Stage 6 — LLM Semantic Interpretations

Requires IONOS API credentials in `.env` (see `.env` for format).

```bash
# Create interpretation tables
psql -d aia_corpus -f etl/schema_interpretations.sql

# Run all LLM analyses (≈120 API calls, ~3-5 minutes)
python3 etl/llm_semantic_etl.py --analysis all
```

Expected interpretation row counts:

| Table | Rows |
|---|---|
| interp_automation_justification | 30 |
| interp_risk_rights_impact | 30 |
| interp_bilingual_divergence | 30 |
| interp_safeguard_compliance | 30 |
| interp_thematic_patterns | 22 |
| interp_run_log | (varies) |

---

## 12. Research Notes

### Item code scoring

AIA JSON answers use the pattern `itemR-S` where `S` is the score:
- `item2-0` → score 0 (typically "No" for binary questions)
- `item1-3` → score 3 (on a 0–4 scale)
- `item2-4` → score 4 (maximum; e.g. "Top Secret" data classification)

For multi-select fields (e.g. `businessDrivers1: ["item6","item5"]`), item codes identify which options were chosen from a fixed list; they do not carry individual scores.

### Bilingual coverage

JSON files carry both English (`data.*`) and French (`translationsOnResult.*`) for narrative fields. French coverage is approximately 50% across text fields — some departments provided only English narratives in the form, relying on external translation of the PDF.

### Form version differences

Most forms use `consultationImplementation*` / `dataQualityImplementation*` / `fairnessImplementation*` / `privacyImplementation*` keys (Implementation phase). One form (`aia-automation.json`) uses `*Design*` equivalents. The ETL handles both transparently with a fallback lookup.

### Known data quality issues

| Issue | Detail |
|---|---|
| `Size` field misalignment | File sizes in the original CSV are not aligned with URL counts per row; cannot be matched per-file reliably |
| 10 missing files | PSPC files require GoC CA bundle; see Stage 2 |
| Truncated URLs in AIA.csv | Original CSV truncates URLs at ~100 chars; full URLs recovered from the actual resource pages |
| Inconsistent FR translation | ~50% of narrative fields lack French content in the JSON source |

### Example research queries

```sql
-- Compare how different departments justify automation
SELECT pd.department, r.public_benefits_en
FROM reasons_for_automation r
JOIN form_submissions fs ON fs.id = r.submission_id
JOIN project_details pd  ON pd.submission_id = r.submission_id
WHERE r.public_benefits_en IS NOT NULL
ORDER BY pd.department;

-- Risk profile scores across all assessments
SELECT pd.project_title_en,
       rp.public_scrutiny_score, rp.high_stakes_score,
       rp.risk_total, fs.impact_level
FROM risk_profile rp
JOIN form_submissions fs ON fs.id = rp.submission_id
JOIN project_details pd  ON pd.submission_id = rp.submission_id
ORDER BY rp.risk_total DESC;

-- Fairness safeguard compliance gaps
SELECT pd.department, pd.project_title_en,
       f.human_override_enabled, f.client_recourse_process,
       f.can_produce_reasons, f.gc_earb_reviewed
FROM fairness f
JOIN form_submissions fs ON fs.id = f.submission_id
JOIN project_details pd  ON pd.submission_id = fs.id;

-- Bilingual divergence in individual impact descriptions
SELECT pd.project_title_en,
       ii.rights_freedoms_en,
       ii.rights_freedoms_fr
FROM individual_impacts ii
JOIN form_submissions fs ON fs.id = ii.submission_id
JOIN project_details pd  ON pd.submission_id = ii.submission_id
WHERE ii.rights_freedoms_en != ''
  AND ii.rights_freedoms_fr != '';
```

---

## Data Source & Licence

All source data is published by the Government of Canada under the [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada) and retrieved from [open.canada.ca](https://open.canada.ca).

Reference: Treasury Board of Canada Secretariat, *Directive on Automated Decision-Making*, 2019 (amended 2023).
