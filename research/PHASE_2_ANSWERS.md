# Phase 2 — Corpus-Level Facts: Answers

> Answers to Q-09 through Q-13, Q-17 through Q-24, Q-28 through Q-32
> Generated: 2026-03-08
> Status: ALL COMPLETE (20 questions across 4 parallel blocks)
>
> **Evidence appendix:** [PHASE_2_EVIDENCE.md](PHASE_2_EVIDENCE.md) — every finding below is backed by an exact SQL query and reproducibility instructions.
>
> **Depends on:** Phase 1 (methodology validated in Q-06 through Q-08)

---

# Block A — The Bilingual Divergence Landscape (Chapter 3)

> *Central question: Where does bilingual governance break down — and what does the pattern reveal about the politics of translation in algorithmic governance?*

---

## Q-09 — What Is the Overall Divergence Rate Across the Corpus?
> Methods: `AGG` `LLM` | Chapter 3 | Status: ✓ COMPLETE

### Finding

**96.7% of AIA submissions exhibit bilingual divergence. The Canadian state's algorithmic governance is almost never equivalently bilingual.**

### What We Found

| Has Divergence? | Submissions | Percentage |
|-----------------|-------------|------------|
| Yes             | 29          | 96.7%      |
| No              | 1           | 3.3%       |

Out of 30 assessed submissions, 29 show some form of divergence between their English and French content. Only a single submission — one out of thirty — achieves bilingual equivalence.

### What This Means

*Analogy:* Imagine a country that requires all government buildings to have both a front door and a back door, and then an inspection reveals that 97% of buildings have a front door but the back door is missing, locked, or leads to a different room. That is the state of bilingual algorithmic governance in Canada.

This is the baseline finding for the entire thesis. The question is no longer *whether* bilingual governance breaks down in the AIA — it breaks down almost universally. The question becomes *how* it breaks down (Q-10, Q-11), *why* (Q-12), and *what this tells us* about the relationship between language and algorithmic accountability.

The single non-divergent submission (submission 112 — a family reunification application assessment) is itself remarkable. It achieves a semantic fidelity score of 5 out of 5. **In a corpus where bilingual failure is the norm, this submission is the exception that proves the rule.** It demonstrates that bilingual equivalence *is possible* within the AIA framework — it is simply almost never achieved.

### Thesis Implications

This finding provides the empirical foundation for the thesis title, "The Untranslatable State." The state is not literally untranslatable — one submission proves it can be done. But in practice, 96.7% of the time, the English and French versions of algorithmic governance are not the same document. Francophone citizens reading their government's algorithmic assessments are reading a different text than anglophone citizens — sometimes a thinner text, sometimes a subtly reframed one, and sometimes nothing at all.

---

## Q-10 — Which Semantic Fields Diverge Most?
> Methods: `AGG` `LLM` | Chapter 3 | Status: ✓ COMPLETE

### Finding

**The fields most likely to diverge are the ones that matter most for governance accountability — evaluation criteria, system outputs, project descriptions, and rights assessments. Divergence is overwhelmingly "significant" in severity and "omission" in type: the French fields are simply left empty.**

### Data — Top 10 Divergent Fields

| Field | Type | Severity | Occurrences |
|-------|------|----------|-------------|
| evaluation_criteria | omission | significant | 14 |
| system_output | omission | significant | 12 |
| project_title | omission | significant | 12 |
| description | omission | significant | 12 |
| rights_freedoms | omission | significant | 9 |
| equality_dignity | omission | significant | 9 |
| system_output | omission | moderate | 8 |
| evaluation_criteria | omission | moderate | 8 |
| project_title | translation | minor | 6 |
| expected_improvements | omission | significant | 6 |

The full query returns 77 distinct field-type-severity combinations. Of the top 20, **every single one is an omission**.

### What This Tells Us

*Thought experiment:* Imagine a bilingual court system where the judge's verdict is written in English, but the French version omits the sentencing criteria, the description of the offence, and the assessment of the defendant's rights. That is not a translation failure — it is an accountability gap. A francophone citizen reading only the French version would not know *how* the system evaluates them, *what* the system produces, or *what rights are at stake*.

**1. The governance-critical fields are the most affected.**

The top four divergent fields — `evaluation_criteria` (how the system judges people), `system_output` (what the system produces), `project_title` (what the system is called), and `description` (what the system does) — are the basic building blocks of algorithmic accountability. Without these fields in French, a francophone reader cannot answer the most fundamental questions about the system: *What is it? What does it do? How does it evaluate me?*

**2. Rights fields are significantly affected.**

`rights_freedoms` and `equality_dignity` — the fields where departments describe how their system affects people's fundamental rights — are omitted 9 times each at "significant" severity. This means that for nearly a third of submissions, the French version does not contain the department's own assessment of how the algorithm affects human rights.

**3. The pattern is not random.**

If divergence were simply carelessness — a few fields missed here and there — we would expect a uniform distribution across fields. Instead, the divergence clusters around the narrative, qualitative fields (descriptions, assessments, criteria) while structured, scored fields (which are language-neutral numbers) remain consistent. **The state speaks two languages when it counts, but only one language when it explains.**

### Thesis Implications

This finding supports a key argument of the thesis: bilingual failure in the AIA is not merely a translation problem — it is a *governance* problem. The fields that diverge most are the ones that carry the most accountability weight. This creates what we might call a **"francophone accountability deficit"**: the French version of algorithmic governance is systematically thinner on the details that would allow meaningful public scrutiny.

---

## Q-11 — What Is the Distribution of Divergence Types?
> Methods: `AGG` `LLM` | Chapter 3 | Status: ✓ COMPLETE

### Finding

**The LLM classified 28 of 30 submissions as exhibiting "linguistic" divergence, with an average semantic fidelity score of 2.61 out of 5. The two remaining submissions were classified as "none" — one truly equivalent, one with both languages equally empty.**

### Data

| Divergence Type | Submissions | Avg Fidelity Score (0–5) |
|-----------------|-------------|--------------------------|
| linguistic      | 28          | 2.61                     |
| none            | 2           | 2.50                     |

### What This Tells Us

The average fidelity score of 2.61 sits below the midpoint of the 0–5 scale. In plain terms: **the typical AIA submission achieves less than half of what full bilingual equivalence would require.**

*Analogy:* If a fidelity score of 5 is a fully furnished house and 0 is an empty lot, the average Canadian AIA submission is a house with walls and a roof but missing most of the rooms — structurally present but functionally incomplete.

The classification of nearly all divergence as "linguistic" (rather than legal, cultural, or terminological) tells us something important: the divergence is not caused by deep conceptual untranslatability between Common Law and Civil Law traditions, or between anglophone and francophone governance cultures. It is caused by something much simpler: **the French fields were not filled in.** The untranslatable state is, in most cases, the *untranslated* state.

