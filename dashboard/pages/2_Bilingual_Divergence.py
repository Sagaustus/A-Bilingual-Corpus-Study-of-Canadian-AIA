"""Page 1 — The Bilingual Divergence Landscape (Q-09 through Q-13)."""

import streamlit as st
import plotly.express as px
import pandas as pd
from db import run_query, sql_expander

st.header("The Bilingual Divergence Landscape")
st.caption("Chapter 3 — Q-09, Q-10, Q-11, Q-12, Q-13")
st.markdown(
    "*Where does bilingual governance break down — and what does the pattern "
    "reveal about the politics of translation in algorithmic governance?*"
)

# ── Q-09: Overall divergence rate ────────────────────────────────────
st.subheader("Q-09 — How Bilingual Is the Corpus, Really?")

Q09_SQL = """
SELECT has_divergence, COUNT(*) AS submissions,
       ROUND(COUNT(*)::numeric / 30 * 100, 1) AS pct
FROM interp_bilingual_divergence GROUP BY has_divergence;
"""
df09 = run_query(Q09_SQL)

col1, col2 = st.columns([1, 2])
with col1:
    st.metric("Divergent", f"{df09[df09['has_divergence']==True]['submissions'].iloc[0]}/30",
              delta="96.7%", delta_color="inverse")
    st.metric("Equivalent", "1/30", delta="3.3%")
with col2:
    fig09 = px.pie(df09, values="submissions", names="has_divergence",
                   color_discrete_sequence=["#8B0000", "#2E8B57"],
                   hole=0.4)
    fig09.update_traces(textinfo="value+percent")
    st.plotly_chart(fig09, use_container_width=True)

sql_expander("Q-09: Overall divergence rate", Q09_SQL)
st.info(
    "97% of submissions show bilingual divergence. "
    "The Canadian state's algorithmic governance is almost never equivalently bilingual."
)

# ── Q-10: Which fields diverge most ─────────────────────────────────
st.subheader("Q-10 — Which Fields Diverge Most?")
st.markdown(
    "The fields most likely to diverge are the ones that matter most for "
    "governance accountability — **evaluation criteria, system outputs, "
    "project descriptions, and rights assessments**."
)

Q10_SQL = """
SELECT field->>'field' AS field_name,
       field->>'type' AS divergence_type,
       field->>'severity' AS severity,
       COUNT(*) AS occurrences
FROM interp_bilingual_divergence,
     jsonb_array_elements(divergent_fields) AS field
GROUP BY field_name, divergence_type, severity
ORDER BY occurrences DESC;
"""
df10 = run_query(Q10_SQL)

# Heatmap: field x severity
pivot = df10.pivot_table(index="field_name", columns="severity",
                         values="occurrences", aggfunc="sum", fill_value=0)
if not pivot.empty:
    severity_order = ["minor", "moderate", "significant"]
    cols = [c for c in severity_order if c in pivot.columns]
    pivot = pivot[cols].sort_values(cols[-1] if cols else pivot.columns[0],
                                   ascending=True)
    fig10 = px.imshow(
        pivot, text_auto=True, aspect="auto",
        color_continuous_scale="YlOrRd",
        labels={"x": "Severity", "y": "Field", "color": "Occurrences"},
    )
    fig10.update_layout(height=600)
    st.plotly_chart(fig10, use_container_width=True)
sql_expander("Q-10: Field divergence heatmap", Q10_SQL)

# ── Q-11: Divergence types ───────────────────────────────────────────
st.subheader("Q-11 — What Kind of Divergence?")

Q11_SQL = """
SELECT overall_divergence_type, COUNT(*) AS submissions,
       ROUND(AVG(semantic_fidelity_score)::numeric, 2) AS avg_fidelity
FROM interp_bilingual_divergence
GROUP BY overall_divergence_type ORDER BY submissions DESC;
"""
df11 = run_query(Q11_SQL)
st.dataframe(df11, use_container_width=True)
sql_expander("Q-11: Divergence type distribution", Q11_SQL)
st.markdown(
    "28 of 30 classified as 'linguistic' divergence — but the real cause is "
    "**omission, not mistranslation**. The average fidelity score of 2.61/5 "
    "means the typical submission achieves less than half of full bilingual equivalence."
)

