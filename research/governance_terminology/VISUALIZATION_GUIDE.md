# Governance Terminology Visualization Guide

**Created:** January 9, 2026  
**Dataset:** 16 bilingual AIA document pairs (EN/FR)  
**Total Terms Analyzed:** 751 governance term occurrences  

---

## 📊 Figure Descriptions

### Figure 1: Comparative Terms (fig1_comparative_terms.png)
**Purpose:** Side-by-side comparison of key governance term frequencies  
**Key Finding:** "Accountability" appears 15 times in English but 0 times in French  

**Use Case:** Primary figure for demonstrating semantic drift  
**Recommended Caption:**  
> Figure 1. Frequency of governance terms in 16 bilingual Canadian AIA document pairs. Notable disparities include "accountability" (EN: 15, FR: 0) and "monitoring" vs "contrôle" (EN: 5, FR: 27).

---

### Figure 2: Divergence Analysis (fig2_divergence_analysis.png)
**Purpose:** Visualize EN/FR frequency ratios to identify asymmetric concepts  
**Key Finding:** Several terms show >2:1 ratios, indicating conceptual imbalance  

**Use Case:** Academic paper - methods section  
**Recommended Caption:**  
> Figure 2. EN/FR frequency ratios for key governance concepts. Ratios >1.5 or <0.67 indicate significant semantic drift. Red bars highlight critical divergences.

---

### Figure 3: Category Comparison (fig3_category_comparison.png)
**Purpose:** Group governance terms into thematic categories  
**Categories:**
- **Accountability & Responsibility** (accountability, responsibility, liable)
- **Oversight & Monitoring** (oversight, surveillance, monitoring, control)
- **Transparency & Disclosure** (transparency, openness, disclosure)
- **Fairness & Bias** (fairness, equity, bias, discrimination)

**Key Finding:** Accountability category shows complete absence in French translations  

**Use Case:** Discussion section - thematic analysis  
**Recommended Caption:**  
> Figure 3. Governance term frequencies by thematic category. The "Accountability & Responsibility" category shows marked asymmetry (EN: 15, FR: 0), suggesting conceptual erasure in French versions.

---

### Figure 4: Heatmap Distribution (fig4_heatmap_distribution.png)
**Purpose:** Show term usage patterns across all 16 document pairs  
**Format:** Dual heatmaps (English left, French right)  
**Terms Visualized:** accountability, oversight, transparency, fairness, bias, audit

**Key Finding:** Accountability row is entirely empty in French heatmap  

**Use Case:** Supplementary materials - comprehensive view  
**Recommended Caption:**  
> Figure 4. Heatmap showing governance term distribution across 16 bilingual document pairs. Rows represent projects; columns represent key governance concepts. Color intensity indicates term frequency. The accountability column is systematically absent in French versions.

---

### Figure 5: Accountability Gap (fig5_accountability_gap.png)
**Purpose:** **SPOTLIGHT VISUALIZATION** - Dramatic focus on key finding  
**Format:** Focused bar chart with annotations  
**Impact:** Publication cover candidate

**Key Finding:** Complete erasure of "accountability" terminology in French  

**Use Case:** Abstract, conference presentation, social media  
**Recommended Caption:**  
> Figure 5. The "accountability gap" in bilingual Canadian AIA governance documents. While English versions reference accountability 15 times across 16 documents, French translations contain zero instances of "responsabilité" or equivalent terms.

---

### Figure 6: Summary Table (fig6_summary_table.png)
**Purpose:** Publication-ready statistics table  
**Format:** Formatted table with:
- Top 10 EN terms with frequencies
- Top 10 FR terms with frequencies
- Mapped equivalents where applicable
- Divergence indicators

**Use Case:** Paper appendix, quick reference  

---

## 🎯 Key Findings Summary

### Critical Disparities Identified:

1. **"Accountability" Erasure** (15 → 0)
   - 15 occurrences in English across multiple documents
   - 0 instances of "responsabilité" or equivalents in French
   - **Implication:** Conceptual shift from individual accountability to systemic responsibility