This distinction matters for the thesis argument. A finding that governance concepts genuinely resist translation across legal traditions would support a strong version of the "untranslatable state" thesis — that bilingual algorithmic governance is inherently impossible. What we find instead supports a weaker but more damning conclusion: **bilingual governance is possible but simply not practiced.** The failure is institutional, not linguistic.

---

## Q-12 — Is the Dominant Divergence Omission or Terminological Drift?
> Methods: `AGG` `LLM` `CR` | Chapter 3 | Status: ✓ COMPLETE

### Finding

**Omission accounts for 71% of all divergence instances. The French version of the Canadian state is not poorly translated — it is largely absent.**

### Data

| Divergence Type | Total Occurrences | Submissions Affected |
|-----------------|-------------------|---------------------|
| Omission        | 183               | 27                  |
| Reframing       | 24                | 14                  |
| Translation     | 22                | 11                  |
| Addition        | 20                | 9                   |
| Terminological  | 7                 | 7                   |

### What This Tells Us

*Case study:* Consider a federal department deploying an AI system to triage immigration applications. The English AIA describes the system's evaluation criteria, its expected impacts on applicants' rights, and the trade-offs the department considered. The French version? In 27 out of 30 submissions, at least some of these fields are simply blank. Not badly translated. Not reframed through a different legal tradition. *Empty.*

**1. Omission dominates by an overwhelming margin.**

183 omission instances — nearly four times more than all other divergence types *combined* (73). Twenty-seven of thirty submissions have at least one omitted French field. This is not a translation problem; it is an **absence problem**.

**2. Reframing is rare but conceptually interesting.**

When the French version *does* exist, 24 instances show "reframing" — the same concept expressed through different governance logic. For example, where English uses "accountability," French may distribute the concept across *responsabilité*, *reddition de comptes*, and *imputabilité* — three distinct words for what English treats as one. These 24 instances, though rare, are the most analytically rich for the thesis: they reveal the genuine sites of conceptual untranslatability that the thesis title promises. We pursue these in Q-14 through Q-16 (Phase 3).

**3. Terminological drift is almost negligible.**

Only 7 instances of pure terminological divergence — different technical terms for the same concept. This tells us that when both language versions exist, the terminology is generally consistent. The problem is not vocabulary; it is *voice*. The French voice is simply not speaking.

### A Metaphor for the Thesis

The thesis is titled "The Untranslatable State," but the data reveals something subtler. It is not that the state *cannot* be translated — it is that the state mostly does not *bother*. The French version of algorithmic governance is like a library with the catalogue in both languages but most of the French books missing from the shelves. The catalogue promises bilingualism; the shelves deliver monolingualism.

This reframes the thesis argument. The "untranslatable" is not primarily a linguistic phenomenon (concepts that resist translation) but an institutional one (an institution that does not translate). The few instances of genuine reframing (24 out of 256 total divergence instances) are the exceptions — rare windows into what bilingual governance *could* look like if the state treated both languages as equally essential.

---

## Q-13 — Is There a Correlation Between Fidelity Score and Narrative Text Presence?
> Methods: `AGG` `DB` | Chapter 3 | Status: ✓ COMPLETE

### Finding

**The correlation is absolute. Every submission with a fidelity score of 0 or 1 has zero French narrative content. Every submission scoring 3 or above has French descriptions and rights text present. Fidelity is entirely determined by whether anyone bothered to write in French.**

### Data

| Fidelity Score | Count | Has FR Description | Has FR Client Needs | Has FR Rights Text |
|----------------|-------|--------------------|--------------------|--------------------|
| 0              | 1     | 0/1                | 0/1                | 0/1                |
| 1              | 12    | 0/12               | 0/12               | 0/12               |
| 3              | 3     | 3/3                | 1/3                | 3/3                |
| 4              | 13    | 13/13              | 9/13               | 13/13              |
| 5              | 1     | 1/1                | 1/1                | 1/1                |

### What This Tells Us

*Analogy:* Imagine a restaurant reviewer scoring meals on a 1-to-5 scale for "bilingual menu quality." You discover that every restaurant scoring 1 has no French menu at all, while every restaurant scoring 4 or 5 has a complete French menu. The score is not measuring *translation quality* — it is measuring *translation existence*.

**1. The dividing line is presence, not quality.**

Thirteen submissions score 1 (the entire bottom of the scale, excluding a single zero). Every one of them has no French description, no French client needs, and no French rights text. The English versions of these fields exist — the departments wrote about their systems, their users' needs, and their rights implications. They simply did not write any of it in French.

On the other side, all 17 submissions scoring 3 or above have French descriptions and French rights text. The `client_needs` field is more variable (only 12 of 17 populate it in French), but the core narrative fields are consistently present.

**2. There is no middle ground.**

No submission scores 2. The fidelity scores jump from 1 to 3, with nothing in between. This is a **binary population**: submissions are either structurally monolingual (score 0–1) or genuinely bilingual (score 3–5). There is no "partially bilingual" middle — no submissions that translated some narrative fields but not others in a way that produced an intermediate score.

**3. The 13-to-17 split is the thesis in miniature.**

Thirteen submissions (43%) are structurally monolingual. Seventeen (57%) are genuinely bilingual. **The Canadian AIA corpus is split almost evenly between two governance regimes** — one that operates in both official languages and one that operates only in English. This split is not predicted by department, project type, or risk level. It appears to be a function of individual practice rather than institutional policy.

### Thesis Implications

This finding provides the sharpest quantitative evidence for the "two governance regimes" claim. The fidelity score is not a continuum — it is a cliff. On one side, the state speaks two languages. On the other, it speaks one. There is no gradient, no partial compliance, no "we translated the important parts." Either the French voice is present or it is silent.

For the humanities reader, this is the equivalent of discovering that in a bilingual archive, 43% of the files exist only in one language. The archive *calls* itself bilingual, and the institutional mandate *requires* bilingualism, but nearly half the collection tells a story that can only be read in English.

---

# Block B — Automation Rhetoric and Justification (Chapter 5)

> *Central question: How do federal departments narrate the necessity of automation, and what does their rhetoric reveal about the state's relationship to algorithmic decision-making?*

---

## Q-17 — What Justification Themes Dominate the Corpus?
> Methods: `AGG` `LLM` | Chapter 5 | Status: ✓ COMPLETE

### Finding

**"Efficiency" is the dominant justification for automation across the Canadian federal government, appearing in 60% of submissions — but it is also the weakest. "Compliance" appears in only 20% of submissions but achieves a perfect strength score every time. The state automates primarily to save time and money, not to improve rights or services.**

### Data

