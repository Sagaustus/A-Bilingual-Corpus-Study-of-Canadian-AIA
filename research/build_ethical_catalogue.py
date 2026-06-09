#!/usr/bin/env python3
"""
Phase 5: Assemble the Catalogue of Ethical Terminologies.

Joins all Phase 1-4 artefacts into:
  1. PostgreSQL table  — ethical_term_catalogue
  2. CSV export        — data/ethical_term_catalogue.csv
  3. Markdown report   — research/ETHICAL_TERM_CATALOGUE.md
  4. JSON export       — data/ethical_term_catalogue.json
"""

import csv
import json
import textwrap
from datetime import date
from pathlib import Path
import psycopg2
import psycopg2.extras

DB_NAME   = "aia_corpus"
DATA_DIR  = Path(__file__).parent.parent / "data"
RES_DIR   = Path(__file__).parent
DATA_DIR.mkdir(exist_ok=True)

BRANCH_LABELS = {
    "metaethics":       "Metaethics",
    "normative_ethics": "Normative Ethics",
    "applied_ethics":   "Applied Ethics",
}

# ── 1. PostgreSQL catalogue table ─────────────────────────────────────────────

CREATE_CATALOGUE = """
DROP TABLE IF EXISTS ethical_term_catalogue CASCADE;

CREATE TABLE ethical_term_catalogue (
    term_id                     TEXT PRIMARY KEY REFERENCES ethical_term_lexicon(id),
    term_en                     TEXT NOT NULL,
    term_fr                     TEXT NOT NULL,
    branch                      TEXT NOT NULL,
    tradition                   TEXT NOT NULL,
    key_philosophers            TEXT NOT NULL,
    philosophical_definition_en TEXT NOT NULL,
    philosophical_definition_fr TEXT NOT NULL,
    aia_relevance               TEXT,

    -- Corpus frequencies
    corpus_frequency_en         INTEGER NOT NULL DEFAULT 0,
    corpus_frequency_fr         INTEGER NOT NULL DEFAULT 0,
    submission_count_en         INTEGER NOT NULL DEFAULT 0,
    submission_count_fr         INTEGER NOT NULL DEFAULT 0,
    en_fr_frequency_ratio       NUMERIC(6,2),

    -- Drift analysis (Phase 3)
    philosophical_origin_summary TEXT,
    dominant_usage_en           TEXT,
    dominant_usage_fr           TEXT,
    drift_type_en               TEXT,
    drift_type_fr               TEXT,
    drift_description_en        TEXT,
    drift_description_fr        TEXT,

    -- Cross-linguistic divergence (Phase 4)
    en_fr_divergence_type       TEXT,
    en_fr_key_contrast          TEXT,
    en_fr_philosophical_significance TEXT,

    -- Representative corpus examples
    key_example_en              TEXT,
    key_example_fr              TEXT,

    -- Synthesis
    key_finding                 TEXT,
    predicted_drift             TEXT,

    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE ethical_term_catalogue IS
  'Phase 5: Master Catalogue of Ethical Terminologies — one row per term, synthesising lexicon, corpus frequencies, LLM drift analysis, and cross-linguistic divergence findings.';
"""

