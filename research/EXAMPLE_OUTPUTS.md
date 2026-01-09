# Example Output: LLM Divergence Analysis

This document shows what your analysis will produce.

## Example 1: Divergence Analysis Output

```json
{
  "record_id": "b92cbf7b-3b1c-4b02-a219-ce5b9bdb030d",
  "title": "Facial Recognition Technology Assessment",
  "en_key_terms": [
    "human-in-the-loop",
    "fairness",
    "bias mitigation",
    "human review",
    "control"
  ],
  "fr_key_terms": [
    "examen humain",
    "équité",
    "atténuation des biais",
    "vérification manuelle",
    "supervision"
  ],
  "direct_equivalents": {
    "fairness": "équité",
    "bias": "biais"
  },
  "divergence_analysis": "English emphasizes individual fairness and active human control ('human-in-the-loop'). French emphasizes collective examination ('examen humain') and institutional process ('supervision'). 'Human-in-the-loop' implies active intervention; 'examen humain' suggests periodic review. Control vs. oversight.",
  "philosophical_assumptions": {
    "english": "Humans are active agents who intervene in algorithmic decisions. Fairness is a property to be achieved through human correction.",
    "french": "Humans have institutional responsibility to examine decisions. Equity emerges from proper process, not individual oversight."
  },
  "untranslatable_concepts": [
    "human-in-the-loop",
    "fairness (as individual property vs. institutional equity)",
    "review (ongoing vs. periodic)"
  ],
  "divergence_origin": "legal",
  "confidence": 0.89,
  "usage": {
    "input_tokens": 412,
    "output_tokens": 187
  }
}
```

### How to Read This:
- **direct_equivalents**: Simple terms that ARE translatable
- **divergence_analysis**: Narrative explanation of where/how they differ
- **philosophical_assumptions**: The underlying worldviews encoded in each term
- **untranslatable_concepts**: Terms that resist 1:1 mapping
- **divergence_origin**: **Why** they diverge (legal=Common Law vs Civil Law)
- **confidence**: LLM's confidence in this analysis (0-1 scale)

---

## Example 2: Aggregated Report

```json
{
  "total_pairs": 5,
  "linguistic_divergences": 1,
  "legal_divergences": 3,
  "cultural_divergences": 1,
  "professional_divergences": 0,
  "avg_confidence": 0.84,
  "untranslatable_terms": {
    "human-in-the-loop": 4,
    "fairness (property vs. process)": 3,
    "transparency": 2,
    "examen humain": 2,
    "oversight vs. supervision": 2,
    "bias mitigation": 1
  },
  "divergence_examples": [
    {
      "record": "b92cbf7b-3b1c-4b02-a219-ce5b9bdb030d",
      "analysis": "English emphasizes individual fairness and active human control. French emphasizes institutional examination and process."
    },
    {
      "record": "eed746a8-a682-47c2-86b1-b427398fa2e2",
      "analysis": "Data quality in English focuses on accuracy and completeness. French emphasizes validation and certification processes."
    }
  ]
}
```

### Key Insights from This Report:
- **60% legal divergences** (largest category) → points to Common Law vs Civil Law tradition
- **"human-in-the-loop" appears in 4/5 pairs** but never with a simple French equivalent
- **Average confidence 0.84** → LLM is fairly confident in categorizations
- **"oversight vs. supervision" is key divergence** → English = control, French = institutional responsibility

---

## Example 3: Network Visualization (for your presentation)

You can create a divergence network showing:

```
                   FAIRNESS
                   /      \
              (EN)          (FR)
             /                  \
      Individual           Institutional
       Property             Equity
          |                    |
       CONTROL          SUPERVISION
          |                    |
    Active Intervention    Periodic Review
```

Or as a heatmap:

```
                Linguistic  Legal  Cultural  Professional
Human-in-loop      0.2     0.7      0.1         0.0
Fairness           0.1     0.6      0.3         0.0
Transparency       0.0     0.4      0.6         0.0
```

---

## Example 4: How This Becomes Your CFP Paper Results Section

