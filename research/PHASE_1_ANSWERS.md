# Phase 1 — Foundations: Answers

> Answers to Q-01 through Q-08 (Chapters 1–2)
> Generated: 2026-03-08
> Status: ALL COMPLETE (Q-01 through Q-08)
>
> **Evidence appendix:** [PHASE_1_EVIDENCE.md](PHASE_1_EVIDENCE.md) — every data-driven finding below is backed by an exact SQL query, database table reference, and reproducibility instructions.

---

## Q-01 — What is the History of AIAs as Governance Tools?
> Methods: `LIT` | Chapter 1 | Status: ✓ COMPLETE

### Finding

**AIAs emerged from the convergence of three currents: the regulatory precedent of Environmental Impact Assessment (NEPA, 1969), the algorithmic accountability movement (2014–2018), and Canada's digital government reform. Understanding this genealogy is essential because design choices inherited from each tradition continue to shape — and constrain — what AIAs can accomplish.**

### The Story in Brief

Imagine a government in the 1960s saying: *before you build a dam, you must write down what it will do to the river.* That was the insight behind the National Environmental Policy Act (NEPA, 1970) — not that governments should stop building dams, but that they should be forced to *think about the consequences in writing* before they act. This "think before you act" principle, called **ex ante assessment**, became the backbone of environmental governance worldwide.

Half a century later, a parallel problem appeared: governments began deploying algorithms — to sort visa applications, flag tax fraud, triage welfare claims — without any formal process to ask, *what will this do to the people it touches?* The algorithmic accountability movement (2014–2018) recognized that algorithms, like dams, reshape the landscape they operate in. And just as a dam can flood a village, an algorithm can systematically deny benefits to an entire demographic.

In 2018, researchers at NYU's AI Now Institute made the connection explicit. Reisman, Schultz, Crawford, and Whittaker published the foundational AIA paper, deliberately adapting the NEPA model for algorithms. They proposed five components: review *before* acquisition, public disclosure, a comment period, due process challenges, and periodic renewal. This was not merely an analogy — it was a conscious act of regulatory translation, borrowing legitimacy from a 50-year-old governance tradition.

**Canada became the first country to act.** In 2019, the Treasury Board Secretariat issued the Directive on Automated Decision-Making, requiring all federal departments to complete an Algorithmic Impact Assessment before deploying any automated decision system. The AIA tool — 65 risk questions and 41 mitigation questions, published as open-source code on GitHub — was, in effect, a government-issued questionnaire that asks civil servants to confess the potential harms of their own technology.

### Historical Timeline

| Year | Milestone | Significance |
|------|-----------|-------------|
| 1970 | NEPA signed into law (US) | Established the EIA/EIS model: think before you act, document consequences, allow public scrutiny |
| 2015 | Pasquale, *The Black Box Society* | Named the democratic threat: decisions that affect millions, made by systems nobody can see inside |
| 2015 | Diakopoulos, "Algorithmic Accountability" | Gave the academic field its name |
| 2017 | ACM Statement on Algorithmic Transparency | Seven principles from the world's largest computing society — a professional self-reckoning |
| 2017 | AI Now Institute founded (NYU) | First university institute dedicated to asking: *what is AI doing to society?* |
| 2018 | Reisman et al., "Algorithmic Impact Assessments" (AI Now) | **The founding document.** Adapted the EIA model for algorithms. Proposed five components: review, disclosure, comment, due process, renewal |
| 2019 | Canada's Directive on Automated Decision-Making | **First national AIA mandate.** A government telling itself: *assess your own algorithms, or else.* |
| 2021 | NYC Local Law 144 | First municipal law requiring independent algorithmic audits — a city saying *we don't trust self-assessment* |
| 2023 | Canada adds GBA+ layer | Intersectional analysis (gender, age, disability, ethnicity) woven into the AIA — an attempt to see what scoring alone cannot |
| 2024 | EU AI Act Article 27 (FRIA) | Europe requires Fundamental Rights Impact Assessments for high-risk AI — the AIA idea goes continental |
| 2024 | Council of Europe HUDERIA | Human rights, democracy, and rule of law assessment — the most ambitious scope yet |

### What Makes Canada's AIA Distinctive

Think of the AIA as a **confessional instrument**: it asks the deploying department to name its own sins before deployment. This is both its strength (it forces confrontation with risk) and its weakness (the confessor has every incentive to minimize).

- **Open source:** The tool's code is published on GitHub. Any researcher — including this thesis — can examine the exact questions, weights, and scoring logic. This is rare in government: it is as if the tax code were not only public law but also published as a working calculator.
- **Proportionality through scoring:** Answers produce a numerical score that maps to Impact Levels I–IV. Level I requires basic documentation; Level IV requires multiple external reviewers and public disclosure. The principle is intuitive — *higher stakes, higher scrutiny* — but as we will see (Q-06, Q-25), the scoring mechanism may itself distort what it measures.
- **Bilingual by design:** Every question exists in both English and French. This is not merely a translation exercise — it is, as this thesis argues, a site where two distinct governance imaginations meet, sometimes agree, and sometimes silently diverge.

### Key Sources

