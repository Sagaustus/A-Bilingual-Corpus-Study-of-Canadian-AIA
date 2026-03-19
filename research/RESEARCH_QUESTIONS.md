# Research Questions — AIA Bilingual Corpus Study

> Structured queries for a Digital Humanities PhD thesis on bilingual algorithmic governance in Canada.
>
> Database: `aia_corpus` (33 tables, PostgreSQL)
> Thesis frame: "The Untranslatable State" — how Canada's official bilingualism produces not one but two distinct algorithmic governance regimes.

---

## Evidence Method Legend

Each research question is tagged with the method(s) required to answer it:

| Tag | Method | Description |
|-----|--------|-------------|
| `DB` | Database Facts | Direct SQL queries returning factual corpus data |
| `AGG` | Aggregation & Statistics | SQL aggregations, distributions, correlations, standard deviations |
| `LLM` | LLM-Driven Semantic Interpretation | Analysis drawn from the `interp_*` tables (Llama 3.3 70B outputs) |
| `NLP` | Computational Text Analysis | Python-based tokenization, TF-IDF, sentiment, discourse parsing |
| `LIT` | Literature & Theory | Published scholarship, philosophical argument, comparative law |
| `CR` | Close Reading | Qualitative human interpretation of individual AIA submissions |

**Status key:** `[ ]` = not started | `[~]` = in progress | `[x]` = complete

---

## Master Question Index

### Part I — Foundations (Chapters 1–2)

| # | Question | Chapter | Methods | Status |
|---|----------|---------|---------|--------|
| **Q-01** | What is the history of AIAs as governance tools? | Ch 1 | `LIT` | `[~]` |
| **Q-02** | What ethical frameworks justify AIAs? | Ch 2 | `LIT` | `[~]` |
| **Q-03** | What are the scholarly critiques of AIAs? | Ch 2 | `LIT` | `[~]` |
| **Q-04** | What are the alternatives to AIAs? | Ch 2 | `LIT` | `[~]` |
| **Q-05** | How does the EIA analogy shape — and limit — AIA design? | Ch 2 | `LIT` | `[~]` |
| **Q-06** | LLM interpretation consistency: does the LLM agree with computed impact levels? | Ch 1 | `AGG` `LLM` | `[x]` |
| **Q-07** | Token usage as complexity proxy across analysis types | Ch 1 | `AGG` | `[x]` |
| **Q-08** | Model provenance audit: full reproducibility trail | Ch 1 | `DB` | `[x]` |

### Part II — The Bilingual Governance Regime (Chapters 3–4)

| # | Question | Chapter | Methods | Status |
|---|----------|---------|---------|--------|
| **Q-09** | What is the overall divergence rate across the corpus? | Ch 3 | `AGG` `LLM` | `[x]` |
| **Q-10** | Which semantic fields diverge most? | Ch 3 | `AGG` `LLM` | `[x]` |
| **Q-11** | What is the distribution of divergence types? | Ch 3 | `AGG` `LLM` | `[x]` |
| **Q-12** | Is the dominant divergence omission or terminological drift? | Ch 3 | `AGG` `LLM` `CR` | `[x]` |
| **Q-13** | Is there a correlation between fidelity score and narrative text presence? | Ch 3 | `AGG` `DB` | `[x]` |
| **Q-14** | Where does "accountability" appear in English structured data? | Ch 4 | `DB` | `[ ]` |
| **Q-15** | How does French distribute the concept of "accountability"? | Ch 4 | `DB` `CR` | `[ ]` |
| **Q-16** | Do divergent fields cluster around accountability-adjacent concepts? | Ch 4 | `LLM` `CR` | `[ ]` |

### Part III — Automation Rhetoric & Justification (Chapter 5)

| # | Question | Chapter | Methods | Status |
|---|----------|---------|---------|--------|
| **Q-17** | What justification themes dominate the corpus? | Ch 5 | `AGG` `LLM` | `[x]` |
| **Q-18** | Do stronger justifications correlate with trade-off acknowledgment? | Ch 5 | `AGG` `LLM` `CR` | `[x]` |
| **Q-19** | How does automation type relate to justification rhetoric? | Ch 5 | `AGG` `DB` `LLM` | `[x]` |
| **Q-20** | What is the relationship between confinement claims and system capabilities? | Ch 5 | `DB` `LLM` `CR` | `[x]` |

### Part IV — Risk, Rights, and the Quantification Problem (Chapter 6)

| # | Question | Chapter | Methods | Status |
|---|----------|---------|---------|--------|
| **Q-21** | What is the risk landscape across the corpus? | Ch 6 | `AGG` `LLM` | `[x]` |
| **Q-22** | Which rights dimensions are most at stake? | Ch 6 | `AGG` `DB` | `[x]` |
| **Q-23** | Is automation proportional to risk? | Ch 6 | `AGG` `DB` `LLM` `CR` | `[x]` |
| **Q-24** | How do reversibility and duration interact with rights impact? | Ch 6 | `AGG` `DB` | `[x]` |
| **Q-25** | Why do different impact categories receive different score distributions? | Ch 6 | `AGG` `LIT` | `[ ]` |
| **Q-26** | Does the scoring algorithm conflate unlike things? | Ch 6 | `AGG` `DB` `CR` | `[ ]` |
| **Q-27** | The commensurability problem: can human rights be scored 0–4? | Ch 6 | `DB` `LLM` `CR` `LIT` | `[ ]` |

### Part V — Safeguard Compliance (Chapter 7)

| # | Question | Chapter | Methods | Status |
|---|----------|---------|---------|--------|
| **Q-28** | What is the compliance distribution? | Ch 7 | `AGG` `LLM` | `[x]` |
| **Q-29** | What are the most common safeguard gaps? | Ch 7 | `AGG` `LLM` | `[x]` |
| **Q-30** | The human override question: explain, override, challenge | Ch 7 | `AGG` `DB` `LLM` | `[x]` |
| **Q-31** | GBA+ and bias testing as governance signifiers | Ch 7 | `DB` `LLM` `CR` | `[x]` |
| **Q-32** | Privacy in the age of automation | Ch 7 | `DB` `LLM` | `[x]` |

### Part VI — Departmental Cultures & Inconsistency (Chapter 8)

| # | Question | Chapter | Methods | Status |
|---|----------|---------|---------|--------|
| **Q-33** | Department-level governance profile (multi-metric) | Ch 8 | `AGG` `LLM` | `[ ]` |
| **Q-34** | Department and bilingual commitment | Ch 8 | `AGG` `LLM` | `[ ]` |
| **Q-35** | Department justification patterns | Ch 8 | `AGG` `LLM` | `[ ]` |
| **Q-36** | How much do departments vary in scoring patterns? | Ch 8 | `AGG` | `[ ]` |
| **Q-37** | Do similar systems receive similar scores? | Ch 8 | `AGG` `DB` | `[ ]` |
| **Q-38** | Temporal drift: do assessments change over time? | Ch 8 | `AGG` `DB` | `[ ]` |
| **Q-39** | Field completion rates: which questions go unanswered? | Ch 8 | `AGG` `DB` | `[ ]` |

### Part VII — Language of Algorithmic Governance (Chapter 9)

| # | Question | Chapter | Methods | Status |
|---|----------|---------|---------|--------|
| **Q-40** | Lexical analysis: what vocabulary dominates AIA discourse? | Ch 9 | `NLP` `DB` | `[ ]` |
| **Q-41** | Hedging and epistemic modality in departmental language | Ch 9 | `NLP` `DB` `CR` | `[ ]` |
| **Q-42** | Passive voice and agency erasure | Ch 9 | `NLP` `CR` `LIT` | `[ ]` |
| **Q-43** | Intertextuality and boilerplate detection | Ch 9 | `NLP` `DB` | `[ ]` |

### Part VIII — Cross-Cutting Patterns (Chapter 10)

| # | Question | Chapter | Methods | Status |
|---|----------|---------|---------|--------|
| **Q-44** | What themes has the LLM identified? | Ch 10 | `LLM` | `[ ]` |
| **Q-45** | Which submissions are thematic outliers? | Ch 10 | `LLM` `CR` | `[ ]` |
| **Q-46** | Do risk, justification, and compliance co-vary? | Ch 10 | `AGG` `LLM` | `[ ]` |
| **Q-47** | Comprehensive submission profile (master table) | Ch 10 | `AGG` `DB` `LLM` | `[ ]` |

### Part IX — Toward a Generalizable Critique (Chapter 11)

