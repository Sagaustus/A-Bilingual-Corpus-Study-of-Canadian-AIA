"""Page 8 — Catalogue of Ethical Terminologies (Phase 6 integration)."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from db import run_query, sql_expander

st.set_page_config(page_title="Ethical Catalogue", layout="wide")
st.header("Catalogue of Ethical Terminologies")
st.caption("Phase 5–6 — Philosophical Origin · Corpus Usage · Cross-Linguistic Divergence")
st.markdown(
    "_How do ethical terms from metaethics, normative ethics, and applied AI ethics "
    "appear — and get transformed — in Canadian federal Algorithmic Impact Assessments?_"
)

BRANCH_COLORS = {
    "metaethics":       "#7B2D8B",
    "normative_ethics": "#1A6B8A",
    "applied_ethics":   "#C0392B",
}
DRIFT_COLORS = {
    "instrumentalized": "#E74C3C",
    "narrowed":         "#E67E22",
    "reframed":         "#F39C12",
    "hollowed":         "#8E44AD",
    "legalized":        "#2980B9",
    "bifurcated":       "#1ABC9C",
    "unnamed":          "#95A5A6",
    "faithful":         "#27AE60",
    "expanded":         "#2ECC71",
    "absent":           "#BDC3C7",
}
DIV_COLORS = {
    "terminological":      "#3498DB",
    "asymmetric_emphasis": "#E67E22",
    "omission":            "#E74C3C",
    "conceptual_shift":    "#8E44AD",
    "register":            "#16A085",
    "faithful":            "#27AE60",
}
ORG_SHORT = {
    "Canada Border Services Agency":            "CBSA",
    "Employment and Social Development Canada": "ESDC",
    "Immigration":                              "IRCC",
    "Public Health Agency of Canada":           "PHAC",
    "Public Services and Procurement Canada":   "PSPC",
    "Refugees and Citizenship Canada":          "RCC",
    "Royal Canadian Mounted Police":            "RCMP",
    "Transport Canada":                         "TC",
    "Treasury Board of Canada Secretariat":     "TBS",
    "Veterans Affairs Canada":                  "VAC",
}

# ── Load data ──────────────────────────────────────────────────────────────────

@st.cache_data(ttl=600)
def load_catalogue():
    return run_query("""
        SELECT term_id, term_en, term_fr, branch, tradition, key_philosophers,
               corpus_frequency_en, corpus_frequency_fr,
               submission_count_en, submission_count_fr,
               en_fr_frequency_ratio,
               philosophical_origin_summary,
               dominant_usage_en, dominant_usage_fr,
               drift_type_en, drift_type_fr,
               drift_description_en, drift_description_fr,
               en_fr_divergence_type, en_fr_key_contrast,
               en_fr_philosophical_significance, key_finding,
               key_example_en, key_example_fr,
               philosophical_definition_en, philosophical_definition_fr,
               aia_relevance
        FROM ethical_term_catalogue
        ORDER BY branch, term_id;
    """)


@st.cache_data(ttl=600)
def load_occurrences():
    return run_query("""
        SELECT term_en, branch, organization,
               submission_language, field, match_language,
               matched_variant, context_before, matched_text, context_after, sentence
        FROM ethical_term_occurrences
        ORDER BY branch, term_en, match_language, organization;
    """)


@st.cache_data(ttl=600)
def load_freq_by_org():
    return run_query("""
        SELECT l.term_en, l.branch, o.name AS org,
               COALESCE(SUM(f.occurrence_count), 0) AS total
        FROM ethical_term_lexicon l
        CROSS JOIN organizations o
        LEFT JOIN ethical_term_frequency f
          ON f.term_id = l.id AND f.organization = o.name
        GROUP BY l.term_en, l.branch, o.name
        ORDER BY l.branch, l.term_en, o.name;
    """)


cat  = load_catalogue()
freq = load_freq_by_org()

# ── Sidebar filters ────────────────────────────────────────────────────────────

st.sidebar.header("Filters")
branch_sel = st.sidebar.multiselect(
    "Branch",
    options=["metaethics", "normative_ethics", "applied_ethics"],
    default=["metaethics", "normative_ethics", "applied_ethics"],
    format_func=lambda x: x.replace("_", " ").title(),
)
drift_sel = st.sidebar.multiselect(
    "EN Drift type",
    options=sorted(cat["drift_type_en"].dropna().unique()),
    default=[],
)
div_sel = st.sidebar.multiselect(
    "EN/FR Divergence type",
    options=sorted(cat["en_fr_divergence_type"].dropna().unique()),
    default=[],
)

filtered = cat[cat["branch"].isin(branch_sel)]
if drift_sel:
    filtered = filtered[filtered["drift_type_en"].isin(drift_sel)]
if div_sel:
    filtered = filtered[filtered["en_fr_divergence_type"].isin(div_sel)]

# ── KPI row ────────────────────────────────────────────────────────────────────

st.markdown("### Corpus at a Glance")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Terms catalogued", len(filtered))
k2.metric("EN occurrences", int(filtered["corpus_frequency_en"].sum()))
k3.metric("FR occurrences", int(filtered["corpus_frequency_fr"].sum()))
k4.metric("Conceptual shifts", int((filtered["en_fr_divergence_type"] == "conceptual_shift").sum()))
k5.metric("Faithful in FR", int((filtered["drift_type_fr"] == "faithful").sum()))

st.divider()

# ── Tab layout ─────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Frequency Heatmap",
    "🔄 Drift Profiles",
    "🔀 EN÷FR Ratio",
    "🗂️ Term Explorer",
    "📝 Concordance Viewer",
])

# ── Tab 1: Heatmap ─────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Ethical Term Occurrences by Organization")
    st.caption("Which departments invoke which ethical concepts — and how often?")

    freq_f = freq[freq["branch"].isin(branch_sel)].copy()
    freq_f["org_short"] = freq_f["org"].map(ORG_SHORT).fillna(freq_f["org"])
    freq_f["log_total"] = np.log1p(freq_f["total"])

    branch_order = ["metaethics", "normative_ethics", "applied_ethics"]
    freq_f["branch_n"] = freq_f["branch"].map({b: i for i, b in enumerate(branch_order)})
    term_order = (
        freq_f.drop_duplicates("term_en")
              .sort_values(["branch_n", "term_en"])["term_en"]
              .tolist()
    )

    pivot = freq_f.pivot_table(
        index="term_en", columns="org_short", values="log_total", aggfunc="sum"
    ).reindex(index=term_order).fillna(0)

    pivot_raw = freq_f.pivot_table(
        index="term_en", columns="org_short", values="total", aggfunc="sum"
    ).reindex(index=term_order).fillna(0)

    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        text=pivot_raw.values.astype(int),
        texttemplate="%{text}",
        colorscale="YlOrRd",
        hovertemplate="<b>%{y}</b> × <b>%{x}</b><br>Occurrences: %{text}<extra></extra>",
        colorbar=dict(title="log₁₊(n)"),
    ))
    fig_heat.update_layout(
        height=max(500, len(term_order) * 22),
        xaxis=dict(side="bottom", tickangle=-35),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=170, r=30, t=30, b=80),
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    sql_expander("Heatmap data", """
        SELECT l.term_en, l.branch, o.name AS org,
               COALESCE(SUM(f.occurrence_count), 0) AS total
        FROM ethical_term_lexicon l
        CROSS JOIN organizations o
        LEFT JOIN ethical_term_frequency f
          ON f.term_id = l.id AND f.organization = o.name
        GROUP BY l.term_en, l.branch, o.name;
    """)


# ── Tab 2: Drift Profiles ──────────────────────────────────────────────────────
with tab2:
    st.subheader("Drift Type Profiles — English vs French")
    st.caption(
        "How does each ethical term's meaning shift from its philosophical origin, "
        "in English vs French AIA submissions?"
    )

    en_counts = (
        filtered.groupby("drift_type_en").size()
                .reset_index(name="count")
                .rename(columns={"drift_type_en": "drift_type"})
    )
    en_counts["language"] = "English"
    fr_counts = (
        filtered.groupby("drift_type_fr").size()
                .reset_index(name="count")
                .rename(columns={"drift_type_fr": "drift_type"})
    )
    fr_counts["language"] = "French"
    drift_df = pd.concat([en_counts, fr_counts])
    drift_df["color"] = drift_df["drift_type"].map(DRIFT_COLORS).fillna("#aaa")

    col_a, col_b = st.columns(2)
    for col, lang in [(col_a, "English"), (col_b, "French")]:
        sub = drift_df[drift_df["language"] == lang].sort_values("count", ascending=True)
        fig_d = px.bar(
            sub, x="count", y="drift_type", orientation="h",
            color="drift_type", color_discrete_map=DRIFT_COLORS,
            title=f"{lang} Submissions",
            labels={"count": "Terms", "drift_type": ""},
        )
        fig_d.update_layout(showlegend=False, height=380,
                            margin=dict(l=10, r=10, t=40, b=10))
        col.plotly_chart(fig_d, use_container_width=True)

    st.markdown("#### Key Contrast")
    st.info(
        "**English** instrumentalizes most (reduces ethics to scores/checklists).  \n"
        "**French** reframes more (displaces concepts toward administrative or civic values).  \n"
        "French has more **absent** terms (8 vs 4) — entire concepts missing from French discourse.  \n"
        "French has more **faithful** terms (2 vs 0) — recourse and non-maleficence treated philosophically."
    )

    # Cross-tab: branch × drift type
    st.markdown("#### EN Drift by Branch")
    cross = (
        filtered.groupby(["branch", "drift_type_en"])
                .size()
                .reset_index(name="n")
    )
    cross["branch_label"] = cross["branch"].str.replace("_", " ").str.title()
    fig_cross = px.bar(
        cross, x="branch_label", y="n", color="drift_type_en",
        color_discrete_map=DRIFT_COLORS,
        barmode="stack",
        labels={"branch_label": "Branch", "n": "Terms", "drift_type_en": "Drift type"},
        height=350,
    )
    fig_cross.update_layout(margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig_cross, use_container_width=True)


# ── Tab 3: EN÷FR Ratio ────────────────────────────────────────────────────────
with tab3:
    st.subheader("English ÷ French Frequency Ratio")
    st.caption(
        "Terms above 1.0 appear more in English; below 1.0 appear more in French. "
        "Bars are coloured by cross-linguistic divergence type."
    )

    ratio_df = filtered[
        (filtered["corpus_frequency_en"] > 0) | (filtered["corpus_frequency_fr"] > 0)
    ].copy()
    ratio_df["ratio_plot"] = ratio_df["en_fr_frequency_ratio"].fillna(
        ratio_df["corpus_frequency_en"].apply(lambda x: 8.0 if x > 0 else 0.0)
    )
    ratio_df["label"] = (
        "EN:" + ratio_df["corpus_frequency_en"].astype(str)
        + " FR:" + ratio_df["corpus_frequency_fr"].astype(str)
    )
    ratio_df = ratio_df.sort_values("ratio_plot", ascending=False)
    ratio_df["div_color"] = ratio_df["en_fr_divergence_type"].map(DIV_COLORS).fillna("#aaa")

    fig_ratio = go.Figure(go.Bar(
        x=ratio_df["ratio_plot"],
        y=ratio_df["term_en"],
        orientation="h",
        marker_color=ratio_df["div_color"],
        text=ratio_df["label"],
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "EN÷FR ratio: %{x:.2f}<br>"
            "%{text}<extra></extra>"
        ),
    ))
    fig_ratio.add_vline(x=1.0, line_dash="dash", line_color="#555",
                        annotation_text="EN = FR", annotation_position="top right")
    fig_ratio.update_layout(
        height=max(500, len(ratio_df) * 22),
        xaxis_title="EN ÷ FR ratio",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=160, r=120, t=30, b=40),
        showlegend=False,
    )
    st.plotly_chart(fig_ratio, use_container_width=True)

    # Divergence type legend
    st.markdown("**Divergence type colour key:**")
    cols = st.columns(len(DIV_COLORS))
    for col, (dtype, color) in zip(cols, DIV_COLORS.items()):
        col.markdown(
            f'<span style="display:inline-block;width:14px;height:14px;'
            f'background:{color};border-radius:2px;margin-right:4px"></span>'
            f'`{dtype}`',
            unsafe_allow_html=True,
        )

    st.markdown("#### Notable asymmetries")
    st.warning(
        "**recourse** (6.63:1 EN) — English submissions articulate recourse far more, "
        "but French treats it more faithfully to the philosophical meaning.  \n"
        "**consent** (6.33:1 EN) — consent as a moral concept is nearly absent from French.  \n"
        "**audit** (0.46 — FR-dominant) — French frames governance as *vérification*, "
        "a more judgment-centered concept than English 'audit'.  \n"
        "**oversight** (≈1:1) — same frequency, opposite governance philosophy."
    )


# ── Tab 4: Term Explorer ───────────────────────────────────────────────────────
with tab4:
    st.subheader("Term-by-Term Explorer")

    term_sel = st.selectbox(
        "Select a term",
        options=filtered["term_en"].tolist(),
        index=0,
    )

    row = filtered[filtered["term_en"] == term_sel].iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("EN occurrences", int(row["corpus_frequency_en"]))
    c2.metric("FR occurrences", int(row["corpus_frequency_fr"]))
    c3.metric(
        "EN÷FR ratio",
        f"{row['en_fr_frequency_ratio']:.2f}" if pd.notna(row["en_fr_frequency_ratio"]) else "N/A",
    )

    st.markdown(f"**FR equivalent(s):** {row['term_fr']}")
    st.markdown(f"**Branch:** {row['branch'].replace('_',' ').title()}  |  "
                f"**Tradition(s):** {row['tradition']}")
    st.markdown(f"**Key philosophers:** {row['key_philosophers']}")

    with st.expander("📖 Philosophical Definitions"):
        st.markdown(f"**EN:** {row['philosophical_definition_en']}")
        st.markdown(f"**FR:** {row['philosophical_definition_fr']}")

    if row.get("philosophical_origin_summary"):
        st.markdown(f"**Philosophical origin (LLM summary):** {row['philosophical_origin_summary']}")

    st.divider()
    col_en, col_fr = st.columns(2)
    with col_en:
        drift_color = DRIFT_COLORS.get(row["drift_type_en"], "#aaa")
        st.markdown(
            f'**English usage** &nbsp; <span style="background:{drift_color};color:#fff;'
            f'padding:2px 8px;border-radius:4px;font-size:12px">{row["drift_type_en"]}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(row["dominant_usage_en"] or "_No summary recorded._")
        st.markdown(f"_Drift:_ {row['drift_description_en'] or '—'}")
        if row.get("key_example_en"):
            st.markdown(f"> *{row['key_example_en']}*")

    with col_fr:
        drift_color_fr = DRIFT_COLORS.get(row["drift_type_fr"], "#aaa")
        st.markdown(
            f'**French usage** &nbsp; <span style="background:{drift_color_fr};color:#fff;'
            f'padding:2px 8px;border-radius:4px;font-size:12px">{row["drift_type_fr"]}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(row["dominant_usage_fr"] or "_No summary recorded._")
        st.markdown(f"_Drift:_ {row['drift_description_fr'] or '—'}")
        if row.get("key_example_fr"):
            st.markdown(f"> *{row['key_example_fr']}*")

    st.divider()
    div_color = DIV_COLORS.get(row["en_fr_divergence_type"], "#aaa")
    st.markdown(
        f'**EN/FR Divergence** &nbsp; <span style="background:{div_color};color:#fff;'
        f'padding:2px 8px;border-radius:4px;font-size:12px">'
        f'{row["en_fr_divergence_type"]}</span>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**Key contrast:** {row['en_fr_key_contrast'] or '—'}")
    st.markdown(f"**Philosophical significance:** {row['en_fr_philosophical_significance'] or '—'}")

    st.success(f"**Key finding:** {row['key_finding'] or '—'}")

    if row.get("aia_relevance"):
        st.caption(f"AIA relevance: {row['aia_relevance']}")


# ── Tab 5: Concordance Viewer ─────────────────────────────────────────────────
with tab5:
    st.subheader("KWIC Concordance Viewer")
    st.caption(
        "Keyword-in-Context view of every ethical term occurrence in the corpus. "
        "Filter by term, language, organization, or field."
    )

    occ = load_occurrences()

    cf1, cf2, cf3, cf4 = st.columns(4)
    c_term = cf1.selectbox("Term", ["(all)"] + sorted(occ["term_en"].unique()))
    c_lang = cf2.selectbox("Language", ["(all)", "en", "fr"])
    c_org  = cf3.selectbox("Organization", ["(all)"] + sorted(occ["organization"].unique()))
    c_field= cf4.selectbox("Field", ["(all)"] + sorted(occ["field"].unique()))

    occ_f = occ.copy()
    if c_term  != "(all)": occ_f = occ_f[occ_f["term_en"]      == c_term]
    if c_lang  != "(all)": occ_f = occ_f[occ_f["match_language"]== c_lang]
    if c_org   != "(all)": occ_f = occ_f[occ_f["organization"]  == c_org]
    if c_field != "(all)": occ_f = occ_f[occ_f["field"]         == c_field]

    st.caption(f"{len(occ_f):,} matches")

    if not occ_f.empty:
        display = occ_f[["term_en", "match_language", "organization",
                          "field", "context_before", "matched_text",
                          "context_after", "sentence"]].copy()
        display.columns = ["Term", "Lang", "Organization",
                           "Field", "Before", "Match", "After", "Full sentence"]
        st.dataframe(display, use_container_width=True, height=480)
    else:
        st.info("No matches for current filters.")

    sql_expander("Concordance data", """
        SELECT term_en, branch, organization, submission_language,
               field, match_language, matched_variant,
               context_before, matched_text, context_after, sentence
        FROM ethical_term_occurrences
        ORDER BY branch, term_en, match_language, organization;
    """)
