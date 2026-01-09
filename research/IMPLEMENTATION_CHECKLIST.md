# LLM Divergence Analysis: Implementation Checklist

## Pre-Implementation (Jan 9-10)

- [ ] Review the three example output documents
  - [ ] `CSDH_2026_STRATEGY.md` — big picture strategy
  - [ ] `LLM_DIVERGENCE_GUIDE.md` — detailed setup & usage
  - [ ] `EXAMPLE_OUTPUTS.md` — what the output looks like

- [ ] Understand the methodological positioning
  - [ ] LLM as *measurement tool*, not replacement for analysis
  - [ ] Transparent about confidence scores & limitations
  - [ ] Contributes to CFP theme "Untranslatable"

- [ ] Plan budget
  - [ ] Test run (3-5 pairs): ~$1-2
  - [ ] Full corpus (29 pairs): ~$8-10
  - [ ] Total: <$20

## Setup (Jan 10-11)

- [ ] Get OpenAI API key
  - [ ] Visit https://platform.openai.com/account/api-keys
  - [ ] Create new secret key
  - [ ] Budget $10-20 credits

- [ ] Install dependencies
  ```bash
  cd /workspaces/aia-eia-js
  pip install openai python-dotenv
  ```

- [ ] Configure .env
  ```bash
  cp research/.env.template research/.env
  # Edit research/.env with your API key
  # ⚠️ DO NOT COMMIT THIS FILE
  ```

- [ ] Verify corpus is processed
  ```bash
  # Check for processed records
  ls data/processed/*/normalized.json | wc -l
  # Should show: 5 (or however many you processed)
  ```

## Testing Phase (Jan 11-13)

- [ ] Dry run (no API calls)
  ```bash
  python research/analyze_divergence.py --dry-run
  # Shows 2 sample bilingual pairs
  ```

- [ ] Test analysis on 3 pairs (~$1 cost)
  ```bash
  python research/analyze_divergence.py --limit 3
  # Generates: research/output/divergence_analyses.jsonl
  ```

- [ ] Review outputs
  - [ ] Open `research/output/divergence_analyses.jsonl`
  - [ ] Check JSON structure matches examples
  - [ ] Read divergence_analysis fields
  - [ ] Note untranslatable_concepts

- [ ] Validate manually
  - [ ] Read 2-3 original EN/FR passages
  - [ ] Compare against LLM's divergence_analysis
  - [ ] Does the LLM's categorization seem accurate?
  - [ ] Record any errors/refinements needed

- [ ] Refine prompts if needed
  - [ ] Edit `ANALYSIS_PROMPT` in `research/analyze_divergence.py`
  - [ ] Re-test on same 3 pairs
  - [ ] Iterate until confident

## Full Analysis (Jan 13-15)

- [ ] Generate full divergence report
  ```bash
  python research/analyze_divergence.py --limit 29
  # Takes ~10-15 minutes
  # Generates: divergence_analyses.jsonl + divergence_report.json
  # Cost: ~$8-10
  ```

- [ ] Review aggregate report
  ```bash
  cat research/output/divergence_report.json | python -m json.tool
  ```

- [ ] Extract key statistics for paper
  - [ ] % divergences by origin (linguistic/legal/cultural/professional)
  - [ ] Top untranslatable concepts (count)
  - [ ] Average LLM confidence
  - [ ] Examples of each divergence type

## Paper Integration (Jan 15-20)

- [ ] Update methodology section
  - [ ] Add paragraph on LLM-powered analysis
  - [ ] Include prompts in appendix
  - [ ] Explain confidence scoring

- [ ] Write results section
  - [ ] Use divergence_report.json statistics
  - [ ] Provide 3-4 specific examples
  - [ ] Include network/heatmap visualization

- [ ] Add limitations/ethical considerations
  - [ ] Acknowledge LLM bias (Anglophone training data)
  - [ ] Note manual validation was performed
  - [ ] Disclose API costs & reproducibility
  - [ ] Explain confidence ≠ ground truth

