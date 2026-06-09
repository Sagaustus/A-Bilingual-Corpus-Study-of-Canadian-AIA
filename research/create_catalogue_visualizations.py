#!/usr/bin/env python3
"""
Phase 6: Catalogue Visualizations (static, publication-quality).

Produces four figures saved to assets_for_paper/:
  fig_cat1_heatmap.png     — Term × Organization frequency heatmap
  fig_cat2_drift.png       — EN vs FR drift-type distribution (by branch)
  fig_cat3_ratio.png       — EN÷FR frequency ratio ranked bar chart
  fig_cat4_divergence.png  — Term × Divergence-type matrix
"""

import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import psycopg2
from pathlib import Path

matplotlib.rcParams.update({
    "font.family":    "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.dpi":        150,
})

DB_NAME   = "aia_corpus"
OUT_DIR   = Path(__file__).parent.parent / "assets_for_paper"
OUT_DIR.mkdir(exist_ok=True)

# Palette consistent across figures
BRANCH_COLORS = {
    "metaethics":       "#7B2D8B",   # purple
    "normative_ethics": "#1A6B8A",   # teal
    "applied_ethics":   "#C0392B",   # crimson
}
BRANCH_LABELS = {
    "metaethics":       "Metaethics",
    "normative_ethics": "Normative Ethics",
    "applied_ethics":   "Applied Ethics",
}
DRIFT_PALETTE = {
    "instrumentalized": "#E74C3C",
    "narrowed":         "#E67E22",
    "reframed":         "#F1C40F",
    "hollowed":         "#8E44AD",
    "legalized":        "#2980B9",
    "bifurcated":       "#1ABC9C",
    "unnamed":          "#95A5A6",
    "faithful":         "#27AE60",
    "expanded":         "#2ECC71",
    "absent":           "#BDC3C7",
}
DIV_PALETTE = {
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


# ── DB helpers ─────────────────────────────────────────────────────────────────

def q(conn, sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn)


# ── Figure 1: Term × Organization Heatmap ─────────────────────────────────────

def fig_heatmap(conn):
    df = q(conn, """
        SELECT o.name AS org,
               l.term_en, l.branch,
               COALESCE(SUM(f.occurrence_count), 0) AS total
        FROM ethical_term_lexicon l
        CROSS JOIN organizations o
        LEFT JOIN ethical_term_frequency f
          ON f.term_id = l.id AND f.organization = o.name
        GROUP BY o.name, l.term_en, l.branch
        ORDER BY l.branch, l.term_en, o.name;
    """)

    df["org_short"] = df["org"].map(ORG_SHORT).fillna(df["org"].str[:6])

    # Order terms by branch then alpha
    branch_order = ["metaethics", "normative_ethics", "applied_ethics"]
    df["branch_n"] = df["branch"].map({b: i for i, b in enumerate(branch_order)})
    term_order = (
        df.drop_duplicates("term_en")
          .sort_values(["branch_n", "term_en"])["term_en"]
          .tolist()
    )
    org_order = sorted(df["org_short"].unique())

    pivot = df.pivot_table(
        index="term_en", columns="org_short", values="total", aggfunc="sum"
    ).reindex(index=term_order, columns=org_order).fillna(0)

    # log1p scale so rare terms are still visible
    pivot_log = np.log1p(pivot)

    # Branch colour bands for Y-axis labels
    term_branches = (
        df.drop_duplicates("term_en")
          .set_index("term_en")["branch"]
    )

    fig, ax = plt.subplots(figsize=(12, 13))
    sns.heatmap(
        pivot_log, ax=ax, cmap="YlOrRd",
        linewidths=0.4, linecolor="#e0e0e0",
        annot=pivot.astype(int), fmt="d",
        annot_kws={"size": 7},
        cbar_kws={"label": "log₁₊(occurrences)", "shrink": 0.6},
    )

    # Colour Y-axis tick labels by branch
    for label in ax.get_yticklabels():
        term = label.get_text()
        branch = term_branches.get(term, "applied_ethics")
        label.set_color(BRANCH_COLORS.get(branch, "#333"))
        label.set_fontsize(8.5)

    ax.set_xticklabels(ax.get_xticklabels(), fontsize=9, rotation=40, ha="right")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title(
        "Ethical Term Occurrences by Organization\n"
        "(log₁₊ scale; cell values = raw counts)",
        fontsize=11, pad=14,
    )

    # Branch legend
    patches = [
        mpatches.Patch(color=c, label=BRANCH_LABELS[b])
        for b, c in BRANCH_COLORS.items()
    ]
    ax.legend(handles=patches, loc="lower right", fontsize=8,
              title="Branch", title_fontsize=8, framealpha=0.85)

    plt.tight_layout()
    out = OUT_DIR / "fig_cat1_heatmap.png"
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out.name}")