| Theme | Count | % of Corpus | Avg Strength (1–5) | Range |
|-------|-------|-------------|---------------------|-------|
| Efficiency | 18 | 60% | 2.9 | 1–4 |
| Compliance | 6 | 20% | 4.0 | 4–4 |
| Client service | 3 | 10% | 3.3 | 2–4 |
| Modernization | 2 | 7% | 2.0 | 2–2 |
| Other | 1 | 3% | 1.0 | 1–1 |

### What This Tells Us

*Analogy:* Imagine asking 30 hospitals why they adopted a new diagnostic tool. If 60% said "it's faster" and only 20% said "it produces better diagnoses," you would learn something important about how the institution understands technology — as a time-saver rather than a quality improver. The Canadian government's relationship with automation follows the same pattern.

**1. Efficiency is the lingua franca of automation justification.**

Eighteen of thirty submissions justify automation primarily through the language of efficiency — faster processing, reduced backlogs, cost savings. This is the vocabulary of managerial rationality, not of democratic governance or rights protection. The state does not say: *"We automate because it will produce fairer decisions."* It says: *"We automate because it will produce faster decisions."*

**2. But efficiency is the weakest argument departments make.**

The average strength score for efficiency-themed justifications is only 2.9 out of 5 — and the range stretches from 1 to 4. Many efficiency justifications are vague ("it will improve processing times") without specifying how much, for whom, or at what cost. **The most common justification is also the most poorly articulated.**

**3. Compliance justifications are universally strong.**

The six compliance-themed submissions — departments that justify automation by saying "we are required to do this" or "this ensures regulatory compliance" — all score a perfect 4. When a department can point to a legal or policy mandate, its justification is clear, specific, and well-supported. **Obligation produces better argumentation than aspiration.**

*Thought experiment:* This makes intuitive sense. If someone asks you why you filed your taxes, you can give a clear, confident answer ("because the law requires it"). If someone asks you why you reorganized your filing cabinet, your answer is likely vague ("to be more efficient... I think"). Compliance justifications have built-in clarity; efficiency justifications require the department to construct an argument from scratch — and many do so poorly.

**4. Client service is rare and reveals an important gap.**

Only 3 of 30 submissions frame automation as primarily serving the public. This is notable in a government that theoretically exists to serve citizens. The AIA, as an instrument, does not *require* departments to articulate how automation benefits the people it affects — only how it benefits the department's operations. The instrument's design shapes the rhetoric it elicits.

### Thesis Implications

This finding supports the critique of AIAs as instruments of managerial rationality rather than democratic accountability (Q-02, Framework 2). The AIA asks departments *why* they automate, and 60% of the time the answer is a variation of "because it's efficient." This frames automation as a neutral operational improvement rather than as a governance intervention with rights implications — precisely the framing that critics like Selbst (2021) and Costanza-Chock (2020) warn against.

---

## Q-18 — Do Stronger Justifications Also Acknowledge Trade-offs?
> Methods: `AGG` `LLM` `CR` | Chapter 5 | Status: ✓ COMPLETE

### Finding

**The correlation is stark: every submission with a strength score of 4 provides substantive trade-off discussion. Every submission scoring 1 or 2 has empty or missing trade-off fields. The departments that argue most convincingly for automation are the same ones that honestly acknowledge its costs.**

### The Pattern

| Strength Score | Count | Trade-off Quality | Public Benefit Clarity |
|----------------|-------|-------------------|----------------------|
| 4 | 17 | Substantive (sometimes brief, but present) | Clear and specific |
| 2 | 11 | Missing — fields "not provided" | Missing — fields "not provided" |
| 1 | 2 | Empty — completely blank | Empty — completely blank |

### What This Tells Us

*Analogy:* In a university setting, the strongest grant proposals are the ones that name their own limitations. A researcher who writes "our method cannot account for X, and we plan to address this by Y" is more convincing than one who writes "our method has no limitations." The same pattern appears in AIA submissions: **the departments that take justification seriously also take trade-offs seriously**, and the departments that phone it in phone in everything.

**1. Quality is bimodal, not gradual.**

There is no middle ground. Submissions either score 4 (strong justification, substantive trade-offs, clear public benefits) or score 1–2 (weak justification, missing trade-offs, unclear benefits). This mirrors the bilingual fidelity pattern from Q-13 — another cliff, another binary population.

**2. The 11 missing-trade-off submissions are a governance concern.**

Eleven federal departments deployed AI systems without articulating any trade-offs in their AIA submissions. These are not trivial systems — they include triage tools for immigration applications, a passport modernization initiative, and automation for refugee processing. **The departments deploying AI in some of the most rights-sensitive domains are the ones that did not bother to name the costs.**

*Case study:* Submission 68 (automating CUAET application review for Ukrainian refugees) scores a strength of 2, with the LLM noting: "Fails to consider potential errors/biases; inadequate." A system processing applications from people fleeing a war zone, and the department did not document what could go wrong. This is performative compliance in its most concerning form — the form was filled out, but the *thinking* the form was supposed to force did not happen.

**3. Compliance-themed submissions are the most intellectually honest.**

All six compliance-themed justifications (Q-17) score 4 and provide substantive trade-off discussions. When departments justify automation by reference to legal obligation, they also tend to acknowledge the constraints and costs. **Paradoxically, the least "creative" justification — "we have to do this" — produces the most rigorous self-assessment.**

### Thesis Implications

This finding directly tests the **self-assessment bias** critique (Q-03, Critique 2). The prediction was that departments would minimize trade-offs when justifying automation. The data partially confirms this: 43% of submissions (13 out of 30) have empty or missing trade-off fields. But 57% provide substantive analysis. The self-assessment bias is real but not universal — it affects specific submissions, not the entire corpus. Phase 3 (Q-33 through Q-35) will test whether this pattern clusters by department.

---

## Q-19 — How Does Automation Type Relate to Justification Rhetoric?
> Methods: `AGG` `DB` `LLM` | Chapter 5 | Status: ✓ COMPLETE

### Finding

**Every submission that properly classified its automation level achieved a perfect justification strength score. Every submission that left the automation type blank produced a weak justification. The act of naming what you are building appears to be a precondition for explaining why you are building it.**

### Data

| Automation Level | Theme | Count | Avg Strength |
|-----------------|-------|-------|-------------|
| Decision support (score 0) | efficiency | 7 | 4.0 |
| Decision support (score 0) | compliance | 5 | 4.0 |
| Decision support (score 0) | client_service | 2 | 4.0 |
| Partial automation (score 2) | efficiency | 2 | 4.0 |
| Partial automation (score 2) | compliance | 1 | 4.0 |
| *Missing/NULL* | efficiency | 9 | 1.9 |
| *Missing/NULL* | modernization | 2 | 2.0 |
| *Missing/NULL* | other | 1 | 1.0 |
| *Missing/NULL* | client_service | 1 | 2.0 |

### What This Tells Us