| # | Question | Chapter | Methods | Status |
|---|----------|---------|---------|--------|
| **Q-48** | What would a generalizable AIA critique framework look like? | Ch 11 | `LIT` `CR` | `[ ]` |
| **Q-49** | Can the Canadian corpus serve as empirical evidence for/against theoretical critiques? | Ch 11 | `AGG` `LLM` `LIT` | `[ ]` |
| **Q-50** | What are the necessary conditions for genuine AIA accountability? | Ch 11 | `LIT` `CR` | `[ ]` |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total research questions | **50** |
| Questions requiring `DB` (database facts) | 27 |
| Questions requiring `AGG` (aggregation) | 30 |
| Questions requiring `LLM` (semantic interpretation) | 24 |
| Questions requiring `NLP` (text analysis) | 4 |
| Questions requiring `LIT` (literature) | 10 |
| Questions requiring `CR` (close reading) | 14 |
| Thesis chapters (excl. conclusion) | **11** |

---

## Thesis Outline

### Chapter 1 — Introduction, Methodology & the AIA Landscape
> *What are AIAs, why do they matter, and how does this thesis study them?*

- **Q-01**: Historical genealogy of AIAs (LIT)
- **Q-06**: LLM interpretation consistency (AGG, LLM)
- **Q-07**: Token usage as complexity proxy (AGG)
- **Q-08**: Model provenance audit (DB)

### Chapter 2 — Philosophy & Applied Ethics of Algorithmic Impact Assessment
> *What ethical frameworks justify AIAs, and what are their philosophical limits?*

- **Q-02**: Ethical justifications — procedural justice, democratic accountability, precautionary principle, proportionality, transparency (LIT)
- **Q-03**: Critique taxonomy — performative compliance, self-assessment bias, quantification reductionism, enforcement gap, temporal mismatch, participation deficit (LIT)
- **Q-04**: Alternatives — independent auditing, participatory governance, moratoriums, HRIAs, continuous monitoring, regulatory sandboxes (LIT)
- **Q-05**: The EIA analogy and its limits (LIT)

### Chapter 3 — The Bilingual Governance Landscape
> *Where does bilingual governance break down, and what does the pattern reveal?*

- **Q-09**: Overall divergence rate (AGG, LLM)
- **Q-10**: Semantic fields that diverge most (AGG, LLM)
- **Q-11**: Distribution of divergence types (AGG, LLM)
- **Q-12**: Omission vs. terminological drift (AGG, LLM, CR)
- **Q-13**: Fidelity score and narrative text correlation (AGG, DB)

### Chapter 4 — The Accountability Gap
> *How does "accountability" fragment across EN/FR governance discourse?*

- **Q-14**: Accountability in English structured data (DB)
- **Q-15**: French distribution — responsabilité, reddition de comptes, imputabilité (DB, CR)
- **Q-16**: Divergent fields clustering around accountability (LLM, CR)

### Chapter 5 — Automation as Managerial Rationality
> *How do departments narrate automation, and what does their rhetoric reveal?*

- **Q-17**: Dominant justification themes (AGG, LLM)
- **Q-18**: Justification strength vs. trade-off acknowledgment (AGG, LLM, CR)
- **Q-19**: Automation type and justification rhetoric (AGG, DB, LLM)
- **Q-20**: Confinement claims vs. system capabilities (DB, LLM, CR)

### Chapter 6 — Risk Construction, Rights & the Quantification Problem
> *How does the AIA construct risk, and can rights be meaningfully quantified?*

- **Q-21**: Risk landscape across the corpus (AGG, LLM)
- **Q-22**: Rights dimensions most at stake (AGG, DB)
- **Q-23**: Proportionality — is automation proportional to risk? (AGG, DB, LLM, CR)
- **Q-24**: Reversibility × duration × rights interaction (AGG, DB)
- **Q-25**: Score distribution asymmetries across impact categories (AGG, LIT)
- **Q-26**: Scoring conflation — do unlike harms produce like scores? (AGG, DB, CR)
- **Q-27**: The commensurability problem — can Charter rights be scored 0–4? (DB, LLM, CR, LIT)

### Chapter 7 — Safeguard Theatre vs. Substantive Compliance
> *Are AIA safeguards genuine accountability mechanisms or performative?*

- **Q-28**: Compliance distribution (AGG, LLM)
- **Q-29**: Most common safeguard gaps (AGG, LLM)
- **Q-30**: The human override trifecta — explain, override, challenge (AGG, DB, LLM)
- **Q-31**: GBA+ and bias testing as governance signifiers (DB, LLM, CR)
- **Q-32**: Privacy protection vs. data sensitivity (DB, LLM)

### Chapter 8 — Departmental Governance Cultures & Inconsistency
> *Do departments produce systematically different governance approaches?*

- **Q-33**: Multi-metric department profile (AGG, LLM)
- **Q-34**: Bilingual commitment by department (AGG, LLM)
- **Q-35**: Department justification patterns (AGG, LLM)
- **Q-36**: Scoring variance within departments (AGG)
- **Q-37**: Score consistency for similar systems (AGG, DB)
- **Q-38**: Temporal drift in assessments (AGG, DB)
- **Q-39**: Field completion rates (AGG, DB)

### Chapter 9 — The Language of Algorithmic Governance
> *What do linguistic features reveal about the state's discursive construction of AI?*

- **Q-40**: Lexical analysis — managerial vs. rights vocabulary (NLP, DB)
- **Q-41**: Hedging and epistemic modality (NLP, DB, CR)
- **Q-42**: Passive voice and agency erasure (NLP, CR, LIT)
- **Q-43**: Boilerplate detection and intertextuality (NLP, DB)

### Chapter 10 — Cross-Cutting Thematic Patterns
> *What latent structures emerge when the corpus is analyzed as a single discourse?*

- **Q-44**: LLM-identified themes (LLM)
- **Q-45**: Thematic outliers (LLM, CR)
- **Q-46**: Risk × justification × compliance co-variation (AGG, LLM)
- **Q-47**: Comprehensive submission profile — master table (AGG, DB, LLM)

### Chapter 11 — Toward a Generalizable Critique of AIAs
> *From Canadian case study to global theory of algorithmic accountability.*

- **Q-48**: A generalizable AIA critique framework (LIT, CR)
- **Q-49**: Canadian corpus as empirical test of theoretical critiques (AGG, LLM, LIT)
- **Q-50**: Necessary conditions for genuine algorithmic accountability (LIT, CR)

### Chapter 12 — Conclusion
> *Synthesis, contributions, and future research directions.*

---

## Answering Sequence & Dependencies

Questions should be answered in this order, respecting dependencies:

```
PHASE 1 — Foundations (no dependencies)
  Q-01 → Q-05 (literature review — can run in parallel)
  Q-06 → Q-08 (methodology validation — can run in parallel)

PHASE 2 — Corpus-Level Facts (depends on Phase 1 methodology)
  Q-09 → Q-13 (bilingual divergence)
  Q-17 → Q-20 (justification rhetoric)
  Q-21 → Q-24 (risk & rights)
  Q-28 → Q-32 (safeguards)
  ↑ These four blocks can run in parallel

PHASE 3 — Comparative & Critical Analysis (depends on Phase 2 results)
  Q-14 → Q-16 (accountability gap — needs Q-09 divergence baseline)
  Q-25 → Q-27 (quantification critique — needs Q-21 risk data)
  Q-33 → Q-39 (departmental & inconsistency — needs all Phase 2)
  Q-40 → Q-43 (text analysis — needs exported corpus text)

PHASE 4 — Synthesis (depends on Phase 3)
  Q-44 → Q-47 (cross-cutting patterns — needs all above)
  Q-48 → Q-50 (generalizable critique — needs empirical + literature)
```

---

## Cross-Reference: Old Axis → New Question Number

