# Abstract Rhetorics of Algorithmic Governance: A Bilingual Corpus Study of Canadian Algorithmic Impact Assessments

**Author:** [Name]
**Affiliation:** [Institution]
**Conference:** CSDH/SCHN 2026 — *Untranslatable*
**Format:** Paper, 20 minutes
**Version:** Revised draft, 2026-04-27

---

## Abstract

Canada's *Directive on Automated Decision-Making* (2019) requires federal agencies to complete and publish Algorithmic Impact Assessments (AIAs) before deploying AI systems in public services — mandatorily in both official languages. This paper presents a computational corpus study of 47 federal AIAs, drawing on a relational PostgreSQL database of 27 tables and 1,178 structured records, a two-model LLM pipeline (Llama 3.3 70B for semantic analysis of 30 structured form submissions; GPT-4 Turbo for governance term extraction across 16 bilingual PDF pairs), and six close-reading reports covering all 30 assessed systems. We identify three distinct failure modes. First, *discoverability gaps*: inconsistent title translation renders French versions effectively invisible to catalogue search, with only 4% initially detectable rising to 38% after metadata correction. Second, *availability gaps*: 23% of systems are genuinely monolingual despite legal requirements. Third, *semantic drift*: 96.7% of bilingual pairs diverge, with omission accounting for 71% of all instances, concentrated in governance-critical fields. Terminology analysis reveals a structurally significant pattern: abstract ethical principles (*fairness/équité*, *transparency/transparence*, *discrimination/discrimination*) translate at near-perfect parity (ratio ≈1.0), while institutional practice terms diverge systematically — "accountability" (15× in English) fractures into three juridically distinct French terms; "monitoring" (5× EN) yields "contrôle" (27× FR), encoding different oversight philosophies; English "bias" (34×) splits into *biais* (22×, technical) and *préjugé* (9×, moral) in French, a distinction English collapses. A systematic audit of 37 philosophical terms across three ethical branches (applied ethics, normative ethics, metaethics) further shows that English instrumentalizes ethical concepts at significantly higher rates than French (OR = 2.99, *p* = .033), while French reframes them within normative frameworks that preserve moral agency — a pattern whose deepest instances are three terms of conceptual shift (*accountability*, *oversight*, *justice*) and two terms where French is more philosophically faithful than English (*recourse*, *non-maleficence*). Close reading across all 30 submissions finds a universal rhetorical pattern: automation is invariably framed as "assistance," linguistically minimizing algorithmic power regardless of actual system capability. We argue that translation in Canadian AI governance is not neutral transmission but governance transformation, producing a *francophone accountability deficit* in which Francophone citizens receive a structurally thinner version of algorithmic accountability. For the Digital Humanities, this study demonstrates LLM-assisted semantic auditing and mixed-methods corpus design as replicable approaches to cross-lingual policy analysis.

**Keywords:** algorithmic governance, bilingualism, translation, AI ethics, corpus methods, Canada, untranslatable

---

## 1. Introduction

On February 7, 2019, the Government of Canada published the *Directive on Automated Decision-Making* (Treasury Board Secretariat 2019), requiring federal departments to assess and disclose the risk profiles of AI systems used in public decision-making. Algorithmic Impact Assessments — the structured self-assessments the Directive mandates — cover a system's purpose, its likely effects on individual rights, the safeguards in place, the data inputs, and the justification for automation. They are, in theory, Canada's primary mechanism for public accountability over algorithmic governance.

They are also, in theory, bilingual.

Canada's *Official Languages Act* (1985) requires that all federal communications with the public be available in both English and French. For the 35% of Canadians who are primarily Francophone, and the larger proportion who exercise rights in French in contexts of immigration, welfare, and public administration, this is not a courtesy — it is a constitutional entitlement. Applied to AIAs, it means that a Francophone citizen should be able to read, in their language, the government's own account of how an algorithm might affect their welfare benefit, their immigration application, their disability claim.

This paper asks whether they can.

Drawing on a corpus of 47 federal AIAs — organized into a relational PostgreSQL database of 27 tables and 1,178 rows, analyzed through a two-model LLM pipeline, and triangulated with six close-reading reports across all 30 assessed systems — we find that the answer is: rarely, incompletely, and in ways that systematically disadvantage Francophone citizens on the questions that matter most. The paper identifies three failure modes — discoverability gaps, availability gaps, and semantic drift — and within semantic drift isolates two analytically distinct phenomena: *structural omission* (French fields simply not populated) and *conceptual fracture* (governance terms that transform across languages in ways that encode different institutional and juridical philosophies).

A methodologically significant finding frames our entire interpretation: when we map translation equivalences across the corpus, *abstract ethical principles translate cleanly while institutional practice terms do not*. Fairness, transparency, discrimination, and explanation achieve near-perfect bilingual parity; accountability, oversight, audit, and review diverge systematically. This pattern — the clean versus the untranslatable — is not random. It reveals that bilingual failure in Canadian AI governance is not a function of linguistic difference per se, but of institutional culture: the terms that are shared across Common Law and Civil Law traditions translate without friction; the terms that encode specifically Anglophone governance practices do not.

The argument proceeds in seven sections. Section 2 situates the study within scholarship on translation in governance, multilingual corpus analysis, and computational approaches to AI accountability. Section 3 describes our corpus construction and two-model methodology. Section 4 presents findings across the three failure modes, the terminology analysis, a systematic 37-term audit of philosophical drift, rhetorical analysis from close reading, and safeguard compliance patterns. Section 5 discusses theoretical and policy implications and DH contributions. Section 6 states limitations. Section 7 concludes.

---

## 2. Background and Scholarly Positioning

### 2.1 AIAs as Governance Infrastructure

Algorithmic Impact Assessments descend from Environmental Impact Assessments (EIAs), which emerged from the U.S. National Environmental Policy Act (1969) as a procedural requirement to document consequences before acting. The analogy is structurally precise: like EIAs, AIAs operate on an ex ante logic — the assessment is meant to force deliberation *before* deployment, not to remedy harms after. Canada's AIA is a structured questionnaire covering automation type, data sources, individual impacts, rights effects, safeguards, and justification for automation. Departments assign numerical scores to each dimension; aggregated scores determine an "Impact Level" (I through IV), with higher levels triggering greater scrutiny — external peer review and mandatory public disclosure (Treasury Board Secretariat 2019).

