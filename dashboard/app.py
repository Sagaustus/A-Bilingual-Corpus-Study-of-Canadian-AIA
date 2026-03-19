"""
The Untranslatable State — AIA Corpus Dashboard
A Digital Humanities research dashboard for exploring Canadian
Algorithmic Impact Assessments through bilingual corpus analysis.

Run: streamlit run dashboard/app.py
"""

import streamlit as st

st.set_page_config(
    page_title="The Untranslatable State — AIA Corpus",
    page_icon="maple_leaf",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ──────────────────────────────────────────────────────────
st.sidebar.title("The Untranslatable State")
st.sidebar.caption(
    "A bilingual corpus study of Canadian Algorithmic Impact Assessments"
)
st.sidebar.divider()
st.sidebar.markdown(
    """
**Database:** `aia_corpus` (PostgreSQL)
**Submissions:** 30 interpreted / 114 total
**Model:** Llama 3.3 70B Instruct
**Prompt version:** 1.0.0
"""
)
st.sidebar.divider()
st.sidebar.markdown(
    "Navigate using the **pages** in the sidebar above. "
    "Every chart includes a *View SQL* expander for full traceability."
)

# ── Main landing ─────────────────────────────────────────────────────
st.title("The Untranslatable State")
st.subheader(
    "How Canada's Official Bilingualism Produces Two Distinct "
    "Algorithmic Governance Regimes"
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Submissions", "114")
col2.metric("Interpreted", "30")
col3.metric("LLM Interpretations", "120")
col4.metric("Thematic Patterns", "22")

st.markdown("---")

st.markdown(
    """
### Dashboard Pages

| Page | Chapter | What You'll Find |
|------|---------|-----------------|
| **Corpus Overview** | Ch 1 | Methodology validation, token complexity, provenance audit |
| **Bilingual Divergence** | Ch 3 | Divergence rates, field-level heatmap, the omission finding |
| **Automation & Justification** | Ch 5 | Efficiency rhetoric, trade-off gaps, confinement claims |
| **Risk, Rights & Proportionality** | Ch 6 | Risk landscape, rights scores, the proportionality gap |
| **Safeguard Compliance** | Ch 7 | Compliance distribution, safeguard gaps, privacy pipeline |
| **The Completeness Cluster** | Cross-cutting | The 13/17 population split — the thesis's central finding |
| **Submission Explorer** | All | Close reading of individual submissions with EN/FR side-by-side |

### The Central Finding

The corpus splits into **two populations**:

- **Population A (~17 submissions):** Bilingual, well-documented, substantive trade-offs, clear confinement, lower risk
- **Population B (~13 submissions):** Monolingual, poorly documented, missing trade-offs, no confinement, higher risk

The departments that engage least with the assessment process are the ones deploying the most consequential algorithms.
"""
)

st.markdown("---")
st.caption(
    "Data source: Government of Canada, Open Government Licence. "
    "LLM interpretations: meta-llama/Llama-3.3-70B-Instruct via IONOS, prompt v1.0.0."
)