POPULATE_CATALOGUE = """
INSERT INTO ethical_term_catalogue (
    term_id, term_en, term_fr, branch, tradition, key_philosophers,
    philosophical_definition_en, philosophical_definition_fr, aia_relevance,
    corpus_frequency_en, corpus_frequency_fr,
    submission_count_en, submission_count_fr, en_fr_frequency_ratio,
    philosophical_origin_summary,
    dominant_usage_en, dominant_usage_fr,
    drift_type_en, drift_type_fr,
    drift_description_en, drift_description_fr,
    en_fr_divergence_type, en_fr_key_contrast, en_fr_philosophical_significance,
    key_example_en, key_example_fr,
    key_finding, predicted_drift
)
SELECT
    l.id,
    l.term_en,
    array_to_string(l.term_fr, ' / ')          AS term_fr,
    l.branch,
    array_to_string(l.tradition, ', ')         AS tradition,
    array_to_string(l.key_philosophers, '; ')  AS key_philosophers,
    l.canonical_definition_en,
    l.canonical_definition_fr,
    l.aia_relevance,

    COALESCE(fe.total_en, 0),
    COALESCE(ff.total_fr, 0),
    COALESCE(fe.sub_en,   0),
    COALESCE(ff.sub_fr,   0),
    CASE
        WHEN COALESCE(ff.total_fr, 0) = 0 AND COALESCE(fe.total_en, 0) = 0 THEN NULL
        WHEN COALESCE(ff.total_fr, 0) = 0 THEN NULL
        WHEN COALESCE(fe.total_en, 0) = 0 THEN NULL
        ELSE ROUND(COALESCE(fe.total_en,0)::numeric / COALESCE(ff.total_fr,1), 2)
    END,

    a.philosophical_origin_summary,
    a.en_usage_summary,
    a.fr_usage_summary,
    a.en_drift_type,
    a.fr_drift_type,
    a.en_drift_description,
    a.fr_drift_description,
    a.en_fr_divergence_type,
    a.en_fr_key_contrast,
    a.en_fr_philosophical_significance,

    ex_en.sentence,
    ex_fr.sentence,

    a.key_finding,
    l.expected_drift

FROM ethical_term_lexicon l
LEFT JOIN ethical_term_analysis a ON a.term_id = l.id
LEFT JOIN (
    SELECT term_id, SUM(occurrence_count) AS total_en, SUM(submission_count) AS sub_en
    FROM ethical_term_frequency WHERE match_language = 'en' GROUP BY term_id
) fe ON fe.term_id = l.id
LEFT JOIN (
    SELECT term_id, SUM(occurrence_count) AS total_fr, SUM(submission_count) AS sub_fr
    FROM ethical_term_frequency WHERE match_language = 'fr' GROUP BY term_id
) ff ON ff.term_id = l.id
LEFT JOIN LATERAL (
    SELECT sentence FROM ethical_term_occurrences
    WHERE term_id = l.id AND match_language = 'en' AND LENGTH(sentence) > 40
    ORDER BY LENGTH(sentence) DESC LIMIT 1
) ex_en ON true
LEFT JOIN LATERAL (
    SELECT sentence FROM ethical_term_occurrences
    WHERE term_id = l.id AND match_language = 'fr' AND LENGTH(sentence) > 40
    ORDER BY LENGTH(sentence) DESC LIMIT 1
) ex_fr ON true
ORDER BY l.branch, l.id;
"""


def build_db_table(conn):
    with conn.cursor() as cur:
        cur.execute(CREATE_CATALOGUE)
        cur.execute(POPULATE_CATALOGUE)
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM ethical_term_catalogue;")
        n = cur.fetchone()[0]
    print(f"  ethical_term_catalogue: {n} rows")


# ── 2. Load catalogue rows ─────────────────────────────────────────────────────