# ── Figure 2: EN vs FR Drift Type Distribution ────────────────────────────────

def fig_drift(conn):
    df = q(conn, """
        SELECT branch, drift_type_en AS drift_type, 'English' AS language
        FROM ethical_term_catalogue
        WHERE drift_type_en IS NOT NULL
        UNION ALL
        SELECT branch, drift_type_fr, 'French'
        FROM ethical_term_catalogue
        WHERE drift_type_fr IS NOT NULL;
    """)

    drift_order = [
        "instrumentalized", "narrowed", "reframed", "hollowed",
        "legalized", "bifurcated", "unnamed", "faithful", "expanded", "absent",
    ]
    branch_order = ["metaethics", "normative_ethics", "applied_ethics"]

    counts = (
        df.groupby(["language", "drift_type"])
          .size()
          .reset_index(name="n")
    )

    fig, axes = plt.subplots(1, 2, figsize=(13, 6), sharey=True)

    for ax, lang in zip(axes, ["English", "French"]):
        sub = counts[counts["language"] == lang].copy()
        sub["drift_type"] = pd.Categorical(sub["drift_type"],
                                           categories=drift_order, ordered=True)
        sub = sub.sort_values("drift_type")
        colors = [DRIFT_PALETTE.get(d, "#aaa") for d in sub["drift_type"]]
        bars = ax.barh(sub["drift_type"], sub["n"], color=colors,
                       edgecolor="white", linewidth=0.8)
        ax.bar_label(bars, padding=3, fontsize=9)
        ax.set_xlim(0, sub["n"].max() + 3)
        ax.set_title(f"{lang} Submissions", fontsize=11, fontweight="bold")
        ax.set_xlabel("Number of terms")
        ax.tick_params(axis="y", labelsize=9)

    fig.suptitle(
        "Drift Type Distribution: How Ethical Terms Shift from Their Philosophical Origins\n"
        "(EN vs FR, across 37 terms)",
        fontsize=12, y=1.01,
    )

    # Shared drift-type legend
    patches = [
        mpatches.Patch(color=DRIFT_PALETTE.get(d, "#aaa"), label=d)
        for d in drift_order
    ]
    fig.legend(handles=patches, loc="lower center", ncol=5,
               fontsize=8, framealpha=0.85, bbox_to_anchor=(0.5, -0.08))

    plt.tight_layout()
    out = OUT_DIR / "fig_cat2_drift.png"
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out.name}")


# ── Figure 3: EN÷FR Ratio Ranked Bar Chart ────────────────────────────────────

