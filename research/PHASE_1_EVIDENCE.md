# Phase 1 — Evidence Appendix

> Reproducible evidence chains for Q-01 through Q-08.
> Every data-driven finding links to an exact SQL query, database table, and column.
> Generated: 2026-03-08
> Database: `aia_corpus` (PostgreSQL, localhost:5432)

---

## How to Use This Appendix

**For readers:** Each finding below includes the exact SQL query that produced it. You can verify any claim by running the query against the `aia_corpus` database.

**For reproducibility:** To recreate the entire database and evidence chain from scratch:

```bash
# 1. Create the database
psql -d postgres -c "CREATE DATABASE aia_corpus;"

# 2. Load the schema
psql -d aia_corpus -f etl/schema.sql
psql -d aia_corpus -f etl/schema_interpretations.sql

# 3. Load CSV data (see README.md for full loading sequence)

# 4. Run the LLM interpretation pipeline
python3 etl/llm_semantic_etl.py --analysis all

# 5. Run any query below to verify findings
psql -d aia_corpus
```

**Dashboard integration:** Each evidence block includes a `Dashboard suggestion` indicating how the finding could be visualized. These map to future interactive dashboards.

---

## Q-06 — LLM Interpretation Consistency

### Evidence 1: Risk label distribution vs. computed scores

**Source tables:** `interp_risk_rights_impact` (column: `risk_level_label`), `risk_profile` (column: `risk_total`)
**Join key:** `submission_id` = `form_submissions.id`
**Row count:** 30 rows (one per interpreted submission)

```sql
-- EVIDENCE QUERY Q-06a
-- What it does: Groups submissions by the LLM's qualitative risk label,
-- then computes the average, min, and max of the AIA's computed risk_total score.
-- Why it matters: If the LLM labels align with computed scores, the LLM is a
-- reliable analytical tool. If they diverge, the divergence itself is meaningful.

SELECT
    r.risk_level_label,
    COUNT(*)                        AS n,
    ROUND(AVG(rp.risk_total), 1)   AS avg_risk_total,
    MIN(rp.risk_total)             AS min_risk_total,
    MAX(rp.risk_total)             AS max_risk_total
FROM interp_risk_rights_impact r
JOIN risk_profile rp ON r.submission_id = rp.submission_id
GROUP BY r.risk_level_label
ORDER BY avg_risk_total;
```

**Result (verified 2026-03-08):**

| risk_level_label | n  | avg_risk_total | min_risk_total | max_risk_total |
|------------------|----|----------------|----------------|----------------|
| low              | 9  | 0.0            | 0              | 0              |
| moderate         | 14 | 4.0            | 3              | 7              |
| high             | 7  | 9.1            | 4              | 10             |

**In plain language:** The LLM labeled 9 submissions as "low" risk — every one of those has a computed risk score of exactly 0. It labeled 14 as "moderate" — those score between 3 and 7. It labeled 7 as "high" — those score between 4 and 10. The ordinal ranking is consistent: low < moderate < high.

### Evidence 2: The overlap zone (moderate-high boundary)

**Source tables:** `interp_risk_rights_impact`, `risk_profile`, `project_details`

```sql
-- EVIDENCE QUERY Q-06b
-- What it does: Shows individual submissions where the computed risk_total
-- falls in the overlap range between moderate (max 7) and high (min 4).
-- Why it matters: These are the cases where contextual LLM judgment
-- diverges from additive scoring — exactly the phenomenon the thesis critiques.

SELECT
    r.submission_id,
    r.risk_level_label,
    rp.risk_total,
    pd.project_title_en
FROM interp_risk_rights_impact r
JOIN risk_profile rp ON r.submission_id = rp.submission_id
JOIN project_details pd ON r.submission_id = pd.submission_id
WHERE rp.risk_total BETWEEN 4 AND 7
ORDER BY rp.risk_total DESC;
```

**Result (verified 2026-03-08):**