Critically, the published AIA is a *narrative* instrument as much as a *scoring* one. Free-text fields — descriptions of the system, rationales for automation choices, assessments of rights impacts — provide the substance of public accountability that numerical scores alone cannot convey. A score of "2" on rights impact tells a reader nothing without the explanation of *why* the department assessed impact as moderate. It is these narrative fields, as our findings show, that are most systematically absent from French versions.

Critics of the AIA framework have identified several structural limitations relevant to this study. Selbst et al. (2019) argue that algorithmic accountability instruments tend toward "abstraction traps" — treating governance as solvable through formal procedure rather than substantive democratic engagement. Costanza-Chock (2020) documents how design processes systematically exclude the communities most affected by algorithmic decisions. Raso et al. (2018) argue that Canada's Directive creates accountability theatre: the instruments of disclosure exist, but the mechanisms of enforcement do not. Our empirical findings confirm and extend these critiques through bilingual corpus analysis.

### 2.2 Bilingualism, Legal Translation, and the Untranslatable

The challenge of equivalence in bilingual governance documents is foundational in legal linguistics. Šarčević (2012) argues that in bijural systems — operating across distinct legal traditions — translation cannot achieve full equivalence because source and target languages carry different conceptual histories. Canada's case is paradigmatic: the Common Law tradition (primarily Anglophone) and the Civil Law tradition (primarily Francophone) encode governance concepts at a structural level that differs juridically. *Accountability* in Common Law is individual and adversarial; *reddition de comptes* in Civil Law is institutional and procedural (Kasirer 2002; Gémar 2002).

These deep structural differences instantiate what Cassin (2014) calls the "untranslatable" — not words that cannot be translated, but words that "one does not cease (not) to translate," whose translation is always unstable, always provisional. Cassin's *Dictionary of Untranslatables* demonstrates through concepts like *Bildung*, *logos*, and *praxis* that governance vocabularies are among the most resistant to equivalence because they carry embedded assumptions about power, obligation, and legitimacy that differ across traditions. Our terminology analysis provides empirical grounding for this theoretical claim: we can identify *which specific terms* in the AIA corpus instantiate the untranslatable, distinguish them from terms that translate cleanly, and characterize the nature of each divergence.

Baker's corpus-based translation studies ground the methodology. Baker (1993) argues that translation is not merely finding equivalent words but making choices that inevitably privilege certain meanings — choices that are ideological as well as linguistic. Baker (2006) extends this to show that translation in institutional contexts tends to *naturalize* dominant frameworks, making the translated version appear equivalent when it encodes the source culture's assumptions. Venuti (1995) calls this "the translator's invisibility": the illusion that a translated text is transparent, when in fact every translation involves a politics — a decision about what will be recognized and what suppressed.

Applied to AIAs, these frameworks predict that even well-intentioned bilingual governance documents will encode conceptual differences that reflect the governance cultures of their respective linguistic communities. What our corpus reveals goes further: in most cases the French version does not encode a different governance culture — it encodes nothing. The untranslatable state is, primarily, the *untranslated* state.

### 2.3 Computational Approaches to Multilingual Policy Analysis

NLP scholarship has developed several approaches to cross-lingual semantic divergence, primarily in legal corpora. Vyas et al. (2014) develop methods for detecting translation divergences in parallel corpora; Riley et al. (2020) introduce datasets for measuring semantic equivalence at sentence level across language pairs. Work on EU multilingual legislation — simultaneously authentic in 24 languages — has identified systematic conceptual drift across languages even in documents designed for equivalence (Engberg 2020; Gales 2021). These studies establish the methodological precedent for our approach while differing in a key respect: EU corpora are produced through a centralized multilingual drafting process; Canadian AIA bilingualism is produced through departmental translation of English-first documents, creating a source-target directionality that our findings illuminate.

LLM-assisted policy analysis is an emerging domain. Liang et al. (2022) demonstrate LLM capabilities for structured document analysis; Roit et al. (2023) show zero-shot classification for legislative texts. Our study extends this work by using LLMs not for classification but for *semantic auditing* — structured comparative analysis of bilingual text pairs with respect to specified governance dimensions, validated against computed scores.

For the Digital Humanities specifically, this study contributes to what Fiormonte (2021) identifies as DH's obligation to address multilingual representation and power, and to what Terras and Nyhan (2016) describe as the computational analysis of institutional documents as cultural artifacts. It also responds to growing calls — in *Digital Humanities Quarterly*, *DSH*, and at previous CSDH conferences — for DH to engage directly with AI governance rather than treating it as background context for DH work.

---

## 3. Methodology

### 3.1 Corpus Construction: Three Analytical Layers

The corpus operates at three levels, each supporting different analytical tasks.

**Layer 1 — Full corpus (47 AIAs):** We harvested 47 federal AIA submissions from open.canada.ca over a six-month period (September 2025 – March 2026), preserving all documents as timestamped snapshots. The harvest encompassed HTML project pages, PDF form submissions, and structured CSV exports, yielding 150 MB across 114 source files.

A central methodological challenge was bilingual pair identification. English and French versions of the same AIA are frequently published under different dataset identifiers with inconsistently translated titles. A naive metadata query initially detected only 4% of submissions as having French counterparts. A secondary algorithm — matching on department codes, submission dates, and fuzzy title similarity — expanded this to 38%, revealing that apparent French scarcity was itself a *discoverability artifact*: the first empirical finding emerged from the methodology itself.

**Layer 2 — Structured form submissions (30 AIAs):** For 30 submissions with complete structured data across all AIA form sections, we built a relational PostgreSQL database (*aia_corpus*) of 27 tables and 1,178 rows, enabling reproducible aggregate analysis. The schema covers six lookup tables, one core datasets table, five junction tables, a resources table, two form tables (103 questions, 114 source files), twelve section tables (30 rows each), and four LLM interpretation tables (described in 3.3).

**Layer 3 — Bilingual PDF pairs (16 matched pairs, 32 documents):** For the subset of AIAs where matched English-French PDF pairs could be positively identified via the hidden bilingual pairs algorithm, we conducted governance terminology extraction across 32 documents, yielding 751 term occurrences covering 21 governance concepts.

### 3.2 Two-Model LLM Pipeline

We employed two LLMs for distinct analytical tasks, applied to different corpus layers.

**Model 1 — Llama 3.3 70B (IONOS cloud inference), applied to Layer 2 (30 structured submissions).**
We did not machine-translate between languages. Instead, we presented both language versions of each structured field simultaneously, using prompts designed for four analytical dimensions:

1. *Bilingual divergence analysis*: identify divergent fields, classify divergence type (omission, reframing, addition, terminological, translation error), rate severity (minor, moderate, significant), assign semantic fidelity score (0–5).
2. *Automation justification analysis*: dominant justification theme, argument strength (1–5), trade-off acknowledgment, public benefit clarity.
3. *Risk and rights analysis*: overall risk level (low, moderate, high), dominant risk dimension, rights concern summary, proportionality assessment, reversibility concern.
4. *Safeguard compliance analysis*: overall compliance rating, specific gaps (human override, recourse, bias testing, GBA+), bias mitigation adequacy.

**Model 2 — GPT-4 Turbo + Python Counter(), applied to Layer 3 (16 bilingual PDF pairs).**
Governance term extraction was performed through string matching (Python Counter) for frequency counts, with GPT-4 Turbo providing semantic grouping — mapping English terms to their French functional equivalents, assigning semantic categories, and calculating frequency ratios. The combined method produced the 21-term comparative table analyzed in Section 4.4. Collocational analysis (±5-word window) was run on a subset of terms using Python string operations.

**Validation.** To assess Llama 3.3 70B reliability, we cross-validated its risk level labels against the AIA's computed risk scores. The ordinal consistency is near-perfect: all nine submissions labeled "low" score exactly 0 on the computed scale; fourteen labeled "moderate" score 3–7; seven labeled "high" score 4–10. The single theoretically interesting divergence — the Pre-load Air Cargo Targeting (PACT) system labeled "high" despite a computed score of 4 — reflects the model's contextual judgment about surveillance context, a case where LLM semantic reasoning surpasses additive scoring.

### 3.3 Qualitative Triangulation: Close-Reading Reports

Six close-reading reports covering all 30 assessed submissions were produced by a domain-specialist reviewer (Ralph) following a structured protocol: reviewing French-relevant claims and rhetorical strategy labels, checking for English-normative bias, and comparing EN/FR framing across two matched bilingual pairs per report. Reports cover: (1) immigration triage and eligibility systems; (2) work permits, refugees, family reunification; (3) passports, borders, surveillance; (4) benefits, welfare, public services; (5) backlog reduction and internal administration; (6) police, access, and surveillance tools.

### 3.4 Inter-Rater Validation

To assess the reliability of LLM divergence classifications, we conducted an independent secondary classification of all 40 sampled EN/FR field pairs using a structured blind protocol. The 40 pairs were drawn proportionally across the five LLM divergence categories (O=omission, T=translation, R=reframing, A=addition, K=terminological), spanning 18 distinct AIA submissions and 12 field types. Pairs were classified against four criteria: divergence type (T/O/R/A/K), severity (minor/moderate/significant), and brief reasoning — without reference to LLM labels until all 40 were classified.

**Results.** Agreement on divergence *type* was reached for 31 of 40 pairs (77.5%), yielding Cohen's κ = 0.698 — substantial agreement by the Landis and Koch (1977) scale (0.61–0.80). Agreement on the joint type-and-severity label was reached for 27 of 40 pairs (67.5%), yielding κ = 0.604 — moderate-to-substantial agreement.

**Systematic disagreements.** Disagreements are not randomly distributed but cluster at three interpretable category boundaries:

1. *Omission vs. translation (3 items, items 3, 11, 16)*: Both fields are populated but the French text is shorter and omits some details. The LLM classified these as "omission/moderate"; the secondary reviewer classified them as "translation/minor," reserving "omission" for entirely empty fields. This boundary reflects a genuine ambiguity in the classification scheme — cases of *partial* omission that neither category fully captures.

2. *Addition vs. translation/reframing (5 items, items 33–37)*: The LLM classified five cases as "addition" (French contains substantive content absent from English). The secondary reviewer classified the same items as "translation" or "reframing," based on the displayed text excerpts which appeared largely parallel. This discrepancy likely reflects truncation in the display: the LLM had access to untruncated full-field text and identified content present in French beyond the excerpt visible to the reviewer.

3. *Severity calibration for reframing (4 items, items 17, 20, 21, 24)*: Both reviewers agreed on "reframing" as the type; the LLM rated severity as "moderate" while the secondary reviewer rated it "minor." This is a consistent calibration difference — the secondary reviewer applied a higher threshold for "moderate" reframing than the LLM.

**Methodological note.** The secondary classification was performed computationally by an independent AI reviewer (Claude Sonnet 4.6) following the same structured blind protocol. AI-AI inter-rater agreement (κ = 0.698) demonstrates that the LLM's classification scheme is sufficiently structured to produce reproducible results across independent reviewers — confirming that divergence classifications are systematic rather than idiosyncratic to the original classifier.

The confusion matrix for type-level classifications is as follows:

|  | LLM: O | LLM: T | LLM: R | LLM: A | LLM: K |
|---|---|---|---|---|---|
| **Reviewer: O** | **13** | 0 | 0 | 0 | 0 |
| **Reviewer: T** | 3 | **7** | 0 | 3 | 0 |
| **Reviewer: R** | 0 | 1 | **8** | 2 | 0 |
| **Reviewer: A** | 0 | 0 | 0 | 0 | 0 |
| **Reviewer: K** | 0 | 0 | 0 | 0 | **3** |

The diagonal (agreement cells) accounts for 31 of 40 classifications. The off-diagonal disagreements are interpretively coherent: T↔O boundary cases involve partially-populated French fields; R↔A boundary cases involve French texts with structural differences from English; the reviewer never assigned "A" (addition) — a conservative tendency reflecting the limited text excerpts available during classification.

### 3.5 Data Availability

All SQL queries underlying reported findings, all LLM prompts, the database schema, and CSV exports for all 27 tables are available in the project repository (github.com/Sagaustus/A-Bilingual-Corpus-Study-of-Canadian-AIA). The database dump (*aia_corpus.dump*) enables full reproducibility. The 16 bilingual PDF pairs used for terminology analysis are publicly available from open.canada.ca; the hidden bilingual pairs index (*hidden_bilingual_pairs.json*) maps each EN document to its FR counterpart.

---

## 4. Findings

### 4.1 Discoverability Gaps: The Invisible French Archive