def fig_ratio(conn):
    df = q(conn, """
        SELECT term_en, branch, en_fr_divergence_type,
               corpus_frequency_en AS en_n,
               corpus_frequency_fr AS fr_n,
               en_fr_frequency_ratio AS ratio
        FROM ethical_term_catalogue
        WHERE corpus_frequency_en > 0 OR corpus_frequency_fr > 0
        ORDER BY en_fr_frequency_ratio DESC NULLS LAST;
    """)

    # Terms with no ratio get a special treatment
    df_ratio = df[df["ratio"].notna()].copy()
    df_en_only = df[(df["en_n"] > 0) & (df["fr_n"] == 0)].copy()
    df_fr_only = df[(df["en_n"] == 0) & (df["fr_n"] > 0)].copy()
    df_absent  = df[(df["en_n"] == 0) & (df["fr_n"] == 0)].copy()

    # Assign synthetic ratios for plotting
    df_en_only["ratio_plot"] = df_ratio["ratio"].max() + 1.5
    df_fr_only["ratio_plot"] = -1.0
    df_absent["ratio_plot"]  = 0.0
    df_ratio["ratio_plot"]   = df_ratio["ratio"]

    combined = pd.concat([df_en_only, df_ratio, df_fr_only, df_absent])
    combined = combined.sort_values("ratio_plot", ascending=False)

    fig, ax = plt.subplots(figsize=(9, 14))

    colors = [DIV_PALETTE.get(d, "#aaa") for d in combined["en_fr_divergence_type"]]
    branch_edgecolors = [BRANCH_COLORS.get(b, "#333") for b in combined["branch"]]

    bars = ax.barh(
        combined["term_en"], combined["ratio_plot"],
        color=colors, edgecolor=branch_edgecolors, linewidth=1.5,
    )

    # Reference line: EN = FR
    ax.axvline(1.0, color="#555", linewidth=1.2, linestyle="--", alpha=0.7)
    ax.text(1.02, len(combined) - 0.5, "EN = FR", fontsize=8, color="#555")

    # Annotate with EN / FR counts
    for bar, (_, row) in zip(bars, combined.iterrows()):
        en_n = int(row["en_n"])
        fr_n = int(row["fr_n"])
        label = f"EN:{en_n} FR:{fr_n}"
        x_pos = bar.get_width() + 0.08
        ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                label, va="center", fontsize=7, color="#333")

    # Colour Y-axis labels by branch
    term_to_branch = combined.set_index("term_en")["branch"].to_dict()
    for lbl in ax.get_yticklabels():
        b = term_to_branch.get(lbl.get_text(), "applied_ethics")
        lbl.set_color(BRANCH_COLORS.get(b, "#333"))
        lbl.set_fontsize(8.5)

    ax.set_xlabel("EN÷FR Frequency Ratio  (>1 = EN-dominant, <1 = FR-dominant)", fontsize=9)
    ax.set_title(
        "English vs French Frequency Ratio — All Ethical Terms\n"
        "(bar colour = divergence type; border = branch)",
        fontsize=11, pad=12,
    )

    # Legends
    div_patches = [
        mpatches.Patch(color=DIV_PALETTE.get(d, "#aaa"), label=d)
        for d in DIV_PALETTE
    ]
    branch_patches = [
        mpatches.Patch(facecolor="white", edgecolor=c, linewidth=2,
                       label=BRANCH_LABELS[b])
        for b, c in BRANCH_COLORS.items()
    ]
    leg1 = ax.legend(handles=div_patches, title="Divergence type",
                     loc="lower right", fontsize=7.5, title_fontsize=8)
    ax.add_artist(leg1)
    ax.legend(handles=branch_patches, title="Branch",
              loc="upper right", fontsize=7.5, title_fontsize=8)

    plt.tight_layout()
    out = OUT_DIR / "fig_cat3_ratio.png"
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out.name}")


# ── Figure 4: Term × Divergence-type Matrix ───────────────────────────────────

def fig_divergence_matrix(conn):
    df = q(conn, """
        SELECT term_en, branch, drift_type_en, drift_type_fr,
               en_fr_divergence_type
        FROM ethical_term_catalogue
        ORDER BY branch, term_id;
    """)

    drift_order_en = [
        "instrumentalized", "narrowed", "reframed", "hollowed",
        "legalized", "bifurcated", "unnamed", "faithful", "expanded", "absent",
    ]
    drift_order_fr = drift_order_en.copy()

    # Build a 37 × (10 EN + 10 FR) presence matrix
    terms = df["term_en"].tolist()
    cols_en = [f"EN:{d}" for d in drift_order_en]
    cols_fr = [f"FR:{d}" for d in drift_order_fr]
    all_cols = cols_en + cols_fr

    mat = pd.DataFrame(0, index=terms, columns=all_cols)
    for _, row in df.iterrows():
        t = row["term_en"]
        if row["drift_type_en"]:
            col = f"EN:{row['drift_type_en']}"
            if col in mat.columns:
                mat.loc[t, col] = 1
        if row["drift_type_fr"]:
            col = f"FR:{row['drift_type_fr']}"
            if col in mat.columns:
                mat.loc[t, col] = 1

    # Colour map: EN columns one shade, FR another
    cmap_en = matplotlib.colors.ListedColormap(["#f8f8f8", "#C0392B"])
    cmap_fr = matplotlib.colors.ListedColormap(["#f8f8f8", "#1A6B8A"])

    fig, axes = plt.subplots(1, 2, figsize=(14, 13),
                             gridspec_kw={"width_ratios": [1, 1], "wspace": 0.05})

    branch_map = df.set_index("term_en")["branch"].to_dict()

    for ax, cols, cmap, lang, lang_key in [
        (axes[0], drift_order_en, cmap_en, "English", "EN"),
        (axes[1], drift_order_fr, cmap_fr, "French", "FR"),
    ]:
        sub = mat[[f"{lang_key}:{c}" for c in cols]]
        sub.columns = cols

        sns.heatmap(
            sub, ax=ax, cmap=cmap,
            linewidths=0.5, linecolor="#ddd",
            cbar=False, vmin=0, vmax=1,
        )
        ax.set_title(f"{lang} Drift Types", fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Drift type", fontsize=9)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=8)

        if ax is axes[0]:
            for lbl in ax.get_yticklabels():
                b = branch_map.get(lbl.get_text(), "applied_ethics")
                lbl.set_color(BRANCH_COLORS.get(b, "#333"))
                lbl.set_fontsize(8.5)
            ax.set_ylabel("")
        else:
            ax.set_yticks([])
            ax.set_ylabel("")

    # Branch legend on right panel
    patches = [
        mpatches.Patch(color=c, label=BRANCH_LABELS[b])
        for b, c in BRANCH_COLORS.items()
    ]
    axes[1].legend(handles=patches, loc="lower right", fontsize=8,
                   title="Branch", title_fontsize=8, framealpha=0.9)

    fig.suptitle(
        "Drift Type Matrix: Each Term's Classification in English and French\n"
        "(filled cell = that drift type applies to this term)",
        fontsize=12, y=1.01,
    )
    plt.tight_layout()
    out = OUT_DIR / "fig_cat4_divergence_matrix.png"
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out.name}")