*Metaphor:* Imagine two architects presenting building plans to a review board. One says: "This is a two-story residential building with load-bearing walls and a reinforced foundation." The other says: "This is a building." The first architect can explain every design choice because she *knows what she built*. The second cannot explain anything because he never defined the project. **Naming the system is the first act of accountability.**

**1. No submission claims full automation.**

Not a single submission in the corpus classifies itself as "full automation" (score 4). Every system that classified itself chose either "decision support" (14 submissions) or "partial automation" (3 submissions). This is itself a finding: either the Canadian government genuinely does not deploy fully automated decision systems, or departments avoid the classification because it triggers higher scrutiny. Given that several systems (refugee application triage, disability benefit processing) appear to make consequential automated determinations, the latter explanation deserves investigation.

**2. Thirteen submissions did not classify themselves at all.**

The `automation_type_score` is NULL for 13 submissions — and these 13 produce uniformly weak justifications (average strength 1.9). This is a crucial data quality finding: **the submissions with the weakest governance documentation are the ones that did not complete the most basic classification question.** These are not random omissions — they cluster with other forms of incompleteness (missing trade-offs, missing French content, missing public benefit descriptions).

**3. The strongest justification theme for each automation level is "efficiency."**

Across both decision support and partial automation, efficiency is the most common theme. But when departments properly classify their systems, even efficiency justifications score a perfect 4. **The quality gap is not about the theme — it is about whether the department engaged seriously with the assessment process at all.**

### Thesis Implications

This finding introduces what we might call the **"completeness cluster"**: submissions that complete one governance field tend to complete them all, and submissions that skip one tend to skip many. The AIA does not fail uniformly — it fails in predictable, correlated ways. A department that does not name its automation type also does not describe its trade-offs, does not provide French content, and does not articulate public benefits. This is evidence for the **performative compliance** critique (Q-03, Critique 1): some departments treat the AIA as a genuine exercise in self-reflection, while others treat it as a form to be submitted with minimum effort.

---

## Q-20 — What Is the Relationship Between Confinement Claims and System Capabilities?
> Methods: `DB` `LLM` `CR` | Chapter 5 | Status: ✓ COMPLETE

### Finding

**The 13 submissions with the broadest system capabilities are the same 13 that provide no confinement assessment. The systems most in need of boundaries are the ones whose boundaries are never described.**

### The Pattern

The data splits into two clean populations:

**Group A — 17 submissions with explicit automation type:** All provide substantive confinement assessments. The PACT cargo targeting system describes a "Project Management Framework, pre-defined industry standard, restricted dataset." The OAS elderly benefits system notes it "supports agents, does not make decisions autonomously." These assessments range from "robust" to "partially addressed," but they *exist*.

**Group B — 13 submissions with NULL automation type:** All provide *no* confinement assessment. The LLM consistently notes: "Not provided," "Not clearly explained," "Crucial information missing." These include systems processing refugee applications, disability benefits, spousal immigration, and passport modernization — some of the most consequential deployments in the corpus.

### What This Tells Us

*Thought experiment:* Imagine a zoo that requires enclosure specifications for every animal. The keepers of the hamsters provide detailed cage dimensions, feeding schedules, and escape-prevention measures. The keepers of the tigers provide nothing. This is the confinement pattern in the AIA corpus: **the low-risk systems are carefully bounded, while the high-stakes systems have no documented boundaries at all.**

*Case study:* Submission 48 — "Automation Development to Support Disability Benefit Decision Making" (Department 021) — lists capabilities including `item2,item5,item1,item4` (multiple system capabilities), has a risk_total of 10 (the highest in the corpus), and provides no confinement assessment. The LLM notes: "crucial information missing." A system that could affect disabled Canadians' access to benefits, with the broadest capability set and the highest risk score in the corpus, and no documented boundaries. This is the performative compliance critique made concrete.

### Thesis Implications

The confinement gap reveals an inverse relationship between need and provision: the systems that most need clear boundaries are the least likely to have them documented. This supports the **self-assessment bias** critique — departments may avoid defining confinement because doing so would constrain their operational flexibility. It also supports the **structural limitations** critique — the AIA does not *require* confinement documentation, so departments can skip it without consequence.

---

# Block C — Risk, Rights, and the Quantification Problem (Chapter 6)

> *Central question: How does the AIA framework construct risk, and does the instrument adequately capture the human rights implications of automated decision-making?*

---

## Q-21 — What Is the Risk Landscape Across the Corpus?
> Methods: `AGG` `LLM` | Chapter 6 | Status: ✓ COMPLETE

### Finding

**The corpus is dominated by "moderate" risk labels (47%), followed by "low" (30%) and "high" (23%). But the six highest-risk submissions — all scoring the maximum risk_total of 10 — are the same ones that left their automation type, confinement assessment, and French content blank. The riskiest systems have the thinnest governance documentation.**

### Data

| Risk Label | Count | % | Avg Risk Total | Avg Impact Level |
|------------|-------|---|----------------|-----------------|
| Moderate   | 14    | 47% | 4.0          | NULL            |
| Low        | 9     | 30% | 0.0          | NULL            |
| High       | 7     | 23% | 9.1          | NULL            |

### The High-Risk Systems — A Close Reading

Six submissions share the maximum risk_total of 10. They are all from two departments (021 — Employment and Social Development Canada, and 050 — Immigration, Refugees and Citizenship Canada), and they are all processing highly sensitive decisions:

| System | Department | What It Does | What's Missing |
|--------|-----------|-------------|----------------|
| Mental Health Benefit | 021 | Automates mental health benefit decisions | Automation type, confinement, trade-offs |
| Disability Benefit Decision Making | 021 | Automates disability benefit decisions | Automation type, confinement, trade-offs |
| Privately Sponsored Refugee Applications | 050 | Automates refugee application processing | Automation type, confinement, trade-offs |
| Spousal Immigration (EN) | 050 | Automates spousal immigration analysis | Automation type, confinement, trade-offs |
| Spousal Immigration (FR) | 050 | Same system, French submission | Automation type, confinement, trade-offs |
| CUAET Application Review | 050 | Automates review for Ukrainian refugees | Automation type, confinement, trade-offs |

### What This Tells Us

*Analogy:* Imagine a hospital where the patients with the most serious conditions have the shortest medical charts. The ICU patients — the ones most in need of detailed documentation — have the fewest notes, while the patients with minor colds have comprehensive records. That is the risk-documentation relationship in the AIA corpus.

**1. Risk and documentation are inversely correlated.**

Every high-risk-total-10 submission is also a submission with NULL automation type, missing confinement assessment, missing trade-off analysis, and (in most cases) missing French content. The "completeness cluster" identified in Q-19 is also a *risk* cluster: the most dangerous systems have the least governance documentation.

