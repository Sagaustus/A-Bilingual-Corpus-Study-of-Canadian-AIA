"""Page 3 — Risk, Rights & Proportionality (Q-21 through Q-24)."""

import streamlit as st
import plotly.express as px
from db import run_query, sql_expander

st.header("Risk, Rights & Proportionality")
st.caption("Chapter 6 — Q-21, Q-22, Q-23, Q-24")
st.markdown(
    "*How does the AIA framework construct risk, and does the instrument "
    "adequately capture the human rights implications of automated decision-making?*"
)

# ── Q-21: Risk landscape ────────────────────────────────────────────
st.subheader("Q-21 — The Risk Landscape")
st.markdown(
    "The six highest-risk submissions — all scoring the **maximum risk_total of 10** — "
    "are the same ones that left their automation type, confinement, and French content blank. "
    "**The riskiest systems have the thinnest governance documentation.**"
)

Q21_HIST_SQL = """
SELECT rri.submission_id, pd.project_title_en, pd.department,
       rri.risk_level_label, rp.risk_total
FROM interp_risk_rights_impact rri
JOIN project_details pd USING (submission_id)
JOIN risk_profile rp USING (submission_id)
ORDER BY rp.risk_total DESC;
"""
df21 = run_query(Q21_HIST_SQL)

fig21 = px.histogram(
    df21, x="risk_total", color="risk_level_label",
    nbins=11, barmode="overlay",
    color_discrete_map={"low": "#2E8B57", "moderate": "#DAA520", "high": "#8B0000"},
    labels={"risk_total": "Computed Risk Total", "risk_level_label": "LLM Risk Label"},
    hover_data=["project_title_en"],
)
st.plotly_chart(fig21, use_container_width=True)

Q21_AGG_SQL = """
SELECT rri.risk_level_label, COUNT(*) AS n,
       ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk_total
FROM interp_risk_rights_impact rri
JOIN risk_profile rp USING (submission_id)
GROUP BY rri.risk_level_label ORDER BY avg_risk_total;
"""
df21_agg = run_query(Q21_AGG_SQL)
st.dataframe(df21_agg, use_container_width=True)
sql_expander("Q-21: Risk landscape", Q21_HIST_SQL)

# High-risk callout
st.error(
    "**The 6 highest-risk systems** (risk_total=10) are all from ESDC (disability, "
    "mental health benefits) and IRCC (refugee, spousal immigration). "
    "They process the most vulnerable populations and have the least documentation."
)

# ── Q-22: Rights dimensions ──────────────────────────────────────────
st.subheader("Q-22 — Which Rights Are Most at Stake?")
st.markdown(
    "All four rights dimensions score close to 1.0 on a 0–4 scale. "
    "Either all systems genuinely have minimal impact, "
    "or departments systematically **understate rights implications** "
    "— like 30 drivers all claiming they drive at exactly the speed limit."
)

Q22_SQL = """
SELECT 'Rights & Freedoms' AS dimension,
       ROUND(AVG(rights_freedoms_score)::numeric, 2) AS avg_score,
       COUNT(*) FILTER (WHERE rights_freedoms_score > 0) AS affected
FROM individual_impacts
UNION ALL
SELECT 'Equality & Dignity', ROUND(AVG(equality_dignity_score)::numeric, 2),
       COUNT(*) FILTER (WHERE equality_dignity_score > 0)
FROM individual_impacts
UNION ALL
SELECT 'Health & Wellbeing', ROUND(AVG(health_wellbeing_score)::numeric, 2),
       COUNT(*) FILTER (WHERE health_wellbeing_score > 0)
FROM individual_impacts
UNION ALL
SELECT 'Economic Interests', ROUND(AVG(economic_interests_score)::numeric, 2),
       COUNT(*) FILTER (WHERE economic_interests_score > 0)
FROM individual_impacts;
"""
df22 = run_query(Q22_SQL)

fig22 = px.bar(
    df22, x="dimension", y="avg_score", color="affected",
    text="avg_score",
    color_continuous_scale="Blues",
    labels={"dimension": "Rights Dimension", "avg_score": "Average Score (0-4)",
            "affected": "Submissions Affected"},
)
fig22.update_layout(yaxis_range=[0, 4])
st.plotly_chart(fig22, use_container_width=True)
st.dataframe(df22, use_container_width=True)
sql_expander("Q-22: Rights dimensions", Q22_SQL)

# ── Q-23: Proportionality ───────────────────────────────────────────
st.subheader("Q-23 — Is Automation Proportional to Risk?")
st.markdown(
    "Proportionality **cannot be assessed** for the riskiest systems "
    "because they did not disclose their automation level. "
    "The safety valve in the governance architecture was never turned on."
)

Q23_SQL = """
SELECT rri.risk_level_label,
       CASE WHEN ad.automation_type_score IS NULL THEN 'Unknown'
            WHEN ad.automation_type_score = 0 THEN 'Decision support'
            WHEN ad.automation_type_score = 2 THEN 'Partial automation'
            ELSE 'Full automation' END AS automation_level,
       COUNT(*) AS n
FROM interp_risk_rights_impact rri
JOIN about_the_decision ad USING (submission_id)
GROUP BY rri.risk_level_label, automation_level
ORDER BY rri.risk_level_label, n DESC;
"""
df23 = run_query(Q23_SQL)

fig23 = px.bar(
    df23, x="risk_level_label", y="n", color="automation_level",
    barmode="stack", text="n",
    color_discrete_map={"Decision support": "#2E8B57",
                        "Partial automation": "#DAA520",
                        "Unknown": "#8B0000"},
    labels={"risk_level_label": "Risk Level", "n": "Submissions",
            "automation_level": "Automation Level"},
    category_orders={"risk_level_label": ["low", "moderate", "high"]},
)
st.plotly_chart(fig23, use_container_width=True)
st.dataframe(df23, use_container_width=True)
sql_expander("Q-23: Proportionality gap", Q23_SQL)

st.warning(
    "**6 of 7 high-risk systems** have unknown automation level. "
    "The AIA's proportionality mechanism works only for systems that don't need it."
)

# ── Q-24: Reversibility ─────────────────────────────────────────────
st.subheader("Q-24 — Reversibility & Duration: The Non-Functional Fields")
st.markdown(
    "This question **cannot be answered as designed**. "
    "All 30 submissions have the same reversibility score (1) and NULL duration. "
    "The instrument contains fields that produce no usable data — "
    "like a thermometer that always reads room temperature."
)

Q24_SQL = """
SELECT ad.impacts_reversible_score, ad.impact_duration_score, COUNT(*) AS n,
       ROUND(AVG(rp.risk_total)::numeric, 1) AS avg_risk
FROM about_the_decision ad
JOIN risk_profile rp USING (submission_id)
GROUP BY ad.impacts_reversible_score, ad.impact_duration_score;
"""
df24 = run_query(Q24_SQL)
st.dataframe(df24, use_container_width=True)
sql_expander("Q-24: Reversibility and duration", Q24_SQL)

st.info(
    "The AIA *knows* that reversibility matters — it asks about it. "
    "But it cannot *measure* it. "
    "This is the gap between the AIA's aspirations and its capabilities."
)