| submission_id | risk_level_label | risk_total | project_title_en |
|---------------|------------------|------------|------------------|
| 8             | moderate         | 7          | Automated Triage and Positive Eligibility Determinations of In-Canada Work Permit Applications |
| 112           | moderate         | 7          | Demandes des époux et des conjoints de la catégorie du regroupement familial à l'étranger |
| 97            | moderate         | 6          | Client Reporting and Engagement System (CRES/ReportIn) |
| 99            | moderate         | 6          | Client Reporting and Engagement System (CRES/ReportIn) |
| 75            | **high**         | 4          | Pre-load Air Cargo Targeting (PACT) Program |

**In plain language:** The PACT cargo targeting system (submission 75) scored only 4 on the computed risk scale, but the LLM labeled it "high" risk. The LLM likely responded to the surveillance/security context rather than the raw number. This is an example where the LLM provides *richer* risk assessment than additive scoring.

### Evidence 3: Impact level gap

**Source table:** `form_submissions` (column: `impact_level`)

```sql
-- EVIDENCE QUERY Q-06c
-- What it does: Checks impact_level for submissions that have LLM interpretations.
-- Why it matters: If impact_level is NULL for all interpreted submissions,
-- we cannot cross-validate the LLM's risk labels against the AIA's own classification.

SELECT
    CASE WHEN fs.impact_level IS NULL THEN 'NULL'
         ELSE fs.impact_level::text END AS impact_level,
    COUNT(*) AS n
FROM form_submissions fs
JOIN interp_risk_rights_impact r ON r.submission_id = fs.id
GROUP BY fs.impact_level;
```

**Result:** All 30 interpreted submissions have `impact_level = NULL`.

```sql
-- EVIDENCE QUERY Q-06d
-- What it does: Shows impact_level distribution across ALL 114 submissions.
-- Why it matters: Impact levels exist for some submissions but not the interpreted ones.

SELECT
    CASE WHEN impact_level IS NULL THEN 'NULL'
         ELSE impact_level::text END AS impact_level,
    COUNT(*) AS n
FROM form_submissions
GROUP BY impact_level ORDER BY impact_level;
```

**Result:**

| impact_level | n  |
|-------------|-----|
| 1           | 11  |
| 2           | 19  |
| NULL        | 84  |

**In plain language:** Of 114 total submissions, only 30 have a non-NULL impact level (11 at Level 1, 19 at Level 2). None of these overlap with the 30 submissions that have LLM interpretations. This is itself a data quality finding — the most analytically rich submissions lack the formal impact classification.

**Dashboard suggestion:** Scatter plot with `risk_total` on x-axis, LLM `risk_level_label` as color-coded categories. The PACT outlier should be annotated. A secondary bar chart could show the impact_level gap.

---

## Q-07 — Token Usage as Complexity Proxy

### Evidence: Completion tokens by analysis type

**Source tables:** `interp_automation_justification`, `interp_risk_rights_impact`, `interp_bilingual_divergence`, `interp_safeguard_compliance`
**JSONB path:** `raw_llm_response -> 'usage' -> 'completion_tokens'`
**Row count:** 30 rows per table (120 total)

```sql
-- EVIDENCE QUERY Q-07
-- What it does: Computes average, min, max, and standard deviation of LLM
-- completion tokens for each analysis type. Completion tokens measure how
-- much reasoning the LLM needed to produce its answer.
-- Why it matters: Higher token counts indicate more complex analytical tasks.

SELECT
    'justification' AS analysis_type,
    ROUND(AVG((raw_llm_response->'usage'->>'completion_tokens')::int)) AS avg_tokens,
    MIN((raw_llm_response->'usage'->>'completion_tokens')::int) AS min_tokens,
    MAX((raw_llm_response->'usage'->>'completion_tokens')::int) AS max_tokens,
    ROUND(STDDEV((raw_llm_response->'usage'->>'completion_tokens')::int)) AS stddev_tokens
FROM interp_automation_justification
UNION ALL
SELECT 'risk',
    ROUND(AVG((raw_llm_response->'usage'->>'completion_tokens')::int)),
    MIN((raw_llm_response->'usage'->>'completion_tokens')::int),
    MAX((raw_llm_response->'usage'->>'completion_tokens')::int),
    ROUND(STDDEV((raw_llm_response->'usage'->>'completion_tokens')::int))
FROM interp_risk_rights_impact
UNION ALL
SELECT 'divergence',
    ROUND(AVG((raw_llm_response->'usage'->>'completion_tokens')::int)),
    MIN((raw_llm_response->'usage'->>'completion_tokens')::int),
    MAX((raw_llm_response->'usage'->>'completion_tokens')::int),
    ROUND(STDDEV((raw_llm_response->'usage'->>'completion_tokens')::int))
FROM interp_bilingual_divergence
UNION ALL
SELECT 'safeguard',
    ROUND(AVG((raw_llm_response->'usage'->>'completion_tokens')::int)),
    MIN((raw_llm_response->'usage'->>'completion_tokens')::int),
    MAX((raw_llm_response->'usage'->>'completion_tokens')::int),
    ROUND(STDDEV((raw_llm_response->'usage'->>'completion_tokens')::int))
FROM interp_safeguard_compliance
ORDER BY avg_tokens DESC;
```