| Old Reference | New # | Short Title |
|---------------|-------|-------------|
| RQ 1.1 | Q-09 | Overall divergence rate |
| RQ 1.2 | Q-10 | Semantic fields divergence |
| RQ 1.3 | Q-11 | Divergence type distribution |
| RQ 1.4 | Q-12 | Omission vs. drift |
| RQ 1.5 | Q-13 | Fidelity–narrative correlation |
| RQ 2.1 | Q-17 | Justification themes |
| RQ 2.2 | Q-18 | Justification vs. trade-offs |
| RQ 2.3 | Q-19 | Automation type × rhetoric |
| RQ 2.4 | Q-20 | Confinement vs. capabilities |
| RQ 3.1 | Q-21 | Risk landscape |
| RQ 3.2 | Q-22 | Rights dimensions |
| RQ 3.3 | Q-23 | Proportionality |
| RQ 3.4 | Q-24 | Reversibility × duration |
| RQ 4.1 | Q-28 | Compliance distribution |
| RQ 4.2 | Q-29 | Safeguard gaps |
| RQ 4.3 | Q-30 | Human override |
| RQ 4.4 | Q-31 | GBA+ & bias testing |
| RQ 4.5 | Q-32 | Privacy |
| RQ 5.1 | Q-33 | Department profile |
| RQ 5.2 | Q-34 | Department bilingualism |
| RQ 5.3 | Q-35 | Department justification |
| RQ 6.1 | Q-14 | Accountability EN |
| RQ 6.2 | Q-15 | Accountability FR |
| RQ 6.3 | Q-16 | Accountability divergence |
| RQ 7.1 | Q-44 | LLM themes |
| RQ 7.2 | Q-45 | Thematic outliers |
| RQ 7.3 | Q-46 | Risk–justification–compliance |
| RQ 7.4 | Q-47 | Master profile |
| RQ 8.1 | Q-06 | LLM consistency |
| RQ 8.2 | Q-07 | Token complexity |
| RQ 8.3 | Q-08 | Model provenance |
| RQ 9.1 | Q-36 | Department scoring variance |
| RQ 9.2 | Q-37 | Similar systems, similar scores? |
| RQ 9.3 | Q-38 | Temporal drift |
| RQ 9.4 | Q-39 | Field completion rates |
| RQ 10.1 | Q-25 | Category score distributions |
| RQ 10.2 | Q-26 | Scoring conflation |
| RQ 10.3 | Q-27 | Commensurability problem |
| RQ 11.1 | Q-40 | Lexical analysis |
| RQ 11.2 | Q-41 | Hedging & modality |
| RQ 11.3 | Q-42 | Passive voice |
| RQ 11.4 | Q-43 | Boilerplate detection |
| RQ 12.1 | Q-01 | AIA history |
| RQ 12.2 | Q-02 | Ethical justifications |
| RQ 12.3 | Q-03 | AIA critiques |
| RQ 12.4 | Q-04 | AIA alternatives |
| RQ 12.5 | Q-48–50 | Generalizable critique |

---

## Detailed Questions & SQL

> Below: full question specifications with SQL queries, methods, and thesis relevance.
> Questions retain their original Axis grouping for reference but are tagged with their new Q-number.

---

---

## Axis 1 — The Bilingual Divergence Landscape
> *Chapter 3 | Q-09 through Q-13*

**Central question:** Where does bilingual governance break down — and what does the pattern of breakdowns reveal about the politics of translation in algorithmic governance?

### RQ 1.1 → Q-09 | What is the overall divergence rate across the corpus?
> Methods: `AGG` `LLM`

```sql
SELECT
    has_divergence,
    COUNT(*) AS submissions,
    ROUND(COUNT(*)::numeric / 30 * 100, 1) AS pct
FROM interp_bilingual_divergence
GROUP BY has_divergence;
```

**Thesis relevance:** Establishes the baseline claim — is bilingual AIA governance genuinely bilingual, or structurally monolingual?

### RQ 1.2 → Q-10 | Which semantic fields diverge most?
> Methods: `AGG` `LLM`

```sql
SELECT
    field->>'field' AS field_name,
    field->>'type' AS divergence_type,
    field->>'severity' AS severity,
    COUNT(*) AS occurrences
FROM interp_bilingual_divergence,
     jsonb_array_elements(divergent_fields) AS field
GROUP BY field_name, divergence_type, severity
ORDER BY occurrences DESC;
```

**Thesis relevance:** Identifies *where* the untranslatable emerges — are rights fields, decision descriptions, or trade-offs the primary sites of semantic rupture?

**Visualization:** Heatmap of divergence frequency by field name and severity (minor/moderate/significant).

### RQ 1.3 → Q-11 | What is the distribution of divergence types?
> Methods: `AGG` `LLM`

```sql
SELECT
    overall_divergence_type,
    COUNT(*) AS submissions,
    ROUND(AVG(semantic_fidelity_score)::numeric, 2) AS avg_fidelity
FROM interp_bilingual_divergence
GROUP BY overall_divergence_type
ORDER BY submissions DESC;
```

**Thesis relevance:** Tests whether divergence is primarily linguistic (grammar), legal (Common Law vs Civil Law), cultural, or professional — supporting or complicating the "two governance regimes" claim.

**Visualization:** Pie chart of divergence origins + box plot of fidelity scores per origin type.

### RQ 1.4 → Q-12 | Is the dominant divergence omission or terminological drift?
> Methods: `AGG` `LLM` `CR`

```sql
SELECT
    field->>'type' AS divergence_type,
    COUNT(*) AS total_occurrences,
    COUNT(DISTINCT bd.submission_id) AS submissions_affected
FROM interp_bilingual_divergence bd,
     jsonb_array_elements(divergent_fields) AS field
GROUP BY divergence_type
ORDER BY total_occurrences DESC;
```

**Thesis relevance:** A critical distinction — if divergence is primarily *omission* (French fields left empty), the problem is structural monolingualism, not translation failure. If it is *terminological* or *reframing*, the problem is deeper: governance concepts genuinely resist equivalence. The data shows **omission dominates overwhelmingly**, reframing the "untranslatable" thesis: the Canadian state doesn't even attempt translation for most narrative governance fields.

**Visualization:** Stacked bar chart of divergence types across fields; word cloud from field-level explanations.

### RQ 1.5 → Q-13 | Is there a correlation between fidelity score and the presence of narrative text?
> Methods: `AGG` `DB`

```sql
SELECT
    bd.submission_id,
    bd.semantic_fidelity_score,
    (CASE WHEN pd.description_fr IS NOT NULL AND pd.description_fr != '' THEN 1 ELSE 0 END) AS has_fr_description,
    (CASE WHEN ra.client_needs_fr IS NOT NULL AND ra.client_needs_fr != '' THEN 1 ELSE 0 END) AS has_fr_client_needs,
    (CASE WHEN ii.rights_freedoms_fr IS NOT NULL AND ii.rights_freedoms_fr != '' THEN 1 ELSE 0 END) AS has_fr_rights
FROM interp_bilingual_divergence bd
JOIN project_details pd USING (submission_id)
JOIN reasons_for_automation ra USING (submission_id)
JOIN individual_impacts ii USING (submission_id)
ORDER BY bd.semantic_fidelity_score;
```

**Thesis relevance:** Tests whether low fidelity is driven by absence (fields not translated at all) or presence (fields translated but with semantic drift) — two very different governance failures.

---

## Axis 2 — Automation Justification Rhetoric
> *Chapter 5 | Q-17 through Q-20*

**Central question:** How do federal departments narrate the necessity of automation, and what does their rhetoric reveal about the state's relationship to algorithmic decision-making?

### RQ 2.1 → Q-17 | What justification themes dominate the corpus?
> Methods: `AGG` `LLM`

```sql
SELECT
    justification_theme,
    COUNT(*) AS n,
    ROUND(AVG(strength_score)::numeric, 1) AS avg_strength,
    MIN(strength_score) AS min_strength,
    MAX(strength_score) AS max_strength
FROM interp_automation_justification
GROUP BY justification_theme
ORDER BY n DESC;
```

**Thesis relevance:** If "efficiency" dominates, the state frames automation as managerial optimization — not as a democratic or rights-affecting intervention. This matters for how algorithmic governance is legitimated.

**Visualization:** Stacked bar chart of theme distribution with strength overlay.

### RQ 2.2 → Q-18 | Do departments with stronger justifications also acknowledge trade-offs?
> Methods: `AGG` `LLM` `CR`

```sql
SELECT
    pd.department,
    aj.justification_theme,
    aj.strength_score,
    LENGTH(aj.trade_off_adequacy) AS trade_off_detail_length,
    aj.trade_off_adequacy
FROM interp_automation_justification aj
JOIN project_details pd USING (submission_id)
ORDER BY aj.strength_score DESC;
```

**Thesis relevance:** Tests whether strong automation advocacy correlates with superficial trade-off analysis — a "pro-automation bias" in the assessment instrument itself.

### RQ 2.3 → Q-19 | How does automation type relate to justification rhetoric?
> Methods: `AGG` `DB` `LLM`