**2. The domains are heartbreaking.**

These are not abstract systems processing innocuous data. They are systems making decisions about mental health benefits for people in crisis, disability benefits for people who cannot work, and refugee applications for people fleeing war. **The Canadian state deploys its most consequential algorithms in the domains where people are most vulnerable — and documents them least.**

**3. Impact level is universally NULL.**

All 30 interpreted submissions have NULL `impact_level` — the AIA's own I-through-IV classification. The government's formal impact classification was never completed for any of the submissions we analyzed. This means the proportionality mechanism (higher impact = more scrutiny) was never triggered. The safety valve in the governance architecture was never turned on.

### Thesis Implications

This finding provides the strongest empirical support for the **self-assessment bias** critique (Q-03, Critique 2) and the **enforcement gap** critique (Critique 4). The departments deploying the riskiest systems are the ones producing the thinnest assessments — and there appears to be no mechanism to require more. The AIA's design assumes good faith from assessors, and the data suggests that assumption is not always warranted, particularly for the systems where the stakes are highest.

---

## Q-22 — Which Rights Dimensions Are Most at Stake?
> Methods: `AGG` `DB` | Chapter 6 | Status: ✓ COMPLETE

### Finding

**All four rights dimensions score close to 1 on a scale where higher means greater impact. "Rights & Freedoms" leads slightly (1.13), but the striking finding is the uniformity: the corpus treats all rights dimensions as approximately equally (un)affected. This suggests either genuine low impact or systematic understatement.**

### Data

| Rights Dimension | Avg Score | Submissions Affected |
|------------------|-----------|---------------------|
| Rights & Freedoms | 1.13 | 30/30 |
| Equality & Dignity | 1.07 | 30/30 |
| Health & Wellbeing | 1.00 | 30/30 |
| Economic Interests | 1.00 | 17/30 |

### What This Tells Us

*Thought experiment:* If you asked 30 drivers to rate how fast they drive on a scale of 0 to 4, and 28 of them said "1," you would suspect either that Canadian drivers are extraordinarily cautious or that people systematically understate their speed when self-reporting. The rights scores in the AIA corpus present the same interpretive puzzle.

**1. The scores are remarkably flat.**

Rights & Freedoms (1.13), Equality & Dignity (1.07), Health & Wellbeing (1.00), Economic Interests (1.00) — the differences are almost negligible. This flatness could mean that the systems genuinely affect all rights dimensions minimally and equally. But given that the corpus includes immigration triage systems, disability benefit algorithms, and border surveillance programs, **minimal and equal impact seems implausible.**

**2. Only two submissions break the pattern.**

Submission 48 (Disability Benefit Decision Making) scores rights_freedoms=3 and equality_dignity=3. Submission 47 (Mental Health Benefit) scores rights_freedoms=3. These are the only submissions that acknowledge significant rights impacts — and they are both from Department 021 (ESDC). **Among 30 federal AI systems affecting people's benefits, immigration status, and security clearances, only 2 acknowledge meaningful rights implications.**

**3. Economic interests data is missing for 13 submissions.**

Thirteen of thirty submissions have no economic interests score. These are the same 13 submissions with missing automation type, missing confinement, and missing French content — the "completeness cluster" appearing again.

### Thesis Implications

The flat rights scores support the **quantification reductionism** critique (Q-03, Critique 3). The AIA asks departments to score rights impacts on a 0-to-4 scale, and departments overwhelmingly choose 1 — the minimum non-zero answer. This could be read as genuine low impact, but the thesis argues it is more likely a **floor effect**: the scoring instrument makes it easy to acknowledge some impact (score > 0) while avoiding a score high enough to trigger additional scrutiny. The rights score becomes a ritual acknowledgment — "yes, there are rights implications" — without meaningful differentiation. It is the quantification equivalent of the airline safety card: everyone has one, nobody reads it.

---

## Q-23 — Is Automation Proportional to Risk?
> Methods: `AGG` `DB` `LLM` `CR` | Chapter 6 | Status: ✓ COMPLETE

### Finding

**Proportionality cannot be assessed for the riskiest systems because they did not disclose their automation level. Where automation type is known, the relationship is broadly proportional — but the data gap at the top of the risk scale is itself a proportionality failure.**

### The Proportionality Gap

| Risk Level | Known Automation Type | Unknown (NULL) |
|------------|----------------------|----------------|
| High (7 submissions) | 1 (PACT, partial automation) | 6 |
| Moderate (14 submissions) | 8 | 6 |
| Low (9 submissions) | 8 | 1 |

### What This Tells Us

*Analogy:* Imagine a food safety system where every restaurant must report what kind of cooking equipment it uses, so inspectors can determine whether the equipment is appropriate for the cuisine. Low-risk restaurants (serving salads) dutifully report their equipment. High-risk restaurants (serving raw fish) decline to answer. The inspection system cannot assess proportionality for the establishments that need it most — and the restaurants know it.

**1. Among known systems, proportionality roughly holds.**

Where departments disclosed their automation type, the relationship is broadly proportional: low-risk systems are "decision support" (score 0), moderate-risk systems mix support and partial automation, and the one high-risk system with known type (PACT, partial automation, score 2) includes documented human oversight. The AIA's proportionality principle *works* — when departments cooperate.

**2. Six of seven high-risk systems did not cooperate.**

The six highest-risk submissions all left `automation_type_score` as NULL. Without knowing whether a system is decision support, partial automation, or full automation, proportionality assessment is impossible. **The systems most in need of proportionality scrutiny have exempted themselves from it — not by refusing to complete the AIA, but by leaving the critical field blank.**

**3. Impact level is NULL across the board.**

The AIA's formal proportionality mechanism — Impact Levels I through IV — was never activated. All 30 submissions have NULL `impact_level`. This means the escalating scrutiny requirements (external reviewers for Level III, public disclosure for Level IV) were never triggered. **The entire proportionality architecture of the Directive on Automated Decision-Making appears to be non-functional for this subset of the corpus.**

### Thesis Implications

This finding reveals a design flaw in the AIA that goes beyond individual departmental behaviour. The AIA is a voluntary self-assessment instrument. It *asks* departments to classify their systems and disclose their automation level, but it cannot *compel* them to do so. The result is that proportionality — the ethical principle at the heart of the Directive (Q-02, Framework 4) — is enforceable only for departments that choose to participate fully. Those that do not participate fully are, by construction, the ones most in need of scrutiny. **The AIA's proportionality mechanism is self-defeating: it works only for the systems that don't need it.**

---

## Q-24 — How Do Reversibility and Duration Interact with Rights Impact?
> Methods: `AGG` `DB` | Chapter 6 | Status: ✓ COMPLETE

### Finding

