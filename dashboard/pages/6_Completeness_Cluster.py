"""Page 5 — The Completeness Cluster (thesis centerpiece)."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db import run_query, sql_expander

st.header("The Completeness Cluster")
st.caption("Cross-cutting finding — the thesis's central discovery")

st.markdown(
    """
### The Single Most Important Finding

The AIA corpus is **not a gradient from good to bad**. It is two distinct populations:

- **Population A (~17 submissions):** Bilingual, well-documented, substantive trade-offs,
  clear confinement, moderate-to-low risk
- **Population B (~13 submissions):** Monolingual, poorly documented, missing trade-offs,
  no confinement, moderate-to-high risk

The departments that engage least with the assessment are deploying the most consequential algorithms.
"""
)

# ── Master query ─────────────────────────────────────────────────────
MASTER_SQL = """
SELECT pd.submission_id, pd.department, pd.project_title_en,
       aj.justification_theme, aj.strength_score,
       rri.risk_level_label, rp.risk_total,
       sc.overall_compliance_label, sc.overall_compliance_score,
       bd.has_divergence, bd.semantic_fidelity_score, bd.divergence_count,
       ad.automation_type_score,
       CASE WHEN bd.semantic_fidelity_score >= 3 THEN 'A — Bilingual'
            ELSE 'B — Monolingual' END AS population
FROM project_details pd
JOIN interp_automation_justification aj USING (submission_id)
JOIN interp_risk_rights_impact rri USING (submission_id)
JOIN risk_profile rp USING (submission_id)
JOIN interp_safeguard_compliance sc USING (submission_id)
JOIN interp_bilingual_divergence bd USING (submission_id)
JOIN about_the_decision ad USING (submission_id)
ORDER BY rp.risk_total DESC;
"""
df = run_query(MASTER_SQL)

# ── Population metrics ───────────────────────────────────────────────
st.subheader("The Two Populations at a Glance")

pop_a = df[df["population"] == "A — Bilingual"]
pop_b = df[df["population"] == "B — Monolingual"]

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Population A — Bilingual")
    st.metric("Count", len(pop_a))
    st.metric("Avg Risk Total", f"{pop_a['risk_total'].mean():.1f}")
    st.metric("Avg Fidelity", f"{pop_a['semantic_fidelity_score'].mean():.1f}/5")
    st.metric("Avg Compliance", f"{pop_a['overall_compliance_score'].mean():.1f}/5")
    st.metric("Avg Justification Strength", f"{pop_a['strength_score'].mean():.1f}/5")
    pct_auto = pop_a["automation_type_score"].notna().mean() * 100
    st.metric("Has Automation Type", f"{pct_auto:.0f}%")

with col2:
    st.markdown("#### Population B — Monolingual")
    st.metric("Count", len(pop_b))
    st.metric("Avg Risk Total", f"{pop_b['risk_total'].mean():.1f}",
              delta=f"{pop_b['risk_total'].mean() - pop_a['risk_total'].mean():+.1f}",
              delta_color="inverse")
    st.metric("Avg Fidelity", f"{pop_b['semantic_fidelity_score'].mean():.1f}/5",
              delta=f"{pop_b['semantic_fidelity_score'].mean() - pop_a['semantic_fidelity_score'].mean():+.1f}",
              delta_color="inverse")
    st.metric("Avg Compliance", f"{pop_b['overall_compliance_score'].mean():.1f}/5",
              delta=f"{pop_b['overall_compliance_score'].mean() - pop_a['overall_compliance_score'].mean():+.1f}",
              delta_color="inverse")
    st.metric("Avg Justification Strength", f"{pop_b['strength_score'].mean():.1f}/5",
              delta=f"{pop_b['strength_score'].mean() - pop_a['strength_score'].mean():+.1f}",
              delta_color="inverse")
    pct_auto_b = pop_b["automation_type_score"].notna().mean() * 100
    st.metric("Has Automation Type", f"{pct_auto_b:.0f}%",
              delta=f"{pct_auto_b - pct_auto:+.0f}pp", delta_color="inverse")

# ── Parallel coordinates ─────────────────────────────────────────────
st.subheader("Parallel Coordinates — Every Submission, Every Dimension")
st.markdown(
    "Each line is one submission. The colour tells you which population it belongs to. "
    "Notice how Population B (red) consistently occupies the *worse* end of every axis."
)

df["pop_code"] = df["population"].map({"A — Bilingual": 0, "B — Monolingual": 1})

fig_pc = go.Figure(data=go.Parcoords(
    line=dict(
        color=df["pop_code"],
        colorscale=[[0, "#2E8B57"], [1, "#8B0000"]],
        showscale=True,
        colorbar=dict(
            tickvals=[0, 1],
            ticktext=["A — Bilingual", "B — Monolingual"],
            title="Population",
        ),
    ),
    dimensions=[
        dict(label="Fidelity (0-5)", values=df["semantic_fidelity_score"],
             range=[0, 5]),
        dict(label="Strength (1-5)", values=df["strength_score"],
             range=[1, 5]),
        dict(label="Compliance (1-5)", values=df["overall_compliance_score"],
             range=[1, 5]),
        dict(label="Risk Total", values=df["risk_total"],
             range=[0, 10]),
        dict(label="Divergence Count", values=df["divergence_count"],
             range=[0, df["divergence_count"].max()]),
    ],
))
fig_pc.update_layout(height=500)
st.plotly_chart(fig_pc, use_container_width=True)

# ── Scatter: Risk vs Fidelity ────────────────────────────────────────
st.subheader("Risk vs. Bilingual Fidelity")
st.markdown(
    "High-risk systems cluster in the **bottom-left** — "
    "high risk, low fidelity, monolingual. "
    "The relationship is not accidental."
)

fig_scatter = px.scatter(
    df, x="semantic_fidelity_score", y="risk_total",
    color="population",
    color_discrete_map={"A — Bilingual": "#2E8B57", "B — Monolingual": "#8B0000"},
    size="overall_compliance_score",
    hover_data=["project_title_en", "department", "justification_theme"],
    labels={"semantic_fidelity_score": "Bilingual Fidelity (0-5)",
            "risk_total": "Risk Total",
            "overall_compliance_score": "Compliance Score"},
)
fig_scatter.update_layout(height=500)
st.plotly_chart(fig_scatter, use_container_width=True)

# ── Binary indicator strip ───────────────────────────────────────────
st.subheader("Completeness Indicators — Every Submission")
st.markdown(
    "Green = present. Red = absent. "
    "The pattern is unmistakable: **completeness clusters**."
)

indicators = df[["submission_id", "project_title_en", "population",
                 "semantic_fidelity_score", "strength_score",
                 "overall_compliance_score", "risk_total"]].copy()
indicators["has_french"] = df["semantic_fidelity_score"] >= 3
indicators["has_auto_type"] = df["automation_type_score"].notna()
indicators["strong_justification"] = df["strength_score"] >= 4
indicators = indicators.sort_values("population")

st.dataframe(
    indicators.style.applymap(
        lambda v: "background-color: #c6efce" if v is True
        else "background-color: #ffc7ce" if v is False else "",
        subset=["has_french", "has_auto_type", "strong_justification"],
    ),
    use_container_width=True,
    height=600,
)

# ── Full master table ────────────────────────────────────────────────
st.subheader("Full Master Table")
with st.expander("View all 30 submissions with all metrics"):
    st.dataframe(df, use_container_width=True)
sql_expander("Master query (all dimensions)", MASTER_SQL)

st.download_button(
    "Download master table as CSV",
    df.to_csv(index=False),
    "aia_completeness_cluster.csv",
    "text/csv",
)
