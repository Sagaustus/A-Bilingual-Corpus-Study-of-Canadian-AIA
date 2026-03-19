# Phase 2 — Evidence Appendix

> Reproducible SQL queries for Q-09 through Q-13, Q-17 through Q-24, Q-28 through Q-32.
> Database: `aia_corpus` (PostgreSQL, localhost:5432)
> Generated: 2026-03-08

---

## How to Use This Appendix

Run any query below against the `aia_corpus` database to verify the corresponding finding:

```bash
psql -d aia_corpus -c "<paste query here>"
```

---

## Block A — Bilingual Divergence (Q-09 through Q-13)

### Q-09: Overall divergence rate

```sql
SELECT has_divergence, COUNT(*) AS submissions,
       ROUND(COUNT(*)::numeric / 30 * 100, 1) AS pct
FROM interp_bilingual_divergence
GROUP BY has_divergence;
```

**Source table:** `interp_bilingual_divergence` (30 rows)

### Q-10: Which semantic fields diverge most

```sql
SELECT field->>'field' AS field_name,
       field->>'type' AS divergence_type,
       field->>'severity' AS severity,
       COUNT(*) AS occurrences
FROM interp_bilingual_divergence,
     jsonb_array_elements(divergent_fields) AS field
GROUP BY field_name, divergence_type, severity
ORDER BY occurrences DESC;
```

**Source table:** `interp_bilingual_divergence.divergent_fields` (JSONB array)

### Q-11: Distribution of divergence types

```sql
SELECT overall_divergence_type, COUNT(*) AS submissions,
       ROUND(AVG(semantic_fidelity_score)::numeric, 2) AS avg_fidelity
FROM interp_bilingual_divergence
GROUP BY overall_divergence_type
ORDER BY submissions DESC;
```

### Q-12: Omission vs terminological drift

```sql
SELECT field->>'type' AS divergence_type,
       COUNT(*) AS total_occurrences,
       COUNT(DISTINCT bd.submission_id) AS submissions_affected
FROM interp_bilingual_divergence bd,
     jsonb_array_elements(divergent_fields) AS field
GROUP BY divergence_type
ORDER BY total_occurrences DESC;
```

### Q-13: Fidelity score and narrative text correlation

```sql
SELECT bd.submission_id, bd.semantic_fidelity_score, bd.divergence_count,
       bd.overall_divergence_type,
       (CASE WHEN pd.description_fr IS NOT NULL AND pd.description_fr != ''
             THEN 1 ELSE 0 END) AS has_fr_description,
       (CASE WHEN ra.client_needs_fr IS NOT NULL AND ra.client_needs_fr != ''
             THEN 1 ELSE 0 END) AS has_fr_client_needs,
       (CASE WHEN ii.rights_freedoms_fr IS NOT NULL AND ii.rights_freedoms_fr != ''
             THEN 1 ELSE 0 END) AS has_fr_rights
FROM interp_bilingual_divergence bd
JOIN project_details pd USING (submission_id)
JOIN reasons_for_automation ra USING (submission_id)
JOIN individual_impacts ii USING (submission_id)
ORDER BY bd.semantic_fidelity_score;
```

**Source tables:** `interp_bilingual_divergence`, `project_details`, `reasons_for_automation`, `individual_impacts`

---

## Block B — Automation Justification (Q-17 through Q-20)

### Q-17: Dominant justification themes

```sql
SELECT justification_theme, COUNT(*) AS n,
       ROUND(AVG(strength_score)::numeric, 1) AS avg_strength,
       MIN(strength_score) AS min_strength,
       MAX(strength_score) AS max_strength
FROM interp_automation_justification
GROUP BY justification_theme
ORDER BY n DESC;
```

**Source table:** `interp_automation_justification` (30 rows)

### Q-18: Justification strength vs trade-off acknowledgment

```sql
SELECT pd.department, pd.project_title_en,
       aj.justification_theme, aj.strength_score,
       aj.trade_off_adequacy, aj.public_benefit_clarity
FROM interp_automation_justification aj
JOIN project_details pd USING (submission_id)
ORDER BY aj.strength_score DESC;
```

**Source tables:** `interp_automation_justification`, `project_details`