def load_catalogue(conn) -> list[dict]:
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT * FROM ethical_term_catalogue
            ORDER BY branch, term_id;
        """)
        return [dict(r) for r in cur.fetchall()]


# ── 3. CSV export ──────────────────────────────────────────────────────────────

CSV_FIELDS = [
    "term_id", "term_en", "term_fr", "branch", "tradition", "key_philosophers",
    "corpus_frequency_en", "corpus_frequency_fr",
    "submission_count_en", "submission_count_fr", "en_fr_frequency_ratio",
    "drift_type_en", "drift_type_fr", "en_fr_divergence_type",
    "dominant_usage_en", "dominant_usage_fr",
    "drift_description_en", "drift_description_fr",
    "en_fr_key_contrast", "en_fr_philosophical_significance",
    "key_example_en", "key_example_fr",
    "key_finding",
    "philosophical_definition_en", "philosophical_definition_fr",
    "philosophical_origin_summary", "aia_relevance",
]


def export_csv(rows: list[dict], path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (row.get(k) or "") for k in CSV_FIELDS})
    print(f"  CSV:  {path}")


# ── 4. JSON export ─────────────────────────────────────────────────────────────

def export_json(rows: list[dict], path: Path):
    output = {
        "metadata": {
            "title": "Catalogue of Ethical Terminologies — Canadian AIA Bilingual Corpus",
            "generated": str(date.today()),
            "total_terms": len(rows),
            "description": (
                "One entry per ethical term. Covers metaethics, normative ethics, "
                "and applied AI ethics. Each entry documents the philosophical origin, "
                "corpus frequency (EN/FR), drift type, and cross-linguistic divergence "
                "as found in 114 Canadian Algorithmic Impact Assessment submissions."
            ),
        },
        "terms": [
            {k: (v if v is not None else "") for k, v in row.items()
             if k not in ("created_at",)}
            for row in rows
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2, default=str)
    print(f"  JSON: {path}")


# ── 5. Markdown catalogue ──────────────────────────────────────────────────────

DRIFT_EMOJI = {
    "instrumentalized": "🔧",
    "hollowed":         "🕳️",
    "reframed":         "🔄",
    "narrowed":         "🔍",
    "bifurcated":       "⚡",
    "legalized":        "⚖️",
    "faithful":         "✅",
    "expanded":         "🌐",
    "unnamed":          "👻",
    "absent":           "❌",
}

DIV_EMOJI = {
    "conceptual_shift":    "🔀",
    "asymmetric_emphasis": "⚖️",
    "omission":            "🚫",
    "addition":            "➕",
    "register":            "🎭",
    "terminological":      "🔤",
    "faithful":            "✅",
}


def wrap(text: str | None, width: int = 100, indent: str = "") -> str:
    if not text:
        return "_Not recorded._"
    lines = textwrap.wrap(text.strip(), width=width)
    return ("\n" + indent).join(lines)


def entry_md(row: dict) -> str:
    tid      = row["term_id"]
    term_en  = row["term_en"]
    term_fr  = row["term_fr"]
    branch   = BRANCH_LABELS.get(row["branch"], row["branch"])
    trad     = row["tradition"] or "—"
    phil     = row["key_philosophers"] or "—"

    en_freq   = row["corpus_frequency_en"] or 0
    fr_freq   = row["corpus_frequency_fr"] or 0
    en_subs   = row["submission_count_en"] or 0
    fr_subs   = row["submission_count_fr"] or 0
    ratio     = row["en_fr_frequency_ratio"]
    ratio_str = f"{ratio:.2f}" if ratio else "N/A"

    d_en  = row["drift_type_en"]  or "—"
    d_fr  = row["drift_type_fr"]  or "—"
    div_t = row["en_fr_divergence_type"] or "—"

    de_emoji  = DRIFT_EMOJI.get(d_en, "")
    df_emoji  = DRIFT_EMOJI.get(d_fr, "")
    div_emoji = DIV_EMOJI.get(div_t, "")

    lines = [
        f"---",
        f"",
        f"### `{tid}` — {term_en}",
        f"",
        f"**FR equivalent(s):** {term_fr}  ",
        f"**Branch:** {branch}  ",
        f"**Tradition(s):** {trad}  ",
        f"**Key philosophers:** {phil}",
        f"",
        f"#### Philosophical Definition",
        f"",
        f"> **EN:** {wrap(row['philosophical_definition_en'], 110)}",
        f">",
        f"> **FR:** {wrap(row['philosophical_definition_fr'], 110)}",
        f"",
        f"#### Corpus Presence",
        f"",
        f"| Language | Occurrences | Submissions |",
        f"|----------|-------------|-------------|",
        f"| English  | {en_freq:>4} | {en_subs:>4} |",
        f"| French   | {fr_freq:>4} | {fr_subs:>4} |",
        f"| **EN÷FR ratio** | **{ratio_str}** | — |",
        f"",
    ]

    if row.get("philosophical_origin_summary"):
        lines += [
            f"#### Philosophical Origin (LLM Summary)",
            f"",
            f"{wrap(row['philosophical_origin_summary'], 110)}",
            f"",
        ]

    lines += [
        f"#### Corpus Usage vs Philosophical Origin",
        f"",
        f"**English** {de_emoji} `{d_en}`",
        f"",
        f"{wrap(row.get('dominant_usage_en'), 110)}",
        f"",
        f"{wrap(row.get('drift_description_en'), 110)}",
        f"",
        f"**French** {df_emoji} `{d_fr}`",
        f"",
        f"{wrap(row.get('dominant_usage_fr'), 110)}",
        f"",
        f"{wrap(row.get('drift_description_fr'), 110)}",
        f"",
    ]

    if row.get("key_example_en"):
        lines += [
            f"**Representative EN corpus sentence:**",
            f"> *{row['key_example_en'].strip()}*",
            f"",
        ]
    if row.get("key_example_fr"):
        lines += [
            f"**Representative FR corpus sentence:**",
            f"> *{row['key_example_fr'].strip()}*",
            f"",
        ]

    lines += [
        f"#### EN/FR Cross-Linguistic Divergence",
        f"",
        f"**Divergence type:** {div_emoji} `{div_t}`",
        f"",
        f"**Key contrast:** {wrap(row.get('en_fr_key_contrast'), 110)}",
        f"",
        f"**Philosophical significance:** {wrap(row.get('en_fr_philosophical_significance'), 110)}",
        f"",
        f"#### Key Finding",
        f"",
        f"> **{wrap(row.get('key_finding'), 110)}**",
        f"",
    ]

    if row.get("aia_relevance"):
        lines += [
            f"_AIA relevance note: {wrap(row['aia_relevance'], 110)}_",
            f"",
        ]

    return "\n".join(lines)


def export_markdown(rows: list[dict], path: Path):
    today = date.today().strftime("%B %d, %Y")
    total = len(rows)

    # Aggregate stats for the preamble
    drift_en_counts: dict[str, int] = {}
    drift_fr_counts: dict[str, int] = {}
    div_counts: dict[str, int] = {}
    for r in rows:
        d = r.get("drift_type_en") or "absent"
        drift_en_counts[d] = drift_en_counts.get(d, 0) + 1
        d = r.get("drift_type_fr") or "absent"
        drift_fr_counts[d] = drift_fr_counts.get(d, 0) + 1
        d = r.get("en_fr_divergence_type") or "unknown"
        div_counts[d] = div_counts.get(d, 0) + 1

    def top(d: dict) -> str:
        return ", ".join(f"{k} ({v})" for k, v in sorted(d.items(), key=lambda x: -x[1]))

    header = [
        f"# Catalogue of Ethical Terminologies",
        f"## Canadian Algorithmic Impact Assessment (AIA) — Bilingual Corpus Study",
        f"",
        f"**Generated:** {today}  ",
        f"**Total terms:** {total}  ",
        f"**Corpus:** 114 federal AIA submissions (57 EN · 36 FR · 21 bilingual)  ",
        f"**Branches covered:** Metaethics · Normative Ethics · Applied Ethics  ",
        f"**Languages:** English / French (Canadian)",
        f"",
        f"---",
        f"",
        f"## About this Catalogue",
        f"",
        f"This catalogue documents {total} ethical terms drawn from three branches of philosophy",
        f"as they appear — and are transformed — in Canadian federal Algorithmic Impact Assessments.",
        f"Each entry records:",
        f"",
        f"- The term's **philosophical origin** (tradition, key thinkers, canonical definition)",
        f"- Its **corpus frequency** in English and French submissions",
        f"- The **drift type** — how and why the term's meaning has shifted from its philosophical origin",
        f"- The **cross-linguistic divergence** — how English and French submissions conceptualize",
        f"  the term differently from each other",
        f"- **Representative corpus sentences** in both languages",
        f"- A **key finding** synthesizing the most important insight for each term",
        f"",
        f"### Drift Type Legend",
        f"",
        f"| Symbol | Type | Meaning |",
        f"|--------|------|---------|",
        f"| 🔧 | instrumentalized | Term used as metric/score/checkbox rather than moral concept |",
        f"| 🕳️ | hollowed | Term present; concept it carries evacuated |",
        f"| 🔄 | reframed | Term repurposed toward efficiency or compliance |",
        f"| 🔍 | narrowed | Term restricted to a subset of its philosophical meaning |",
        f"| ⚡ | bifurcated | Term used in two incompatible senses simultaneously |",
        f"| ⚖️ | legalized | Meaning collapsed into legal definition |",
        f"| ✅ | faithful | Close alignment with philosophical origin |",
        f"| 🌐 | expanded | Term carries more meaning than philosophical origin |",
        f"| 👻 | unnamed | Concept operationalized without being named |",
        f"| ❌ | absent | Term variants appear but concept is missing/unrelated |",
        f"",
        f"### Cross-Linguistic Divergence Legend",
        f"",
        f"| Symbol | Type | Meaning |",
        f"|--------|------|---------|",
        f"| 🔀 | conceptual_shift | Different word, meaningfully different concept |",
        f"| ⚖️ | asymmetric_emphasis | Both languages use the term; one foregrounds it far more |",
        f"| 🚫 | omission | Concept articulated in one language, absent in the other |",
        f"| ➕ | addition | One language introduces a concept the other omits |",
        f"| 🎭 | register | Same concept; bureaucratic register in one, moral in the other |",
        f"| 🔤 | terminological | Different word, essentially same concept |",
        f"| ✅ | faithful | EN and FR treat the term similarly |",
        f"",
        f"---",
        f"",
        f"## Corpus-Level Summary",
        f"",
        f"**EN drift distribution:** {top(drift_en_counts)}",
        f"",
        f"**FR drift distribution:** {top(drift_fr_counts)}",
        f"",
        f"**Cross-linguistic divergence distribution:** {top(div_counts)}",
        f"",
        f"---",
        f"",
    ]

    # Group by branch
    by_branch: dict[str, list[dict]] = {}
    for row in rows:
        b = row["branch"]
        by_branch.setdefault(b, []).append(row)

    branch_order = ["metaethics", "normative_ethics", "applied_ethics"]
    body_lines = []

    for b in branch_order:
        branch_rows = by_branch.get(b, [])
        if not branch_rows:
            continue
        label = BRANCH_LABELS[b]
        body_lines += [
            f"## Branch I: {label}" if b == "metaethics"
            else f"## Branch II: {label}" if b == "normative_ethics"
            else f"## Branch III: {label}",
            f"",
            f"_{len(branch_rows)} terms_",
            f"",
        ]
        # TOC for branch
        for row in branch_rows:
            d_en = DRIFT_EMOJI.get(row.get("drift_type_en") or "", "")
            d_fr = DRIFT_EMOJI.get(row.get("drift_type_fr") or "", "")
            en_n = row["corpus_frequency_en"] or 0
            fr_n = row["corpus_frequency_fr"] or 0
            body_lines.append(
                f"- **[{row['term_id']}]** {row['term_en']} / {row['term_fr']}  "
                f"  EN:{en_n} FR:{fr_n}  "
                f"  drift EN:{d_en} FR:{d_fr}"
            )
        body_lines.append("")

        for row in branch_rows:
            body_lines.append(entry_md(row))
            body_lines.append("")

    full = "\n".join(header + body_lines)
    path.write_text(full, encoding="utf-8")
    print(f"  MD:   {path}  ({len(full):,} chars, {full.count(chr(10))} lines)")


# ── 6. Console summary ─────────────────────────────────────────────────────────

def print_summary(rows: list[dict]):
    print("\n━━━ Catalogue Summary ━━━")
    print(f"  {'Term':<22} {'EN':>5} {'FR':>5} {'Ratio':>6}  "
          f"{'EN drift':<16} {'FR drift':<16} {'EN/FR divergence'}")
    print(f"  {'-'*22} {'-'*5} {'-'*5} {'-'*6}  {'-'*16} {'-'*16} {'-'*22}")

    current_branch = None
    for row in rows:
        if row["branch"] != current_branch:
            print(f"\n  ── {BRANCH_LABELS.get(row['branch'], row['branch']).upper()} ──")
            current_branch = row["branch"]
        ratio = row["en_fr_frequency_ratio"]
        ratio_str = f"{ratio:.2f}" if ratio else "  N/A"
        print(
            f"  {row['term_en']:<22} "
            f"{row['corpus_frequency_en']:>5} "
            f"{row['corpus_frequency_fr']:>5} "
            f"{ratio_str:>6}  "
            f"{(row['drift_type_en'] or '—'):<16} "
            f"{(row['drift_type_fr'] or '—'):<16} "
            f"{row['en_fr_divergence_type'] or '—'}"
        )

    total_en = sum(r["corpus_frequency_en"] or 0 for r in rows)
    total_fr = sum(r["corpus_frequency_fr"] or 0 for r in rows)
    print(f"\n  {'TOTALS':<22} {total_en:>5} {total_fr:>5}")

    # Highlight the 3 conceptual shifts
    print("\n━━━ Conceptual shifts (most significant divergences) ━━━")
    for row in rows:
        if row["en_fr_divergence_type"] == "conceptual_shift":
            print(f"\n  [{row['term_id']}] {row['term_en']}")
            print(f"  EN: {row['drift_type_en']}  →  FR: {row['drift_type_fr']}")
            contrast = (row.get("en_fr_key_contrast") or "")[:180]
            print(f"  {contrast}")

    # Faithful FR where EN is worse
    print("\n━━━ Terms where French is more philosophically faithful than English ━━━")
    for row in rows:
        if row.get("drift_type_fr") == "faithful" and row.get("drift_type_en") != "faithful":
            print(f"  [{row['term_id']}] {row['term_en']}  —  EN: {row['drift_type_en']}  FR: {row['drift_type_fr']}")

    # Expanded (only one)
    print("\n━━━ Terms where French expands beyond philosophical origin ━━━")
    for row in rows:
        if row.get("drift_type_fr") == "expanded":
            print(f"  [{row['term_id']}] {row['term_en']}  —  EN: {row['drift_type_en']}  FR: {row['drift_type_fr']}")
            print(f"  {(row.get('key_finding') or '')[:180]}")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    print("Phase 5: Catalogue of Ethical Terminologies\n")

    conn = psycopg2.connect(dbname=DB_NAME)
    try:
        print("Building PostgreSQL catalogue table...")
        build_db_table(conn)

        rows = load_catalogue(conn)

        print("Exporting artefacts...")
        export_csv(rows,      DATA_DIR / "ethical_term_catalogue.csv")
        export_json(rows,     DATA_DIR / "ethical_term_catalogue.json")
        export_markdown(rows, RES_DIR  / "ETHICAL_TERM_CATALOGUE.md")

        print_summary(rows)

    finally:
        conn.close()

    print("\nPhase 5 complete.")
    print("  DB table : ethical_term_catalogue")
    print("  CSV      : data/ethical_term_catalogue.csv")
    print("  JSON     : data/ethical_term_catalogue.json")
    print("  Markdown : research/ETHICAL_TERM_CATALOGUE.md")


if __name__ == "__main__":
    main()