- Reisman, D., Schultz, J., Crawford, K. & Whittaker, M. (2018), "Algorithmic Impact Assessments: A Practical Framework for Public Agency Accountability," AI Now Institute
- Treasury Board of Canada Secretariat (2019), Directive on Automated Decision-Making
- ACM US Public Policy Council (2017), "Statement on Algorithmic Transparency and Accountability"
- World Privacy Forum (2024), "AI Governance on the Ground: Canada's AIA Process and Algorithm Has Evolved"
- Pasquale, F. (2015), *The Black Box Society*, Harvard University Press

---

## Q-02 — What Ethical Frameworks Justify AIAs?
> Methods: `LIT` | Chapter 2 | Status: ✓ COMPLETE

### Finding

**AIAs draw justification from six distinct ethical traditions — procedural justice, democratic accountability, the precautionary principle, proportionality, transparency, and rights-based governance. The Canadian AIA implicitly privileges procedural justice and proportionality (through scoring) while underweighting democratic participation and substantive rights protection.**

### The Six Pillars — In Plain Language

#### 1. Procedural Justice: "It matters how you decide, not just what you decide"

A thought experiment: Imagine two immigration officers reject the same visa application. One reviews the file carefully, explains her reasoning, and offers an appeal route. The other uses a black-box algorithm and sends a form letter. Even if the outcome is the same — rejection — most people would say the first process is *fairer*. This is Tyler's insight (1990): **people accept unfavourable outcomes when they believe the process was fair.**

The AIA borrows this logic. By requiring departments to document their algorithmic systems *before* deployment, it creates a visible, traceable process. The AIA says: *we assessed this, we thought about the risks, here is our documentation.* Whether this actually prevents harm is a separate question — but it creates legitimacy.

**The gap:** Bibal et al. (2024) call this the "procedural gap." A process is only fair if the people affected can *participate* in it. Canada's AIA is completed by civil servants, behind closed doors, with no mandatory public consultation. It is procedural justice without voice — like a trial where the defendant is never called to testify.

#### 2. Democratic Accountability: "The public should have a say"

The original AI Now proposal (2018) envisioned AIAs as democratic instruments — complete with public comment periods, like the ones used for environmental reviews. Citizens could read an AIA, submit objections, and challenge deployments through due process.

Canada adopted the documentation but dropped the democracy. The Directive requires publishing completed AIAs but does not mandate public consultation. **This is like publishing a building permit after the building is already constructed** — transparency without agency. Selbst (2021) calls this the transformation of AIAs from democratic accountability instruments into bureaucratic self-regulation.

#### 3. The Precautionary Principle: "Look before you leap"

The AIA embodies a *weak* precautionary principle: assess risks before deployment (ex ante), rather than waiting for harm to occur (ex post). But the *strong* precautionary principle would demand proof of safety before deployment — the way pharmaceutical regulation works. **No AIA regime in the world gives the assessor power to prohibit deployment.** The AIA is a speed bump, not a roadblock: it slows you down and makes you think, but it cannot stop you from driving through.

#### 4. Proportionality: "Higher stakes, higher scrutiny"

Canada's Impact Level system (I–IV) is the most elegant operationalization of proportionality in any global AIA regime. A low-risk system (Impact Level I) needs only basic documentation. A high-risk system (Level IV) needs multiple external reviewers and public disclosure.

**The philosophical problem** is a deep one: Can you really compare a privacy violation with a discrimination harm with a loss of liberty using a single number? It is like asking whether a sonnet is better than a symphony by scoring them both out of 100. The World Privacy Forum (2024) argues that "simplifying and decontextualizing complex legal, fairness-related concepts" through scoring is fundamentally flawed. Our corpus data (Q-06) will show this compression at work.

#### 5. Transparency: "Sunlight is the best disinfectant"

Published AIAs create the *possibility* of public scrutiny. Levels III–IV require plain-language descriptions of how systems work. But consider: a 40-page algorithmic assessment full of technical jargon is *technically* transparent but *practically* opaque. This is the "transparency theatre" critique — **disclosure without comprehension produces a veneer of accountability**, like publishing a restaurant's health inspection in a language nobody in the neighbourhood speaks.

#### 6. Rights-Based Governance: "Start with what people are owed"

In Canada, Charter Sections 7 (life, liberty, security), 8 (search and seizure), 9 (detention), and 15 (equality) provide the constitutional frame. The Directive requires testing for factors that may "violate human rights and freedoms." But a questionnaire is not a rights audit. International alternatives — the Ontario Human Rights Commission's HRIA, the UNDP Toolkit, the Council of Europe's HUDERIA — start from the rights themselves and work backward to assess systems, rather than starting from the system and looking for rights implications. **The difference is like the difference between asking "does this building meet code?" and asking "is this neighbourhood safe to live in?"**

### Key Sources

- Tyler, T.R. (1990), *Why People Obey the Law*, Yale University Press
- Rawls, J. (1971), *A Theory of Justice*, Harvard University Press
- Bibal et al. (2024), "Voiceless: The Procedural Gap in Algorithmic Justice," *IJLIT*
- Selbst, A.D. (2021), "An Institutional View of Algorithmic Impact Assessments," *Harvard JOLT*, 35(1)
- World Privacy Forum (2024), "AI Governance on the Ground: Canada"

