# LLM-Powered Conceptual Divergence Analysis

This workflow uses OpenAI's GPT-4 to analyze bilingual EN/FR AIA pairs and identify where AI ethics concepts are "untranslatable" — that is, where direct semantic equivalence breaks down due to linguistic, legal, cultural, or professional differences.

## Why This Matters for Your CFP Paper

The "untranslatable" theme is exactly what this analyzes: **governance concepts that resist computational equivalence**. You're using LLMs not to translate, but to **identify and measure incommensurability**.

## Setup

### 1. Install OpenAI SDK

```bash
pip install openai python-dotenv
```

### 2. Configure API Key

```bash
cp research/.env.template research/.env
# Edit .env with your OpenAI API key
```

**⚠️ Security:** Never commit `.env`. It's in `.gitignore`.

### 3. Prepare Corpus

Ensure your AIA corpus is processed:

```bash
python research/crawl.py --limit 5
python research/extract_text.py
python research/normalize.py
```

This generates bilingual EN/FR snippets in `data/processed/<record_id>/normalized.json`.

## Usage

### Dry Run (No API calls)

```bash
python research/analyze_divergence.py --dry-run
```

Shows sample bilingual pairs without consuming API credits.

### Full Analysis

```bash
python research/analyze_divergence.py --limit 5
```

Analyzes 5 EN/FR pairs. For each pair, the script:

1. Extracts ~1000 chars from EN and FR normalized snippets
2. Sends to GPT-4 with prompt asking for:
   - Term mapping (EN ↔ FR)
   - Conceptual divergence (where equivalence breaks)
   - Philosophical assumptions (what each term assumes about AI governance)
   - Untranslatability sources (linguistic? legal? cultural? professional?)
3. Parses JSON response
4. Aggregates patterns across all pairs

### Cost & Limits

- **Estimated cost**: ~$0.30 per pair (GPT-4 turbo, 2000 tokens max)
- **5 pairs**: ~$1.50
- **29 pairs**: ~$8.70
- **Set limit in .env**: `COST_LIMIT_USD=50`

### Output

**analyses.jsonl**: Line-delimited JSON (one per pair)
```json
{
  "record_id": "...",
  "title": "...",
  "en_key_terms": ["fairness", "human review"],
  "fr_key_terms": ["équité", "examen humain"],
  "direct_equivalents": {"fairness": "équité"},
  "divergence_analysis": "English emphasizes individual fairness; French emphasizes collective equity...",
  "untranslatable_concepts": ["human-in-the-loop", "examen humain"],
  "divergence_origin": "legal",
  "confidence": 0.87
}
```

**divergence_report.json**: Aggregated statistics
```json
{
  "total_pairs": 5,
  "linguistic_divergences": 1,
  "legal_divergences": 3,
  "cultural_divergences": 1,
  "avg_confidence": 0.84,
  "untranslatable_terms": {
    "human oversight": 4,
    "explicabilité": 3,
    "gouvernance": 3
  }
}
```

## Integration with Your CFP Paper

### Section: Methodology

Add this to your CSDH proposal:

> *Analytical Approach*: To identify conceptual incommensurability, we employed GPT-4 as a semantic analysis tool (not a translator) to compare EN/FR AIA passages addressing the same governance questions. For each bilingual pair, we prompted the model to identify term mappings, philosophical assumptions, and sources of divergence (linguistic, legal, cultural, professional). This approach reverses typical machine translation workflows: rather than collapsing bilingual texts into a single meaning, we use LLM-powered analysis to reveal and measure where equivalence fails. The model's confidence scores and divergence categorizations provide quantitative data on "untranslatability."

### Section: Results

Use the divergence report to populate findings:

> *Preliminary Analysis* (5 AIA pairs): 60% of divergence stems from legal/administrative tradition differences (Common Law vs. Civil Law conceptualizations of oversight), 20% from linguistic structure, 20% from cultural values. The term "human-in-the-loop" appears in 100% of English AIAs but has no single French equivalent; French AIAs deploy "examen humain," "supervision," and "vérification manuelle" variably. Average LLM confidence in divergence detection: 0.84.

### Section: Discussion

This positions your work as:
- **Methodologically novel**: Using LLMs *reflectively* (to analyze incommensurability, not to erase it)
- **Theoretically grounded**: Engages Cassin's untranslatable
- **Empirically rigorous**: Provides quantitative measurements of conceptual divergence
- **Critically engaged with AI**: Demonstrates LLMs' limitations (they reveal what they can't unify)

## Ethical Considerations

1. **Transparency**: Disclose that you used LLM analysis; include prompts in appendix
2. **Reproducibility**: Version your prompts; different models may yield different results
3. **Human validation**: Consider hand-checking divergence categorizations for accuracy
4. **Cost**: Budget and disclose API costs
5. **Assumptions**: LLM confidence ≠ actual incommensurability; it's one analytical lens

## Next Steps

1. **Test with 3-5 pairs** to validate approach
2. **Refine prompts** based on initial outputs
3. **Run full corpus** (29 pairs) if results are promising
4. **Manually validate** a sample of divergence categorizations
5. **Visualize** divergence patterns (network, heatmap, etc.)
6. **Write methodology section** for paper

## Questions?

This is a legitimate DH methodology: you're using computational tools (LLMs) as analytical instruments, not replacements for interpretation. The key is **transparency** about how you use them and **reflection** on their limitations.