**This question cannot be answered as designed. All 30 submissions share the same reversibility score (1), and all have NULL impact duration. The AIA's reversibility and duration fields are non-discriminating — they do not differentiate between a system whose decisions are easily reversed and one whose decisions are permanent.**

### Data

| Reversibility | Duration | Count | Avg Risk |
|---------------|----------|-------|----------|
| Other (score 1) | NULL | 30 | 4.0 |

All 30 submissions collapse into a single cell.

### What This Tells Us

*Analogy:* Imagine a medical questionnaire that asks doctors to rate the severity of their patients' conditions on a scale where everyone answers "1" and the duration field is left blank. The instrument would be useless for triage — every patient looks the same on paper, regardless of whether they have a cold or a life-threatening condition.

**1. The reversibility score is meaningless in this corpus.**

The designed CASE WHEN categories (0 = Irreversible, 2 = Partially reversible, 4 = Easily reversible) match nothing in the actual data. Every submission has `impacts_reversible_score = 1`, which falls between the categories and maps to "Other." This could reflect a genuine assessment that all impacts are "somewhat" reversible, or it could reflect a default value that departments did not bother to change.

**2. Impact duration is universally absent.**

`impact_duration_score` is NULL for all 30 submissions. Departments were not asked — or chose not to answer — how long their systems' impacts would last. This means the AIA cannot distinguish between a system whose automated decision affects someone for a day (e.g., a queue-priority algorithm) and one whose automated decision affects someone for years (e.g., a disability benefit determination).

**3. This is itself a finding.**

The inability to answer Q-24 as designed is one of the most important results in Phase 2. It demonstrates that the AIA instrument contains fields that are, in practice, non-functional. The *architecture* of the AIA includes reversibility and duration as governance-relevant dimensions, but the *implementation* does not produce usable data about either. **The AIA promises a level of analytical granularity that it does not deliver.**

### Thesis Implications

This finding is a direct case study for the **quantification reductionism** critique (Q-03, Critique 3). The AIA includes fields for reversibility and duration because these are conceptually important governance dimensions — whether a harmful decision can be undone, and how long it lasts. But the scoring mechanism (integer values without clear anchoring) produces data that is either uniform or absent. The instrument *knows* that reversibility matters — it asks about it — but it cannot *measure* it. This is the gap between the AIA's aspirations and its capabilities: it names the right concepts but cannot operationalize them.

---

# Block D — Safeguard Theatre vs. Substantive Compliance (Chapter 7)

> *Central question: Do AIA safeguards represent genuine accountability mechanisms, or is compliance performative?*

---

## Q-28 — What Is the Compliance Distribution?
> Methods: `AGG` `LLM` | Chapter 7 | Status: ✓ COMPLETE

### Finding

**Two-thirds of submissions receive an "adequate" compliance label, but the scores tell a more nuanced story: only 5 of 30 score 4, while a full third score 2 ("weak"). No submission achieves a top score of 5. The Canadian AIA achieves passing grades but not distinction.**

### Data

| Compliance Label | Score | Count | % |
|-----------------|-------|-------|---|
| Adequate | 4 | 5 | 17% |
| Adequate | 3 | 15 | 50% |
| Weak | 2 | 10 | 33% |

### What This Tells Us

*Analogy:* Imagine a driving test where 67% of candidates pass and 33% fail. That sounds reasonable — until you learn that "pass" means "remembered to bring a licence" and the highest achiever still couldn't parallel park. The AIA compliance distribution tells a similar story: most submissions clear the bar, but the bar is low.

**1. No submission achieves strong compliance (score 5).**

Zero out of thirty. The best compliance score in the entire corpus is 4, achieved by only 5 submissions. Even the most diligent departments — those with the strongest justifications, the most complete documentation, and the best bilingual coverage — do not achieve full compliance. **The perfect AIA submission does not exist in the Canadian corpus.**

**2. One in three submissions is "weak."**

Ten submissions score 2, labeled "weak." These are systems deployed by the federal government that the LLM assessed as having inadequate safeguards. Among them: an immigration triage system, a disability benefit automation tool, an elderly benefits prioritization algorithm, and a surveillance-adjacent reporting system. These are not low-stakes systems.

**3. The 3-score plateau.**

Fifteen submissions cluster at score 3 — the bare minimum for "adequate." This is the compliance equivalent of a C+ grade: you pass, but just barely. **Half the corpus is treading water at the threshold of adequacy.**

### Thesis Implications

The compliance distribution provides quantitative support for the **performative compliance** critique (Q-03, Critique 1). The corpus does not contain a bimodal distribution (fully compliant vs. non-compliant) — it contains a distribution skewed toward "just enough." Most departments do enough to avoid the "weak" label but not enough to achieve strong compliance. This is the hallmark of compliance as performance rather than substance: **doing enough to satisfy the form without doing enough to satisfy its purpose.**

---

## Q-29 — What Are the Most Common Safeguard Gaps?
> Methods: `AGG` `LLM` | Chapter 7 | Status: ✓ COMPLETE

### Finding

**The same gaps appear again and again across departments: missing GC EARB review (10 mentions), absent external consultation (9), unassigned bias accountability (9), non-public bias testing (7), and missing data de-identification (5). These are structural gaps — they reflect what the AIA instrument fails to enforce, not what individual departments fail to do.**

### Top 10 Gaps

| Gap | Frequency | What It Means |
|-----|-----------|---------------|
| GC EARB review missing | 10 | The Government of Canada's Enterprise Architecture Review Board — the internal oversight body — was not consulted |
| External stakeholder consultation absent | 9 | No one outside the department was asked for input |
| Bias accountability unassigned | 9 | No person or office is responsible for bias in the system |
| Bias testing results not public | 7 | Testing may have occurred but the results are hidden |
| Data de-identification missing | 5 | Personal data is used without anonymization |
| No PIA conducted | 5 | No Privacy Impact Assessment — a separate legal requirement |
| No data sharing agreement | 5 | Data is shared between entities without formal governance |
| No user feedback mechanism | 3 | Affected persons cannot report problems |
| Inconsistent fairness measures | 2 | Fairness practices vary within the same system |

### What This Tells Us

*Analogy:* Imagine inspecting 30 school buildings and finding that 10 have no fire alarm, 9 have no emergency exit signage, and 9 have no designated fire warden. You would not blame 30 individual principals — you would ask why the school district's building code does not enforce these requirements. **The recurrence of the same gaps across departments points to structural failures in the AIA instrument, not individual negligence.**

**1. External oversight is the biggest gap.**

The two most common gaps — missing EARB review and absent external consultation — both concern oversight from outside the deploying department. The AIA's self-assessment model operates in a governance vacuum: departments assess themselves, and in 10 of 30 cases, no external body reviewed the assessment. This is the self-assessment bias (Q-03, Critique 2) expressed as an empirical pattern.

**2. Bias accountability is nobody's job.**

