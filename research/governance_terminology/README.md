# Governance Terminology Analysis - Quick Reference

**Analysis Date:** January 9, 2026  
**Status:** ✅ Complete - Publication Ready

---

## 📊 Visualizations (6 figures)

All visualizations are **300 DPI, publication-ready PNG format**.

**Location:** `research/governance_terminology/figures/`

| File | Description | Use Case |
|------|-------------|----------|
| `fig1_comparative_terms.png` | EN/FR term frequency comparison | Main results figure |
| `fig2_divergence_analysis.png` | EN/FR ratio analysis | Methodology demonstration |
| `fig3_category_comparison.png` | Thematic category breakdown | Discussion section |
| `fig4_heatmap_distribution.png` | Term usage across all 16 pairs | Comprehensive overview |
| `fig5_accountability_gap.png` | **SPOTLIGHT: Accountability erasure** | **Abstract/cover figure** |
| `fig6_summary_table.png` | Summary statistics table | Appendix/reference |

**Quick View:**
```bash
# Open all figures
xdg-open research/governance_terminology/figures/*.png

# Or individually
xdg-open research/governance_terminology/figures/fig5_accountability_gap.png
```

---

## 📁 Data Files

### Primary Analysis Output
- **`full_terminology_analysis.json`** (3,228 lines)
  - Complete term frequencies for 16 document pairs
  - LLM semantic analyses
  - Sample contexts for each term occurrence
  - Summary statistics (EN/FR top terms)

### Comparative Tables
- **`en_fr_terminology_comparison.csv`**
  - Side-by-side term comparison
  - Frequency ratios
  - Import into Excel/R/Python for further analysis

### Narrative Report
- **`semantic_drift_report.md`**
  - Project-by-project findings
  - LLM-identified semantic differences
  - Qualitative interpretations

---

## 📄 Documentation

### Visualization Guide
**`VISUALIZATION_GUIDE.md`** - Complete guide to all 6 figures
- Figure descriptions and captions
- Suggested uses (abstract, paper, presentation)
- Methodological notes
- Citation suggestions

### Key Findings Report
**`KEY_FINDINGS.md`** - Executive summary of analysis
- Critical discoveries (accountability gap, control vs monitoring)
- Category-level analysis
- Cross-cultural governance implications
- Academic implications
- Next steps

### This File
**`README.md`** - Quick reference (you are here!)

---

## 🔬 Analysis Scripts

### Primary Scripts
| Script | Purpose | Output |
|--------|---------|--------|
| `extract_governance_terminology.py` | Extract + analyze terms | JSON, CSV, MD |
| `create_terminology_visualizations.py` | Generate all figures | 6 PNG files |
| `detect_hidden_bilingual_pairs.py` | Find bilingual pairs | JSON |

### Execution
```bash
# Re-run terminology extraction (if needed)
python3 research/extract_governance_terminology.py

# Re-generate visualizations
python3 research/create_terminology_visualizations.py

# Find bilingual pairs (already done)
python3 research/detect_hidden_bilingual_pairs.py
```

---

## 🎯 Key Findings Summary

### The "Accountability Gap" 🚨
- **English:** 15 occurrences of "accountability"
- **French:** 0 occurrences of "responsabilité" or equivalents
- **Implication:** Conceptual erasure during translation

### Control vs Monitoring
- **English:** 5 occurrences of "monitoring"
- **French:** 27 occurrences of "contrôle" (5.4x more)
- **Implication:** French emphasizes regulatory control over passive monitoring

### Bias Framing
- **English:** 34 "bias" (technical framing)
- **French:** 22 "biais" + 9 "préjugé" (adds moral dimension)
- **Implication:** Different conceptual frameworks

---

## 📊 Dataset Statistics

- **16 bilingual document pairs** analyzed (32 documents)
- **751 governance term occurrences** extracted
- **20+ terms per language** tracked
- **2 pairs excluded** (PDF extraction issues)
- **50-character context windows** for each term

---

## 📝 For CSDH 2026 Abstract

**Recommended Figure:** `fig5_accountability_gap.png`

**Key Statistics to Cite:**
- 16 bilingual pairs analyzed
- 751 governance terms extracted
- "Accountability" appears 15× in EN, 0× in FR
- "Contrôle" appears 5.4× more than "monitoring"

**Argument:**
> Translation of AI governance documents is not neutral transfer but conceptual transformation, reflecting deeper cultural-philosophical differences between governance traditions.

---

## 🔗 Quick Links

**View Figures:**
```bash
ls -lh research/governance_terminology/figures/
```

**Read Full Analysis:**
```bash
cat research/governance_terminology/KEY_FINDINGS.md
```

**Open Main Data:**
```bash
code research/governance_terminology/full_terminology_analysis.json
```

**Browse Reports:**
```bash
cd research/governance_terminology && ls -la
```

---

## ⚡ One-Command Summary

```bash
# Generate everything fresh
python3 research/extract_governance_terminology.py && \
python3 research/create_terminology_visualizations.py && \
echo "✅ Analysis complete. See research/governance_terminology/figures/"
```

---

## 📧 File Manifest

```
research/governance_terminology/
├── README.md                               # This file
├── VISUALIZATION_GUIDE.md                  # Figure descriptions
├── KEY_FINDINGS.md                         # Analysis summary
├── full_terminology_analysis.json          # Raw data (3,228 lines)
├── en_fr_terminology_comparison.csv        # Comparative table
├── semantic_drift_report.md                # Narrative findings
└── figures/
    ├── fig1_comparative_terms.png          # 199 KB
    ├── fig2_divergence_analysis.png        # 162 KB
    ├── fig3_category_comparison.png        # 180 KB
    ├── fig4_heatmap_distribution.png       # 507 KB
    ├── fig5_accountability_gap.png         # 164 KB ⭐
    └── fig6_summary_table.png              # 239 KB
```

**Total Size:** ~1.5 MB

---

**Created:** January 9, 2026  
**Status:** Publication-ready ✅  
**Next Step:** Draft CSDH abstract (250 words)