- [ ] Create visualizations
  - [ ] Network graph (divergence_origin as node type)
  - [ ] Heatmap (EN terms vs. divergence categories)
  - [ ] Bar chart (untranslatable concepts by frequency)

## CFP Submission (Jan 20-26)

- [ ] Finalize 500-word abstract
  - [ ] Use real findings from divergence analysis
  - [ ] Include methodology brief
  - [ ] State conclusions clearly
  - [ ] ≤500 words

- [ ] Prepare supplementary materials
  - [ ] Analysis prompts (for transparency)
  - [ ] Sample divergence analyses (JSON)
  - [ ] Divergence report (statistics)
  - [ ] Visualizations (PNG)

- [ ] Submit via ConfTool
  - [ ] URL: https://conftool.net/csdh-schn-2026/
  - [ ] Deadline: Monday, Jan 26, 11:59 pm EST
  - [ ] Type: Paper (20 minutes)
  - [ ] Theme: Untranslatable

## Optional: Graduate Travel Grant (Jan 23)

- [ ] If applicable, apply for travel support
  - [ ] Fill form: https://forms.gle/3ARtG7cu65hfw87R8
  - [ ] Deadline: Friday, Jan 23, 11:59 pm EST
  - [ ] Indicate in ConfTool submission

## Post-Submission (Jan 27+)

- [ ] Commit all code & results to GitHub
  ```bash
  git add research/analyze_divergence.py
  git add research/CSDH_* research/LLM_* research/EXAMPLE_*
  git commit -m "feat: add LLM-powered bilingual divergence analysis"
  git push origin master
  ```

- [ ] Create reproducible environment
  - [ ] Document API costs in README
  - [ ] Ensure .env.template exists
  - [ ] Include example outputs in repo

- [ ] Prepare for potential acceptance
  - [ ] Full 29-pair analysis (if not done)
  - [ ] Peer validation of divergence categorizations
  - [ ] Draft slides/poster materials

## Success Metrics

✓ Paper accepted to CSDH/SCHN 2026  
✓ Real LLM-generated divergence data in results section  
✓ Demonstrated novel DH methodology (LLM as analytical tool)  
✓ Transparent about limitations & costs  
✓ Contributes meaningfully to "Untranslatable" theme  

---

## Troubleshooting

**Q: "ModuleNotFoundError: No module named 'openai'"**  
A: Run `pip install openai python-dotenv`

**Q: "OPENAI_API_KEY not found"**  
A: Make sure `.env` file exists in `research/` and has your key

**Q: LLM analysis seems inaccurate**  
A: Try refining the prompt in `ANALYSIS_PROMPT`. Different phrasings yield different results.

**Q: Running out of budget?**  
A: Stop and use cached results. Each pair costs ~$0.30; budget ~$10 for 29 pairs.

**Q: JSON parse errors?**  
A: Some LLM responses wrap JSON in markdown. The script handles this, but check the raw output if errors persist.

---

## Timeline Summary

| Phase | Dates | Tasks | Cost |
|-------|-------|-------|------|
| Setup | Jan 10-11 | Install, configure, verify corpus | $0 |
| Testing | Jan 11-13 | Test 3 pairs, validate, refine | $1-2 |
| Full Analysis | Jan 13-15 | Run 29 pairs, generate report | $8-10 |
| Paper Integration | Jan 15-20 | Write methodology/results | $0 |
| Submission | Jan 20-26 | Finalize & submit | $0 |
| **Total** | | | **<$20** |

---

**Ready to start? Begin with the "Setup" section above.**

Questions? Check:
1. `LLM_DIVERGENCE_GUIDE.md` for detailed usage
2. `EXAMPLE_OUTPUTS.md` for what to expect
3. `CSDH_2026_STRATEGY.md` for big-picture context