```sql
SELECT
    CASE ad.automation_type_score
        WHEN 0 THEN 'Decision support'
        WHEN 2 THEN 'Partial automation'
        WHEN 4 THEN 'Full automation'
        ELSE 'Unknown'
    END AS automation_level,
    aj.justification_theme,
    COUNT(*) AS n,
    ROUND(AVG(aj.strength_score)::numeric, 1) AS avg_strength
FROM interp_automation_justification aj
JOIN about_the_decision ad USING (submission_id)
GROUP BY automation_level, aj.justification_theme
ORDER BY automation_level, n DESC;
```

**Thesis relevance:** Are fully automated systems justified differently than decision-support tools? Does rhetoric escalate with automation level?

**Visualization:** Grouped bar chart (automation level x justification theme).

### RQ 2.4 → Q-20 | What is the relationship between confinement claims and system capabilities?
> Methods: `DB` `LLM` `CR`

```sql
SELECT
    pd.system_capabilities,
    aj.confinement_assessment,
    ad.automation_type_score,
    ad.used_by_different_org_score
FROM interp_automation_justification aj
JOIN project_details pd USING (submission_id)
JOIN about_the_decision ad USING (submission_id)
WHERE pd.system_capabilities IS NOT NULL
  AND pd.system_capabilities != '';
```

**Thesis relevance:** Do departments claim narrow confinement while listing broad capabilities? Reveals gaps between rhetoric and technical reality.

---

## Axis 3 — Risk, Rights, and Proportionality
> *Chapter 6 | Q-21 through Q-24*

**Central question:** How does the AIA framework construct risk, and does the instrument adequately capture the human rights implications of automated decision-making?

### RQ 3.1 → Q-21 | What is the risk landscape across the corpus?
> Methods: `AGG` `LLM`

```sql
SELECT
    rri.risk_level_label,
    COUNT(*) AS n,
    ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk_total,
    ROUND(AVG(fs.impact_level)::numeric, 1) AS avg_impact_level
FROM interp_risk_rights_impact rri
JOIN risk_profile rp USING (submission_id)
JOIN form_submissions fs ON fs.id = rri.submission_id
GROUP BY rri.risk_level_label
ORDER BY n DESC;
```

**Thesis relevance:** If all assessments cluster at low/moderate, the AIA framework may systematically understate risk — a structural design critique.

**Visualization:** Radar chart of average risk dimension scores; histogram of risk_total distribution.

### RQ 3.2 → Q-22 | Which rights dimensions are most at stake?
> Methods: `AGG` `DB`

```sql
SELECT
    'Rights & Freedoms' AS dimension,
    ROUND(AVG(rights_freedoms_score)::numeric, 2) AS avg_score,
    COUNT(*) FILTER (WHERE rights_freedoms_score > 0) AS affected_count
FROM individual_impacts
UNION ALL
SELECT 'Equality & Dignity', ROUND(AVG(equality_dignity_score)::numeric, 2),
    COUNT(*) FILTER (WHERE equality_dignity_score > 0)
FROM individual_impacts
UNION ALL
SELECT 'Health & Wellbeing', ROUND(AVG(health_wellbeing_score)::numeric, 2),
    COUNT(*) FILTER (WHERE health_wellbeing_score > 0)
FROM individual_impacts
UNION ALL
SELECT 'Economic Interests', ROUND(AVG(economic_interests_score)::numeric, 2),
    COUNT(*) FILTER (WHERE economic_interests_score > 0)
FROM individual_impacts;
```

**Thesis relevance:** Which fundamental rights does the Canadian state consider most at risk from its own automated systems?

**Visualization:** Lollipop chart comparing the four rights dimensions.

### RQ 3.3 → Q-23 | Is automation proportional to risk?
> Methods: `AGG` `DB` `LLM` `CR`

```sql
SELECT
    pd.project_title_en,
    pd.department,
    rri.risk_level_label,
    rri.proportionality_assessment,
    ad.automation_type_score,
    rp.risk_total,
    fs.impact_level
FROM interp_risk_rights_impact rri
JOIN project_details pd USING (submission_id)
JOIN about_the_decision ad USING (submission_id)
JOIN risk_profile rp USING (submission_id)
JOIN form_submissions fs ON fs.id = rri.submission_id
ORDER BY rp.risk_total DESC;
```

**Thesis relevance:** Are high-risk systems still being fully automated? Tests whether proportionality is enforced or merely documented.

### RQ 3.4 → Q-24 | How do reversibility and duration interact with rights impact?
> Methods: `AGG` `DB`

```sql
SELECT
    CASE ad.impacts_reversible_score
        WHEN 0 THEN 'Irreversible'
        WHEN 2 THEN 'Partially reversible'
        WHEN 4 THEN 'Easily reversible'
        ELSE 'Other'
    END AS reversibility,
    CASE ad.impact_duration_score
        WHEN 0 THEN 'Long-term'
        WHEN 2 THEN 'Medium-term'
        WHEN 4 THEN 'Brief'
        ELSE 'Other'
    END AS duration,
    COUNT(*) AS n,
    ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk
FROM about_the_decision ad
JOIN risk_profile rp USING (submission_id)
GROUP BY reversibility, duration
ORDER BY avg_risk DESC;
```

**Thesis relevance:** The combination of irreversible + long-term + automated decision-making represents the highest-stakes governance scenario. How common is it?

**Visualization:** Bubble chart (reversibility x duration, bubble size = count, color = avg risk).

---

## Axis 4 — Safeguard Theatre vs. Substantive Compliance
> *Chapter 7 | Q-28 through Q-32*

**Central question:** Do AIA safeguards represent genuine accountability mechanisms, or is compliance performative?

### RQ 4.1 → Q-28 | What is the compliance distribution?
> Methods: `AGG` `LLM`

```sql
SELECT
    overall_compliance_label,
    overall_compliance_score,
    COUNT(*) AS n
FROM interp_safeguard_compliance
GROUP BY overall_compliance_label, overall_compliance_score
ORDER BY overall_compliance_score DESC;
```

**Visualization:** Donut chart of compliance labels.

### RQ 4.2 → Q-29 | What are the most common safeguard gaps?
> Methods: `AGG` `LLM`

```sql
SELECT
    gap::text AS gap_description,
    COUNT(*) AS frequency
FROM interp_safeguard_compliance,
     jsonb_array_elements(gaps_identified) AS gap
GROUP BY gap_description
ORDER BY frequency DESC
LIMIT 15;
```

**Thesis relevance:** Identifies systematic blind spots — if the same gaps appear across departments, the problem is structural (in the AIA instrument) rather than departmental.

**Visualization:** Horizontal bar chart of gap frequency.

### RQ 4.3 → Q-30 | The human override question
> Methods: `AGG` `DB` `LLM`

```sql
SELECT
    f.human_override_enabled,
    f.client_recourse_process,
    f.can_produce_reasons,
    COUNT(*) AS n,
    ROUND(AVG(sc.overall_compliance_score)::numeric, 1) AS avg_compliance
FROM fairness f
JOIN interp_safeguard_compliance sc USING (submission_id)
GROUP BY f.human_override_enabled, f.client_recourse_process, f.can_produce_reasons
ORDER BY n DESC;
```

**Thesis relevance:** The trifecta of algorithmic accountability — can the system explain itself, can humans override it, and can affected persons challenge decisions? How many systems satisfy all three?

### RQ 4.4 → Q-31 | GBA+ and bias testing as governance signifiers
> Methods: `DB` `LLM` `CR`

```sql
SELECT
    pd.department,
    dqb.gba_plus_conducted,
    dqb.bias_testing_documented,
    dqb.bias_testing_public,
    sc.bias_mitigation_assessment
FROM data_quality_bias dqb
JOIN project_details pd USING (submission_id)
JOIN interp_safeguard_compliance sc USING (submission_id)
ORDER BY pd.department;
```

**Thesis relevance:** Gender-Based Analysis Plus (GBA+) is a Canadian governance innovation. Is it actually being conducted, or merely checked off? Is bias testing documented but not made public (transparency gap)?

### RQ 4.5 → Q-32 | Privacy in the age of automation
> Methods: `DB` `LLM`

```sql
SELECT
    ps.pia_conducted,
    ps.privacy_by_design,
    ps.de_identification_applied,
    atd.uses_personal_info,
    atd.security_classification_score,
    sc.privacy_assessment
FROM privacy_security ps
JOIN about_the_data atd USING (submission_id)
JOIN interp_safeguard_compliance sc USING (submission_id)
WHERE atd.uses_personal_info > 0;
```