### Q-19: Automation type and justification rhetoric

```sql
SELECT CASE ad.automation_type_score
           WHEN 0 THEN 'Decision support'
           WHEN 2 THEN 'Partial automation'
           WHEN 4 THEN 'Full automation'
           ELSE 'Unknown/NULL'
       END AS automation_level,
       aj.justification_theme, COUNT(*) AS n,
       ROUND(AVG(aj.strength_score)::numeric, 1) AS avg_strength
FROM interp_automation_justification aj
JOIN about_the_decision ad USING (submission_id)
GROUP BY automation_level, aj.justification_theme
ORDER BY automation_level, n DESC;
```

**Source tables:** `interp_automation_justification`, `about_the_decision`

### Q-20: Confinement claims vs system capabilities

```sql
SELECT pd.project_title_en, pd.department, pd.system_capabilities,
       aj.confinement_assessment, ad.automation_type_score,
       ad.used_by_different_org_score
FROM interp_automation_justification aj
JOIN project_details pd USING (submission_id)
JOIN about_the_decision ad USING (submission_id)
ORDER BY ad.automation_type_score DESC;
```

**Source tables:** `interp_automation_justification`, `project_details`, `about_the_decision`

---

## Block C — Risk, Rights, and Proportionality (Q-21 through Q-24)

### Q-21: Risk landscape

```sql
SELECT rri.risk_level_label, COUNT(*) AS n,
       ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk_total,
       ROUND(AVG(fs.impact_level)::numeric, 1) AS avg_impact_level
FROM interp_risk_rights_impact rri
JOIN risk_profile rp USING (submission_id)
JOIN form_submissions fs ON fs.id = rri.submission_id
GROUP BY rri.risk_level_label
ORDER BY n DESC;
```

**Full detail query:**

```sql
SELECT rri.submission_id, pd.project_title_en, pd.department,
       rri.risk_level_label, rri.dominant_risk_dimension,
       rri.rights_concern_summary, rri.proportionality_assessment,
       rri.reversibility_concern, rp.risk_total
FROM interp_risk_rights_impact rri
JOIN project_details pd USING (submission_id)
JOIN risk_profile rp USING (submission_id)
ORDER BY rp.risk_total DESC;
```

### Q-22: Which rights dimensions are most at stake

```sql
SELECT 'Rights & Freedoms' AS dimension,
       ROUND(AVG(rights_freedoms_score)::numeric, 2) AS avg_score,
       COUNT(*) FILTER (WHERE rights_freedoms_score > 0) AS affected_count
FROM individual_impacts
UNION ALL
SELECT 'Equality & Dignity',
       ROUND(AVG(equality_dignity_score)::numeric, 2),
       COUNT(*) FILTER (WHERE equality_dignity_score > 0)
FROM individual_impacts
UNION ALL
SELECT 'Health & Wellbeing',
       ROUND(AVG(health_wellbeing_score)::numeric, 2),
       COUNT(*) FILTER (WHERE health_wellbeing_score > 0)
FROM individual_impacts
UNION ALL
SELECT 'Economic Interests',
       ROUND(AVG(economic_interests_score)::numeric, 2),
       COUNT(*) FILTER (WHERE economic_interests_score > 0)
FROM individual_impacts;
```

**Source table:** `individual_impacts` (30 rows)

### Q-23: Proportionality — automation level vs risk

```sql
SELECT pd.project_title_en, pd.department,
       rri.risk_level_label, rri.proportionality_assessment,
       ad.automation_type_score, rp.risk_total, fs.impact_level
FROM interp_risk_rights_impact rri
JOIN project_details pd USING (submission_id)
JOIN about_the_decision ad USING (submission_id)
JOIN risk_profile rp USING (submission_id)
JOIN form_submissions fs ON fs.id = rri.submission_id
ORDER BY rp.risk_total DESC;
```

### Q-24: Reversibility and duration

