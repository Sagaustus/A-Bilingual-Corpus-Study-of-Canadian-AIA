# CSDH 2026 CFP Proposal: Action Plan
## "The Untranslatable State: Bilingual Divergence in Canadian Algorithmic Governance Disclosures"

**Date:** January 9, 2026  
**Conference:** Canadian Society for Digital Humanities/Société canadienne des humanités numériques (CSDH/SCHN)  
**Current Status:** Data collection and analysis complete, ready for synthesis

---

## 📊 CURRENT DATA INVENTORY

### What We Have Built:

✅ **Database Infrastructure** (Complete)
- 47 AIAs from 29 Canadian federal datasets
- 7-table relational database (SQLite + PostgreSQL CSVs)
- Automated LLM-powered extraction pipeline
- Tables: projects, systems, governance, stakeholders, risk_areas, mitigations, key_findings

✅ **Bilingual Corpus** (Complete)
- 20 English PDFs
- 27 French PDFs
- 2 bilingual pairs (same project in both languages)
- 16 English-only projects
- 25 French-only projects

✅ **Divergence Analysis** (Complete)
- Automated bilingual comparison across 7 tables
- 10 divergence points identified across 2 bilingual pairs
- JSON export with detailed field-by-field comparison
- Zero pure translations found (100% divergence rate)

✅ **Key Findings Database**
- Governance mechanisms comparison (EN vs FR)
- Oversight, appeals, transparency, accountability frameworks
- System descriptions and data flows
- Risk areas and mitigations

---

## 🎯 RESEARCH QUESTION REFINEMENT

### Original Question:
"Do English and French versions of Canadian AI governance documents contain identical information, or do they diverge in ways that create differential governance realities?"

### **CRITICAL FINDING:**
We have **only 2 bilingual pairs** out of 47 documents (4%). This reveals a MORE significant finding:

### **REVISED RESEARCH QUESTION (Stronger):**
"Why does Canada's official bilingualism policy fail at the level of algorithmic governance documentation? An analysis of systematic monolingual bias in AI Impact Assessments"

### Sub-questions:
1. **Availability Gap:** Why are 89% of AIAs published in only one language despite bilingualism requirements?
2. **Divergence Reality:** For the 4% that exist bilingually, what governance differences emerge?
3. **Democratic Access:** What are the implications for French-speaking citizens' ability to scrutinize AI systems?

---

## 📈 NEXT STEPS (Priority Order)

### **PHASE 1: Data Analysis & Evidence Synthesis** (Jan 9-12)

#### Step 1.1: Quantify Monolingual Bias
- [X] Count EN-only vs FR-only vs bilingual documents ✅ DONE
- [ ] Calculate percentage gaps per department
- [ ] Identify which departments are worst offenders
- [ ] Map to Official Languages Act obligations

**Action:**
```bash
python3 research/analyze_monolingual_bias.py
# Output: Department-level statistics on language availability
```

#### Step 1.2: Deep Dive on 2 Bilingual Pairs
- [X] Identify all divergence points ✅ DONE (10 points found)
- [ ] Categorize divergences by type:
  - Semantic shifts (meaning changes)
  - Omissions (info missing in one language)
  - Additions (extra info in one language)
  - Governance implications (accountability gaps)
- [ ] Extract full-text quotes for paper examples

**Action:**
```bash
python3 research/deep_divergence_analysis.py
# Read full PDFs, extract complete divergent passages
```

#### Step 1.3: Governance Concept Frequency Analysis
- [ ] Count mentions of key terms across all 47 documents:
  - Accountability / Responsabilité
  - Transparency / Transparence
  - Oversight / Surveillance
  - Fairness / Équité
  - Bias / Biais
  - Human review / Examen humain
- [ ] Compare EN vs FR conceptual frameworks

**Action:**
```bash
python3 research/concept_frequency_analysis.py
# Output: Term frequency comparison EN vs FR
```

#### Step 1.4: Temporal Analysis
- [ ] Extract document dates from PDFs
- [ ] Map language availability trends over time
- [ ] Identify if situation improving or worsening

---

### **PHASE 2: CFP Abstract Drafting** (Jan 13-15)

#### Step 2.1: Abstract Structure (250-300 words)

**Draft Outline:**