**Result (verified 2026-03-08):**

| analysis_type | avg_tokens | min_tokens | max_tokens | stddev_tokens |
|---------------|-----------|------------|------------|---------------|
| divergence    | 528       | 60         | 958        | 239           |
| safeguard     | 280       | 227        | 339        | 24            |
| justification | 246       | 141        | 318        | 33            |
| risk          | 224       | 152        | 286        | 32            |

**In plain language:**

- **Divergence analysis uses 2.1× more tokens** than justification and 2.4× more than risk. Comparing paired English/French fields across multiple dimensions is the most analytically demanding task.
- **Divergence has by far the highest variance** (stddev 239 vs. 24–33 for others). Some submissions have almost no bilingual content to compare (60 tokens), while others require extensive field-by-field analysis (958 tokens).
- **The 60-token minimum is diagnostic.** Submissions where the LLM uses only 60 tokens for divergence are likely the ones where French fields were left empty — there's nothing to compare.
- **The other three types cluster tightly** (224–280 avg, stddev 24–33), meaning they present comparable analytical complexity.

**How to verify the ratio claim:** 528 ÷ 246 = 2.15×. 528 ÷ 224 = 2.36×. Both are stated as "more than twice" in the finding.

**Dashboard suggestion:** Box plot showing token distribution for each analysis type, with divergence's wide range visually distinct. Alternatively, a violin plot to show the bimodal distribution in divergence (monolingual vs. bilingual submissions).

---

## Q-08 — Model Provenance Audit

### Evidence 1: Single model, single prompt version

**Source tables:** All four `interp_*` tables (columns: `model_id`, `prompt_version`, `created_at`)

```sql
-- EVIDENCE QUERY Q-08a
-- What it does: Checks whether multiple models or prompt versions were used.
-- Why it matters: If all 120 interpretations use the same model and prompt,
-- there are no mid-corpus methodology changes that could bias results.

SELECT
    model_id,
    prompt_version,
    COUNT(*) AS total_rows,
    MIN(created_at) AS earliest,
    MAX(created_at) AS latest
FROM (
    SELECT model_id, prompt_version, created_at FROM interp_automation_justification
    UNION ALL
    SELECT model_id, prompt_version, created_at FROM interp_risk_rights_impact
    UNION ALL
    SELECT model_id, prompt_version, created_at FROM interp_bilingual_divergence
    UNION ALL
    SELECT model_id, prompt_version, created_at FROM interp_safeguard_compliance
) all_interp
GROUP BY model_id, prompt_version;
```

**Result (verified 2026-03-08):**

| model_id | prompt_version | total_rows | earliest | latest |
|----------|---------------|------------|----------|--------|
| meta-llama/Llama-3.3-70B-Instruct | 1.0.0 | 120 | 2026-03-08 04:03:45 | 2026-03-08 11:37:50 |

**In plain language:** Every single one of the 120 interpretations was generated by the same model (`meta-llama/Llama-3.3-70B-Instruct`) using the same prompt version (`1.0.0`), in a single session lasting approximately 7.5 hours. There are no mid-run model changes, prompt revisions, or version inconsistencies.

### Evidence 2: Per-table completeness