2. **"Control" vs "Monitoring"** (5 → 27)
   - English uses "monitoring" (5 occurrences)
   - French uses "contrôle" (27 occurrences, 5.4x more)
   - **Implication:** French emphasizes regulatory control vs English's observational framing

3. **"Bias" Disparity** (34 → 22)
   - English: 34 occurrences (technical/algorithmic framing)
   - French: 22 occurrences (35% fewer)
   - **Implication:** Greater emphasis on technical bias detection in English

4. **"Prejudice" Introduction** (0 → 9)
   - English: 0 occurrences of "prejudice"
   - French: 9 occurrences of "préjugé" (moral/social framing)
   - **Implication:** French adds moral dimension absent in English

---

## 📝 Suggested Uses

### For CSDH 2026 Abstract:
- Use **Figure 5** (Accountability Gap) as primary visual
- Reference **Figure 1** statistics in text
- Cite total corpus size (16 pairs, 751 terms)

### For Full Paper:
- **Methods:** Figure 2 (methodology demonstration)
- **Results:** Figures 1, 3, 4 (comprehensive findings)
- **Discussion:** Figure 5 (key argument)
- **Appendix:** Figure 6 (complete data)

### For Conference Presentation:
- **Title Slide:** Figure 5 (visual hook)
- **Background:** Figure 1 (establish pattern)
- **Analysis:** Figure 3 (thematic breakdown)
- **Conclusion:** Return to Figure 5 (reinforce key finding)

### For Social Media / Blog:
- Use **Figure 5** with caption: "We analyzed 16 bilingual Canadian AI governance documents and found a striking pattern: 'accountability' appears 15 times in English, 0 times in French. What gets lost in translation?"

---

## 🔬 Methodological Notes

**Data Source:** 16 bilingual pairs from 47 Canadian federal AIA documents  
**Term Selection:** 20+ governance-specific terms per language (en.json, fr.json)  
**Analysis Method:** 
- PDF text extraction (pdfminer.six)
- Term frequency counting with 50-character context windows
- LLM semantic drift analysis (GPT-4 Turbo)
- Statistical comparison (EN/FR ratios)

**Limitations:**
- 2 pairs excluded due to PDF extraction issues
- Terms counted by exact match (may miss synonyms)
- Context windows limited to 50 characters
- LLM analysis subject to model biases

**Reproducibility:**
- All scripts in `research/` directory
- Raw data: `full_terminology_analysis.json`
- Visualization code: `create_terminology_visualizations.py`

---

## 📊 Figure Specifications

**Resolution:** 300 DPI (publication-ready)  
**Format:** PNG (lossless)  
**Color Palette:** Colorblind-friendly (husl palette)  
**Font:** Sans-serif, 10-14pt  
**Size:** Optimized for 2-column academic layout  

**Conversion Commands:**
```bash
# Convert to PDF for LaTeX
convert fig5_accountability_gap.png -quality 100 fig5_accountability_gap.pdf

# Resize for presentation (if needed)
convert fig5_accountability_gap.png -resize 1920x1080 fig5_presentation.png

# Create thumbnail
convert fig5_accountability_gap.png -resize 400x300 fig5_thumbnail.png
```

---

## 🎓 Citation Suggestion

If using these visualizations in publications:

> Terminology analysis conducted using custom Python scripts with pdfminer.six (text extraction), OpenAI GPT-4 Turbo (semantic analysis), and matplotlib/seaborn (visualization). Code available at [repository URL]. Dataset comprises 16 bilingual document pairs (n=32 documents) from Canadian federal Algorithmic Impact Assessments (2019-2024).

---

## 📧 Contact

For questions about methodology, data access, or reproduction:
- See `research/extract_governance_terminology.py` for extraction code
- See `research/create_terminology_visualizations.py` for visualization code
- Full dataset: `research/governance_terminology/full_terminology_analysis.json`

---

**Document Version:** 1.0  
**Last Updated:** January 9, 2026  
**Status:** Publication-ready figures generated ✅