**Thesis relevance:** For systems processing personal information, is privacy protection proportional to data sensitivity?

---

## Axis 5 — Departmental Governance Cultures
> *Chapter 8 | Q-33 through Q-35*

**Central question:** Do different federal departments produce systematically different algorithmic governance approaches, and what does this reveal about bureaucratic culture?

### RQ 5.1 → Q-33 | Department-level profile
> Methods: `AGG` `LLM`

```sql
SELECT
    pd.department,
    COUNT(*) AS submissions,
    ROUND(AVG(aj.strength_score)::numeric, 1) AS avg_justification_strength,
    ROUND(AVG(sc.overall_compliance_score)::numeric, 1) AS avg_compliance,
    ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk,
    ROUND(AVG(bd.semantic_fidelity_score)::numeric, 1) AS avg_fidelity
FROM project_details pd
JOIN interp_automation_justification aj USING (submission_id)
JOIN interp_safeguard_compliance sc USING (submission_id)
JOIN risk_profile rp USING (submission_id)
JOIN interp_bilingual_divergence bd USING (submission_id)
GROUP BY pd.department
ORDER BY submissions DESC;
```

**Thesis relevance:** Core comparative table for the thesis — reveals whether algorithmic governance is uniform or fragmented across the federal bureaucracy.

**Visualization:** Multi-metric radar chart, one trace per department.

### RQ 5.2 → Q-34 | Department and bilingual commitment
> Methods: `AGG` `LLM`

```sql
SELECT
    pd.department,
    COUNT(*) AS n,
    ROUND(AVG(bd.semantic_fidelity_score)::numeric, 1) AS avg_fidelity,
    COUNT(*) FILTER (WHERE bd.semantic_fidelity_score >= 4) AS high_fidelity,
    COUNT(*) FILTER (WHERE bd.semantic_fidelity_score <= 2) AS low_fidelity
FROM project_details pd
JOIN interp_bilingual_divergence bd USING (submission_id)
GROUP BY pd.department
ORDER BY avg_fidelity;
```

**Thesis relevance:** Which departments take bilingual governance seriously? Which produce structurally monolingual assessments despite the bilingual mandate?

**Visualization:** Diverging bar chart (high fidelity left, low fidelity right, by department).

### RQ 5.3 → Q-35 | Department justification patterns
> Methods: `AGG` `LLM`

```sql
SELECT
    pd.department,
    aj.justification_theme,
    COUNT(*) AS n
FROM project_details pd
JOIN interp_automation_justification aj USING (submission_id)
GROUP BY pd.department, aj.justification_theme
ORDER BY pd.department, n DESC;
```

**Thesis relevance:** Do service-delivery departments (IRCC) justify differently than regulatory departments? Does institutional mission shape automation rhetoric?

**Visualization:** Stacked 100% bar chart (department x justification theme).

---

## Axis 6 — The Accountability Gap (Spotlight)
> *Chapter 4 | Q-14 through Q-16*

**Central question:** How does the English concept of "accountability" fragment across French governance discourse, and what does this reveal about the limits of bilingual algorithmic governance?

### RQ 6.1 → Q-14 | Accountability in the structured data
> Methods: `DB`

```sql
-- Where "accountability" appears in English text fields
SELECT
    'project_details.description_en' AS source,
    pd.submission_id,
    pd.description_en
FROM project_details pd
WHERE pd.description_en ILIKE '%accountab%'
UNION ALL
SELECT
    'reasons_for_automation.public_benefits_en',
    ra.submission_id,
    ra.public_benefits_en
FROM reasons_for_automation ra
WHERE ra.public_benefits_en ILIKE '%accountab%'
UNION ALL
SELECT
    'about_the_decision.evaluation_criteria_en',
    ad.submission_id,
    ad.evaluation_criteria_en
FROM about_the_decision ad
WHERE ad.evaluation_criteria_en ILIKE '%accountab%';
```

### RQ 6.2 → Q-15 | The French distribution of accountability
> Methods: `DB` `CR`

```sql
-- Search French fields for the distributed accountability terms
SELECT
    source_table,
    term,
    COUNT(*) AS occurrences
FROM (
    SELECT 'project_details' AS source_table, 'responsabilite' AS term, submission_id
    FROM project_details WHERE description_fr ILIKE '%responsabilit%'
    UNION ALL
    SELECT 'project_details', 'reddition de comptes', submission_id
    FROM project_details WHERE description_fr ILIKE '%reddition%'
    UNION ALL
    SELECT 'project_details', 'imputabilite', submission_id
    FROM project_details WHERE description_fr ILIKE '%imputabil%'
    UNION ALL
    SELECT 'reasons_for_automation', 'responsabilite', submission_id
    FROM reasons_for_automation WHERE public_benefits_fr ILIKE '%responsabilit%'
    UNION ALL
    SELECT 'reasons_for_automation', 'reddition de comptes', submission_id
    FROM reasons_for_automation WHERE public_benefits_fr ILIKE '%reddition%'
) sub
GROUP BY source_table, term
ORDER BY occurrences DESC;
```

**Thesis relevance:** This is the signature finding — English "accountability" maps to at least three French terms, each encoding a different governance philosophy:
- **responsabilit** = moral/personal responsibility
- **reddition de comptes** = formal reporting obligation (administrative tradition)
- **imputabilit** = legal attributability (Civil Law tradition)

**Visualization:** Sankey diagram showing EN "accountability" splitting into three FR governance streams.

### RQ 6.3 → Q-16 | Do divergent fields cluster around accountability-adjacent concepts?
> Methods: `LLM` `CR`

```sql
SELECT
    field->>'field' AS field_name,
    field->>'explanation' AS explanation
FROM interp_bilingual_divergence,
     jsonb_array_elements(divergent_fields) AS field
WHERE field->>'explanation' ILIKE '%accountab%'
   OR field->>'explanation' ILIKE '%responsab%'
   OR field->>'explanation' ILIKE '%reddition%'
   OR field->>'explanation' ILIKE '%oversight%'
   OR field->>'explanation' ILIKE '%surveillance%';
```

---

## Axis 7 — Cross-Cutting Thematic Patterns
> *Chapter 10 | Q-44 through Q-47*

**Central question:** What latent structures emerge when the entire corpus is analyzed as a single discourse?

### RQ 7.1 → Q-44 | What themes has the LLM identified?
> Methods: `LLM`

```sql
SELECT
    pattern_type,
    theme_label,
    theme_description,
    prevalence,
    array_length(submission_ids, 1) AS submission_count
FROM interp_thematic_patterns
ORDER BY pattern_type, prevalence DESC;
```

**Visualization:** Treemap (area = prevalence, grouped by pattern_type).

### RQ 7.2 → Q-45 | Which submissions are thematic outliers?
> Methods: `LLM` `CR`

```sql
SELECT
    tp.pattern_type,
    tp.theme_label,
    outlier->>'submission_id' AS submission_id,
    outlier->>'reason' AS reason
FROM interp_thematic_patterns tp,
     jsonb_array_elements(notable_outliers) AS outlier
WHERE notable_outliers IS NOT NULL
  AND jsonb_array_length(notable_outliers) > 0
ORDER BY tp.pattern_type;
```

**Thesis relevance:** Outliers are often the most theoretically interesting cases — they reveal where the AIA framework fails to normalize governance discourse.

### RQ 7.3 → Q-46 | Do risk, justification, and compliance co-vary?
> Methods: `AGG` `LLM`

```sql
SELECT
    aj.justification_theme,
    rri.risk_level_label,
    sc.overall_compliance_label,
    COUNT(*) AS n
FROM interp_automation_justification aj
JOIN interp_risk_rights_impact rri USING (submission_id)
JOIN interp_safeguard_compliance sc USING (submission_id)
GROUP BY aj.justification_theme, rri.risk_level_label, sc.overall_compliance_label
ORDER BY n DESC;
```

**Thesis relevance:** Tests whether high-risk systems with efficiency justifications are the ones with the weakest safeguards — the most concerning governance configuration.

**Visualization:** Alluvial/Sankey diagram (justification theme -> risk level -> compliance label).

### RQ 7.4 → Q-47 | Comprehensive submission profile
> Methods: `AGG` `DB` `LLM`

