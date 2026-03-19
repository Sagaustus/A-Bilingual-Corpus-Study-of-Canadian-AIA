"""Page 6 — Submission Explorer / Close Reading."""

import streamlit as st
import pandas as pd
from db import run_query, sql_expander

st.header("Submission Explorer — Close Reading")
st.caption("Deep-dive into individual AIA submissions with EN/FR side-by-side comparison")

# ── Submission selector ──────────────────────────────────────────────
LIST_SQL = """
SELECT pd.submission_id, pd.project_title_en, pd.department, rp.risk_total,
       bd.semantic_fidelity_score
FROM project_details pd
JOIN risk_profile rp USING (submission_id)
JOIN interp_bilingual_divergence bd USING (submission_id)
ORDER BY rp.risk_total DESC;
"""
df_list = run_query(LIST_SQL)

options = {
    f"{r['submission_id']} — {r['project_title_en'][:60]} "
    f"(risk={r['risk_total']}, fidelity={r['semantic_fidelity_score']})": r["submission_id"]
    for _, r in df_list.iterrows()
}
selected_label = st.selectbox("Select a submission", list(options.keys()))
sid = options[selected_label]

# ── Profile card ─────────────────────────────────────────────────────
PROFILE_SQL = f"""
SELECT pd.submission_id, pd.department, pd.project_title_en,
       pd.project_title_fr, pd.description_en, pd.description_fr,
       pd.system_capabilities,
       rp.risk_total,
       bd.semantic_fidelity_score, bd.has_divergence, bd.divergence_count,
       bd.overall_divergence_type,
       sc.overall_compliance_label, sc.overall_compliance_score,
       aj.justification_theme, aj.strength_score,
       rri.risk_level_label, rri.dominant_risk_dimension,
       ad.automation_type_score
FROM project_details pd
JOIN risk_profile rp USING (submission_id)
JOIN interp_bilingual_divergence bd USING (submission_id)
JOIN interp_safeguard_compliance sc USING (submission_id)
JOIN interp_automation_justification aj USING (submission_id)
JOIN interp_risk_rights_impact rri USING (submission_id)
JOIN about_the_decision ad USING (submission_id)
WHERE pd.submission_id = {sid};
"""
profile = run_query(PROFILE_SQL).iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Risk Total", profile["risk_total"])
col2.metric("Fidelity", f"{profile['semantic_fidelity_score']}/5")
col3.metric("Compliance", f"{profile['overall_compliance_score']}/5")
col4.metric("Strength", f"{profile['strength_score']}/5")
col5.metric("Divergences", profile["divergence_count"])

population = ("A — Bilingual" if profile["semantic_fidelity_score"] >= 3
              else "B — Monolingual")
risk_color = {"low": "green", "moderate": "orange", "high": "red"}.get(
    profile["risk_level_label"], "gray")

st.markdown(
    f"**Department:** {profile['department']}  |  "
    f"**Risk:** :{risk_color}[{profile['risk_level_label']}]  |  "
    f"**Population:** {population}  |  "
    f"**Theme:** {profile['justification_theme']}  |  "
    f"**Automation:** {profile['automation_type_score']}"
)

st.divider()

# ── EN/FR side-by-side ───────────────────────────────────────────────
st.subheader("EN/FR Side-by-Side Comparison")
st.markdown(
    "English text on the left, French on the right. "
    "Empty French fields are highlighted — these are the **omissions** "
    "that drive the divergence findings."
)

BILINGUAL_SQL = f"""
SELECT
    pd.description_en, pd.description_fr,
    ra.efficiency_gains_en, ra.efficiency_gains_fr,
    ra.client_needs_en, ra.client_needs_fr,
    ra.public_benefits_en, ra.public_benefits_fr,
    ad.evaluation_criteria_en, ad.evaluation_criteria_fr,
    ii.rights_freedoms_en, ii.rights_freedoms_fr,
    ii.equality_dignity_en, ii.equality_dignity_fr,
    ii.health_wellbeing_en, ii.health_wellbeing_fr
FROM project_details pd
JOIN reasons_for_automation ra USING (submission_id)
JOIN about_the_decision ad USING (submission_id)
JOIN individual_impacts ii USING (submission_id)
WHERE pd.submission_id = {sid};
"""
bilingual = run_query(BILINGUAL_SQL).iloc[0]

fields = [
    ("Description", "description"),
    ("Efficiency Gains", "efficiency_gains"),
    ("Client Needs", "client_needs"),
    ("Public Benefits", "public_benefits"),
    ("Evaluation Criteria", "evaluation_criteria"),
    ("Rights & Freedoms", "rights_freedoms"),
    ("Equality & Dignity", "equality_dignity"),
    ("Health & Wellbeing", "health_wellbeing"),
]