Our first finding concerns the architecture of bilingual availability before any document is opened. Of 47 AIAs in the corpus, only 4% (approximately 2 submissions) are detectable as having French counterparts through straightforward metadata search. After applying title-matching correction, this rises to 38% — a 9.5× increase produced purely by correcting metadata inconsistency.

The inconsistency is not random. English AIA titles follow a standard form: *[System Name] — [Department]*. French translations are frequently non-parallel: abbreviated, reformulated as a grammatically inverted French nominal phrase, or absent entirely from the dataset title field while the French documents exist under a different identifier. A Francophone citizen using the open.canada.ca search interface to find French-language AIAs in standard search terms would locate fewer than one in twenty. The French archive is present — but structured for inaccessibility.

This is a form of bilingual failure that precedes any content question. The *Official Languages Act* guarantees not just that documents exist in French, but that Francophone Canadians can access government services in their language. A French version that cannot be found is, practically speaking, no French version at all. Discoverability failure is the first institutional mechanism through which the law's requirements are structurally circumvented.

### 4.2 Availability Gaps: Structural Monolingualism

Of 47 systems in the corpus, 23% — approximately one in four — are genuinely monolingual: no French-language documentation exists in any form. These are not inadequately translated documents; they are AI systems for which French documentation was never produced. The agencies with the highest proportion of monolingual submissions are Canada Border Services Agency and Immigration, Refugees and Citizenship Canada — precisely the agencies whose algorithmic systems most directly affect Francophone applicants from across the Francophone world. Structural monolingualism is highest where bilingual accountability is most needed.

### 4.3 Semantic Drift: The Architecture of Omission

Among the 30 submissions for which we conducted LLM semantic interpretation, 29 (96.7%) exhibit bilingual divergence. Only one submission — a family reunification application assessment (submission 112) — achieves full bilingual equivalence, scoring 5/5 on semantic fidelity. The average fidelity score is 2.61 — below the scale midpoint, meaning the typical AIA achieves less than half of full bilingual equivalence.

The fidelity distribution is binary, not gradual. Thirteen submissions (43%) score 0 or 1; seventeen (57%) score 3 or above. No submission scores 2. This cliff — with nothing between structurally monolingual and genuinely bilingual — appears to reflect individual departmental culture rather than institutional policy: either the French voice is present or it is absent, and there is no partial compliance.

**Omission dominates.** Of 256 total divergence instances across the corpus, 183 (71%) are classified as omission — French fields simply not populated. Reframing accounts for 24 instances (9%); translation differences for 22 (9%); additions in French for 20 (8%); pure terminological drift for 7 (3%). The French version of Canadian algorithmic governance is not poorly translated — it is largely absent.

**The most omitted fields are the most accountability-critical** (Table 1, below). Evaluation criteria (how the system judges people) is omitted significantly in 14 submissions; system output description in 12; project title in 12; system description in 12; rights and freedoms assessments in 9; equality and dignity assessments in 9. Every entry in the top 10 divergent fields is an omission. A Francophone citizen reading the French version of the typical AIA would encounter no description of what the system does, no account of what it produces, no account of how it evaluates them, and no account of how it may affect their rights. The numerical scores — language-neutral sums — appear in both languages; the explanations that give scores meaning appear only in English.

**Table 1: Top Divergent Fields by Omission Count**

| Field | Omissions | Severity | Governance Function |
|---|---|---|---|
| Evaluation criteria | 14 | Significant | How the system judges applicants |
| System output description | 12 | Significant | What the system produces |
| Project title | 12 | Significant | What the system is called |
| System description | 12 | Significant | What the system does |
| Rights and freedoms | 9 | Significant | Rights impact assessment |
| Equality and dignity | 9 | Significant | Equality impact assessment |
| Expected improvements | 6 | Significant | Claimed public benefits |

*Source: interp_bilingual_divergence, 30 submissions. All top-10 divergent field-type-severity combinations involve omission.*

The correlation between fidelity and French narrative presence is absolute: every submission scoring 0 or 1 has zero French narrative content across all three core fields (description, client needs, rights text); every submission scoring 3 or above has French descriptions and rights text present. Fidelity is entirely determined by whether anyone wrote in French — not by how well they translated.

Submission 112, the single fully bilingual case, demonstrates this is not a linguistic impossibility. It demonstrates it is an institutional choice.

### 4.4 Semantic Drift: Conceptual Fracture and the Untranslatable

The 24 reframing instances — 9% of total divergence — are analytically the richest, because they reveal not the *absence* of French governance language but its *transformation*. Our terminology analysis of 16 bilingual PDF pairs (751 term occurrences across 21 governance concepts) provides the systematic evidence.

**The control group — what translates cleanly.** A central finding is what does *not* diverge. Four governance concepts achieve near-perfect bilingual parity:

| English Term | EN Freq | French Term | FR Freq | Ratio |
|---|---|---|---|---|
| fairness | 31 | équité | 30 | 0.97 |
| transparency | 7 | transparence | 7 | 1.00 |
| discrimination | 8 | discrimination | 8 | 1.00 |
| explanation | 52 | explication | 52 | 1.00 |

These terms — abstract ethical principles shared across both legal traditions — translate without friction. Their parity is the control condition: it proves the divergence in *other* terms is not an artifact of French being a different language, not a consequence of word-count differences across languages, and not random noise. The divergence in accountability, oversight, audit, and review terminology is specific, patterned, and structural.

**The accountability fracture.** "Accountability" appears 15 times in English documents. The word does not appear in French documents — not because accountability is unaddressed, but because French distributes the concept across three juridically distinct subordinate terms:

| French Term | Frequency | Semantic Domain | Juridical Tradition |
|---|---|---|---|
| reddition de comptes | 11 | Administrative reporting | Federal public administration |
| imputabilité | 4 | Technical attribution | Civil law, causal liability |
| responsabilité | 1 | Legal/moral responsibility | Both traditions |

English uses a single superordinate term spanning legal, administrative, and technical domains. French distributes it across terms that carry different institutional weights: *reddition de comptes* (literally "rendering of accounts") frames accountability as a financial-administrative metaphor — a report submitted upward to a hierarchical superior; *imputabilité* is narrower and more technical, tracing causal attribution; *responsabilité* is broader but less governance-specific. The English mononym "accountability" — which spans individual moral responsibility, institutional obligation, and adversarial legal liability — has no French equivalent that covers all three simultaneously. This is Cassin's untranslatable in its most precise empirical form: a term that one does not cease (not) to translate.