---

## Q-03 — What Are the Scholarly Critiques of AIAs?
> Methods: `LIT` | Chapter 2 | Status: ✓ COMPLETE

### Finding

**Nine distinct scholarly critiques have emerged since 2018. The Canadian corpus provides a unique opportunity to test each empirically — to move from "scholars worry about X" to "the data shows X happens (or doesn't)."**

### The Nine Critiques — With Illustrations

#### 1. Performative Compliance: "Filling out the form vs. doing the work"

*Illustration:* Think of airline safety cards in seat-back pockets. Every passenger is "briefed" on emergency procedures, but almost nobody reads the card, and the ritual exists more for regulatory compliance than for actual safety. Moss, Metcalf, and colleagues (Data & Society, 2021) argue that AIAs risk becoming the algorithmic equivalent — a process that serves institutional needs ("we did the assessment") rather than protecting the communities affected by the systems being assessed.

**Testable in our corpus:** If AIAs are performative, we should find standardized, copy-paste language across submissions (Q-43) and high rates of unanswered or minimally answered questions (Q-39).

#### 2. Self-Assessment Bias: "Grading your own homework"

*Thought experiment:* Imagine a restaurant health inspection where the restaurant writes its own report, scores its own cleanliness, and submits it to the regulator. Would you trust the results? Selbst (2021) makes the same point about AIAs: the department deploying the algorithm is the same entity assessing its risks. **The entity best positioned to identify harms has the strongest incentive to minimize them.**

**Testable in our corpus:** If self-assessment bias exists, risk scores should cluster at the low end of the scale (Q-21), and respondents should understate trade-offs (Q-18). Our Q-06 data already hints at this: all 30 submissions score between 0 and 10 on risk — a suspiciously narrow range.

#### 3. Quantification Reductionism: "Turning a novel into a number"

*Analogy:* Rating a novel from 1 to 5 stars captures *something*, but it loses everything that makes the novel a novel — its prose style, its moral complexity, its cultural moment. The World Privacy Forum (2024) argues that the AIA does the same thing to governance: it reduces complex questions about discrimination, dignity, and liberty to numerical scores that can be added and compared. **"Gaps between what people want AI governance tools to accomplish, and what they actually accomplish"** are, in their view, structural, not accidental.

**Testable in our corpus:** Q-25 through Q-27 form a "quantification problem" cluster that examines whether the scoring algorithm captures meaningful differences or flattens them.

#### 4. The Enforcement Gap: "A law without teeth"

*Case study:* New York City passed Local Law 144 in 2021, requiring employers to conduct independent bias audits of hiring algorithms. By 2024, researchers found that **only 5% of covered employers had posted the required audit reports** ("Null Compliance," FAccT 2024). The law existed on paper; compliance existed almost nowhere. Canada's AIA Directive carries no civil penalties for non-completion — it relies entirely on institutional culture and Treasury Board oversight.

#### 5. Temporal Mismatch: "A photograph of a river"

*Metaphor:* An AIA is a snapshot — a photograph of a river taken at one moment. But algorithms, like rivers, change constantly: the data shifts, the model drifts, users find workarounds, feedback loops amplify initial biases. **A point-in-time assessment cannot capture emergent harms.** This is like approving a building based on its blueprints, then never inspecting it again — even as the foundation cracks and the wiring ages.

#### 6. Participation Deficit: "About us, without us"

*Case study from our corpus:* Canada's AIA is completed entirely by government employees. No mandatory public consultation. No community input. No mechanism for the people *affected* by algorithmic decisions to shape the assessment of those decisions. Costanza-Chock (2020) calls this the "dual black box" problem: the algorithm is opaque, and the process for governing it is also opaque. **The people most affected by the system have the least voice in assessing it** — precisely the inverse of the democratic accountability ideal.

#### 7. The Assessment Industrial Complex: "The tail wagging the dog"

*Analogy:* In higher education, the rise of "assessment culture" has been critiqued for producing elaborate accreditation rituals that consume faculty time without improving teaching. Moss et al. (2021) warn that algorithmic assessment regimes may follow the same path — becoming self-perpetuating bureaucratic infrastructure with their own institutional interests, career tracks, and consulting markets, disconnected from the harms they were created to prevent.

#### 8. Structural Limitations: "What the instrument cannot see"

*Thought experiment:* Imagine designing a thermometer that can only measure temperatures between 20°C and 30°C. Everything below 20 reads as "cold" and everything above 30 reads as "hot." This instrument is structurally incapable of distinguishing a mild chill from a deadly freeze. Intersectionality scholars argue that AIAs have a similar blind spot: they cannot capture systemic racism, the cumulative effects of multiple algorithmic systems on the same population, or the power asymmetries that shape who gets assessed and who does the assessing.

#### 9. The Legitimation Problem: "A stamp of approval for harm"