```sql
SELECT CASE ad.impacts_reversible_score
           WHEN 0 THEN 'Irreversible'
           WHEN 2 THEN 'Partially reversible'
           WHEN 4 THEN 'Easily reversible'
           ELSE 'Other (' || ad.impacts_reversible_score || ')'
       END AS reversibility,
       CASE ad.impact_duration_score
           WHEN 0 THEN 'Long-term'
           WHEN 2 THEN 'Medium-term'
           WHEN 4 THEN 'Brief'
           ELSE 'Other (' || COALESCE(ad.impact_duration_score::text, 'NULL') || ')'
       END AS duration,
       COUNT(*) AS n,
       ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk
FROM about_the_decision ad
JOIN risk_profile rp USING (submission_id)
GROUP BY reversibility, duration
ORDER BY avg_risk DESC;
```

**Source tables:** `about_the_decision`, `risk_profile`

---

## Block D — Safeguard Compliance (Q-28 through Q-32)

### Q-28: Compliance distribution

```sql
SELECT overall_compliance_label, overall_compliance_score,
       COUNT(*) AS n
FROM interp_safeguard_compliance
GROUP BY overall_compliance_label, overall_compliance_score
ORDER BY overall_compliance_score DESC;
```

**Source table:** `interp_safeguard_compliance` (30 rows)

### Q-29: Most common safeguard gaps

```sql
SELECT gap::text AS gap_description, COUNT(*) AS frequency
FROM interp_safeguard_compliance,
     jsonb_array_elements(gaps_identified) AS gap
GROUP BY gap_description
ORDER BY frequency DESC
LIMIT 20;
```

**Source column:** `interp_safeguard_compliance.gaps_identified` (JSONB array)

### Q-30: Human override trifecta

```sql
SELECT f.human_override_enabled, f.client_recourse_process,
       f.can_produce_reasons, COUNT(*) AS n,
       ROUND(AVG(sc.overall_compliance_score)::numeric, 1) AS avg_compliance
FROM fairness f
JOIN interp_safeguard_compliance sc USING (submission_id)
GROUP BY f.human_override_enabled, f.client_recourse_process,
         f.can_produce_reasons
ORDER BY n DESC;
```

**Source tables:** `fairness`, `interp_safeguard_compliance`

### Q-31: GBA+ and bias testing

```sql
SELECT pd.department, dqb.gba_plus_conducted,
       dqb.bias_testing_documented, dqb.bias_testing_public,
       sc.bias_mitigation_assessment
FROM data_quality_bias dqb
JOIN project_details pd USING (submission_id)
JOIN interp_safeguard_compliance sc USING (submission_id)
ORDER BY pd.department;
```

**Source tables:** `data_quality_bias`, `project_details`, `interp_safeguard_compliance`

### Q-32: Privacy in the age of automation

```sql
SELECT pd.project_title_en, pd.department,
       ps.pia_conducted, ps.privacy_by_design,
       ps.de_identification_applied, atd.uses_personal_info,
       sc.privacy_assessment
FROM privacy_security ps
JOIN about_the_data atd USING (submission_id)
JOIN interp_safeguard_compliance sc USING (submission_id)
JOIN project_details pd USING (submission_id)
ORDER BY atd.uses_personal_info DESC;
```

**Source tables:** `privacy_security`, `about_the_data`, `interp_safeguard_compliance`, `project_details`

---

## Dashboard Suggestions

| Question(s) | Visualization | Data Source |
|-------------|--------------|-------------|
| Q-09 | Donut chart: divergent vs. non-divergent | `interp_bilingual_divergence` |
| Q-10 | Heatmap: field × severity, color = occurrence count | `divergent_fields` JSONB |
| Q-12 | Stacked bar: divergence types across fields | `divergent_fields` JSONB |
| Q-13 | Scatter: fidelity score vs. count of FR fields present | Multiple JOINs |
| Q-17 | Grouped bar: justification themes with strength overlay | `interp_automation_justification` |
| Q-21 | Histogram: risk_total distribution with risk labels | `risk_profile` + `interp_risk_rights_impact` |
| Q-22 | Lollipop chart: four rights dimensions | `individual_impacts` |
| Q-28 | Donut chart: compliance distribution | `interp_safeguard_compliance` |
| Q-29 | Horizontal bar: gap frequency | `gaps_identified` JSONB |
| Q-31 | Pipeline funnel: GBA+ conducted → tested → published | `data_quality_bias` |
| Q-32 | Stacked bar: privacy measures by submission | `privacy_security` + `about_the_data` |