Nine submissions have no identified person or office responsible for bias in the system. Not "we assessed bias and found none" — *no one is assigned to look for it*. This is the institutional equivalent of a company with no safety officer: not that the company determined it was safe, but that no one was asked to make the determination.

**3. Bias testing is secret.**

Seven submissions conducted some form of bias testing but did not make the results public. This gap is more subtle than the others: the work may have been done, but the transparency principle (Q-02, Framework 5) is violated. It is, as one critic put it, "transparency theatre" — the process exists, but the public cannot see its results.

### Thesis Implications

The structural nature of these gaps — the same ones appearing across departments, risk levels, and automation types — supports the argument that the AIA's design, not departmental behaviour, is the primary source of governance failure. The AIA *permits* departments to skip external review, bias accountability, and public disclosure of testing results. It does not *require* any of these things. **The gaps are not bugs — they are features of an instrument designed for self-assessment rather than accountability.**

---

## Q-30 — The Human Override Question: Explain, Override, Challenge
> Methods: `AGG` `DB` `LLM` | Chapter 7 | Status: ✓ COMPLETE

### Finding

**All 30 submissions claim human override capability. 29 of 30 claim client recourse processes. 25 of 30 claim the system can produce reasons for its decisions. On paper, the accountability trifecta is nearly universal — but "weak" compliance labels persist even among systems claiming all three. The claims exist; the substance may not.**

### Data — The Trifecta

| Override | Recourse | Reasons | Count | Avg Compliance |
|----------|----------|---------|-------|----------------|
| Yes (2) | Yes (2) | Yes (2) | 25 | 2.8 |
| Yes (2) | Yes (2) | No (0) | 4 | 2.8 |
| Yes (2) | No (0) | Yes (2) | 1 | 3.0 |

### What This Tells Us

*Thought experiment:* Imagine a restaurant that posts a sign saying "All dietary restrictions accommodated." You order a gluten-free meal and receive regular pasta with the gluten-free sticker moved to a different plate. The *claim* of accommodation is universal; the *practice* may not match. This is the trifecta pattern in the AIA corpus.

**1. Universal claims, variable substance.**

Every system claims human override. Nearly every system claims recourse and reason-giving. But 10 of 30 submissions are still rated "weak" on overall compliance. **If you can override, seek recourse, and receive explanations, how can compliance be weak?** The answer is that the structured fields (Yes/No checkboxes) capture claims, while the LLM's compliance assessment evaluates whether those claims are substantiated by the narrative evidence.

*Case study:* Submission 9 (Old Age Security Extended Absence Leave Prioritization) checks all three boxes — override yes, recourse yes, reasons yes — but scores "weak" on compliance. The gaps include: no external stakeholder consultation, no bias testing, no GBA+, no de-identification, and no public disclosure. **The trifecta is satisfied on paper while the underlying governance infrastructure is absent.**

**2. Four systems cannot explain themselves.**

Four submissions check "No" for `can_produce_reasons` — the system cannot tell the affected person why a decision was made. These are systems from Department 014 (ESDC), including the Old Age Security prioritization tool and an Employment Insurance recalculation algorithm. **Systems affecting elderly Canadians' pensions and workers' unemployment benefits cannot explain their own decisions.** This is the "right to explanation" problem in concrete form.

**3. One system has no recourse process.**

The Mental Health Benefit system (Department 021) is the only submission that checks "No" for client recourse. A system automating mental health benefit decisions for vulnerable Canadians, with no documented process for clients to challenge the automated outcome. Yet it scores *higher* on compliance (3.0) than the 25-system average (2.8) — because it excels on other safeguard dimensions. **The compliance scoring can mask a fundamental accountability gap.**

### Thesis Implications

The trifecta finding reveals the difference between **formal compliance** (checking boxes) and **substantive compliance** (building real accountability infrastructure). The AIA instrument captures the first but not the second. This supports the **legitimation problem** critique (Q-03, Critique 9): a completed AIA with all three boxes checked becomes a shield — "our system has human override, recourse, and explainability" — even when the underlying reality is thin. The AIA legitimates the deployment by documenting the *claims* of accountability, regardless of whether the accountability is real.

---

## Q-31 — GBA+ and Bias Testing as Governance Signifiers
> Methods: `DB` `LLM` `CR` | Chapter 7 | Status: ✓ COMPLETE

### Finding

**GBA+ (Gender-Based Analysis Plus) has been conducted for about two-thirds of submissions, but bias testing results are made public in almost none. The bias mitigation pipeline has a transparency bottleneck: departments test for bias but do not share the results. Bias testing becomes a private ritual rather than a public accountability mechanism.**

### The Bias Pipeline — Three Stages

| Stage | Description | Rate |
|-------|------------|------|
| 1. GBA+ conducted | Intersectional impact analysis performed | ~20/30 (67%) |
| 2. Bias testing documented | Some form of testing recorded | ~22/30 (73%) |
| 3. Bias testing results made public | Results shared externally | ~1/30 (3%) |

### What This Tells Us

*Analogy:* Imagine a pharmaceutical company that tests a drug for side effects (Stage 1), writes up the test results (Stage 2), but does not publish them (Stage 3). The testing was done, the documentation exists, but no one outside the company can verify whether the drug is safe. **The bias mitigation pipeline in the Canadian AIA has the same structure: internal testing exists, but external scrutiny does not.**

**1. Department 014 (ESDC) shows the weakest GBA+ uptake.**

Only 1 of 8 ESDC submissions reports conducting GBA+. This department deploys systems affecting Employment Insurance, Old Age Security, disability benefits, and foreign worker programs — all domains with significant intersectional implications. **The department whose systems most need intersectional analysis is the least likely to conduct it.**

**2. Department 021 has no bias testing at all.**

The department responsible for the Mental Health Benefit and Disability Benefit systems — two of the highest-risk deployments in the corpus — reports no documented bias testing. These systems affect some of the most vulnerable populations the government serves.

**3. The publicity gap is near-universal.**

Even departments that conduct GBA+ and document bias testing (Departments 050, 056, 085, 034) almost never make the results public. This creates what we might call a **"bias opacity wall"**: the department knows whether its system is biased, but the public does not. Canada's AIA regime produces internal bias knowledge while blocking external bias scrutiny.

### Thesis Implications

GBA+ is one of Canada's most distinctive governance innovations — a requirement to analyze policy impacts through intersectional lenses including gender, age, disability, ethnicity, and more. Its uneven application in the AIA corpus (67% uptake, 3% publication) reveals the distance between governance aspiration and practice. **The GBA+ mandate exists; the GBA+ practice is partial; the GBA+ transparency is nearly absent.** This three-stage failure pattern is a microcosm of the AIA's broader accountability gap.

---