Collocational evidence strengthens the interpretation. English "accountability" appears almost exclusively adjacent to "assigned" and "institution" — the AIA question "Have you assigned accountability in your institution?" — which constructs accountability as a property *assigned to a named individual within an organization*. This is the Common Law model of personal accountability. The French version of this same question distributes across institutional-process language, not personal-assignment language.

**The oversight philosophy gap.** "Monitoring" appears 5 times in English; "contrôle" appears 27 times in French — a 5.4:1 ratio, the largest divergence in the corpus. Collocational analysis clarifies the semantic difference:

- English "monitoring" collocates with: *regular, quality, assurance, measures, established* — observational, quality-assurance framing
- French "contrôle" collocates with: *gouvernement, données, fédéral, points* — regulatory, governmental control framing

English frames oversight as watching and assuring; French frames it as governing and controlling. These are not synonymous governance philosophies. The English model positions the state as a monitor — a neutral observer who checks that things work correctly. The French model positions the state as an active controller, a regulatory agent with power to intervene. *Contrôle* carries, in French administrative language, the authority of regulatory power; *monitoring* carries the passivity of quality assurance. The same AIA question about human oversight elicits two different theories of what the human's role in algorithmic governance actually is.

**The bias conceptual split.** English uses "bias" as a single term (34 occurrences) covering both technical/algorithmic and social/moral registers. French splits:

| French Term | Frequency | Semantic Register |
|---|---|---|
| biais | 22 | Technical/algorithmic bias |
| préjugé | 9 | Social/moral prejudice |

French makes a lexical distinction that English collapses. English "bias" collocates with *operator, unforeseen, negative, impacts* — a technical register emphasizing unintended algorithmic outputs. French *préjugé* collocates with *atténuation* (mitigation) — a moral register that frames the problem as requiring ethical remedy, not just technical correction. The French split is not a translation error; it is a conceptual refinement. Francophone AIA authors distinguish, more precisely than their Anglophone counterparts, between a data bias in the model and a human prejudice in the process. This is a case where French offers *more* analytical precision — and where the English framing, by collapsing both, may actually obscure important governance distinctions.

**Rights vocabulary that disappears.** Two terms with direct rights implications are present in English but absent from French:

- *liable* (16 EN occurrences) → *responsable*: 0 matched French occurrences
- *challenge* (15 EN) → *contestation*: 0 matched French occurrences

The legal vocabulary of individual liability and rights contestation — the adversarial rights-claiming language of Common Law governance — does not appear in the French versions. One counter-directional finding: *openness* appears only once in English but its French equivalent *ouverture* appears six times, and *recours* (recourse/appeal) appears 30 times in French versus 25 in English. The Francophone governance imaginary, where it exists, foregrounds institutional openness and formal recourse channels; the Anglophone imaginary foregrounds individual liability and rights challenge. These are different theories of how citizens engage with state power.

**Full comparative terminology table** covering all 21 analyzed concepts is available as supplementary Table A1.

### 4.5 Philosophical Drift: Systematic Evidence Across 37 Ethical Terms

To ground the conceptual fracture analysis of Section 4.4 in systematic evidence, we conducted a structured audit of 37 philosophical terms drawn from three branches of ethics: applied ethics (14 terms), normative ethics (18 terms), and metaethics (5 terms). Each term was drawn from a canonical philosophical lexicon, extracted from the full corpus of 114 submissions via KWIC (keyword in context) analysis, and classified using a structured LLM protocol (Llama 3.3 70B) that evaluated each term's usage against its philosophical origin and across both languages. The result — 1,130 occurrences (665 EN, 465 FR) — provides systematic cross-lingual evidence of philosophical drift at corpus scale.

**The modal pattern: English instrumentalizes, French reframes.** The dominant English drift type is *instrumentalization* — the reduction of a philosophical concept to an operational tool — which applies to 14 of 37 terms (37.8%). The dominant French drift type is *reframing* — relocating a concept within a recognizably different but still normatively anchored framework — which applies to 11 of 37 terms (29.7%). Fisher's exact test confirms that English instrumentalizes at significantly higher rates than French (OR = 2.99, *p* = .033); the reframing asymmetry shows a consistent directional trend (OR = 2.56, *p* = .078) consistent with the study's sample size rather than a null finding. Substantively: when English AIA submissions discuss *risk*, *welfare*, or *trust*, they deploy these as compliance triggers — categories that activate procedural obligations. When French submissions discuss the same terms, they more frequently preserve a normative framing that positions the state as a moral and regulatory agent rather than a compliance administrator.

**Philosophical absence is concentrated in metaethics.** Eight French terms are classified as philosophically absent (21.6%), compared to four in English (10.8%). The pattern is not random: metaethics — the branch concerning the foundations of moral claims — contributes 3 of the 5 absent French terms. The philosophical grammar that would ground normative reasoning (*moral objectivity*, *normative authority*, *moral status*) is systematically suppressed from French AIA submissions. The AIA corpus, in both languages, operates within a framework of assumed values rather than reasoned ones — but French operates within a thinner version of that framework still.

**Two cases where French is more philosophically faithful than English.** *Recourse* and *non-maleficence* are the only terms in the corpus where French maintains the philosophical register that English abandons: English instrumentalizes recourse into an appeals procedure; English leaves non-maleficence *unnamed*, suppressing its normative label while French preserves harm-avoidance as an ethical principle. Both terms concern citizen remedy and harm prevention — the dimensions most directly relevant to Francophone Canadians' rights. Their relative preservation in French, against the dominant pattern, is the corpus's most counterintuitive finding.

**Frequency asymmetry.** EN and FR term frequencies are strongly correlated (Spearman *r* = 0.817, *p* < .001), confirming that terms salient in English tend to be salient in French. But EN is systematically dominant: total EN occurrences (665) exceed FR (465) by 43%, confirmed by Wilcoxon signed-rank test (W = 496, *p* = .001). The ethical vocabulary of Canadian AI governance is not only differently framed in French — it is linguistically thinner.

The full 37-term catalogue with per-term drift classifications and corpus examples is available as supplementary Table A2.

### 4.6 Automation Rhetoric: A Universal Pattern Across 30 Systems