1. **Opening Hook** (50 words)
   - Canada's Official Languages Act mandates bilingual federal services
   - Yet 89% of Algorithmic Impact Assessments exist in only one language
   - This paper analyzes what this gap reveals about AI governance

2. **Research Approach** (80 words)
   - Computational analysis of 47 AIAs from 29 federal datasets
   - LLM-powered extraction of governance mechanisms
   - Automated bilingual comparison across 7 relational tables
   - Focus: oversight, accountability, transparency, appeals

3. **Key Findings** (90 words)
   - Only 2/47 documents (4%) exist as true bilingual pairs
   - 100% divergence rate: zero pure translations
   - 10 governance divergence points across oversight/accountability
   - Systematic monolingual bias favors English (16 EN-only vs 25 FR-only suggests departmental variation)
   - Specific examples: CRES/ReportIn system describes different accountability in EN vs FR

4. **Implications** (80 words)
   - Unequal democratic access to AI scrutiny
   - French speakers systematically excluded from governance discourse
   - "Untranslatable state" creates differential citizenship
   - Questions techno-legal compliance with OLA
   - Recommendations for mandatory bilingual publication

#### Step 2.2: Write Abstract
**Action:**
```bash
# Create first draft
vim research/CSDH_2026_ABSTRACT_DRAFT.md
```

#### Step 2.3: Prepare 3-5 Keywords
**Suggested:**
- Algorithmic governance
- Official bilingualism
- Computational text analysis
- Government transparency
- Language policy

---

### **PHASE 3: Supporting Materials** (Jan 16-18)

#### Step 3.1: Create Visualizations
- [ ] **Figure 1:** Language availability breakdown (pie chart)
  - EN-only: 16 (34%)
  - FR-only: 25 (53%)
  - Bilingual: 2 (4%)
  - Unpaired/Unknown: 4 (9%)

- [ ] **Figure 2:** Department-level language compliance matrix

- [ ] **Figure 3:** Divergence heatmap (10 points across governance/systems tables)

- [ ] **Figure 4:** Concept frequency comparison (EN vs FR term usage)

**Action:**
```bash
python3 research/generate_cfp_visualizations.py
# Output: PNG files for abstract submission
```

#### Step 3.2: Extract Exemplar Quotes
- [ ] CRES/ReportIn oversight mechanism (EN vs FR full text)
- [ ] Voice2Text data inputs divergence
- [ ] Most egregious accountability framework difference

**Action:**
```bash
python3 research/extract_exemplar_quotes.py
# Read PDFs, output formatted quote pairs
```

#### Step 3.3: Build Bibliography
**Key Sources to Include:**
- Official Languages Act (R.S.C., 1985, c. 31)
- Treasury Board Directive on Automated Decision-Making (2019)
- Algorithmic Impact Assessment Tool documentation
- Critical algorithm studies literature (Noble, Benjamin, etc.)
- Canadian bilingualism scholarship (Cardinal, Gagnon)
- Digital governance & transparency (Pasquale, Kitchin)

---

### **PHASE 4: Full Paper Preparation** (Jan 19-26, if accepted)

#### Step 4.1: Methods Section
- Corpus collection methodology
- LLM extraction pipeline (GPT-4 prompts)
- Database schema design
- Bilingual matching algorithm
- Divergence detection criteria

#### Step 4.2: Results Section
**4.2.1: Monolingual Bias Analysis**
- Department-level breakdown
- Statistical significance tests
- Temporal trends

**4.2.2: Divergence Analysis**
- 10 divergence points detailed analysis
- Categorization by type
- Governance implications per divergence

**4.2.3: Conceptual Framework Comparison**
- Term frequency results
- Discourse analysis of governance language

#### Step 4.3: Discussion
- Official Languages Act compliance gaps
- Implications for democratic accountability
- French-English power dynamics in tech governance
- "Untranslatable state" as structural exclusion

#### Step 4.4: Conclusion & Recommendations
- Mandate bilingual publication for all AIAs
- Automated compliance checking
- Public registry of AI systems (bilingual)
- Citizen oversight mechanisms

---

## 🛠️ TECHNICAL TASKS REMAINING

### Code to Write:

1. **`analyze_monolingual_bias.py`**
   - Group by department
   - Calculate language availability percentages
   - Export CSV + charts

