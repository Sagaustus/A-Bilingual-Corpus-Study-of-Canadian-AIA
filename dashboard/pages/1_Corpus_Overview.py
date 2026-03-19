"""Page 0 — Corpus Overview & Methodology Validation (Q-06, Q-07, Q-08)."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from db import run_query, sql_expander

st.header("Corpus Overview & Methodology Validation")
st.caption("Chapter 1 — Q-06, Q-07, Q-08")

# ── Q-06: LLM vs Computed Risk ──────────────────────────────────────
st.subheader("Q-06 — Does the AI Reader Agree with the Scoring Algorithm?")
st.markdown(
    "We asked an AI to read what departments wrote about their own algorithms, "
    "then compared its qualitative risk labels against the AIA's computed scores. "
    "Think of it as a **standardized test vs. an experienced teacher** reading the same essays."
)

Q06_SQL = """
SELECT r.risk_level_label, COUNT(*) AS n,
       ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk_total,
       MIN(rp.risk_total) AS min_risk, MAX(rp.risk_total) AS max_risk
FROM interp_risk_rights_impact r
JOIN risk_profile rp ON r.submission_id = rp.submission_id
GROUP BY r.risk_level_label
ORDER BY avg_risk_total;
"""
df06 = run_query(Q06_SQL)

fig06 = px.bar(
    df06, x="risk_level_label", y="n",
    color="avg_risk_total",
    color_continuous_scale="RdYlGn_r",
    labels={"risk_level_label": "LLM Risk Label", "n": "Submissions",
            "avg_risk_total": "Avg Computed Score"},
    text="n",
)
fig06.update_layout(xaxis_categoryorder="array",
                    xaxis_categoryarray=["low", "moderate", "high"])
st.plotly_chart(fig06, use_container_width=True)
st.dataframe(df06, use_container_width=True)
sql_expander("Q-06: LLM vs computed risk", Q06_SQL)

# PACT outlier callout
st.info(
    "**The PACT outlier:** The Pre-load Air Cargo Targeting system scored only 4 "
    "on the computed scale but was labeled 'high' risk by the AI — "
    "it read the surveillance context that the numbers missed."
)

# ── Q-07: Token Usage ────────────────────────────────────────────────
st.subheader("Q-07 — Which Analysis Takes the Most Thinking?")
st.markdown(
    "Token counts measure how much reasoning the AI needed. "
    "Longer responses = more complex analysis. "
    "Think of tokens as **the length of a scholar's marginal notes**."
)

Q07_SQL = """
SELECT 'Justification' AS analysis_type,
       (raw_llm_response->'usage'->>'completion_tokens')::int AS tokens
FROM interp_automation_justification
UNION ALL
SELECT 'Risk',
       (raw_llm_response->'usage'->>'completion_tokens')::int
FROM interp_risk_rights_impact
UNION ALL
SELECT 'Divergence',
       (raw_llm_response->'usage'->>'completion_tokens')::int
FROM interp_bilingual_divergence
UNION ALL
SELECT 'Safeguard',
       (raw_llm_response->'usage'->>'completion_tokens')::int
FROM interp_safeguard_compliance;
"""
df07 = run_query(Q07_SQL)

fig07 = px.box(
    df07, x="analysis_type", y="tokens", color="analysis_type",
    category_orders={"analysis_type": ["Divergence", "Safeguard",
                                        "Justification", "Risk"]},
    labels={"analysis_type": "Analysis Type", "tokens": "Completion Tokens"},
    color_discrete_sequence=["#8B0000", "#CD853F", "#4682B4", "#2E8B57"],
)
fig07.update_layout(showlegend=False)
st.plotly_chart(fig07, use_container_width=True)
sql_expander("Q-07: Token usage by analysis type", Q07_SQL)

st.markdown(
    "**Bilingual divergence requires 2.1x more reasoning** than any other type. "
    "The wide range (60–958 tokens) reflects the omission problem: "
    "some submissions have no French content to compare."
)

# ── Q-08: Provenance Audit ───────────────────────────────────────────
st.subheader("Q-08 — The Provenance Audit: One Model, One Rubric, One Sitting")

Q08_SQL = """
SELECT model_id, prompt_version, COUNT(*) AS total_rows,
       MIN(created_at) AS earliest, MAX(created_at) AS latest
FROM (
    SELECT model_id, prompt_version, created_at FROM interp_automation_justification
    UNION ALL SELECT model_id, prompt_version, created_at FROM interp_risk_rights_impact
    UNION ALL SELECT model_id, prompt_version, created_at FROM interp_bilingual_divergence
    UNION ALL SELECT model_id, prompt_version, created_at FROM interp_safeguard_compliance
) all_interp
GROUP BY model_id, prompt_version;
"""
df08 = run_query(Q08_SQL)
st.dataframe(df08, use_container_width=True)
sql_expander("Q-08: Model provenance", Q08_SQL)

Q08_LOG_SQL = """
SELECT id, analysis_type, submissions_processed, submissions_skipped,
       errors, run_started_at, run_finished_at
FROM interp_run_log ORDER BY id;
"""
st.markdown("#### ETL Run Log — The Full Audit Trail")
st.markdown(
    "The run log tells the story of what worked and what broke — "
    "because **transparency includes confessing your mistakes**."
)
df08_log = run_query(Q08_LOG_SQL)
st.dataframe(df08_log, use_container_width=True)
sql_expander("Q-08: Run log", Q08_LOG_SQL)