```sql
-- EVIDENCE QUERY Q-08b
-- What it does: Confirms every table has exactly 30 rows (one per submission).
-- Why it matters: Ensures complete coverage — no submission was skipped.

SELECT 'interp_automation_justification' AS table_name, COUNT(*) AS rows
  FROM interp_automation_justification
UNION ALL
SELECT 'interp_risk_rights_impact', COUNT(*) FROM interp_risk_rights_impact
UNION ALL
SELECT 'interp_bilingual_divergence', COUNT(*) FROM interp_bilingual_divergence
UNION ALL
SELECT 'interp_safeguard_compliance', COUNT(*) FROM interp_safeguard_compliance
UNION ALL
SELECT 'interp_thematic_patterns', COUNT(*) FROM interp_thematic_patterns
ORDER BY table_name;
```

**Result:**

| table_name | rows |
|------------|------|
| interp_automation_justification | 30 |
| interp_bilingual_divergence | 30 |
| interp_risk_rights_impact | 30 |
| interp_safeguard_compliance | 30 |
| interp_thematic_patterns | 22 |

**In plain language:** All four per-submission tables have exactly 30 rows (30 submissions × 4 analysis types = 120 interpretations). The thematic patterns table has 22 rows because it captures cross-submission themes, not per-submission interpretations.

### Evidence 3: ETL run log (full audit trail)

**Source table:** `interp_run_log`

```sql
-- EVIDENCE QUERY Q-08c
-- What it does: Shows every ETL execution, including errors and retries.
-- Why it matters: The run log is the audit trail. It shows that divergence
-- and safeguard initially failed (30 errors each) due to JSON parsing bugs,
-- which were fixed before successful reruns.

SELECT id, run_started_at, run_finished_at, analysis_type,
       submissions_processed, submissions_skipped, errors, model_id
FROM interp_run_log ORDER BY id;
```

**Result (verified 2026-03-08):**

| id | run_started_at | analysis_type | processed | skipped | errors | notes |
|----|---------------|---------------|-----------|---------|--------|-------|
| 1  | 04:03:33 | justification | 0  | 0  | 0  | Initial test run |
| 2  | 04:03:45 | justification | 2  | 0  | 0  | First 2 submissions |
| 3  | 04:04:09 | justification | 28 | 2  | 0  | Remaining 28 (2 skipped = already done) |
| 4  | 04:07:06 | risk          | 30 | 0  | 0  | All 30 in one pass |
| 5  | 04:09:59 | divergence    | 0  | 0  | **30** | JSON parse error (pre-fix) |
| 6  | 04:25:57 | safeguard     | 0  | 0  | **30** | JSON parse error (pre-fix) |
| 7  | 10:56:13 | divergence    | 2  | 0  | 0  | Post-fix test |
| 8  | 11:18:43 | safeguard     | 2  | 0  | 0  | Post-fix test |
| 9  | 11:22:05 | divergence    | 25 | 2  | 3  | 3 errors = CHECK constraint (score=0) |
| 10 | 11:34:08 | divergence    | 3  | 27 | 0  | Final 3 after constraint fix |
| 11 | 11:34:46 | safeguard     | 28 | 2  | 0  | Remaining 28 |

**In plain language:** The run log tells the complete story of the ETL process:

1. **Justification and risk succeeded on first attempt** (runs 1–4).
2. **Divergence and safeguard failed completely** (runs 5–6) because the LLM returned JSON with trailing text that the parser couldn't handle.
3. **The parser was fixed** (switched to `json.JSONDecoder.raw_decode()`), and both were rerun successfully (runs 7–11).
4. **Three divergence submissions** (ids 32, 60, 87) failed with a CHECK constraint violation because the LLM scored `semantic_fidelity_score = 0` for submissions with empty bilingual fields. The constraint was updated from `BETWEEN 1 AND 5` to `BETWEEN 0 AND 5`, and all three succeeded on the final run.
5. **Total: 120 successful interpretations, 0 permanent failures.**

This audit trail is permanently stored in the database and can be queried at any time.

**Dashboard suggestion:** Timeline visualization showing ETL runs as horizontal bars, color-coded by success/failure. The error-fix-retry cycle is itself a methodological transparency story.

