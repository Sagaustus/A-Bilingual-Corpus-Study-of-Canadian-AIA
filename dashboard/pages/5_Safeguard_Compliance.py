"""Page 4 — Safeguard Theatre vs. Substantive Compliance (Q-28 through Q-32)."""

import streamlit as st
import plotly.express as px
from db import run_query, sql_expander

st.header("Safeguard Theatre vs. Substantive Compliance")
st.caption("Chapter 7 — Q-28, Q-29, Q-30, Q-31, Q-32")
st.markdown(
    "*Do AIA safeguards represent genuine accountability mechanisms, "
    "or is compliance performative?*"
)

# ── Q-28: Compliance distribution ────────────────────────────────────
st.subheader("Q-28 — The Compliance Landscape")
st.markdown(
    "No submission achieves strong compliance (5/5). "
    "Half the corpus treads water at the threshold of adequacy (score 3). "
    "One-third scores 'weak.' **The perfect AIA does not exist.**"
)

Q28_SQL = """
SELECT overall_compliance_label, overall_compliance_score, COUNT(*) AS n
FROM interp_safeguard_compliance
GROUP BY overall_compliance_label, overall_compliance_score
ORDER BY overall_compliance_score DESC;
"""
df28 = run_query(Q28_SQL)

fig28 = px.pie(
    df28, values="n", names="overall_compliance_label",
    color="overall_compliance_label",
    color_discrete_map={"adequate": "#DAA520", "weak": "#8B0000"},
    hole=0.4,
)
fig28.update_traces(textinfo="value+percent+label")
st.plotly_chart(fig28, use_container_width=True)
st.dataframe(df28, use_container_width=True)
sql_expander("Q-28: Compliance distribution", Q28_SQL)

# ── Q-29: Safeguard gaps ────────────────────────────────────────────
st.subheader("Q-29 — The Same Gaps, Again and Again")
st.markdown(
    "The same structural gaps recur across departments: "
    "missing external review, unassigned bias accountability, "
    "non-public testing. These are **design flaws, not individual failures**."
)

Q29_SQL = """
SELECT gap::text AS gap_description, COUNT(*) AS frequency
FROM interp_safeguard_compliance,
     jsonb_array_elements(gaps_identified) AS gap
GROUP BY gap_description ORDER BY frequency DESC LIMIT 15;
"""
df29 = run_query(Q29_SQL)

# Clean up the gap descriptions (remove JSON quotes)
df29["gap_description"] = df29["gap_description"].str.strip('"')

fig29 = px.bar(
    df29, x="frequency", y="gap_description", orientation="h",
    text="frequency",
    color="frequency", color_continuous_scale="Reds",
    labels={"frequency": "Occurrences", "gap_description": "Safeguard Gap"},
)
fig29.update_layout(height=500, yaxis={"categoryorder": "total ascending"},
                    showlegend=False)
st.plotly_chart(fig29, use_container_width=True)
sql_expander("Q-29: Safeguard gaps", Q29_SQL)

# ── Q-30: The human override trifecta ────────────────────────────────
st.subheader("Q-30 — Explain, Override, Challenge: The Accountability Trifecta")
st.markdown(
    "All 30 systems claim human override. "
    "But 10 still score 'weak' on compliance. "
    "**Claiming accountability is not the same as having it** — "
    "like a restaurant sign saying 'All dietary restrictions accommodated' "
    "while serving regular pasta with a gluten-free sticker."
)

Q30_SQL = """
SELECT f.human_override_enabled, f.client_recourse_process,
       f.can_produce_reasons, COUNT(*) AS n,
       ROUND(AVG(sc.overall_compliance_score)::numeric, 1) AS avg_compliance
FROM fairness f
JOIN interp_safeguard_compliance sc USING (submission_id)
GROUP BY f.human_override_enabled, f.client_recourse_process,
         f.can_produce_reasons
ORDER BY n DESC;
"""
df30 = run_query(Q30_SQL)
st.dataframe(df30, use_container_width=True)
sql_expander("Q-30: Human override trifecta", Q30_SQL)

col1, col2, col3 = st.columns(3)
col1.metric("Human Override", "30/30", delta="100%")
col2.metric("Client Recourse", "29/30", delta="97%")
col3.metric("Can Produce Reasons", "25/30", delta="83%")

st.warning(
    "**4 systems cannot explain their own decisions** — including systems "
    "affecting elderly pensions and unemployment benefits."
)

# ── Q-31: GBA+ and bias testing pipeline ─────────────────────────────
st.subheader("Q-31 — The Bias Transparency Pipeline")
st.markdown(
    "GBA+ is conducted 67% of the time, bias testing is documented 73% — "
    "but results are made public in only **3%** of cases. "
    "Bias testing is a private ritual, not a public safeguard."
)

Q31_SQL = """
SELECT pd.department,
       COUNT(*) AS submissions,
       COUNT(*) FILTER (WHERE dqb.gba_plus_conducted > 0) AS gba_conducted,
       COUNT(*) FILTER (WHERE dqb.bias_testing_documented > 0) AS bias_documented,
       COUNT(*) FILTER (WHERE dqb.bias_testing_public > 0) AS bias_public
FROM data_quality_bias dqb
JOIN project_details pd USING (submission_id)
GROUP BY pd.department ORDER BY submissions DESC;
"""
df31 = run_query(Q31_SQL)
st.dataframe(df31, use_container_width=True)
sql_expander("Q-31: GBA+ and bias testing", Q31_SQL)

# Funnel visualization
import plotly.graph_objects as go
funnel_data = {
    "Stage": ["GBA+ Conducted", "Bias Testing Documented", "Results Made Public"],
    "Count": [20, 22, 1],
}
fig31 = go.Figure(go.Funnel(
    y=funnel_data["Stage"], x=funnel_data["Count"],
    textinfo="value+percent initial",
    marker={"color": ["#DAA520", "#CD853F", "#8B0000"]},
))
fig31.update_layout(title="The Bias Transparency Funnel")
st.plotly_chart(fig31, use_container_width=True)

# ── Q-32: Privacy ────────────────────────────────────────────────────
st.subheader("Q-32 — Privacy: More Promise Than Practice")
st.markdown(
    "93% of systems process personal data. All claim 'privacy by design.' "
    "But only 14% actually de-identify the data. "
    "**'Privacy by design' has become a governance slogan, not a technical standard.**"
)

Q32_SQL = """
SELECT pd.project_title_en,
       ps.pia_conducted, ps.privacy_by_design,
       ps.de_identification_applied, atd.uses_personal_info
FROM privacy_security ps
JOIN about_the_data atd USING (submission_id)
JOIN project_details pd USING (submission_id)
ORDER BY atd.uses_personal_info DESC;
"""
df32 = run_query(Q32_SQL)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Use Personal Data", "28/30")
col2.metric("Privacy by Design", "28/28")
col3.metric("PIA Conducted", "15/28")
col4.metric("De-identified", "4/28")

with st.expander("Full privacy detail"):
    st.dataframe(df32, use_container_width=True)
sql_expander("Q-32: Privacy measures", Q32_SQL)