# ── Concordance HTML ──────────────────────────────────────────────────────────

def export_concordance_html(conn):
    df = q(conn, """
        SELECT
            o.term_en, o.branch, o.organization, o.submission_language,
            o.field, o.match_language,
            o.matched_variant,
            o.context_before, o.matched_text, o.context_after,
            o.sentence
        FROM ethical_term_occurrences o
        ORDER BY o.branch, o.term_en, o.match_language, o.organization;
    """)

    drift = q(conn, """
        SELECT term_en,
               drift_type_en AS en_drift,
               drift_type_fr AS fr_drift,
               en_fr_divergence_type AS divergence
        FROM ethical_term_catalogue;
    """)
    df = df.merge(drift, on="term_en", how="left")

    rows_html = []
    for _, r in df.iterrows():
        kwic = (
            f'<span class="ctx">{r["context_before"]}</span> '
            f'<strong class="kw">{r["matched_text"]}</strong> '
            f'<span class="ctx">{r["context_after"]}</span>'
        )
        lang_badge = (
            f'<span class="badge {"en" if r["match_language"]=="en" else "fr"}">'
            f'{r["match_language"].upper()}</span>'
        )
        branch_class = r["branch"].replace("_", "-")
        rows_html.append(f"""
        <tr class="branch-{branch_class}"
            data-term="{r['term_en']}"
            data-lang="{r['match_language']}"
            data-branch="{r['branch']}"
            data-org="{r['organization']}"
            data-drift="{r['en_drift'] if r['match_language']=='en' else r['fr_drift']}">
          <td>{r['term_en']}</td>
          <td>{lang_badge}</td>
          <td><span class="branch {branch_class}">{BRANCH_LABELS.get(r['branch'],r['branch'])}</span></td>
          <td>{r['organization']}</td>
          <td>{r['field']}</td>
          <td class="kwic">{kwic}</td>
          <td><small>{r.get('en_drift','') if r['match_language']=='en' else r.get('fr_drift','')}</small></td>
        </tr>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Ethical Term Concordance — AIA Corpus</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; font-size: 13px;
          margin: 0; background: #f9f9f9; color: #222; }}
  h1   {{ background: #1a1a2e; color: #fff; margin: 0; padding: 18px 24px; font-size: 18px; }}
  .controls {{ background: #fff; border-bottom: 1px solid #ddd;
               padding: 12px 24px; display: flex; gap: 16px; flex-wrap: wrap; align-items: center; }}
  .controls label {{ font-size: 12px; color: #555; }}
  select, input {{ border: 1px solid #ccc; border-radius: 4px;
                   padding: 5px 8px; font-size: 12px; }}
  #count {{ margin-left: auto; font-size: 12px; color: #888; }}
  table  {{ border-collapse: collapse; width: 100%; background: #fff; }}
  th     {{ background: #2c3e50; color: #fff; padding: 8px 10px;
            font-size: 12px; position: sticky; top: 0; z-index: 2; text-align: left; }}
  td     {{ padding: 6px 10px; border-bottom: 1px solid #eee; vertical-align: top; }}
  tr:hover {{ background: #f0f4ff; }}
  .badge {{ padding: 2px 6px; border-radius: 3px; font-size: 11px; font-weight: bold; }}
  .badge.en {{ background: #d4edda; color: #155724; }}
  .badge.fr {{ background: #cce5ff; color: #004085; }}
  .branch  {{ display: inline-block; padding: 2px 7px; border-radius: 10px;
              font-size: 11px; font-weight: 600; }}
  .branch.metaethics       {{ background: #f3e5f5; color: #7B2D8B; }}
  .branch.normative-ethics {{ background: #e0f2f7; color: #1A6B8A; }}
  .branch.applied-ethics   {{ background: #fdecea; color: #C0392B; }}
  .ctx {{ color: #777; }}
  .kw  {{ color: #c0392b; background: #fef9e7; padding: 1px 3px; border-radius: 2px; }}
  .kwic {{ font-size: 12px; max-width: 580px; line-height: 1.5; }}
  tr.hidden {{ display: none; }}
</style>
</head>
<body>
<h1>Ethical Term Concordance — AIA Bilingual Corpus &nbsp;
    <small style="font-weight:normal;font-size:13px">{len(df):,} matches · 37 terms · 114 submissions</small>
</h1>
<div class="controls">
  <div>
    <label>Term</label><br>
    <select id="fTerm" onchange="filter()">
      <option value="">All terms</option>
      {''.join(f'<option>{t}</option>' for t in sorted(df["term_en"].unique()))}
    </select>
  </div>
  <div>
    <label>Language</label><br>
    <select id="fLang" onchange="filter()">
      <option value="">EN + FR</option>
      <option value="en">English only</option>
      <option value="fr">French only</option>
    </select>
  </div>
  <div>
    <label>Branch</label><br>
    <select id="fBranch" onchange="filter()">
      <option value="">All branches</option>
      <option value="metaethics">Metaethics</option>
      <option value="normative_ethics">Normative Ethics</option>
      <option value="applied_ethics">Applied Ethics</option>
    </select>
  </div>
  <div>
    <label>Organization</label><br>
    <select id="fOrg" onchange="filter()">
      <option value="">All orgs</option>
      {''.join(f'<option>{o}</option>' for o in sorted(df["organization"].unique()))}
    </select>
  </div>
  <div>
    <label>Drift type</label><br>
    <select id="fDrift" onchange="filter()">
      <option value="">All drift types</option>
      {''.join(f'<option>{d}</option>' for d in sorted(set(
          list(df["en_drift"].dropna()) + list(df["fr_drift"].dropna())
      )))}
    </select>
  </div>
  <div>
    <label>Search text</label><br>
    <input type="text" id="fSearch" placeholder="keyword in sentence…" oninput="filter()">
  </div>
  <div id="count"></div>
</div>
<table id="concordTable">
<thead>
  <tr>
    <th>Term</th><th>Lang</th><th>Branch</th>
    <th>Organization</th><th>Field</th><th>KWIC Context</th><th>Drift type</th>
  </tr>
</thead>
<tbody>
{''.join(rows_html)}
</tbody>
</table>
<script>
function filter() {{
  const term   = document.getElementById('fTerm').value.toLowerCase();
  const lang   = document.getElementById('fLang').value.toLowerCase();
  const branch = document.getElementById('fBranch').value.toLowerCase();
  const org    = document.getElementById('fOrg').value.toLowerCase();
  const drift  = document.getElementById('fDrift').value.toLowerCase();
  const search = document.getElementById('fSearch').value.toLowerCase();
  let visible  = 0;
  document.querySelectorAll('#concordTable tbody tr').forEach(row => {{
    const m =
      (!term   || row.dataset.term.toLowerCase()   === term)   &&
      (!lang   || row.dataset.lang.toLowerCase()   === lang)   &&
      (!branch || row.dataset.branch.toLowerCase() === branch) &&
      (!org    || row.dataset.org.toLowerCase().includes(org)) &&
      (!drift  || row.dataset.drift.toLowerCase()  === drift)  &&
      (!search || row.textContent.toLowerCase().includes(search));
    row.classList.toggle('hidden', !m);
    if (m) visible++;
  }});
  document.getElementById('count').textContent = visible + ' rows shown';
}}
filter();
</script>
</body>
</html>"""

    out = OUT_DIR / "ethical_term_concordance.html"
    out.write_text(html, encoding="utf-8")
    print(f"  Saved {out.name}  ({len(df):,} concordance rows)")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    print("Phase 6: Creating catalogue visualizations\n")
    conn = psycopg2.connect(dbname=DB_NAME)
    try:
        print("Figure 1 — Term × Organization heatmap...")
        fig_heatmap(conn)

        print("Figure 2 — Drift type distribution (EN vs FR)...")
        fig_drift(conn)

        print("Figure 3 — EN÷FR frequency ratio ranked chart...")
        fig_ratio(conn)

        print("Figure 4 — Term × Divergence-type matrix...")
        fig_divergence_matrix(conn)

        print("Concordance HTML viewer...")
        export_concordance_html(conn)

    finally:
        conn.close()

    print(f"\nAll outputs saved to  {OUT_DIR}/")


if __name__ == "__main__":
    main()