# ── Q-12: Omission vs drift ─────────────────────────────────────────
st.subheader("Q-12 — Omission or Terminological Drift?")
st.markdown(
    "This is the thesis's defining finding: **the French version of the "
    "Canadian state is not badly translated — it is largely absent.**"
)

Q12_SQL = """
SELECT field->>'type' AS divergence_type,
       COUNT(*) AS total_occurrences,
       COUNT(DISTINCT bd.submission_id) AS submissions_affected
FROM interp_bilingual_divergence bd,
     jsonb_array_elements(divergent_fields) AS field
GROUP BY divergence_type ORDER BY total_occurrences DESC;
"""
df12 = run_query(Q12_SQL)

fig12 = px.bar(
    df12, x="divergence_type", y="total_occurrences",
    color="submissions_affected",
    text="total_occurrences",
    color_continuous_scale="Reds",
    labels={"divergence_type": "Type", "total_occurrences": "Occurrences",
            "submissions_affected": "Submissions"},
)
st.plotly_chart(fig12, use_container_width=True)
st.dataframe(df12, use_container_width=True)
sql_expander("Q-12: Omission vs drift", Q12_SQL)

st.warning(
    "**Omission: 183 instances (71%).** "
    "Reframing: 24. Translation: 22. Addition: 20. Terminological: 7. "
    "The untranslatable state is, in most cases, the *untranslated* state."
)

# ── Q-13: Fidelity vs narrative presence ─────────────────────────────
st.subheader("Q-13 — The Binary Population: Bilingual or Not")
st.markdown(
    "Fidelity scores jump from 1 to 3 with **nothing in between**. "
    "The corpus splits into two clean populations: "
    "structurally monolingual (0–1) and genuinely bilingual (3–5)."
)

Q13_SQL = """
SELECT bd.submission_id, bd.semantic_fidelity_score,
       (CASE WHEN pd.description_fr IS NOT NULL AND pd.description_fr != ''
             THEN 1 ELSE 0 END) AS has_fr_description,
       (CASE WHEN ra.client_needs_fr IS NOT NULL AND ra.client_needs_fr != ''
             THEN 1 ELSE 0 END) AS has_fr_client_needs,
       (CASE WHEN ii.rights_freedoms_fr IS NOT NULL AND ii.rights_freedoms_fr != ''
             THEN 1 ELSE 0 END) AS has_fr_rights
FROM interp_bilingual_divergence bd
JOIN project_details pd USING (submission_id)
JOIN reasons_for_automation ra USING (submission_id)
JOIN individual_impacts ii USING (submission_id)
ORDER BY bd.semantic_fidelity_score;
"""
df13 = run_query(Q13_SQL)
df13["fr_fields_present"] = (df13["has_fr_description"] +
                              df13["has_fr_client_needs"] +
                              df13["has_fr_rights"])
df13["population"] = df13["semantic_fidelity_score"].apply(
    lambda x: "Monolingual (0-1)" if x <= 1 else "Bilingual (3-5)"
)

fig13 = px.scatter(
    df13, x="semantic_fidelity_score", y="fr_fields_present",
    color="population",
    color_discrete_map={"Monolingual (0-1)": "#8B0000", "Bilingual (3-5)": "#2E8B57"},
    labels={"semantic_fidelity_score": "Semantic Fidelity Score (0-5)",
            "fr_fields_present": "French Narrative Fields Present (0-3)"},
    hover_data=["submission_id"],
    size_max=12,
)
# Highlight the gap at score=2
fig13.add_vrect(x0=1.5, x1=2.5, fillcolor="gray", opacity=0.15,
                annotation_text="No submissions score 2",
                annotation_position="top")
st.plotly_chart(fig13, use_container_width=True)
sql_expander("Q-13: Fidelity vs narrative presence", Q13_SQL)

col1, col2 = st.columns(2)
col1.metric("Monolingual (score 0-1)", "13 submissions (43%)")
col2.metric("Bilingual (score 3-5)", "17 submissions (57%)")