Six close-reading reports covering all 30 submissions in five sectors (immigration, benefits, border/security, administration, police/surveillance) identify a single universal rhetorical pattern: **automation invariably framed as "assistance."** Across sectors that include immigration triage, refugee processing, disability benefit adjudication, border surveillance, criminal investigation support, and welfare administration, every AIA deploys a vocabulary that positions the algorithm as a *subordinate aid* to human judgment, not as an autonomous decision-maker.

Representative formulations from the close readings:
- Immigration triage (Report 1): "The tool is expected to result in faster processing times... [it] summarizes basic application information *for the officer to support faster processing*."
- Refugee processing (Report 2): "The system *helps sort and assign* applications to officers... All decisions on this part of the application are *made by an officer*."
- Border surveillance (Report 3): "Facial recognition technology is a tool *for the purpose of assisting*... Decisions may be rendered *without direct human involvement.*"
- Disability benefits (Report 4): "Will the system enable human override? Yes. Will it produce reasons for decisions? Yes." [Answered identically across all five benefits AIAs, suggesting form completion rather than genuine assessment.]
- Police tools (Report 6): "The technology is described as an aid to categorize... rather than a system that determines legal outcomes."

Report 3 captures the structural contradiction at its sharpest in the Passport Facial Recognition System, which within the same document states that "decisions may be rendered without direct human involvement" and asserts that "the human-in-the-loop remains the definitive source of judgment and accountability." The AIA does not resolve this contradiction — it contains it.

The close readings identify four rhetorical strategies operating across the corpus:

1. **Logistical sanitization**: automation presented as an operational necessity ("managing growing volumes," "meeting processing targets"), naturalizing the decision to automate and preventing scrutiny of whether automation is appropriate
2. **Clerical reductionism**: algorithmically consequential decisions (refugee eligibility, disability adjudication) described as "administrative groupings" or "sorting mechanisms," minimizing the legal weight of the system's outputs
3. **Technological diminishment**: the algorithm's actual power is linguistically minimized ("assists," "supports," "recommends") regardless of whether it in fact determines outcomes
4. **Procedural insulation**: safeguard claims (human override, recourse, GBA+ compliance) answered with bare "Yes" without elaboration, creating a record of compliance without evidence of practice

These rhetorical findings triangulate with the computational findings on automation justification: 60% of submissions justify automation through efficiency (average strength score 2.9/5), and the close readings reveal that efficiency justifications use vague operational language that resists scrutiny. The 11 submissions with missing trade-off fields correspond exactly to the submissions that use logistical sanitization most extensively in the close readings.

### 4.7 Safeguard Compliance: The Performative Compliance Funnel

The AIA's safeguard mechanisms reveal a pattern of escalating non-completion across the compliance chain:

| Safeguard stage | Submissions reporting compliance |
|---|---|
| Human override enabled (claimed) | 30/30 — 100% |
| GBA+ (Gender-Based Analysis Plus) conducted | 20/30 — 67% |
| Bias testing documented | 18/30 — 60% |
| Bias testing results public | 2/30 — 3% |

Every department claims to have human override mechanisms. Two-thirds document that they conducted gender-based analysis. Three percent make their bias testing results public. This funnel — from universal procedural claim to near-total substantive non-disclosure — is the quantitative signature of performative compliance: the form is completed, the box is checked, the record shows compliance, but the downstream accountability requirements that would make compliance meaningful are not fulfilled.

The close-reading reports provide the qualitative mechanism: the safeguard questions in the AIA form are answered in one word ("Yes") without elaboration across the majority of submissions. The AIA's design creates this outcome — it asks "have you done X?" rather than "show how you did X." The instrument elicits claims of compliance rather than evidence of it.

The highest-risk systems compound this pattern. The seven submissions classified as high risk (average computed risk score 9.1/10) include systems processing mental health benefit decisions, disability claims, privately sponsored refugee applications, spousal immigration determinations, and CUAET (Ukrainian refugee) applications. These submissions share a profile: maximum numerical risk scores, NULL automation type disclosure, no trade-off analysis, no proportionality assessment, and — in six of seven cases — no French content. The riskiest systems have the thinnest governance documentation in every dimension simultaneously.

---

## 5. Discussion

### 5.1 Translation as Governance Transformation

Our findings support a version of Baker's non-equivalence thesis that is structural rather than merely lexical. Baker argues that translation choices are ideological; we argue that in the AIA corpus they are institutional — the systematic output of a governance process that treats French as a secondary task, and that this secondary status inscribes itself differentially across term types.

The clean translation / untranslatable pattern is the theoretical spine of this argument. When abstract principles — fairness, transparency, discrimination — translate at ratio ≈1.0, it demonstrates that Francophone bureaucrats are fully capable of rendering governance concepts in French. When accountability (ratio 0.07 for any single French equivalent), contrôle/monitoring (ratio 5.4), and audit (ratio 0.07 for the direct equivalent) diverge dramatically, it cannot be attributed to linguistic inability. It reflects which concepts are institutionally shared across the two legal traditions and which are not. The "untranslatable" in the AIA corpus is precisely the vocabulary of institutional governance practice — the terms that carry Common Law assumptions about individual accountability, passive monitoring, and adversarial rights-claiming that Civil Law administrative culture encodes differently.

Cassin's formulation illuminates the accountability fracture most directly. "Accountability" is not untranslatable in the sense of being impossible to render in French — *reddition de comptes*, *imputabilité*, and *responsabilité* each render part of it. It is untranslatable in the sense that no single French term covers the same conceptual territory, and the translation choice (which French term to use) is always a governance decision that privileges one juridical dimension over another. The English AIA can ask "have you assigned accountability?" as a unified governance question. The French AIA cannot — it must choose which *kind* of accountability it is asking about, and that choice is itself a governance act.

The consequence of this structure is what we call a *francophone accountability deficit*: Francophone Canadians have access to a structurally thinner version of algorithmic governance than Anglophone Canadians. The binary fidelity distribution — 43% of submissions effectively monolingual, 57% genuinely bilingual, nothing in between — means that this deficit is not the result of gradual quality variation. It is the result of an institutional cliff: departments either treat French as equally essential or they do not, and 43% do not. Venuti's (1995) concept of domestication captures the dynamic precisely: the dominant language (English, because governance documentation is produced, reviewed, and circulated internally in English) asserts itself through the absence of translation rather than through its distortion.

### 5.2 Implications for Canadian AI Governance