for label, key in fields:
    en_val = bilingual.get(f"{key}_en", "")
    fr_val = bilingual.get(f"{key}_fr", "")
    en_text = en_val if en_val else "*— empty —*"
    fr_text = fr_val if fr_val else "*— empty —*"
    fr_missing = not fr_val or str(fr_val).strip() == ""

    st.markdown(f"#### {label}")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**English**")
        st.markdown(en_text)
    with c2:
        if fr_missing:
            st.markdown("**French** :red[MISSING]")
            st.error("This field was not provided in French.")
        else:
            st.markdown("**French**")
            st.markdown(fr_text)
    st.divider()

# ── LLM Interpretation Panel ────────────────────────────────────────
st.subheader("LLM Interpretations")

# Justification
with st.expander("Justification Analysis", expanded=True):
    JUST_SQL = f"""
    SELECT justification_theme, strength_score, public_benefit_clarity,
           trade_off_adequacy, confinement_assessment
    FROM interp_automation_justification
    WHERE submission_id = {sid};
    """
    just = run_query(JUST_SQL).iloc[0]
    st.markdown(f"**Theme:** {just['justification_theme']}  |  **Strength:** {just['strength_score']}/5")
    st.markdown(f"**Public benefit:** {just['public_benefit_clarity']}")
    st.markdown(f"**Trade-offs:** {just['trade_off_adequacy']}")
    st.markdown(f"**Confinement:** {just['confinement_assessment']}")
    sql_expander("Justification query", JUST_SQL)

# Risk
with st.expander("Risk & Rights Analysis", expanded=True):
    RISK_SQL = f"""
    SELECT risk_level_label, dominant_risk_dimension,
           rights_concern_summary, proportionality_assessment,
           reversibility_concern
    FROM interp_risk_rights_impact
    WHERE submission_id = {sid};
    """
    risk = run_query(RISK_SQL).iloc[0]
    st.markdown(f"**Risk label:** {risk['risk_level_label']}  |  "
                f"**Dominant dimension:** {risk['dominant_risk_dimension']}")
    st.markdown(f"**Rights concerns:** {risk['rights_concern_summary']}")
    st.markdown(f"**Proportionality:** {risk['proportionality_assessment']}")
    st.markdown(f"**Reversibility:** {risk['reversibility_concern']}")
    sql_expander("Risk query", RISK_SQL)

# Divergence
with st.expander("Bilingual Divergence Analysis", expanded=True):
    DIV_SQL = f"""
    SELECT has_divergence, divergence_count, overall_divergence_type,
           semantic_fidelity_score, divergent_fields, untranslatable_concepts
    FROM interp_bilingual_divergence
    WHERE submission_id = {sid};
    """
    div = run_query(DIV_SQL).iloc[0]
    st.markdown(f"**Fidelity:** {div['semantic_fidelity_score']}/5  |  "
                f"**Divergences:** {div['divergence_count']}  |  "
                f"**Type:** {div['overall_divergence_type']}")
    if div["divergent_fields"]:
        st.json(div["divergent_fields"])
    sql_expander("Divergence query", DIV_SQL)

# Safeguard
with st.expander("Safeguard Compliance", expanded=True):
    SAFE_SQL = f"""
    SELECT overall_compliance_label, overall_compliance_score,
           consultation_assessment, bias_mitigation_assessment,
           fairness_assessment, privacy_assessment, gaps_identified
    FROM interp_safeguard_compliance
    WHERE submission_id = {sid};
    """
    safe = run_query(SAFE_SQL).iloc[0]
    st.markdown(f"**Compliance:** {safe['overall_compliance_label']} "
                f"({safe['overall_compliance_score']}/5)")
    st.markdown(f"**Consultation:** {safe['consultation_assessment']}")
    st.markdown(f"**Bias mitigation:** {safe['bias_mitigation_assessment']}")
    st.markdown(f"**Fairness:** {safe['fairness_assessment']}")
    st.markdown(f"**Privacy:** {safe['privacy_assessment']}")
    if safe["gaps_identified"]:
        st.markdown("**Gaps identified:**")
        st.json(safe["gaps_identified"])
    sql_expander("Safeguard query", SAFE_SQL)

# ── Source SQL for the whole view ────────────────────────────────────
sql_expander("Profile query", PROFILE_SQL)
sql_expander("Bilingual fields query", BILINGUAL_SQL)