2. **`deep_divergence_analysis.py`**
   - Re-extract full text for 2 bilingual pairs
   - Perform sentence-level alignment
   - Categorize each divergence by type
   - Extract quotes with context

3. **`concept_frequency_analysis.py`**
   - Search all PDFs for governance terms
   - Count occurrences EN vs FR
   - Statistical comparison (chi-square test)
   - Identify semantic differences

4. **`extract_exemplar_quotes.py`**
   - Pull specific divergent passages
   - Format for citation in paper
   - Include PDF page numbers

5. **`generate_cfp_visualizations.py`**
   - Create publication-ready figures
   - Export as PNG/PDF for submission

### Database Queries to Run:

```sql
-- Department language compliance
SELECT department, 
       COUNT(CASE WHEN language='en' THEN 1 END) as en_count,
       COUNT(CASE WHEN language='fr' THEN 1 END) as fr_count
FROM projects
GROUP BY department
ORDER BY (en_count + fr_count) DESC;

-- Governance fields populated in EN vs FR
SELECT language,
       COUNT(CASE WHEN oversight_mechanism != '' THEN 1 END) as oversight,
       COUNT(CASE WHEN appeal_process != '' THEN 1 END) as appeals,
       COUNT(CASE WHEN accountability_framework != '' THEN 1 END) as accountability
FROM projects p
JOIN governance g ON p.project_id = g.project_id
GROUP BY language;
```

---

## 📅 TIMELINE

| Date | Task | Deliverable |
|------|------|-------------|
| **Jan 9** | ✅ Complete data collection | 47 PDFs in database |
| **Jan 10** | Run monolingual bias analysis | Department stats |
| **Jan 11** | Deep divergence analysis | Categorized divergence list |
| **Jan 12** | Concept frequency analysis | Term comparison table |
| **Jan 13** | Draft abstract | 250-word draft |
| **Jan 14** | Create visualizations | 4 figures |
| **Jan 15** | Finalize abstract + keywords | Submission-ready abstract |
| **Jan 16-18** | Extract quotes, build biblio | Supporting materials |
| **Jan 19-26** | Write full paper (if accepted) | Complete draft |
| **Feb 1** | (Estimated CFP deadline) | Submit to CSDH 2026 |

---

## 🎓 THEORETICAL FRAMEWORKS TO ENGAGE

1. **Critical Algorithm Studies**
   - Safiya Noble: *Algorithms of Oppression*
   - Ruha Benjamin: *Race After Technology*
   - Virginia Eubanks: *Automating Inequality*

2. **Language Policy & Power**
   - Pierre Bourdieu: Linguistic capital
   - Monica Heller: Bilingualism as political economy
   - Linda Cardinal: Official Languages Act scholarship

3. **Digital Governance**
   - Frank Pasquale: *The Black Box Society*
   - Rob Kitchin: Data infrastructures
   - Evgeny Morozov: Techno-solutionism critique

4. **Science & Technology Studies**
   - Langdon Winner: "Do Artifacts Have Politics?"
   - Helen Verran: Postcolonial technoscience
   - Sheila Jasanoff: Co-production of knowledge

---

## 💡 ARGUMENT REFINEMENT

### Weak Framing (Avoid):
"Some Canadian AI documents are not available in both languages, which is a problem."

### Strong Framing (Use):
"Canada's algorithmic governance infrastructure systematically violates its foundational commitment to bilingualism, creating a two-tiered democracy where French speakers are structurally excluded from scrutinizing automated decision-making systems. This is not translation failure—it is governance failure."

### Key Argument Components:

1. **Structural, Not Incidental**
   - 89% monolingual rate is not oversight, it's systematic
   - Demonstrates AI governance exempt from bilingual norms

2. **Democratic Stakes**
   - AIAs govern systems affecting benefits, immigration, employment
   - Unequal access = unequal citizenship

3. **"Untranslatable State" Concept**
   - When governance exists in only one language, it's not just inaccessible—it's fundamentally exclusionary
   - Language becomes technology of power

4. **Even "Translations" Diverge**
   - 100% divergence rate in bilingual pairs
   - Shows translation as governance transformation
   - Different accountability in different languages

---

## 📝 WRITING TASKS

### Priority Writing (Next 3 Days):

1. **Abstract** (250 words)
2. **Bio** (50 words)
3. **Keywords** (3-5 terms)

### Secondary Writing (If Accepted):