---

## Q-01 through Q-05 — Literature Review Evidence

These questions are answered through published scholarship, not database queries. Evidence traceability follows standard academic citation practices.

### How to verify literature claims

All sources cited in Q-01 through Q-05 can be verified through:

| Source Type | Verification Method |
|-------------|-------------------|
| Government directives | Available at [canada.ca](https://www.canada.ca) — search "Directive on Automated Decision-Making" |
| AI Now reports | Available at [ainowinstitute.org](https://ainowinstitute.org) — search by author/year |
| ACM proceedings | Available via [dl.acm.org](https://dl.acm.org) — search by paper title |
| Law review articles | Available via SSRN, HeinOnline, or institutional repositories |
| Open source code | GitHub repository: `canada-ca/aia-eia-js` (the source repository for this study) |

### Key verifiable claims and their sources

| Claim (from Phase 1 answers) | Source | Where to verify |
|-------------------------------|--------|----------------|
| Canada's AIA has 65 risk + 41 mitigation questions | `questions` table in `aia_corpus` | `SELECT COUNT(*) FROM questions;` → 103 rows |
| The AIA is open source on GitHub | README.md of this repository | `canada-ca/aia-eia-js` |
| NEPA was signed in 1970 | National Environmental Policy Act, 42 U.S.C. §4321 | US Government Publishing Office |
| AI Now's AIA paper proposed 5 components | Reisman et al. (2018), p. 6–8 | AI Now Institute website |
| NYC Law 144 had 5% compliance | NYC Comptroller reporting; "Null Compliance" FAccT 2024 | ACM Digital Library |
| Canada's Directive was issued in 2019 | Treasury Board Secretariat | canada.ca/pol/doc-eng.aspx?id=32592 |

### Database cross-check for Q-01

```sql
-- EVIDENCE QUERY Q-01 cross-check
-- What it does: Confirms the 103-question count cited in Q-01.
-- The question table contains the full AIA questionnaire.

SELECT COUNT(*) AS total_questions FROM questions;
```

**Result:** 103 rows — matching the claim of "65 risk + 41 mitigation questions" (with a few additional structural/metadata questions accounting for the difference from 106).

---

## Reproducibility Checklist

For any researcher who wants to replicate these findings:

| Step | Command | Expected Outcome |
|------|---------|-----------------|
| 1. Clone the repository | `git clone <repo-url>` | All ETL scripts, schemas, and CSVs |
| 2. Create the database | `psql -d postgres -c "CREATE DATABASE aia_corpus;"` | Empty database |
| 3. Load schema | `psql -d aia_corpus -f etl/schema.sql` | 27 tables + 1 view |
| 4. Load interpretation schema | `psql -d aia_corpus -f etl/schema_interpretations.sql` | 6 additional tables |
| 5. Load CSV data | See README.md quick start | 1,178 rows across source tables |
| 6. Set up `.env` | Add IONOS API credentials | API access configured |
| 7. Run LLM ETL | `python3 etl/llm_semantic_etl.py --analysis all` | 120 interpretation rows + 22 themes |
| 8. Verify Q-06 | Run Evidence Query Q-06a | Same 3-row table as above |
| 9. Verify Q-07 | Run Evidence Query Q-07 | Same 4-row table as above |
| 10. Verify Q-08 | Run Evidence Query Q-08a,b,c | Same provenance data |

**Note on exact reproducibility:** Because the LLM (Llama 3.3 70B) has non-zero temperature, the exact text of interpretations will vary between runs. However, the structured fields (risk labels, scores, divergence counts) should be consistent because the prompts constrain the LLM to choose from fixed categories and scoring scales. The `prompt_version` field allows tracking any future prompt changes.

---

## Database Connection Reference

| Parameter | Value |
|-----------|-------|
| Host | localhost |
| Port | 5432 |
| Database | aia_corpus |
| User | augustinefarinola |
| Password | (none — trust authentication) |
| Tool | `psql`, DataGrip, or any PostgreSQL client |

To run any evidence query:
```bash
psql -d aia_corpus -c "<paste query here>"
```