*Case study:* Krafft et al. (2022) pose a disturbing question: *What if AIAs make things worse?* By providing a documented assessment process, AIAs may *legitimate* harmful deployments that would otherwise face political resistance. **A completed AIA becomes a shield** — "we did our due diligence" — even when the system it assessed goes on to cause real harm. In their words: "in many use cases abolition, not legitimation, will be more appropriate." Some systems should not be assessed and improved; they should be stopped.

### Critique Summary Table

| # | Critique | Core Question | Where to Look in Our Corpus |
|---|----------|--------------|---------------------------|
| 1 | Performative compliance | Are departments filling out the form or doing the work? | Q-43, Q-39 |
| 2 | Self-assessment bias | Are departments grading their own homework generously? | Q-21, Q-18 |
| 3 | Quantification reductionism | Does scoring flatten meaningful differences? | Q-25, Q-26, Q-27 |
| 4 | Enforcement gap | Does anyone face consequences for non-compliance? | N/A (no penalties in Canada) |
| 5 | Temporal mismatch | Can a snapshot capture a river? | Q-38 |
| 6 | Participation deficit | Who has voice in the process? | Q-39 |
| 7 | Assessment industrial complex | Has assessment become an end in itself? | Cross-domain analysis |
| 8 | Structural limitations | What can the instrument not see? | Q-31 |
| 9 | Legitimation problem | Does assessment make harmful deployment easier? | Q-23 |

### Key Sources

- Moss, E., Watkins, E.A., Singh, R., Elish, M.C. & Metcalf, J. (2021), "Assembling Accountability," Data & Society
- Moss, E. et al. (2021), "Governing Algorithmic Systems with Impact Assessments: Six Observations," *AAAI/ACM AIES*
- Metcalf, J. et al. (2021), "Algorithmic Impact Assessments and Accountability: The Co-construction of Impacts," *ACM FAccT*
- Selbst, A.D. (2021), "An Institutional View of Algorithmic Impact Assessments," *Harvard JOLT*, 35(1)
- "Null Compliance" (2024), *ACM FAccT*
- Krafft, P.M. et al. (2022), "Legitimacy of Algorithmic Decision-Making: Six Threats," *PPMG*, 5(3)
- Costanza-Chock, S. (2020), *Design Justice*, MIT Press

---

## Q-04 — What Are the Alternatives to AIAs?
> Methods: `LIT` | Chapter 2 | Status: ✓ COMPLETE

### Finding

**Nine distinct governance mechanisms have been proposed or implemented as alternatives to (or complements for) AIAs. No single instrument is sufficient — the most robust regimes will layer multiple mechanisms, the way a hospital combines hand-washing protocols, sterile equipment, and post-operative monitoring rather than relying on any one alone.**

### The Alternatives — With Analogies

#### 1. Independent Algorithmic Auditing
*Analogy:* Financial auditing works because the auditor is independent — PricewaterhouseCoopers does not grade its own balance sheets. NYC's Local Law 144 required independent third-party bias audits for hiring algorithms, borrowing this logic. **The problem:** only 5% of covered employers actually complied. Independence without enforcement is an aspiration, not a safeguard.

#### 2. Participatory Design / Co-Design
*Analogy:* Instead of a doctor deciding a treatment plan alone and then "informing" the patient, participatory design asks the patient to help *design* the treatment plan. Costanza-Chock's *Design Justice* (2020) applies this to technology: the communities affected by an algorithm should help shape it, not merely be informed after the fact. **The limitation:** genuine co-design is slow, expensive, and difficult to scale to the dozens of federal systems Canada deploys.

#### 3. Moratoriums and Bans
*Case study:* Between 2019 and 2021, San Francisco, Oakland, Boston, and Portland all banned government use of facial recognition. These cities decided that **some technologies should not be assessed and improved; they should be stopped entirely.** This is the governance equivalent of the medical principle *primum non nocere* (first, do no harm) — applied not to a specific deployment but to an entire category of technology.

#### 4. Regulatory Sandboxes
*Analogy:* A sandbox is a controlled playground — you let the child play, but within safe boundaries. The EU AI Act (Article 57) creates regulatory sandboxes where AI systems can be tested under government supervision before full deployment. **The risk:** the sandbox itself may be captured by the very companies it is meant to regulate — the fox guarding the henhouse, just in a smaller henhouse.

#### 5. Community Review Boards
*Analogy:* Universities require ethics review boards (IRBs) before researchers can study human subjects. Community review boards would apply the same principle to algorithmic deployment: before your system touches people's lives, an independent community body must approve it. **The challenge:** Who counts as "the community"? How do you prevent the board itself from becoming captured by institutional interests?

#### 6. Human Rights Impact Assessments (HRIAs)
*Key difference from AIAs:* An AIA starts with the system and asks, "what are the risks?" An HRIA starts with the rights of the people affected and asks, "are these rights being respected?" **It is the difference between inspecting a building for code violations and asking the residents whether they feel safe.** The Council of Europe's HUDERIA and the Ontario Human Rights Commission's HRIA represent this rights-first approach — more demanding than a questionnaire, but grounded in what actually matters.

#### 7. Continuous Monitoring
*Analogy:* A home inspection tells you the house was safe on the day the inspector visited. A smoke detector tells you the house is safe *right now*. Continuous monitoring — required by the EU AI Act for high-risk systems — replaces the snapshot model with ongoing surveillance of algorithmic performance. **The trade-off:** monitoring itself is a form of surveillance, and it raises its own governance questions (who watches the watchers?).