### Paper Excerpt:

> **Preliminary Findings:** Analysis of 5 AIA pairs revealed systematic conceptual divergence across governance terminology. The term "human-in-the-loop," appearing in 80% of English AIAs, proved untranslatable into French, which instead deployed variable phrasings ("examen humain," "vérification manuelle," "supervision humaine") encoding different assumptions about human agency. GPT-4 analysis categorized 60% of divergences as stemming from legal tradition differences (Common Law emphasis on individual fairness vs. Civil Law emphasis on institutional equity), 20% from linguistic structure, and 20% from cultural values. Average confidence in divergence detection was 0.84. These findings suggest that bilingual governance does not simply duplicate meaning but bifurcates it, producing two distinct algorithmic imaginaries within a single federal apparatus.

---

## Example 5: Cost Breakdown (for your budget)

| Component | Pairs | Tokens/Pair | $ per 1K tokens | Est. Cost |
|-----------|-------|------------|------------------|-----------|
| Input (EN+FR + prompt) | 5 | 500 | $0.01 | $0.025 |
| Output (analysis) | 5 | 250 | $0.03 | $0.038 |
| **Subtotal (5 pairs)** | | | | **~$0.30** |
| **Full corpus (29 pairs)** | | | | **~$1.74** |

*(Prices as of Jan 2026; check OpenAI pricing for current rates)*

---

## How to Present This in Your CFP Paper

### Methodology Section:

> *To identify conceptual incommensurability, we employed GPT-4-turbo as an analytical tool (not a translator) to compare EN/FR passages addressing the same governance questions. Rather than using machine translation to collapse bilingual texts into a single semantic space, we used LLM-powered analysis to measure and categorize where equivalence fails. For each bilingual pair, we prompted the model to: (1) identify term mappings, (2) analyze divergence sources, (3) extract philosophical assumptions, and (4) categorize divergence origin (linguistic/legal/cultural/professional). Prompts are included in Appendix A. Confidence scores reflect model uncertainty; we validated a sample of categorizations against independent linguistic analysis.*

### Results Section:

> *Quantitative divergence analysis (N=5 AIA pairs) revealed: 60% of divergences traced to legal tradition differences, 20% to linguistic structure, 20% to cultural values. The concept "human oversight," appearing in 80% of English AIAs, had no consistent French equivalent (LLM confidence 0.87). French deployments of "examen," "supervision," and "vérification" encoded different assumptions about temporality (ongoing vs. periodic), agency (individual vs. institutional), and responsibility (control vs. stewardship). These divergences were not translation failures but indicators of genuinely distinct governance imaginaries.*

---

## Questions to Expect (and How to Answer)

**Q: Isn't this just using AI to replace analysis?**  
**A:** No. We use LLMs as measurement instruments, not as interpretive authorities. We explicitly validate results, disclose confidence scores, and frame findings as computational observations requiring human interpretation.

**Q: How is this better than manual comparison?**  
**A:** Scalability and consistency. Manual comparison of 29 pairs would be subjective and time-intensive. LLM analysis gives us quantitative metrics (% linguistic divergences, confidence scores) that enable pattern detection across large corpora.

**Q: What about LLM bias?**  
**A:** Excellent question. GPT-4 was trained on Anglophone-heavy data, so it may favor English semantics. We acknowledge this and recommend validating results against human experts or other LLMs (e.g., Claude, Gemini).

**Q: Is this reproducible?**  
**A:** Yes. We release prompts, .env configuration, and results on GitHub. Cost is low (~$10) and budgeted transparently. Different LLM versions may yield slightly different results, but we document all versions used.

---

## Next Steps

1. **Get API key** (OpenAI: $5-10 in credits recommended)
2. **Run test analysis** on 3-5 pairs (~$1 cost)
3. **Validate manually** against your own linguistic judgment
4. **Refine prompts** if needed
5. **Scale to 29 pairs** (~$10, ~30 min runtime)
6. **Write results section** with real data

This gives you quantitative evidence for a strong CFP paper. Ready to start?
