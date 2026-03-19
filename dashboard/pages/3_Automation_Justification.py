"""Page 2 — Automation Rhetoric & Justification (Q-17 through Q-20)."""

import streamlit as st
import plotly.express as px
from db import run_query, sql_expander

st.header("Automation Rhetoric & Justification")
st.caption("Chapter 5 — Q-17, Q-18, Q-19, Q-20")
st.markdown(
    "*How do federal departments narrate the necessity of automation, "
    "and what does their rhetoric reveal about the state's relationship "
    "to algorithmic decision-making?*"
)

# ── Q-17: Justification themes ──────────────────────────────────────
st.subheader("Q-17 — Why Does the Government Automate?")
st.markdown(
    "60% of submissions justify automation through **efficiency** — "
    "faster processing, reduced backlogs, cost savings. "
    "But efficiency is also the *weakest* justification departments make."
)

Q17_SQL = """
SELECT justification_theme, COUNT(*) AS n,
       ROUND(AVG(strength_score)::numeric, 1) AS avg_strength,
       MIN(strength_score) AS min_strength,
       MAX(strength_score) AS max_strength
FROM interp_automation_justification
GROUP BY justification_theme ORDER BY n DESC;
"""
df17 = run_query(Q17_SQL)

fig17 = px.bar(
    df17, x="justification_theme", y="n",
    color="avg_strength", text="n",
    color_continuous_scale="RdYlGn",
    labels={"justification_theme": "Theme", "n": "Submissions",
            "avg_strength": "Avg Strength (1-5)"},
)
st.plotly_chart(fig17, use_container_width=True)
st.dataframe(df17, use_container_width=True)
sql_expander("Q-17: Justification themes", Q17_SQL)

# ── Q-18: Strength vs trade-offs ─────────────────────────────────────
st.subheader("Q-18 — Do Stronger Arguments Acknowledge Costs?")
st.markdown(
    "Every submission scoring 4 provides substantive trade-off discussion. "
    "Every submission scoring 1-2 leaves the trade-off field empty. "
    "**The departments that argue most convincingly also acknowledge costs honestly.**"
)

Q18_SQL = """
SELECT pd.department, pd.project_title_en,
       aj.justification_theme, aj.strength_score,
       aj.trade_off_adequacy, aj.public_benefit_clarity
FROM interp_automation_justification aj
JOIN project_details pd USING (submission_id)
ORDER BY aj.strength_score DESC;
"""
df18 = run_query(Q18_SQL)

fig18 = px.strip(
    df18, x="strength_score", y="justification_theme",
    color="justification_theme",
    hover_data=["project_title_en", "department"],
    labels={"strength_score": "Justification Strength (1-5)",
            "justification_theme": "Theme"},
)
fig18.update_layout(showlegend=False)
st.plotly_chart(fig18, use_container_width=True)

with st.expander("Full trade-off detail"):
    st.dataframe(
        df18[["project_title_en", "department", "strength_score",
              "trade_off_adequacy"]],
        use_container_width=True,
    )
sql_expander("Q-18: Strength vs trade-offs", Q18_SQL)

# ── Q-19: Automation type × rhetoric ─────────────────────────────────
st.subheader("Q-19 — Naming Your System Is the First Act of Accountability")
st.markdown(
    "Every submission that properly classified its automation level scored a "
    "**perfect 4 on justification strength**. Every submission that left it blank "
    "scored 1-2. The act of naming what you build forces you to explain why."
)

Q19_SQL = """
SELECT CASE ad.automation_type_score
           WHEN 0 THEN 'Decision support'
           WHEN 2 THEN 'Partial automation'
           WHEN 4 THEN 'Full automation'
           ELSE 'Not classified'
       END AS automation_level,
       aj.justification_theme, COUNT(*) AS n,
       ROUND(AVG(aj.strength_score)::numeric, 1) AS avg_strength
FROM interp_automation_justification aj
JOIN about_the_decision ad USING (submission_id)
GROUP BY automation_level, aj.justification_theme
ORDER BY automation_level, n DESC;
"""
df19 = run_query(Q19_SQL)

fig19 = px.bar(
    df19, x="automation_level", y="n", color="justification_theme",
    text="avg_strength", barmode="group",
    labels={"automation_level": "Automation Level", "n": "Submissions",
            "justification_theme": "Theme", "avg_strength": "Avg Strength"},
    color_discrete_sequence=px.colors.qualitative.Set2,
)
st.plotly_chart(fig19, use_container_width=True)
st.dataframe(df19, use_container_width=True)
sql_expander("Q-19: Automation type vs rhetoric", Q19_SQL)

# ── Q-20: Confinement gap ────────────────────────────────────────────
st.subheader("Q-20 — The Tiger Cages Have No Specifications")
st.markdown(
    "The 13 submissions with the **broadest system capabilities** are the same 13 "
    "that provide **no confinement assessment**. The systems most in need of "
    "boundaries are the ones whose boundaries are never described."
)

Q20_SQL = """
SELECT pd.project_title_en, pd.department,
       aj.confinement_assessment,
       ad.automation_type_score,
       rp.risk_total
FROM interp_automation_justification aj
JOIN project_details pd USING (submission_id)
JOIN about_the_decision ad USING (submission_id)
JOIN risk_profile rp USING (submission_id)
ORDER BY rp.risk_total DESC;
"""
df20 = run_query(Q20_SQL)
df20["has_confinement"] = df20["confinement_assessment"].apply(
    lambda x: "No" if x is None or "not provided" in str(x).lower()
    or "not clearly" in str(x).lower() or "crucial" in str(x).lower()
    else "Yes"
)

fig20 = px.scatter(
    df20, x="risk_total", y="project_title_en",
    color="has_confinement",
    color_discrete_map={"Yes": "#2E8B57", "No": "#8B0000"},
    labels={"risk_total": "Risk Total", "project_title_en": "System",
            "has_confinement": "Confinement Documented?"},
    hover_data=["department", "confinement_assessment"],
)
fig20.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig20, use_container_width=True)
sql_expander("Q-20: Confinement vs capabilities", Q20_SQL)