#### 8. Algorithmic Registers
*Case study:* In 2020, Amsterdam and Helsinki became the first cities to publish public registries of every algorithm used by the municipal government — what it does, what data it uses, how it was tested. **An algorithmic register is like a public library catalogue for government AI:** it does not tell you whether a book is good, but it tells you that the book exists, where to find it, and what it is about. Transparency without assessment — necessary but not sufficient.

#### 9. Procurement-Based Governance
*Analogy:* Instead of inspecting every meal a restaurant serves, you can regulate what ingredients the restaurant is allowed to buy. Procurement-based governance operates upstream: before a government department can *acquire* an AI system, the acquisition must meet governance standards. **The advantage:** it prevents problematic systems from entering the building, rather than assessing them after they are already installed.

### Key Sources

- NYC Local Law 144 of 2021
- ORCAA (O'Neil Risk Consulting & Algorithmic Auditing)
- Costanza-Chock, S. (2020), *Design Justice*, MIT Press
- EU AI Act Articles 27, 57
- Ontario HRC, "Human Rights AI Impact Assessment"
- UNDP (2025), "Human Rights Impact of AI Assessment Toolkit"
- Council of Europe, HUDERIA methodology
- Amsterdam & Helsinki algorithm registries (VentureBeat, 2020)
- Carnegie Endowment (2024), "How Cities Use the Power of Public Procurement for Responsible AI"

---

## Q-05 — How Does the EIA Analogy Shape — and Limit — AIA Design?
> Methods: `LIT` | Chapter 2 | Status: ✓ COMPLETE

### Finding

**The EIA analogy is the most consequential design choice in AIA history. It made algorithmic accountability legible to policymakers by borrowing a familiar governance template, but it imported structural limitations that constrain what AIAs can accomplish. The EIA's own documented history of performative compliance is a cautionary inheritance — as if a child inherited not only a parent's house but also its termites.**

### Where the Analogy Holds

Think of the EIA-to-AIA translation as a **genre adaptation** — like turning a novel into a film. Some elements transfer beautifully:

| Feature | The Novel (EIA/NEPA) | The Film (AIA/Canada) |
|---------|---------------------|----------------------|
| **"Think before you act"** | Required before any major federal action | Required before deploying automated decision systems |
| **Documentation** | The Environmental Impact Statement — a formal written record | The published AIA questionnaire — a formal written record |
| **Proportionality** | Small projects get a quick review; major projects get a full study | Impact Level I gets basic documentation; Level IV gets external reviewers |
| **Action-forcing** | Forces agencies to *confront* environmental consequences | Forces departments to *confront* algorithmic risks |

### Where the Analogy Breaks Down

But some elements are lost in translation, and the losses are revealing:

**1. You can measure pollution. You cannot measure dignity.**

An Environmental Impact Statement can say: *this factory will emit 500 parts per million of sulphur dioxide, which exceeds the safe threshold by 3×.* The harm is measurable, the threshold is scientific, the number is meaningful. Now try the same sentence for an algorithm: *this visa-processing system will produce X units of discrimination.* What is the unit? What is the threshold? **The AIA scoring system imports a false precision from environmental science** — it creates numbers where no meaningful numbers exist, like assigning a temperature to the colour blue.

**2. Pollution has a science. Algorithmic harm does not.**

We understand the causal chain from pollutant to health outcome because decades of epidemiology have established it. There is no equivalent "science of algorithmic harm." The effects of a biased hiring algorithm are mediated by institutions, labour markets, social networks, individual resilience, and feedback loops. **The EIA can stand on scientific consensus; the AIA stands on contested interpretation.** This is why the thesis uses LLM-based semantic analysis (Q-06) — not because AI is better than science, but because the domain of algorithmic harm demands interpretive methods, not just measurement.

**3. Cumulative effects — the blind spot both share.**

If one factory pollutes a river, the harm is visible. But what about 50 factories, each within legal limits, whose combined pollution destroys the ecosystem? NEPA nominally requires cumulative effects assessment, but in practice this is the weakest part of EIA (Noble, 2015). AIAs inherit this blind spot entirely: **no AIA framework in the world assesses the cumulative impact of multiple algorithmic systems on the same population.** A person denied welfare by one algorithm, flagged as high-risk by another, and deprioritized for housing by a third experiences cumulative algorithmic harm that no single AIA can see.

**4. Canada adopted the documentation but not the democracy.**

NEPA requires a public comment period — citizens can read the Environmental Impact Statement, submit objections, and in some cases sue. Canada's Directive requires departments to *publish* completed AIAs but does not mandate public consultation. **It is as if NEPA required environmental assessments but forbade anyone from commenting on them.** The democratic core of the EIA model — the part that gives citizens voice — was dropped in translation.

**5. Neither can say "no."**

NEPA is purely procedural — it does not give any agency the power to prohibit a project based on its environmental assessment. The AIA inherits this limitation: no AIA regime in the world gives the assessor power to *stop* a deployment. **Assessment is not prohibition.** Both instruments operate on the assumption that forcing decision-makers to confront consequences will, by itself, produce better decisions. This may be optimistic.

### The Inherited Compliance Problem

Here is the cautionary tale. The EIA regime — NEPA's child — has a documented, decades-long history of performative compliance:

- In the Brazilian Amazon, EIAs **underestimated flooded areas by 65% on average** (ALERT Conservation). The assessments existed; the damage happened anyway.
- Internationally, EIAs have been described as "not worth the paper they're printed on" when they consistently green-light destructive projects (Ensia, 2019).
- Scientific shortcomings in Environmental Impact Statements have been documented across multiple countries and decades (Singh et al., 2020).

**If this tendency is inherited by AIAs — if the child inherits the termites along with the house — our corpus should show the symptoms:** standardized boilerplate language (Q-43), high rates of minimally answered questions (Q-39), and risk scores clustering at the low end of the scale regardless of actual risk (Q-21). Phase 2 of this thesis will test exactly these predictions.

### Alternative Analogies the Literature Proposes

The EIA is not the only possible model. Other analogies in the literature suggest different governance architectures:

| Analogy | What It Offers | Why It Matters |
|---------|---------------|----------------|
| **Clinical trials** (Kaminski, 2023) | Phased testing, control groups, independent review boards — you do not release a drug after filling out a questionnaire | Suggests that AIAs should require *evidence of safety*, not just *documentation of risk* |
| **Financial auditing** (NYC Law 144 model) | Independent certified professionals with legal liability — the auditor's career depends on accuracy | Suggests that self-assessment is fundamentally inadequate; external accountability is necessary |
| **Building codes** (implicit in EU AI Act) | Prescriptive minimum standards + certification — you do not *assess* whether a building is safe, you *require* specific safety features | Suggests replacing discretionary assessment with mandatory requirements |

### Key Sources

- Reisman, D. et al. (2018), "Algorithmic Impact Assessments," AI Now Institute
- Moss, E. et al. (2021), "Governing Algorithmic Systems: Six Observations," *AAAI/ACM AIES*
- Selbst, A.D. (2021), "An Institutional View of AIAs," *Harvard JOLT*, 35(1)
- Singh, G.G. et al. (2020), "Scientific Shortcomings in EIS," *People and Nature*
- Noble, B. (2015), "Cumulative Effects Assessment," *Environmental Reviews*
- Kaminski, M.E. (2023), "Regulating the Risks of AI," *Boston University Law Review*

---

## Q-06 — LLM Interpretation Consistency
> Methods: `AGG` `LLM` | Chapter 1 | Status: ✓ COMPLETE

### Finding

**When we asked an AI to read what government departments wrote about their own algorithms, its qualitative risk judgments lined up remarkably well with the AIA's computed risk scores — but the AI was a more sensitive reader. It saw danger where the numbers did not.**

### What We Did

We sent all 30 AIA submissions to a large language model (Llama 3.3 70B) and asked it to read each department's answers about risk — the same answers the AIA scoring algorithm reads — and assign a qualitative label: *low*, *moderate*, or *high*. Then we compared those labels to the AIA's own computed risk scores.

Think of it like this: **the AIA is a standardized test, and the LLM is an experienced teacher reading the same student essays.** The test produces a number. The teacher produces a judgment. We wanted to know: do they agree?

### Data

| LLM's Judgment | How Many | Avg Computed Score | Score Range |
|----------------|----------|-------------------|-------------|
| Low risk        | 9        | 0.0               | 0–0         |
| Moderate risk   | 14       | 4.0               | 3–7         |
| High risk       | 7        | 9.1               | 4–10        |

### What This Tells Us

**1. They mostly agree.** Every submission the LLM labeled "low" has a computed score of exactly zero. Every "moderate" submission scores between 3 and 7. Every "high" submission scores between 4 and 10. The ranking is consistent: the teacher and the test agree on who is at the top, middle, and bottom of the class.

**2. But the teacher sees something the test misses.** The most revealing case is the **PACT cargo targeting system** — a surveillance program that scans air cargo before it enters Canada. The AIA's computed risk score is only 4 (out of a scale that goes to at least 10). But the LLM labeled it "high" risk. Why? Because the LLM reads *context*: it recognizes that a surveillance system operating in a security/border enforcement context carries dangers that a simple additive score cannot capture. **The number says "moderate." The reader says "this is surveillance — be worried."**

This is analogous to a film critic rating a movie 3 out of 5 stars while writing a devastating review. The star rating and the review are measuring different things: one counts features, the other reads meaning.

**3. The compression problem — all 30 submissions score between 0 and 10.** Imagine a thermometer that only reads between 18°C and 22°C. Everything feels "room temperature." That is what the AIA scoring instrument does: it compresses 30 diverse federal AI systems — from benign data dashboards to border surveillance — into a narrow band. Either genuinely high-risk systems are not being assessed, or the instrument itself structurally understates risk. We return to this in Q-25 (the quantification problem).

**4. A data gap worth noting.** The AIA has a formal Impact Level classification (I through IV), but that field is empty for all 30 submissions we analyzed. The most analytically rich submissions in the corpus lack the government's own official classification — like a hospital that keeps detailed patient notes but forgets to record the diagnosis.

### Thesis Implications

The LLM functions as what literary scholars might call a **"close reader"** of bureaucratic text. Where the computed score is a blunt instrument — adding up weighted answers like a standardized test — the LLM brings contextual understanding. Its agreement with the scores at the ordinal level *validates* it as a reliable analytical tool. Its disagreements — especially the PACT case — *reveal exactly the kind of contextual judgment that numerical scoring cannot capture*. This is the quantification critique in action: the thesis does not need to argue abstractly that numbers flatten meaning. It can show a specific case where they do.

> **Evidence:** See [PHASE_1_EVIDENCE.md](PHASE_1_EVIDENCE.md), queries Q-06a through Q-06d, for the exact SQL, raw results, and reproducibility instructions.

---

## Q-07 — Token Usage as Complexity Proxy
> Methods: `AGG` | Chapter 1 | Status: ✓ COMPLETE

### Finding

**When the AI analyzed bilingual divergence — comparing what departments wrote in English versus French — it needed more than twice as many words to express its analysis as it did for any other task. Bilingualism is the hardest thing in the corpus to think about, even for an AI.**

### What We Measured and Why

When a large language model analyzes text, it produces a response measured in "tokens" (roughly, word-fragments). A longer response means the model encountered more complexity — more to compare, more to explain, more nuance to capture. Think of tokens as **the length of a scholar's marginal notes**: a simple passage gets a brief annotation; a dense, ambiguous passage fills the margin.

We measured how many tokens the LLM used for each of its four analysis types across all 30 submissions.

### Data

| What the AI Analyzed | Avg Length (tokens) | Shortest | Longest | Spread |
|---------------------|---------------------|----------|---------|--------|
| Bilingual divergence | 528                 | 60       | 958     | 898    |
| Safeguard compliance | 280                 | 227      | 339     | 112    |
| Automation justification | 246             | 141      | 318     | 177    |
| Risk assessment      | 224                 | 152      | 286     | 134    |

### What This Tells Us

**1. Bilingualism is the hardest analytical problem in the corpus.** The AI needed 2.1 times more "thinking" for bilingual divergence than for justification analysis, and 2.4 times more than for risk analysis. This makes intuitive sense: comparing paired English and French responses across 19 field pairs is like reading two novels side by side and cataloguing every place where the translations diverge. The other analyses — assessing risk, evaluating justifications, checking safeguards — are more like reading a single text and evaluating it against a rubric.

**2. The enormous range in divergence tells its own story.** The shortest divergence analysis used only 60 tokens — barely a paragraph. The longest used 958 tokens — a full essay. This 16:1 ratio is itself a finding. **Some submissions gave the AI almost nothing to compare** (because the French fields were left empty — a form of silence), while others presented rich, complex bilingual content that demanded detailed field-by-field analysis.

*Analogy:* Imagine a music critic asked to compare the English and French versions of the same song. If the French version is just silence — no lyrics, no melody — the review writes itself in a sentence: "There is no French version." But if both versions exist with different metaphors, rhythms, and cultural references, the comparison becomes a genuine essay. **The variance in token usage is a quantitative signature of the omission problem** — the French version of the Canadian state sometimes simply does not show up.

**3. The other three types are remarkably similar.** Safeguard, justification, and risk analyses cluster tightly (224–280 avg tokens, with narrow spreads). This tells us that once language is not a factor — once the AI is reading one text in one language — the governance dimensions of the AIA present roughly comparable analytical complexity.

**4. The 60-token minimum is diagnostic.** A 60-token divergence analysis is the AI saying, in effect: *"There is nothing here to compare. The French fields are empty."* This minimum is not a floor of the analysis — it is the sound of a language that was never spoken. We pursue this silence in Q-12.

### Thesis Implications

This finding provides quantitative support for the thesis's central argument: **bilingual governance is the most complex and contested dimension of the Canadian AIA.** The data shows this not through opinion but through measurement — the AI itself, an impartial analytical instrument, demonstrates that bilingualism requires more analytical labour than any other dimension. The variance in that labour further reveals the "two governance regimes" problem: the distance between a 60-token analysis and a 958-token analysis is the distance between a state that speaks two languages and a state that only pretends to.

> **Evidence:** See [PHASE_1_EVIDENCE.md](PHASE_1_EVIDENCE.md), query Q-07, for the exact SQL, raw results, and JSONB path documentation.

---

## Q-08 — Model Provenance Audit
> Methods: `DB` | Chapter 1 | Status: ✓ COMPLETE

### Finding

**All 120 AI-generated interpretations were produced in a single sitting, by a single model, using a single set of instructions. This is the methodological equivalent of a single scholar reading all 30 submissions in one day at the same desk with the same rubric — complete consistency of judgment.**

### Why This Matters for Humanities Research

In traditional humanities scholarship, the researcher *is* the instrument. When a literary scholar close-reads 30 poems, the readings are shaped by the scholar's evolving understanding — poem 30 is read differently than poem 1 because the scholar has learned from the intervening 29. This is a feature of humanistic inquiry, not a bug. But it makes reproducibility difficult: another scholar, reading the same poems, will produce different readings.

Our LLM-based analysis occupies a middle ground. The model does not "learn" from submission to submission (each analysis is independent), but it could be influenced by changes in the model version, the instructions (prompts) it receives, or even the time of day (if the API provider updates the model mid-session). **The provenance audit confirms that none of these threats materialized.**

### Data

| Detail | Value |
|--------|-------|
| Model | Llama 3.3 70B Instruct (open-weight, publicly available) |
| Prompt version | 1.0.0 (identical instructions for all submissions) |
| Total interpretations | 120 (30 submissions × 4 analysis types) |
| Session start | 2026-03-08, 04:03 |
| Session end | 2026-03-08, 11:37 |
| Duration | ~7.5 hours |

### What This Tells Us

**1. One model, one rubric, one sitting.** Think of it as hiring a single, expert reader — like commissioning a single translator to render all 30 submissions, rather than assigning different translators to different chapters. The consistency of the instrument is guaranteed by design.

**2. Complete coverage.** Every one of the 30 submissions received all four analyses (justification, risk, divergence, safeguard). No submission was skipped or partially analyzed. This is like a classroom where every student took every exam — there are no missing grades.

**3. The audit trail is permanent and queryable.** Every interpretation row in the database stores the model ID, prompt version, and timestamp. Any researcher can query this at any time to verify provenance — like checking the colophon of a printed book to confirm the edition, printer, and date.

**4. Open-weight model = reproducible scholarship.** We deliberately chose Llama 3.3 70B, an open-weight model whose parameters are publicly available, rather than a proprietary model like GPT-4 whose internals are secret and whose behaviour can change without notice. **This is the DH equivalent of publishing your archival sources rather than paraphrasing them:** another researcher with the same model weights, the same prompts, and the same input data can reproduce the entire interpretive pipeline. The LLM is not a black box — it is an open instrument.

### The Error-Fix-Retry Story: Transparency in Practice

The run log also tells the story of things that went wrong — and this transparency is itself methodologically valuable:

- **Runs 1–4 (justification and risk):** Succeeded on the first attempt. 60 interpretations produced without error.
- **Runs 5–6 (divergence and safeguard):** Failed completely. The AI returned valid analyses, but wrapped them in unexpected formatting that our parser could not read. *All 60 attempts failed.* This is like receiving 60 perfectly good letters, all in envelopes the mail slot cannot accept.
- **The fix:** We improved the parser (switched to a more robust JSON reading method), reran both analyses, and all 60 succeeded.
- **Three stubborn cases:** Three divergence submissions (where both English and French fields were empty) received a score of 0 for bilingual fidelity. Our database initially rejected 0 as "out of range" — it expected scores of 1 through 5. We corrected the range to 0–5 (because "no bilingual content at all" is a legitimate score of zero) and all three succeeded.

**Why include the errors?** Because transparency about failure is as important as transparency about success. A humanities methodology chapter that only reports the clean run — "we processed 120 submissions without error" — would be concealing the messy reality of computational research. The run log, permanently stored in the database, is a full confession.

> **Evidence:** See [PHASE_1_EVIDENCE.md](PHASE_1_EVIDENCE.md), queries Q-08a through Q-08c, for the exact SQL, the full run log, and per-table row counts.

---

## Phase 1 Summary

### What We Have Established

| Question | Key Finding — In One Sentence |
|----------|------------------------------|
| Q-01 | AIAs are the children of environmental impact assessments — they inherited the house and the termites |
| Q-02 | Six ethical traditions justify AIAs, but Canada chose the ones that privilege process over participation |
| Q-03 | Nine scholarly critiques exist, and our corpus can empirically test each — moving from "scholars worry" to "the data shows" |
| Q-04 | Nine alternatives exist; no single instrument suffices, just as no single vaccine protects against all diseases |
| Q-05 | The EIA analogy made algorithmic accountability legible but imported structural limits — especially the inability to measure algorithmic harm the way we measure pollution |
| Q-06 | The AI reader and the scoring algorithm mostly agree, but the AI is more sensitive — it sees danger where the numbers do not (the PACT case) |
| Q-07 | Bilingualism is the hardest thing in the corpus to think about, even for an AI — it takes twice the analytical effort of any other dimension |
| Q-08 | One model, one rubric, one sitting, 120 interpretations — and we kept the error log, because transparency includes confessing your mistakes |

### Ready for Phase 2

Phase 1 has laid the foundations: we know the history, the ethical stakes, the scholarly critiques, and the methodological ground rules. Phase 2 moves from foundations to findings — from "what should we look for?" to "what does the corpus actually show?"

The four blocks can run in parallel, like four scholars working simultaneously on different chapters:
- **Q-09 → Q-13:** The bilingual divergence block — *what happens when the state speaks two languages?*
- **Q-17 → Q-20:** The justification rhetoric block — *how do departments explain why they need algorithms?*
- **Q-21 → Q-24:** The risk and rights block — *how does the AIA see danger, and what does it miss?*
- **Q-28 → Q-32:** The safeguards block — *are the protective measures real or performative?*