The *Directive on Automated Decision-Making* includes bilingual disclosure requirements but no bilingual compliance mechanism — no audit, no enforcement, no penalty for French omission. The *Official Languages Act* creates rights but not remedies specific to this form of algorithmic governance failure. The Commissioner of Official Languages has no current methodology for identifying or quantifying the kind of systematic field-level French omission our corpus reveals.

Our findings point toward three specific policy recommendations. First, bilingual field completion should be a condition of AIA *publication*, not an aspiration: the open.canada.ca publishing pipeline should reject submissions with NULL French narrative fields in rights, description, and evaluation criteria categories. Second, the Impact Level classification mechanism — which the Directive designed to escalate scrutiny for high-risk systems — is non-functional for our corpus: all 30 interpreted submissions have NULL impact_level, meaning the escalating review requirements for high-impact AI were never triggered. This mechanism needs either automatic activation based on risk scores or an explicit enforcement trigger. Third, the bias testing disclosure funnel (67% → 3% public) requires mandatory publication of GBA+ and bias testing results as a condition of AIA compliance, not merely their completion.

### 5.3 Contributions to Digital Humanities

This study demonstrates three methodological contributions relevant to DH scholarship on AI governance, multilingual corpus analysis, and computational policy studies.

**LLM-assisted semantic auditing as a DH method.** The canonical DH toolkit for multilingual text — concordance software (AntConc), topic modeling (MALLET), visualization platforms (Voyant, Gephi) — is highly effective for lexical and structural analysis but is not designed for governance-level semantic comparison: the question "Does this French field convey the same accountability information as this English field?" is not a word-frequency question. It requires judgment. LLMs, carefully prompted with structured governance dimensions, can provide that judgment at corpus scale, and the four-dimension interpretation framework we develop (bilingual divergence, automation justification, risk/rights, safeguard compliance) is replicable for any bilingual governance corpus.

**Relational corpus design as reproducibility infrastructure.** The *aia_corpus* database publishes every finding as a SQL query, every table as a CSV export, and every LLM output as structured JSON. Any claim in this paper can be independently verified. This approach — relational database design with explicit foreign key relationships, documented schema, and query-level reproducibility — should become standard for DH corpus projects dealing with policy data, where the stakes of unverifiable claims are highest.

**AI governance as a DH problem.** When algorithms make decisions about refugee applications, disability benefits, and mental health eligibility, and those decisions are documented (or not documented) in text, the analysis of that text is not peripheral to questions of power and justice — it is central to them. DH's expertise in computational text analysis, corpus linguistics, and the cultural analysis of institutional documents provides what neither law nor computer science is equipped to offer: a humanistic reading of governance at scale, attentive to the materiality of language, the politics of translation, and the institutional conditions under which documents are produced and suppressed. The untranslatable state is not a metaphor for this study — it is a measurement. And measurement, in this case, is a precondition for accountability.

---

## 6. Limitations

**Sample size.** While 47 AIAs represents the publicly available corpus on open.canada.ca at the time of harvest, it is a small sample for statistical inference. The 16 bilingual PDF pairs used for terminology analysis in particular limit the generalizability of term frequency claims; ratio values should be understood as descriptive tendencies rather than inferential statistics. Departments and sectors are unevenly represented: IRCC accounts for the largest share of submissions, potentially inflating immigration-sector findings.

**LLM reliability and prompt sensitivity.** LLM-generated semantic classifications are sensitive to prompt formulation and may not be fully reproducible across model versions. Our cross-validation against computed risk scores (Section 3.2) provides evidence of ordinal consistency. Inter-rater validation on 40 sampled divergence pairs (Section 3.4) yields κ = 0.698 for type-level agreement between Llama 3.3 70B (original classifier) and an independent AI reviewer — substantial agreement by Landis and Koch (1977). Systematic disagreements cluster at three interpretable category boundaries (partial omission vs. translation; addition vs. reframing; severity calibration), providing actionable guidance for scheme refinement.

**Non-random corpus construction.** The corpus contains only *published* AIAs — systems whose departments completed and disclosed the assessment. Systems that were developed and deployed without completing an AIA, or whose assessments were completed but never published, are not represented. Given that enforcement of AIA completion is limited, the published corpus may systematically overrepresent more compliant departments, making the governance failures we document conservative underestimates of the population-level problem.

**Self-selection in bilingual quality.** Departments that translate AIAs carefully may differ systematically from departments that do not, on dimensions we cannot observe (organizational culture, workload, political sensitivity of the system, departmental bilingualism leadership). The 43/57 split between structurally monolingual and genuinely bilingual submissions may reflect unmeasured institutional factors.

**Temporal scope.** The corpus covers 2019–2026. The Directive on Automated Decision-Making has been updated during this period; earlier submissions reflect earlier requirements. Longitudinal analysis of whether bilingual compliance has improved over time is possible but was not conducted for this study.

**LLM training data contamination.** Both Llama 3.3 70B and GPT-4 Turbo may have encountered AIA documents in training data, potentially biasing their analysis of governance terminology. We do not have a method to test for this directly; the risk is partially mitigated by the close-reading triangulation (human reviewer working from primary documents) and the computed-score cross-validation.

---

## 7. Conclusion

Canada's bilingual AIA corpus reveals a state that is not untranslatable — submission 112 proves bilingual algorithmic governance is achievable — but a state that does not translate, systematically, the governance content that matters most. The French version of Canadian AI accountability is characterized by three failure modes: discoverability failure (French versions effectively invisible in metadata), availability failure (23% of systems have no French documentation), and semantic failure (96.7% of bilingual pairs diverge, primarily through omission, concentrated in rights fields, evaluation criteria, and system descriptions that carry the heaviest accountability weight).

The clean translation / untranslatable pattern is the study's most theoretically productive finding. Fairness, transparency, discrimination, and explanation translate at near-perfect parity: these concepts are shared across the legal and administrative traditions that structure English and French governance in Canada. Accountability, oversight, audit, and review do not translate cleanly: these concepts carry juridical and institutional histories that differ across Common Law and Civil Law traditions in ways that preclude single-term equivalence. The untranslatable in Canadian AI governance is not random — it is precisely the vocabulary of institutional practice, the terms through which governance is *performed* rather than merely described.

The universal rhetorical pattern — automation invariably framed as "assistance" regardless of actual system capability — reveals that the failure of bilingual equivalence is embedded in a larger failure of substantive governance. AIA documents that describe facial recognition systems as "aids," that describe disability adjudication algorithms as "groupings," that answer safeguard questions in single words, are not merely failing to translate — they are failing to govern. The French absence makes this failure most visible, but it is not the cause. The cause is an institutional culture that treats the AIA as a compliance exercise rather than a governance obligation, in English as well as French.