```sql
SELECT
    pd.department,
    pd.project_title_en,
    aj.justification_theme,
    aj.strength_score,
    rri.risk_level_label,
    rp.risk_total,
    sc.overall_compliance_label,
    sc.overall_compliance_score,
    bd.has_divergence,
    bd.semantic_fidelity_score,
    fs.impact_level
FROM project_details pd
JOIN interp_automation_justification aj USING (submission_id)
JOIN interp_risk_rights_impact rri USING (submission_id)
JOIN risk_profile rp USING (submission_id)
JOIN interp_safeguard_compliance sc USING (submission_id)
JOIN interp_bilingual_divergence bd USING (submission_id)
JOIN form_submissions fs ON fs.id = pd.submission_id
ORDER BY rp.risk_total DESC;
```

**Thesis relevance:** The "master table" for the thesis — every submission with all four interpretation dimensions. Export as CSV for statistical analysis or case selection.

---

## Axis 8 — Methodological Reflections
> *Chapter 1 | Q-06 through Q-08*

**Central question:** What does using LLMs to study algorithmic governance reveal about the limits and possibilities of computational hermeneutics?

### RQ 8.1 → Q-06 | LLM interpretation consistency
> Methods: `AGG` `LLM`

```sql
-- Compare LLM risk labels against computed impact levels
SELECT
    rri.risk_level_label AS llm_assessment,
    fs.impact_level AS computed_level,
    COUNT(*) AS n
FROM interp_risk_rights_impact rri
JOIN form_submissions fs ON fs.id = rri.submission_id
WHERE fs.impact_level IS NOT NULL
GROUP BY llm_assessment, computed_level
ORDER BY computed_level, llm_assessment;
```

**Thesis relevance:** Does the LLM's qualitative risk assessment align with the AIA's computed impact level? Divergence here reveals either LLM limitations or limitations in the scoring algorithm — both methodologically important.

### RQ 8.2 → Q-07 | Token usage as complexity proxy
> Methods: `AGG`

```sql
SELECT
    'justification' AS analysis,
    ROUND(AVG((raw_llm_response->'usage'->>'completion_tokens')::int)::numeric) AS avg_tokens
FROM interp_automation_justification
UNION ALL
SELECT 'risk',
    ROUND(AVG((raw_llm_response->'usage'->>'completion_tokens')::int)::numeric)
FROM interp_risk_rights_impact
UNION ALL
SELECT 'divergence',
    ROUND(AVG((raw_llm_response->'usage'->>'completion_tokens')::int)::numeric)
FROM interp_bilingual_divergence
UNION ALL
SELECT 'safeguard',
    ROUND(AVG((raw_llm_response->'usage'->>'completion_tokens')::int)::numeric)
FROM interp_safeguard_compliance;
```

**Thesis relevance:** Which analysis type requires the most LLM reasoning? This is a methodological data point about the relative complexity of governance dimensions.

### RQ 8.3 → Q-08 | Model provenance audit
> Methods: `DB`

```sql
SELECT
    model_id,
    prompt_version,
    COUNT(*) AS rows,
    MIN(created_at) AS earliest,
    MAX(created_at) AS latest
FROM (
    SELECT model_id, prompt_version, created_at FROM interp_automation_justification
    UNION ALL SELECT model_id, prompt_version, created_at FROM interp_risk_rights_impact
    UNION ALL SELECT model_id, prompt_version, created_at FROM interp_bilingual_divergence
    UNION ALL SELECT model_id, prompt_version, created_at FROM interp_safeguard_compliance
) all_interps
GROUP BY model_id, prompt_version;
```

**Thesis relevance:** Full reproducibility audit trail — critical for DH methodology chapter.

---

## Axis 9 — Inconsistency in Canadian Government AIA Practice
> *Chapter 8 | Q-36 through Q-39*

**Central question:** Are Canadian federal departments completing AIAs consistently, and what does systematic variation reveal about the reliability of the instrument as a governance tool?

### RQ 9.1 → Q-36 | How much do departments vary in scoring patterns?
> Methods: `AGG`

```sql
SELECT
    pd.department,
    COUNT(*) AS submissions,
    ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk,
    ROUND(STDDEV(rp.risk_total)::numeric, 1) AS risk_stddev,
    ROUND(AVG(fs.impact_level)::numeric, 1) AS avg_impact,
    MIN(fs.impact_level) AS min_impact,
    MAX(fs.impact_level) AS max_impact
FROM project_details pd
JOIN risk_profile rp USING (submission_id)
JOIN form_submissions fs ON fs.id = pd.submission_id
GROUP BY pd.department
HAVING COUNT(*) > 1
ORDER BY risk_stddev DESC NULLS LAST;
```

**Thesis relevance:** If departments with multiple submissions show high variance, the AIA instrument is not producing stable readings — the same organization interprets the same tool differently across projects. This supports the supervisor's intuition that AIAs are inconsistent. As the World Privacy Forum (Dixon et al., 2024) documented, "not all of Canada's AIAs are created equal."

### RQ 9.2 → Q-37 | Do similar systems receive similar scores?
> Methods: `AGG` `DB`

```sql
SELECT
    a.submission_id AS system_a,
    b.submission_id AS system_b,
    a_pd.project_title_en AS title_a,
    b_pd.project_title_en AS title_b,
    a_ad.automation_type_score AS auto_type_a,
    b_ad.automation_type_score AS auto_type_b,
    a_rp.risk_total AS risk_a,
    b_rp.risk_total AS risk_b,
    ABS(a_rp.risk_total - b_rp.risk_total) AS risk_diff
FROM about_the_decision a_ad
JOIN about_the_decision b_ad ON a_ad.automation_type_score = b_ad.automation_type_score
    AND a_ad.submission_id < b_ad.submission_id
JOIN risk_profile a_rp ON a_rp.submission_id = a_ad.submission_id
JOIN risk_profile b_rp ON b_rp.submission_id = b_ad.submission_id
JOIN project_details a_pd ON a_pd.submission_id = a_ad.submission_id
JOIN project_details b_pd ON b_pd.submission_id = b_ad.submission_id
WHERE a_ad.automation_type_score = b_ad.automation_type_score
ORDER BY risk_diff DESC;
```

**Thesis relevance:** Systems with the same automation type should cluster in risk scores. Wide dispersion suggests the instrument's questions are interpreted inconsistently — a measurement reliability problem.

### RQ 9.3 → Q-38 | Temporal drift: do assessments change over time?
> Methods: `AGG` `DB`

```sql
SELECT
    EXTRACT(YEAR FROM fs.modified_at) AS year,
    EXTRACT(QUARTER FROM fs.modified_at) AS quarter,
    COUNT(*) AS submissions,
    ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk,
    ROUND(AVG(fs.impact_level)::numeric, 1) AS avg_impact
FROM form_submissions fs
JOIN risk_profile rp ON rp.submission_id = fs.id
WHERE fs.modified_at IS NOT NULL
GROUP BY year, quarter
ORDER BY year, quarter;
```

**Thesis relevance:** The TBS has adjusted the scoring algorithm multiple times and added questions since 2019. If average scores shift over time, the assessment standard itself has changed — creating temporal inconsistency where two identical systems assessed in different years could receive different impact levels.

### RQ 9.4 → Q-39 | Field completion rates: which questions go unanswered?
> Methods: `AGG` `DB`

```sql
SELECT
    'description_en' AS field,
    COUNT(*) FILTER (WHERE description_en IS NOT NULL AND description_en != '') AS filled,
    COUNT(*) FILTER (WHERE description_en IS NULL OR description_en = '') AS empty
FROM project_details
UNION ALL
SELECT 'description_fr',
    COUNT(*) FILTER (WHERE description_fr IS NOT NULL AND description_fr != ''),
    COUNT(*) FILTER (WHERE description_fr IS NULL OR description_fr = '')
FROM project_details
UNION ALL
SELECT 'public_benefits_en',
    COUNT(*) FILTER (WHERE public_benefits_en IS NOT NULL AND public_benefits_en != ''),
    COUNT(*) FILTER (WHERE public_benefits_en IS NULL OR public_benefits_en = '')
FROM reasons_for_automation
UNION ALL
SELECT 'rights_freedoms_en',
    COUNT(*) FILTER (WHERE rights_freedoms_en IS NOT NULL AND rights_freedoms_en != ''),
    COUNT(*) FILTER (WHERE rights_freedoms_en IS NULL OR rights_freedoms_en = '')
FROM individual_impacts;
```

