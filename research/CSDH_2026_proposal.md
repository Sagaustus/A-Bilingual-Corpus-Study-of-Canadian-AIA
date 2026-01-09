# CSDH/SCHN 2026 Paper Proposal

**Title:** The Untranslatable State: Bilingual Divergence in Canadian Algorithmic Governance Disclosures

**Author:** [Your Name]  
**Affiliation:** [Your Institution]  
**Type:** Paper (20 minutes)  
**Theme:** Untranslatable  

---

## Abstract (500 words)

Canada's 2019 Directive on Automated Decision-Making requires federal agencies to publish Algorithmic Impact Assessments (AIAs) documenting risks of deploying AI systems in public services. These disclosures are mandated to appear in both official languages, yet translation is not merely linguistic conversion—it is a site where technical vocabularies, bureaucratic norms, and governance imaginaries collide. This paper presents a computational analysis of 29 bilingual AIA disclosures to examine what becomes "untranslatable" when algorithmic power is articulated across French and English.

Drawing on Barbara Cassin's concept of the untranslatable as that which "one does not cease (not) to translate," I argue that bilingual AIAs expose governance concepts that resist equivalence: terms like "fairness," "bias," and "accountability" carry divergent philosophical and legal genealogies in Francophone and Anglophone administrative traditions. Where English AIAs emphasize "human-in-the-loop" oversight (appearing in 60% of assessed systems), French counterparts often deploy "examen humain" or "supervision humaine," terms that encode different assumptions about human agency, responsibility, and the boundaries of machine autonomy. These are not translation errors but revelations of conceptual incommensurability.

**Methodology:** I constructed a bilingual corpus by ethically crawling 29 AIA project pages from open.canada.ca, preserving immutability through timestamped snapshots and cryptographic checksums. The corpus includes 41 documents (32 AIAs, 3 Gender-Based Analysis Plus assessments, 6 peer reviews) totaling 150 MB of HTML, PDF, and CSV resources. I developed a Python pipeline (1,060 lines) to extract plaintext, apply heuristic thematic tagging across seven governance categories (privacy, fairness/bias, security, governance, transparency, data quality, human oversight), and generate exports compatible with Voyant Tools, MALLET, AntConc, and Gephi for distributed analysis.

Crucially, I did *not* machine-translate between languages. Instead, I retained language codes and document-type metadata to enable comparative discourse analysis that respects linguistic materiality. This methodological choice foregrounds what cannot be computationally unified: the cultural specificity of governance rhetoric.

**Preliminary Findings:** Keyword co-occurrence networks reveal that English-language AIAs cluster "transparency" with "explainability" and "interpretability" (terms rooted in Anglophone AI ethics), while French AIAs associate "transparence" with "reddition de comptes" (accountability) and "gouvernance," foregrounding institutional hierarchy over technical intelligibility. Human oversight terminology diverges structurally: English favors agentive constructions ("human review," "manual verification"), while French employs process-oriented phrasing ("processus de vérification," "examen manuel"). These divergences suggest that bilingualism does not duplicate governance but bifurcates it, producing two distinct algorithmic imaginaries within a single federal apparatus.

**Stakes:** At a moment when large language models claim universal translatability across human knowledge, this corpus demonstrates that governance concepts—especially those negotiating human–machine boundaries—resist computational flattening. For Digital Humanities in the Canadian context, bilingualism is not an accessibility feature but an epistemological multiplier, revealing how power operates differently across linguistic worlds. The untranslatable in algorithmic governance is not a problem to solve but a political fact to recognize: automated decision-making in a bilingual state is always at least two things at once, and perhaps never the same thing twice.

This research contributes to DH debates on AI ethics, multilingual corpus methods, and the materiality of computational governance, offering a reproducible pipeline for comparative policy analysis across linguistic regimes.

---

**Word count:** 498  
**Keywords:** algorithmic governance, bilingualism, translation, AI ethics, corpus methods, Canada

**Presenter will attend in person:** [Yes/No]  
**Requests remote presentation option:** [Yes/No]

---

## Submission Checklist

- [ ] Abstract ≤500 words ✓
- [ ] Specifies thesis (untranslatable governance concepts)
- [ ] Describes methodology (bilingual corpus, ethical crawl, comparative analysis)
- [ ] States conclusions (bilingualism bifurcates governance, not duplicates)
- [ ] Connects to conference theme ("Untranslatable")
- [ ] Addresses Canadian context (federal bilingualism)
- [ ] Demonstrates DH methods (corpus construction, computational analysis)
- [ ] Submit via https://conftool.net/csdh-schn-2026/ by Jan 26, 2026
- [ ] Ensure CSDH/SCHN membership by conference date

## Alternative: Digital Demonstration Proposal (if preferred)

If you'd prefer to showcase the corpus as a tool/resource, I can draft a 300-word demo proposal focusing on:
- Interactive corpus exploration (Voyant)
- Reproducible pipeline walkthrough
- Bilingual tag network visualization
- Open data for other researchers

Let me know if you'd like that version instead!
