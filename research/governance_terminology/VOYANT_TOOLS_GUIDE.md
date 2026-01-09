# Using Voyant Tools & Spyral for Bilingual Semantic Drift Analysis

## Overview

Voyant Tools (https://voyant-tools.org) and Spyral (its notebook environment) are powerful platforms for analyzing your bilingual terminology data. This guide shows how to leverage them for your CSDH 2026 paper on semantic drift in AI Impact Assessments.

---

## 🎯 **Key Analysis Methods for Your Research**

### **1. Concordance Analysis (Keywords in Context)**

**Goal:** Find how "accountability" appears in EN vs how "responsabilité"/"reddition de comptes"/"imputabilité" appear in FR

**Voyant Tool:** `Contexts` panel

**Method:**
1. Upload your XML file to https://voyant-tools.org
2. Click on `Contexts` tool
3. Search for: `accountability` (EN corpus) or `responsabilité|reddition|imputabilité` (FR corpus)
4. Export KWIC (Keywords in Context) results as CSV

**What You'll Discover:**
- EN "accountability" appears with: *framework*, *mechanism*, *ensure*, *governance*
- FR "reddition de comptes" appears with: *mécanisme*, *cadre*, *assurer* (juridical context)
- FR "imputabilité" appears in risk/liability contexts (different semantic field)

**For Your Paper:** Quote these collocational differences to show conceptual drift

---

### **2. Collocations & N-grams**

**Goal:** Identify what words cluster around governance terms

**Voyant Tool:** `Collocates` panel + `Phrases` panel

**Method:**
1. Select term: `accountability` or `monitoring`
2. Set context window: 5 words left/right
3. Compare EN collocates with FR equivalents
4. Extract 2-grams and 3-grams containing key terms

**Expected Findings:**
- EN: "accountability **mechanism**" vs FR: "mécanisme de **reddition de comptes**"
- EN: "**ensure** accountability" vs FR: "**assurer** la reddition de comptes"
- EN: "monitoring **system**" vs FR: "système de **contrôle**" (control, not monitoring!)

**Spyral Code:**
```javascript
// Get collocates for "accountability" in EN corpus
let corpus = await Spyral.Corpus.load("voyant_corpus_en_full.txt");
let table = await corpus.collocates({query: "accountability", context: 5});
table.show();
```

---

### **3. Comparative Corpus Analysis**

**Goal:** Compare term frequencies EN vs FR side-by-side

**Voyant Tool:** `TermsBerry` + `Trends` panels

**Method:**
1. Load both `voyant_corpus_en_full.txt` AND `voyant_corpus_fr_full.txt` as separate documents
2. In `Summary` panel, compare word counts across corpora
3. In `Trends` panel, track how terms distribute across documents
4. Use `TermsBerry` to visualize term clusters

**Spyral Code for Comparative Analysis:**
```javascript
// Load both corpora
let enCorpus = await Spyral.Corpus.load("voyant_corpus_en_full.txt");
let frCorpus = await Spyral.Corpus.load("voyant_corpus_fr_full.txt");

// Compare term frequencies
let enTerms = await enCorpus.terms({query: "accountability", stopList: "auto"});
let frTerms = await frCorpus.terms({query: "responsabilité|reddition|imputabilité", stopList: "auto"});

// Create visualization
enTerms.show();
frTerms.show();
```

---

### **4. Links & Network Analysis**

**Goal:** Visualize semantic relationships between governance concepts

**Voyant Tool:** `Links` panel (word co-occurrence network)

**Method:**
1. Upload XML or TXT corpus
2. Open `Links` tool
3. Filter for governance terms: `accountability, transparency, bias, audit, fairness`
4. Adjust network parameters (minimum frequency, context window)
5. Export graph as PNG or interactive HTML

**What This Shows:**
- EN corpus: "accountability" → "transparency" → "audit" (linear governance chain)
- FR corpus: "reddition de comptes" → "vérification" → "contrôle" (control-centric network)

**For Your Paper:** Network diagram showing divergent conceptual structures

---

### **5. Distribution Patterns (Trends Over Documents)**

**Goal:** See which documents emphasize which terms

**Voyant Tool:** `Trends` panel

**Method:**
1. Load all 16 bilingual pairs as separate documents (use `voyant_pairs/` folder)
2. In `Trends`, search for: `accountability` (EN) and `reddition` (FR)
3. Observe which pairs show spikes
4. Cross-reference with department metadata

**Analysis Question:**
- Do certain departments (TBS, IRCC, ESDC) show more divergence?
- Are implementation-phase AIAs more divergent than planning-phase?

---

### **6. Distinctive Words Analysis**

**Goal:** Identify terms uniquely characteristic of EN vs FR

**Voyant Tool:** `Distinctive Words` feature

**Method:**
1. Create two sub-corpora: all EN pairs vs all FR pairs
2. Use `Distinctive Words` to find terms statistically over-represented in each
3. Sort by TF-IDF or statistical significance

**Expected Results:**
- EN distinctive: `accountability` (15 vs 0), `liable` (16 vs ?)
- FR distinctive: `contrôle` (27 vs 5), `préjugé` (9 vs 0), `suivi` (4 vs ?)

---

## 📊 **Spyral Notebook Workflows**

### **Workflow 1: Extract Accountability Gap Contexts**

```javascript
// Load corpus
let corpus = await Spyral.Corpus.load("full_terminology_analysis.xml");

// Get all contexts containing "accountability"
let accountabilityContexts = await corpus.contexts({
  query: "accountability",
  context: 50 // 50 chars each side
});

// Display as table
accountabilityContexts.show();

// Export as CSV
let csv = accountabilityContexts.toCsv();
Spyral.download(csv, "accountability_kwic.csv");
```

### **Workflow 2: Collocational Strength (PMI)**

```javascript
// Measure how strongly "accountability" associates with nearby words
let corpus = await Spyral.Corpus.load("voyant_corpus_en_full.txt");
let collocates = await corpus.collocates({
  query: "accountability",
  context: 5,
  minRawFreq: 2
});

// Sort by PMI (Pointwise Mutual Information)
collocates.sort("pmi", "descending");
collocates.show();
```

### **Workflow 3: Create Parallel Concordance**

```javascript
// Load bilingual pair
let enDoc = await Spyral.Corpus.load("voyant_pairs/pair_1_en.txt");
let frDoc = await Spyral.Corpus.load("voyant_pairs/pair_1_fr.txt");

// Get parallel contexts
let enContexts = await enDoc.contexts({query: "accountability"});
let frContexts = await frDoc.contexts({query: "responsabilité|reddition|imputabilité"});

// Display side-by-side
Spyral.panel("EN Contexts", enContexts);
Spyral.panel("FR Contexts", frContexts);
```

---

## 🔧 **Data Preparation Tips**

### **Option 1: Use XML Directly**
- Voyant can parse XML and extract text nodes
- Upload `full_terminology_analysis.xml`
- Voyant will treat each `<item>` as a document segment

### **Option 2: Use Pre-Extracted Text Files** (Recommended)
You'll need to create plain text versions of your data:

```python
import json

with open('full_terminology_analysis.json', 'r') as f:
    data = json.load(f)

# Extract all EN governance contexts
en_texts = []
fr_texts = []

for pair in data['pair_analyses']:
    # Get EN document contexts
    if 'llm_semantic_analysis' in pair:
        en_divergences = pair['llm_semantic_analysis'].get('divergence_analysis', '')
        en_texts.append(en_divergences)
    
    # Get FR document contexts
    # ... similar for FR

# Write to files
with open('voyant_en_corpus.txt', 'w') as f:
    f.write('\n\n===DOCUMENT BREAK===\n\n'.join(en_texts))
```

### **Option 3: Use Individual Pair Files**
- Upload the `voyant_pairs/` folder to Voyant (32 files)
- Each file = one document in corpus
- Enables document-level comparisons (e.g., "which pairs show most divergence?")

---

## 📈 **Specific Analyses for CSDH Paper**

### **Analysis 1: Accountability Gap Visualization**

**Steps:**
1. Upload EN corpus → Search `accountability` → Get frequency = 15
2. Upload FR corpus → Search `responsabilité` → Get frequency = 0
3. Search FR corpus for alternatives: `reddition` (11), `imputabilité` (4)
4. Use `Cirrus` word cloud to show FR alternatives visually
5. Export for paper figure

**Paper Caption:**
> "Word cloud showing French translations of 'accountability': while EN uses single term (15×), FR distributes across *reddition de comptes* (11×) and *imputabilité* (4×), reflecting distinct juridical traditions."

---

### **Analysis 2: Monitoring vs Contrôle Semantic Field**

**Spyral Workflow:**
```javascript
// Get collocates for "monitoring" in EN
let enMonitoring = await enCorpus.collocates({query: "monitoring", context: 5});

// Get collocates for "contrôle" in FR
let frControle = await frCorpus.collocates({query: "contrôle", context: 5});

// Compare: EN "monitoring" → passive observation
// FR "contrôle" → active management, verification
```

**Expected Collocates:**
- EN monitoring: *continuous*, *system*, *processes*, *activities*
- FR contrôle: *mesures*, *procédures*, *vérification*, *gestion*

**Paper Argument:**
> "Collocational analysis reveals conceptual divergence: EN *monitoring* (5×) frames oversight as observation, while FR *contrôle* (27×) embeds active regulatory intervention."

---

### **Analysis 3: Bias vs Biais/Préjugé Semantic Split**

**Voyant Analysis:**
1. Search EN corpus: `bias` → 34 occurrences
2. Search FR corpus: `biais` → 22 occurrences, `préjugé` → 9 occurrences
3. Use `Contexts` to compare usage:
   - `biais`: technical/statistical contexts (algorithmic bias)
   - `préjugé`: social/ethical contexts (human prejudice)
4. Extract KWIC examples

**For Your Paper:**
> "French documents lexically distinguish *biais* (algorithmic/technical, 22×) from *préjugé* (social/ethical, 9×), a semantic split absent in English *bias* (34×)."

---

## 🎓 **Advanced Spyral: Custom Divergence Metrics**

### **Calculate Semantic Drift Index**

```javascript
// Define term pairs
let termPairs = [
  {en: "accountability", fr: "responsabilité|reddition|imputabilité"},
  {en: "monitoring", fr: "surveillance|contrôle|suivi"},
  {en: "bias", fr: "biais|préjugé"}
];

// Calculate frequency ratios
let driftScores = [];
for (let pair of termPairs) {
  let enFreq = await enCorpus.terms({query: pair.en}).count();
  let frFreq = await frCorpus.terms({query: pair.fr}).count();
  
  let ratio = enFreq / frFreq;
  driftScores.push({
    term: pair.en,
    enFreq: enFreq,
    frFreq: frFreq,
    ratio: ratio,
    divergence: Math.abs(1 - ratio) // Deviation from 1:1 parity
  });
}

// Display
Spyral.table(driftScores).show();
```

---

## 📚 **Recommended Voyant Tools for Your Project**

| Tool | Purpose | Best For |
|------|---------|----------|
| **Cirrus** | Word cloud | Visualizing accountability gap |
| **Contexts** | KWIC concordance | Extracting quotable examples |
| **Collocates** | Co-occurrence | Finding semantic associations |
| **Trends** | Distribution over docs | Document-level patterns |
| **Links** | Network graph | Conceptual relationship mapping |
| **TermsBerry** | Term clustering | Identifying semantic fields |
| **Correlations** | Statistical correlation | Finding term co-variance |
| **Distinctive Words** | Comparative analysis | EN vs FR unique vocabulary |

---

## 🚀 **Quick Start Workflow**

1. **Go to:** https://voyant-tools.org
2. **Upload:** `full_terminology_analysis.xml` OR the TXT files in `voyant_pairs/`
3. **First Analysis - Accountability Gap:**
   - Open `Contexts` tool
   - Search: `accountability`
   - Note: All contexts are EN (none in FR)
   - Export contexts as CSV
4. **Second Analysis - Collocations:**
   - Open `Collocates` tool
   - Search: `monitoring` (EN) and `contrôle` (FR)
   - Compare collocate networks
5. **Third Analysis - Visualization:**
   - Open `Links` tool
   - Filter for: `accountability, transparency, monitoring, audit, fairness`
   - Export network graph
6. **Export All Results** for your paper appendix

---

## 💡 **Tips for CSDH Presentation**

1. **Live Demo:** Show Voyant analyzing your corpus in real-time (audience engagement)
2. **Interactive Notebook:** Share Spyral notebook URL (reproducible research)
3. **Embed Visualizations:** Export Cirrus/Links as PNG for slides
4. **KWIC Examples:** Project concordance lines showing accountability gap
5. **Comparative Dashboard:** Split screen showing EN Cirrus vs FR Cirrus

---

## 📖 **Further Resources**

- Voyant Tools Documentation: https://voyant-tools.org/docs/#!/guide/start
- Spyral Notebooks: https://voyant-tools.org/spyral/
- Tutorials: https://voyant-tools.org/docs/#!/guide/tutorial
- Gallery Examples: https://voyant-tools.org/docs/#!/guide/gallery

---

## 🎯 **Next Steps**

1. Create clean TXT versions of your data (EN corpus, FR corpus, individual pairs)
2. Upload to Voyant and explore each tool
3. Run Spyral notebooks for custom analyses
4. Export visualizations for CSDH abstract/paper
5. Document methodology in "Methods" section of paper

**Key Argument for Paper:**
> "We employed Voyant Tools' concordance and collocation analysis to trace semantic drift across 16 bilingual pairs, revealing systematic divergence in accountability terminology (EN: *accountability* 15×; FR: *responsabilité* 0×, *reddition de comptes* 11×, *imputabilité* 4×)."