**Thesis relevance:** If narrative fields (especially rights-related ones) are frequently left blank, departments are treating the AIA as a quantitative scoring exercise and ignoring its qualitative governance functions. This is the "checkbox compliance" problem identified by Moss et al. (2021).

**Visualization:** Completion rate heatmap (fields x departments).

---

## Axis 10 — The Quantification Problem
> *Chapter 6 | Q-25 through Q-27*

**Central question:** Can the ethical and rights implications of automated decision-making be meaningfully reduced to numerical scores, and what do the scoring patterns reveal about the limits of quantification in algorithmic governance?

### RQ 10.1 → Q-25 | Why do different impact categories receive different score distributions?
> Methods: `AGG` `LIT`

```sql
SELECT
    'Rights & Freedoms' AS category,
    ROUND(AVG(rights_freedoms_score)::numeric, 2) AS avg,
    ROUND(STDDEV(rights_freedoms_score)::numeric, 2) AS stddev,
    MIN(rights_freedoms_score) AS min_score,
    MAX(rights_freedoms_score) AS max_score,
    COUNT(*) FILTER (WHERE rights_freedoms_score = 0) AS zero_count
FROM individual_impacts
UNION ALL
SELECT 'Equality & Dignity',
    ROUND(AVG(equality_dignity_score)::numeric, 2),
    ROUND(STDDEV(equality_dignity_score)::numeric, 2),
    MIN(equality_dignity_score), MAX(equality_dignity_score),
    COUNT(*) FILTER (WHERE equality_dignity_score = 0)
FROM individual_impacts
UNION ALL
SELECT 'Health & Wellbeing',
    ROUND(AVG(health_wellbeing_score)::numeric, 2),
    ROUND(STDDEV(health_wellbeing_score)::numeric, 2),
    MIN(health_wellbeing_score), MAX(health_wellbeing_score),
    COUNT(*) FILTER (WHERE health_wellbeing_score = 0)
FROM individual_impacts
UNION ALL
SELECT 'Economic Interests',
    ROUND(AVG(economic_interests_score)::numeric, 2),
    ROUND(STDDEV(economic_interests_score)::numeric, 2),
    MIN(economic_interests_score), MAX(economic_interests_score),
    COUNT(*) FILTER (WHERE economic_interests_score = 0)
FROM individual_impacts;
```

**Thesis relevance:** If rights and dignity scores cluster near zero while economic scores are higher, the instrument structurally privileges quantifiable economic harms over harder-to-measure rights impacts. This speaks directly to the supervisor's concern: "Are there issues that can't be quantified? (Human rights.)"

**Visualization:** Violin plots comparing score distributions across the four impact categories.

### RQ 10.2 → Q-26 | Does the scoring algorithm conflate unlike things?
> Methods: `AGG` `DB` `CR`

```sql
SELECT
    pd.project_title_en,
    ii.rights_freedoms_score,
    ii.equality_dignity_score,
    ii.health_wellbeing_score,
    ii.economic_interests_score,
    rp.risk_total,
    fs.impact_level,
    (ii.rights_freedoms_score + ii.equality_dignity_score +
     ii.health_wellbeing_score + ii.economic_interests_score) AS individual_impact_sum
FROM individual_impacts ii
JOIN risk_profile rp USING (submission_id)
JOIN form_submissions fs ON fs.id = ii.submission_id
JOIN project_details pd USING (submission_id)
ORDER BY rp.risk_total DESC;
```

**Thesis relevance:** Can a system with zero rights impact but high economic impact receive the same overall score as one with high rights impact but zero economic impact? If so, the additive scoring model treats fundamentally different governance concerns as interchangeable — a category error with serious ethical implications.

### RQ 10.3 → Q-27 | The commensurability problem: can human rights be scored 0–4?
> Methods: `DB` `LLM` `CR` `LIT`

```sql
SELECT
    pd.project_title_en,
    pd.department,
    ii.rights_freedoms_en,
    ii.rights_freedoms_score,
    rri.rights_analysis
FROM individual_impacts ii
JOIN project_details pd USING (submission_id)
JOIN interp_risk_rights_impact rri USING (submission_id)
WHERE ii.rights_freedoms_score > 0
ORDER BY ii.rights_freedoms_score DESC;
```

**Thesis relevance:** Close reading of how departments narrate rights impacts alongside their numerical scores. Do the qualitative descriptions support the quantitative assignment, or do they reveal that the scoring compresses incommensurable harms? This is the core philosophical critique: ordinal scales assume commensurability, but Charter rights violations cannot meaningfully be scored as "2 out of 4."

---

## Axis 11 — Language Patterns and Textual Analysis
> *Chapter 9 | Q-40 through Q-43*

**Central question:** What do the linguistic features of AIA text fields reveal about how the Canadian state discursively constructs algorithmic governance?

### RQ 11.1 → Q-40 | Lexical analysis: what vocabulary dominates AIA discourse?
> Methods: `NLP` `DB`

```sql
SELECT
    pd.submission_id,
    pd.department,
    pd.description_en,
    ra.efficiency_gains_en,
    ra.public_benefits_en,
    ra.client_needs_en
FROM project_details pd
JOIN reasons_for_automation ra USING (submission_id)
WHERE pd.description_en IS NOT NULL
  AND pd.description_en != '';
```

**Method:** Export to Python for tokenization, frequency analysis, and TF-IDF. Key analytical questions:
- Does managerial vocabulary ("efficiency," "streamline," "optimize," "modernize") dominate over rights vocabulary ("fairness," "equity," "dignity," "rights")?
- Are there departments with distinctive lexical profiles?

**Visualization:** Word frequency comparison chart (managerial vs. rights vocabulary); TF-IDF word clouds by department.

### RQ 11.2 → Q-41 | Hedging and epistemic modality: how certain are departments about their own systems?
> Methods: `NLP` `DB` `CR`

```sql
SELECT
    pd.department,
    pd.project_title_en,
    pd.description_en,
    ra.public_benefits_en,
    ii.rights_freedoms_en
FROM project_details pd
JOIN reasons_for_automation ra USING (submission_id)
JOIN individual_impacts ii USING (submission_id)
WHERE pd.description_en IS NOT NULL;
```

**Method:** Corpus linguistic analysis of hedging markers ("may," "might," "could," "potentially," "it is anticipated that," "to the extent possible"). High hedging density in rights-related fields may indicate departments are uncertain about — or strategically distancing themselves from — the rights implications of their systems.

**Visualization:** Hedging frequency by field type (description vs. benefits vs. rights).

### RQ 11.3 → Q-42 | Passive voice and agency erasure
> Methods: `NLP` `CR` `LIT`

**Method:** Parse narrative fields for passive constructions ("decisions are made," "data is collected," "impacts are mitigated") vs. active constructions with specified agents. Heavy use of passive voice in AIA texts may perform a discursive function: erasing the human agents responsible for algorithmic decisions.

**Thesis relevance:** Connects to critical discourse analysis (Fairclough, van Dijk) — the AIA instrument may enable a rhetoric of automation where "the system decides" rather than "we decide through the system." This linguistic pattern mirrors the accountability gap identified in Axis 6.

### RQ 11.4 → Q-43 | Intertextuality and boilerplate detection
> Methods: `NLP` `DB`

```sql
SELECT
    a.submission_id AS sub_a,
    b.submission_id AS sub_b,
    a_pd.department AS dept_a,
    b_pd.department AS dept_b,
    a_pd.description_en AS desc_a,
    b_pd.description_en AS desc_b
FROM project_details a_pd
JOIN project_details b_pd ON a_pd.submission_id < b_pd.submission_id
    AND a_pd.description_en IS NOT NULL
    AND b_pd.description_en IS NOT NULL
    AND a_pd.description_en != ''
    AND b_pd.description_en != ''
    AND a_pd.submission_id = a.submission_id
    AND b_pd.submission_id = b.submission_id
CROSS JOIN LATERAL (SELECT a_pd.submission_id) a(submission_id)
CROSS JOIN LATERAL (SELECT b_pd.submission_id) b(submission_id);
```

**Method:** Export text pairs and compute Jaccard similarity or cosine similarity. High textual similarity across submissions — especially across departments — would indicate copy-paste boilerplate culture: departments recycling language rather than conducting genuine assessment.

**Thesis relevance:** Boilerplate is the textual signature of performative compliance (Moss et al., 2021).

**Visualization:** Similarity matrix heatmap across all submissions.

---

## Axis 12 — Philosophy and Applied Ethics of AIAs
> *Chapters 1–2, 11 | Q-01 through Q-05, Q-48 through Q-50*