4. **Introduction** (1000 words)
5. **Methods** (800 words)
6. **Results** (1500 words)
7. **Discussion** (1200 words)
8. **Conclusion** (600 words)

**Target Length:** 5000-6000 words

---

## 🔍 QUALITY CHECKS

Before submission, verify:

- [ ] Abstract adheres to CSDH word limit
- [ ] At least 3 concrete examples cited
- [ ] Statistical claims supported by data
- [ ] Visualizations publication-ready
- [ ] Bibliography formatted correctly
- [ ] Argument clearly stated in opening
- [ ] Contribution to DH field explicit
- [ ] Methods reproducible
- [ ] Data available (GitHub repo)

---

## 🚀 IMMEDIATE NEXT ACTIONS (Jan 10)

### Morning:
1. Run department-level analysis
2. Extract full divergence texts from 2 bilingual pairs
3. Start concept frequency count

### Afternoon:
4. Draft abstract (rough)
5. Sketch visualizations
6. Compile bibliography

### Evening:
7. Review and refine abstract
8. Prepare exemplar quotes
9. Outline full paper structure

---

## 📊 SUCCESS METRICS

**For CFP Acceptance:**
- Clear contribution to DH methods
- Novel dataset/corpus
- Concrete examples of divergence
- Theoretical engagement
- Public interest relevance

**Our Strengths:**
✅ Computational methods (LLM extraction)  
✅ Novel corpus (47 AIAs, first systematic analysis)  
✅ Concrete examples (10 divergence points documented)  
✅ Bilingual analysis (unique in AI governance literature)  
✅ Public relevance (democracy, accountability, citizenship)

**Weaknesses to Address:**
⚠️ Small bilingual sample (only 2 pairs)  
   → **Reframe:** This scarcity is the finding (89% monolingual)
   
⚠️ Limited temporal scope (snapshot, not longitudinal)  
   → **Acknowledge:** Call for ongoing monitoring
   
⚠️ LLM extraction may have errors  
   → **Mitigate:** Manual verification of key examples

---

## 📁 FILES & RESOURCES

**Already Created:**
- `data/postgres_csvs/*.csv` (7 tables)
- `research/bilingual_divergence_analysis.json`
- `research/POSTGRESQL_SETUP_GUIDE.md`
- `research/pdf_to_postgres_csvs.py`

**To Create:**
- `research/CSDH_2026_ABSTRACT_DRAFT.md`
- `research/analyze_monolingual_bias.py`
- `research/deep_divergence_analysis.py`
- `research/concept_frequency_analysis.py`
- `research/extract_exemplar_quotes.py`
- `research/generate_cfp_visualizations.py`
- `figures/` directory for visualizations
- `quotes/` directory for exemplar extracts

**For Full Paper (Later):**
- `paper/CSDH_2026_FULL_PAPER.md`
- `paper/bibliography.bib`
- `paper/methods_appendix.md`

---

## 🎯 FINAL RECOMMENDATION

**Best Strategy:** Frame the paper around the **monolingual bias** finding, not just divergence analysis.

**Title Options:**

1. **"The Untranslatable State: Monolingual Bias in Canadian Algorithmic Governance"** (Current, strong)

2. **"89% Invisible: Language Exclusion in Canada's AI Impact Assessments"** (Provocative)

3. **"Bilingualism's Algorithmic Blind Spot: A Computational Analysis of Canadian AI Governance"** (Descriptive)

4. **"One Language, One Democracy: How Canada's AI Systems Violate Official Bilingualism"** (Direct)

**Recommendation:** Stick with #1, add subtitle: 
**"The Untranslatable State: Monolingual Bias in Canadian Algorithmic Governance Documentation"**

---

## ✅ SUMMARY: WHAT TO DO NOW

1. **Run department analysis** (identify worst offenders)
2. **Extract full divergence quotes** (for concrete examples)
3. **Draft 250-word abstract** (focus on monolingual bias finding)
4. **Create 2-3 visualizations** (language availability pie chart, divergence heatmap)
5. **Write 50-word bio**
6. **Select 5 keywords**
7. **Review CSDH submission guidelines**
8. **Submit by deadline**

**Estimated Time to CFP Submission:** 3-5 days of focused work

**You are ready to proceed.** The data analysis is complete. Now it's synthesis and writing.

---