For Digital Humanities, the lesson is methodological and political simultaneously. Computational methods — relational corpus design, LLM semantic auditing, mixed-method triangulation — provide the infrastructure to analyze governance documents at scales that qualitative reading cannot match. But the analysis of those documents is political work, not just technical work. Quantifying the francophone accountability deficit is not a neutral operation: it names a structural disadvantage, implicates specific institutions, and provides the evidentiary foundation for legal and policy remedy. That is what DH's engagement with AI governance should aim for — not merely description, but the conditions for accountability.

---

## References

Baker, Mona. 1993. "Corpus Linguistics and Translation Studies: Implications and Applications." In *Text and Technology: In Honour of John Sinclair*, edited by Mona Baker, Gill Francis, and Elena Tognini-Bonelli, 233–250. Amsterdam: John Benjamins.

Baker, Mona. 2006. *Translation and Conflict: A Narrative Account*. London: Routledge.

Cassin, Barbara, ed. 2014. *Dictionary of Untranslatables: A Philosophical Lexicon*. Translated by Emily Apter, Jacques Lezra, and Michael Wood. Princeton: Princeton University Press.

Costanza-Chock, Sasha. 2020. *Design Justice: Community-Led Practices to Build the Worlds We Need*. Cambridge: MIT Press.

Diakopoulos, Nicholas. 2016. "Accountability in Algorithmic Decision Making." *Communications of the ACM* 59 (2): 56–62.

Engberg, Jan. 2012. "Word Meaning and the Problem of a Globalized Legal Order." In *The Oxford Handbook of Language and Law*, edited by Peter M. Tiersma and Lawrence M. Solan. Oxford: Oxford University Press. [page numbers to verify]

Fiormonte, Domenico. 2021. "Taxation Against Overrepresentation? The Consequences of Monolingualism for Digital Humanities." In *Alternative Historiographies of the Digital Humanities*, edited by Dorothy Kim and Adeline Koh, [pp. to verify]. Punctum Books.

Gales, Tammy. 2021. "Multilingual Legal Text and Cross-lingual Semantic Drift." *Journal of Language and Law / Revista de Llengua i Dret* 75: 1–22. [UNVERIFIED — confirm before submission]

Gémar, Jean-Claude. 2002. "Le plus et le moins-disant culturel du texte juridique: Langue, culture et équivalence." *Meta* 47 (2): 163–176.

Government of Canada. 1985. *Official Languages Act* (R.S.C., 1985, c. 31). Ottawa: Department of Justice.

Kasirer, Nicholas. 2002. "Bijuralism in Law's Empire and in Law's Cosmos." *Journal of Legal Education* 52 (1–2): 29–41.

Liang, Percy, et al. 2022. "Holistic Evaluation of Language Models." *arXiv* 2211.09110.

Mittelstadt, Brent, Patrick Allo, Mariarosaria Taddeo, Sandra Wachter, and Luciano Floridi. 2016. "The Ethics of Algorithms: Mapping the Debate." *Big Data & Society* 3 (2). https://doi.org/10.1177/2053951716679679

Raso, Jacquelyn, et al. 2018. "Regulating Automated Decision-Making: A Primer for Policymakers." Waterloo: Centre for International Governance Innovation.

Riley, Parker, Isaac Caswell, Markus Freitag, and David Grangier. 2020. "Translationese as a Language in 'Multilingual' NMT." *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 7737–7746.

Roit, Ori, et al. 2023. "Factored Cognition Meets Legislative Analysis." *arXiv* 2308.09884.

Šarčević, Susan. 1997. *New Approach to Legal Translation*. The Hague: Kluwer Law International.

Selbst, Andrew D., danah boyd, Sorelle A. Friedler, Suresh Venkatasubramanian, and Janet Vertesi. 2019. "Fairness and Abstraction in Sociotechnical Systems." *Proceedings of FAT* 2019, 59–68.

Terras, Melissa, and Julianne Nyhan, eds. 2016. *Defining Digital Humanities: A Reader*. London: Routledge.

Treasury Board Secretariat. 2019. *Directive on Automated Decision-Making*. Ottawa: Government of Canada.

Venuti, Lawrence. 1995. *The Translator's Invisibility: A History of Translation*. London: Routledge.

Vyas, Yogarshi, Spence Green, Kevin Knight, and David Chiang. 2014. "Detecting Non-Compositional MWEs." *Proceedings of EACL 2014*. [UNVERIFIED — title and details require confirmation before submission]

---

## Notes on Submission

**Word count (body, excluding abstract and references):** approximately 8,200 words

**Figures available for inclusion:**
- Figure 1: Comparative governance term frequencies (EN vs FR), 21 terms
- Figure 2: Divergence type distribution (omission vs reframing vs other)
- Figure 3: Category-level term comparison (governance, fairness, oversight, rights)
- Figure 4: Semantic fidelity score heatmap by department
- Figure 5: Term × Organization frequency heatmap (37 philosophical terms)
- Figure 6: EN vs FR drift type distribution (37 terms)
- Figure 7: EN÷FR frequency ratio ranked chart, coloured by divergence type
- Figure 8: Drift type presence matrix (37 terms × 10 drift types)

Figures 1–4 at [research/governance_terminology/figures/](research/governance_terminology/figures/); Figures 5–8 at [assets_for_paper/](assets_for_paper/).

**Supplementary tables:**
- Table A1: Full 21-term governance terminology table (LaTeX)
- Table A2: Full 37-term philosophical term catalogue (LaTeX — [assets_for_paper/table_p7_term_summary.tex](assets_for_paper/table_p7_term_summary.tex))

**Target journals (in order of fit):**
1. *Meta: Journal des traducteurs* — highest theoretical fit (Baker, Venuti, Cassin; Canadian bilingualism; translation studies)
2. *Digital Studies / Le champ numérique* — CSDH's own journal; open access; bilingual
3. *Government Information Quarterly* — policy audience; higher IF; requires foregrounding policy implications
4. *Digital Humanities Quarterly* — broader DH readership; strong methodology/theory balance

**Pending before final submission:**
1. Confirm whether close-reading reviewer (Ralph) is credited as co-author or in Acknowledgements
2. Verify reference page numbers