**Central question:** What are the ethical foundations, justifications, and philosophical critiques of Algorithmic Impact Assessments as governance instruments?

### RQ 12.1 → Q-01 | Historical genealogy: how did AIAs emerge as governance tools?
> Methods: `LIT`

**Key sources:**
- Reisman, Schultz, Crawford & Whittaker (2018), "Algorithmic Impact Assessments: A Practical Framework for Public Agency Accountability" — AI Now Institute
- Canada's Directive on Automated Decision-Making (Treasury Board, 2019) — first national AIA mandate
- NYC Local Law 144 (2021) — first municipal algorithmic audit law
- EU AI Act Article 27 (2024) — Fundamental Rights Impact Assessment (FRIA) requirement

**Research questions:**
1. How did the Environmental Impact Assessment (EIA) analogy shape the design of AIAs, and where does the analogy break down?
2. Is Canada's AIA framework a product of the precautionary principle, procedural justice theory, or managerial rationality — and does this origin shape its limitations?
3. How has the AIA instrument evolved since 2019, and what does each revision reveal about lessons learned?

### Q-05 | How does the EIA analogy shape — and limit — AIA design?
> Methods: `LIT`

**Research questions:**
1. How did Reisman et al. (2018) adapt the Environmental Impact Statement (EIS/NEPA) model for algorithmic contexts?
2. Where does the analogy hold (ex ante assessment, public participation, documentation) and where does it break down (measurability of harms, scientific characterizability, cumulative effects)?
3. Has the EIA regime's own history of performative compliance been inherited by the AIA model?

**Key sources:** Reisman, Schultz, Crawford & Whittaker (2018); NEPA scholarship; EIA effectiveness literature.

### RQ 12.2 → Q-02 | What ethical frameworks justify AIAs?
> Methods: `LIT`

**Research questions:**
1. **Procedural justice:** Do AIAs produce legitimacy through process, even if substantive outcomes remain unchanged? (Cf. Tyler, 1990; Rawls's pure procedural justice.)
2. **Democratic accountability:** Do AIAs serve as instruments of democratic self-governance, or do they substitute bureaucratic process for genuine democratic deliberation? (Cf. Selbst, 2021.)
3. **Precautionary principle:** Do AIAs embody a precautionary approach to algorithmic governance — requiring proof of safety before deployment — or do they merely require documentation of risk?
4. **Proportionality:** Does Canada's tiered impact-level system (I–IV) operationalize proportionality effectively, or does the scoring methodology distort proportionality by treating unlike harms as commensurable?
5. **Transparency:** Do published AIAs actually enable meaningful public scrutiny, or do they produce "transparency theatre" — disclosure without comprehension?

### RQ 12.3 → Q-03 | What are the critiques of AIAs as governance tools?
> Methods: `LIT`

**Critique taxonomy:**

| Critique | Key Scholars | Core Argument |
|---|---|---|
| Performative compliance | Moss, Metcalf et al. (Data & Society, 2021) | AIAs become self-referential bureaucratic processes serving institutional needs rather than affected communities |
| Self-assessment bias | Selbst (Harvard JOLT, 2021) | Reliance on good-faith self-assessment is undermined by institutional incentives; the fox guards the henhouse |
| Quantification reductionism | World Privacy Forum (Dixon et al., 2024) | Scoring complex legal/fairness concepts as numerical ratings decontextualizes and distorts them |
| Enforcement gap | NYC Comptroller audit (2025) | Without meaningful penalties, AIAs become voluntary exercises |
| Temporal mismatch | EU AI Act drafters | Point-in-time assessments cannot capture emergent harms from model drift and changing data |
| Participation deficit | ACM FAccT scholarship | Affected communities rarely have meaningful input into assessments about systems that affect them |
| The assessment industrial complex | Data & Society AIML | Assessment regimes become self-perpetuating bureaucratic infrastructure |

**Thesis relevance:** The Canadian corpus provides empirical evidence to test each of these theoretical critiques. Do the AIAs in our database exhibit checkbox compliance? Self-assessment bias? Quantification failures?

### RQ 12.4 → Q-04 | What are the alternatives to AIAs?
> Methods: `LIT`

**Research questions:**
1. **Independent algorithmic auditing** vs. self-assessment: Would mandatory third-party audits (as in NYC Local Law 144) produce more reliable assessments than Canada's self-assessment model?
2. **Participatory governance:** Could affected community review boards provide accountability mechanisms that bureaucratic instruments cannot? What would this look like for Canada's federal systems?
3. **Moratoriums and bans:** For which automated decision systems — if any — should the response be prohibition rather than assessment? (Cf. bans on facial recognition in law enforcement.)
4. **Human Rights Impact Assessments (HRIAs):** Do frameworks like the Ontario Human Rights Commission's HRIA, the UNDP's AI assessment toolkit, or the Council of Europe's HUDERIA offer more rigorous rights analysis than Canada's scoring model?
5. **Continuous monitoring:** Should Canada move from point-in-time AIAs to lifecycle governance with ongoing post-deployment monitoring, as required by the EU AI Act?
6. **Regulatory sandboxes:** Could controlled testing environments (cf. EU AI Act Article 57, Utah AI Policy Act 2024) complement or replace ex ante impact assessment?

### RQ 12.5 → Q-48, Q-49, Q-50 | Toward a critique framework: from Canadian case to general theory
> Methods: `LIT` `CR` `AGG` `LLM`

**Research questions:**
1. What would a generalizable framework for critiquing AIAs look like, starting from the Canadian evidence but applicable to the EU FRIA, NYC AEDT audits, and future regimes?
2. Can the Canadian AIA corpus serve as empirical evidence for or against the theoretical critiques in the literature?
3. What are the necessary and sufficient conditions for an AIA regime to produce genuine accountability rather than performative compliance?

**Thesis relevance:** This axis positions the thesis as not merely a study of Canadian bilingual governance but as a contribution to the global debate on algorithmic accountability. The supervisor's instruction — "develop a strategy for critiquing AIAs starting with the Canadian ones, but applicable beyond" — is operationalized here.

---

## Suggested Thesis Chapter Mapping

| Chapter | Research Axes | Key Visualizations |
|---|---|---|
| 1. Introduction & Framework | Axis 8 (methodology), Axis 12 (philosophy) | Pipeline diagram, ER diagram, AIA genealogy timeline |
| 2. Philosophy & Ethics of AIAs | Axis 12 (philosophy/ethics) | Critique taxonomy table, alternatives comparison matrix |
| 3. The Bilingual Governance Landscape | Axis 1 (divergence) | Divergence heatmap, fidelity distribution |
| 4. The Accountability Gap | Axis 6 (spotlight) | Sankey: EN accountability -> FR terms |
| 5. Automation as Managerial Rationality | Axis 2 (justification) | Theme distribution, strength by department |
| 6. Risk Construction & Rights | Axis 3 (risk/rights), Axis 10 (quantification) | Radar chart, violin plots of score distributions |
| 7. Safeguard Compliance | Axis 4 (safeguards) | Gap frequency chart, compliance donut |
| 8. Departmental Cultures & Inconsistency | Axis 5 (departments), Axis 9 (inconsistency) | Multi-metric radar, completion rate heatmap |
| 9. Language of Algorithmic Governance | Axis 11 (text analysis) | Word clouds, hedging frequency charts, similarity matrix |
| 10. Cross-Cutting Patterns | Axis 7 (thematic) | Alluvial diagram, treemap |
| 11. Toward a Generalizable Critique | Axis 12.5 (general theory) | Comparative framework table (Canada, EU, NYC) |
| 12. Conclusion | All | Master profile table |

---

## Visualization Toolkit

Recommended tools for producing publication-ready figures:

| Tool | Use case |
|---|---|
| `matplotlib` / `seaborn` | Statistical charts (bar, histogram, box, scatter) |
| `plotly` | Interactive Sankey, treemap, alluvial diagrams |
| `altair` | Declarative statistical visualizations |
| `networkx` | Concept relationship graphs |
| `d3.js` | Interactive web-based visualizations for digital demonstration |

All queries above can be run directly against `psql -d aia_corpus` or exported as CSV for visualization in Python/R.

---

## Data Source

All source data: Government of Canada, [Open Government Licence](https://open.canada.ca/en/open-government-licence-canada).
LLM interpretations: `meta-llama/Llama-3.3-70B-Instruct` via IONOS inference API, prompt version 1.0.0.