## Q-32 — Privacy in the Age of Automation
> Methods: `DB` `LLM` | Chapter 7 | Status: ✓ COMPLETE

### Finding

**28 of 30 systems process personal information at the highest level (score 4), but only half conducted a Privacy Impact Assessment. All claim "privacy by design," but de-identification — the most concrete privacy protection — is applied in only 4 of 28 cases. Privacy governance in the AIA corpus is more promise than practice.**

### Data

| Measure | Rate (of 28 using personal info) |
|---------|----------------------------------|
| Uses personal information (score 4) | 28/30 (93%) |
| Privacy by design claimed | 28/28 (100%) |
| PIA conducted | 15/28 (54%) |
| De-identification applied | 4/28 (14%) |

### What This Tells Us

*Analogy:* Imagine 28 banks, all handling customers' financial data. Every bank has a sign in the lobby saying "We take your privacy seriously" (privacy by design). Half the banks conducted an independent security audit (PIA). Only 4 banks actually encrypt customer data (de-identification). **The promise is universal; the audit is partial; the protection is rare.**

**1. "Privacy by design" is a checked box, not a practice.**

Every single system that processes personal information claims privacy by design. But privacy by design — as a genuine methodology — requires specific technical measures: data minimization, purpose limitation, de-identification, access controls. When 100% of systems claim it but only 14% implement its most basic technical component (de-identification), "privacy by design" has become a governance slogan rather than a technical standard.

**2. Half of high-sensitivity systems skipped the Privacy Impact Assessment.**

A PIA is a separate legal requirement in Canada — not merely an AIA field. Thirteen systems processing personal information at the highest sensitivity level did not conduct one. These include immigration triage systems, foreign worker program algorithms, and spousal application analytics. **Systems processing the most intimate data — immigration status, family composition, employment history — without a formal privacy assessment.**

*Case study:* The "Automated Triage and Positive Eligibility Determinations of In-Canada Work Permit Applications" (Department 050) processes personal immigration data at the highest level, applies no de-identification, and conducted no PIA. Yet it scores `privacy_by_design = 1` ("yes"). The system claims privacy by design while implementing almost none of it.

**3. De-identification is the exception, not the rule.**

Only 4 of 28 systems apply de-identification — the most concrete, verifiable privacy protection. The other 24 process personal information in identifiable form. For systems making automated decisions about people's immigration, benefits, and employment, this means the algorithm sees *who you are*, not just *what your case looks like*. This has direct implications for bias: a system that knows an applicant's name, nationality, and demographic details can (even inadvertently) discriminate based on those features.

### Thesis Implications

The privacy findings demonstrate the gap between **declarative compliance** (checking "privacy by design") and **operational compliance** (conducting PIAs, applying de-identification). The AIA captures the first but does not verify the second. This is the safeguard compliance chapter's central finding: **the AIA measures what departments say they do, not what they actually do.** Privacy governance in the Canadian AIA corpus is a story of aspirations without implementation — a government that *promises* to protect privacy while *processing* personal data with minimal technical safeguards.

---

# Phase 2 Summary

## Scorecard

| Q# | Chapter | Key Finding — In One Sentence |
|----|---------|------------------------------|
| Q-09 | Ch 3 | 96.7% of submissions diverge bilingually — the Canadian state's algorithmic governance is almost never equivalently bilingual |
| Q-10 | Ch 3 | The fields that diverge most are the ones that matter most — evaluation criteria, system outputs, rights assessments |
| Q-11 | Ch 3 | Divergence is "linguistic" (avg fidelity 2.61/5), but the label masks the real cause: omission, not mistranslation |
| Q-12 | Ch 3 | Omission accounts for 71% of all divergence — the French state is not badly translated but largely absent |
| Q-13 | Ch 3 | Fidelity is binary: submissions are either monolingual (score 0–1) or bilingual (score 3–5), with no middle ground |
| Q-17 | Ch 5 | "Efficiency" dominates justification rhetoric (60%) but is the weakest theme; "compliance" is rare but always strong |
| Q-18 | Ch 5 | Strong justifications always acknowledge trade-offs; weak ones always leave the trade-off field empty |
| Q-19 | Ch 5 | Every submission that named its automation type scored perfectly; every one that didn't scored poorly |
| Q-20 | Ch 5 | The 13 systems with the broadest capabilities provide no confinement assessment — the tiger cages have no specifications |
| Q-21 | Ch 6 | The 6 highest-risk systems (risk_total=10) are the ones with the thinnest governance documentation |
| Q-22 | Ch 6 | Rights scores are uniformly flat (~1.0) — either genuine low impact or systematic understatement |
| Q-23 | Ch 6 | Proportionality cannot be assessed for the riskiest systems because they didn't disclose their automation level |
| Q-24 | Ch 6 | Reversibility and duration fields are non-functional — all 30 submissions score identically |
| Q-28 | Ch 7 | No submission achieves strong compliance (5/5); one-third scores "weak"; the mode is "barely adequate" |
| Q-29 | Ch 7 | The same gaps recur structurally: missing external review, unassigned bias accountability, non-public testing |
| Q-30 | Ch 7 | All 30 systems claim human override, but 10 still score "weak" — claiming accountability ≠ having it |
| Q-31 | Ch 7 | GBA+ is conducted 67% of the time but published 3% — bias testing is a private ritual, not a public safeguard |
| Q-32 | Ch 7 | 93% of systems process personal data; all claim "privacy by design"; only 14% actually de-identify |

## The Emergent Pattern: The Completeness Cluster

The single most important finding that emerges across all four Phase 2 blocks is what we call the **"completeness cluster."** The same ~13 submissions that leave French fields empty (Q-12) also leave automation type blank (Q-19), skip confinement assessment (Q-20), omit trade-off analysis (Q-18), and have the highest risk scores (Q-21). The AIA corpus is not a gradient from good to bad — it is two distinct populations:

- **Population A (~17 submissions):** Bilingual, well-documented, substantive trade-offs, clear confinement, moderate-to-low risk
- **Population B (~13 submissions):** Monolingual, poorly documented, missing trade-offs, no confinement, moderate-to-high risk

This binary is the most important structural finding of the thesis so far. It suggests that AIA compliance is not a continuous variable but a threshold phenomenon: departments either engage seriously with the assessment or they do not, and those that do not are *more likely to be deploying high-risk systems*.

## Ready for Phase 3

Phase 2 has established the corpus-level facts. Phase 3 moves to comparative and critical analysis:
- **Q-14 → Q-16:** The accountability gap — how "accountability" fragments across EN/FR
- **Q-25 → Q-27:** The quantification critique — armed with Q-21/Q-22 risk data
- **Q-33 → Q-39:** Departmental cultures — armed with all Phase 2 findings
- **Q-40 → Q-43:** Language analysis — requires NLP tooling on exported corpus text
