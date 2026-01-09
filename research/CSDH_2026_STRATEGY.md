# LLM-Powered Analysis: CSDH 2026 Strategy

## The Big Picture

You now have a **three-layer approach** to your CFP paper:

### Layer 1: Corpus (Already Done)
- 29 AIA disclosures crawled
- 41 PDFs integrated (AIAs, GBA+, peer reviews)
- 5 records fully processed
- Bilingual EN/FR text extracted and preserved
- **Output**: Reproducible corpus pipeline

### Layer 2: Computational Tagging (Already Done)
- Heuristic keyword lexicons (7 categories)
- Thematic tagging across 5 records
- Tag frequency analysis
- **Output**: Demonstrates you can scale analysis

### Layer 3: LLM-Powered Divergence Analysis (NEW)
- Uses GPT-4 to analyze EN/FR conceptual incommensurability
- Identifies where AI ethics terms resist equivalence
- Measures divergence origin (linguistic/legal/cultural/professional)
- **Output**: Quantitative data on "untranslatability"

## Why This Strengthens Your CFP Proposal

### 1. **Directly Addresses "Untranslatable" Theme**

Your paper will demonstrate:
- Specific terminology that cannot be 1:1 translated
- Why (legal tradition? linguistic structure? philosophical assumptions?)
- How this matters for algorithmic governance across bilingual states

### 2. **Shows Sophisticated DH Methodology**

You use LLMs *critically*:
- Not for translation (that's not DH)
- Not to replace human analysis (that's not serious scholarship)
- **For measurement and pattern detection** (legitimate computational tool)

### 3. **Produces Publishable Data**

You'll have:
- Divergence statistics (% of terms that are untranslatable)
- Categorized examples (legal divergences, linguistic divergences, etc.)
- Confidence metrics from the LLM
- Network visualizations of conceptual gaps

### 4. **Positions You as Methodologically Innovative**

Most bilingual corpus work uses:
- Manual comparison (slow, subjective)
- Machine translation (erases divergence)
- Statistical term frequency (surface-level)

You're using:
- **Automated semantic analysis + human interpretation**
- **Measurement of incommensurability** (not equivalence)
- **Transparent tool use** (disclosure of LLM limitations)

## Workflow: From Now to January 26

### Week 1 (Jan 9-15)
- [ ] Get OpenAI API key
- [ ] Test with 3-5 AIA pairs (cost ~$1-2)
- [ ] Refine prompts based on results
- [ ] Validate divergence categorizations manually

### Week 2 (Jan 16-20)
- [ ] Run full corpus (29 pairs, cost ~$8-10)
- [ ] Generate divergence report
- [ ] Create visualizations (network, heatmap)
- [ ] Compile results into paper narrative

### Week 3 (Jan 21-26)
- [ ] Write methodology section
- [ ] Integrate results into findings
- [ ] Finalize abstract (500 words)
- [ ] Submit via ConfTool

## Paper Structure with LLM Analysis

```
1. Introduction
   - CFP theme: "Untranslatable"
   - RQ: What governance concepts resist bilingual equivalence?

2. Background
   - Canadian bilingual context
   - AI ethics as contested terminology

3. Methodology
   - Corpus construction (ethical crawl)
   - Heuristic tagging (existing layer)
   - LLM-powered divergence analysis (NEW)
     * Prompts included in appendix
     * Confidence scoring & validation

4. Results
   - Divergence statistics (% untranslatable)
   - Examples by category (legal, linguistic, cultural)
   - Network visualizations of conceptual gaps
   - LLM confidence metrics

5. Discussion
   - What does untranslatability reveal about AI governance?
   - Implications for bilingual policymaking
   - Limitations of LLM analysis (important to acknowledge!)
   - Future work (other language pairs, diachronic analysis)

6. Conclusion
   - Bilingualism as epistemological multiplier
   - Computing cannot unify governance concepts
```

## Key Methodological Transparency Points

(These go in your paper's "Limitations" section)

### Acknowledge:
1. **LLM Bias**: GPT-4 was trained on Anglophone data; may favor English semantics
2. **Token Limits**: We sampled 1000 chars per text; longer passages may reveal other divergences
3. **Prompt Design**: Analysis depends on how we ask questions; different prompts = different results
4. **Confidence ≠ Ground Truth**: LLM confidence scores are model uncertainty, not empirical validation
5. **Cost/Reproducibility**: Full 29-pair analysis costs ~$10; not free, but documented and budgeted

### Mitigate:
- Manual validation of ~10% of divergence categorizations
- Compare LLM results against independent linguistic analysis
- Release prompts and results openly (GitHub)
- Report API costs & token usage transparently

## The Pitch to Reviewers

> *This research demonstrates that bilingual corpora are not simply doubled versions of a single text. Using computational analysis grounded in Digital Humanities methodology, we reveal that Canadian AI governance operates within two distinct semantic fields simultaneously. Where English AIAs emphasize "human oversight" as active control, French AIAs deploy "examen humain" as institutional process. These are not translation failures but fundamental divergences rooted in legal tradition, linguistic structure, and political culture. This work contributes to current DH conversations about the "untranslatable" by demonstrating that even when large language models promise universal translatability, governance concepts resist computational unification. For bilingual states, this untranslatability is not a problem to solve but a political resource to recognize.*

## Next Step: Start Small

```bash
# Install dependencies
pip install openai python-dotenv

# Setup API (costs ~$1-2 for this test)
cp research/.env.template research/.env
# Edit .env with your API key

# Test with 3 pairs (dry run first)
python research/analyze_divergence.py --dry-run
python research/analyze_divergence.py --limit 3
```

This gives you real data to refine your CFP paper before the Jan 26 deadline.

**Does this approach work for you?**
