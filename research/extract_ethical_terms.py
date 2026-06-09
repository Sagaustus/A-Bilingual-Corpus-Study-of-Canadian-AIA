#!/usr/bin/env python3
"""
Phase 2: Corpus Extraction & Concordance for the Ethical Term Catalogue.

For every term in ethical_term_lexicon, this script:
  1. Searches all EN and FR text fields across 7 tables
  2. Extracts KWIC (Keyword In Context) windows around each match
  3. Extracts the full sentence containing each match
  4. Writes results to ethical_term_occurrences
  5. Builds a frequency summary in ethical_term_frequency
"""

import re
import sys
import psycopg2
import psycopg2.extras
from dataclasses import dataclass, field
from typing import Optional

DB_NAME = "aia_corpus"
KWIC_WINDOW = 150  # characters either side of the match

# ── Schema ────────────────────────────────────────────────────────────────────

DROP_TABLES = """
DROP TABLE IF EXISTS ethical_term_frequency   CASCADE;
DROP TABLE IF EXISTS ethical_term_occurrences CASCADE;
DROP VIEW  IF EXISTS corpus_text_fields        CASCADE;
"""

CREATE_VIEW = """
CREATE VIEW corpus_text_fields AS

-- project_details
SELECT fs.id AS submission_id, o.name AS organization,
       fs.language AS submission_language,
       'project_title'          AS field,
       pd.project_title_en      AS text_en,
       pd.project_title_fr      AS text_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN project_details pd ON pd.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'project_description',
       pd.description_en, pd.description_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN project_details pd ON pd.submission_id = fs.id

-- about_the_decision
UNION ALL
SELECT fs.id, o.name, fs.language,
       'decision_description',
       ad.decision_description_en, ad.decision_description_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN about_the_decision ad ON ad.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'system_role',
       ad.system_role_en, ad.system_role_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN about_the_decision ad ON ad.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'evaluation_criteria',
       ad.evaluation_criteria_en, ad.evaluation_criteria_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN about_the_decision ad ON ad.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'system_output',
       ad.system_output_en, ad.system_output_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN about_the_decision ad ON ad.submission_id = fs.id

-- individual_impacts
UNION ALL
SELECT fs.id, o.name, fs.language,
       'rights_freedoms',
       ii.rights_freedoms_en, ii.rights_freedoms_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN individual_impacts ii ON ii.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'equality_dignity',
       ii.equality_dignity_en, ii.equality_dignity_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN individual_impacts ii ON ii.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'health_wellbeing',
       ii.health_wellbeing_en, ii.health_wellbeing_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN individual_impacts ii ON ii.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'economic_interests',
       ii.economic_interests_en, ii.economic_interests_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN individual_impacts ii ON ii.submission_id = fs.id

-- reasons_for_automation
UNION ALL
SELECT fs.id, o.name, fs.language,
       'motivation_other',
       r.motivation_other_en, r.motivation_other_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN reasons_for_automation r ON r.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'client_needs',
       r.client_needs_en, r.client_needs_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN reasons_for_automation r ON r.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'public_benefits',
       r.public_benefits_en, r.public_benefits_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN reasons_for_automation r ON r.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'expected_improvements',
       r.expected_improvements_en, r.expected_improvements_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN reasons_for_automation r ON r.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'system_confinement',
       r.system_confinement_en, r.system_confinement_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN reasons_for_automation r ON r.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'trade_offs',
       r.trade_offs_en, r.trade_offs_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN reasons_for_automation r ON r.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'why_automation_preferred',
       r.why_automation_preferred_en, r.why_automation_preferred_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN reasons_for_automation r ON r.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'no_deploy_consequence',
       r.no_deploy_consequence_en, r.no_deploy_consequence_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN reasons_for_automation r ON r.submission_id = fs.id

-- consultation
UNION ALL
SELECT fs.id, o.name, fs.language,
       'internal_stakeholders',
       c.internal_stakeholders_other_en, c.internal_stakeholders_other_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN consultation c ON c.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'external_stakeholders',
       c.external_stakeholders_other_en, c.external_stakeholders_other_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN consultation c ON c.submission_id = fs.id

-- privacy_security
UNION ALL
SELECT fs.id, o.name, fs.language,
       'pia_description',
       ps.pia_description_en, ps.pia_description_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN privacy_security ps ON ps.submission_id = fs.id

UNION ALL
SELECT fs.id, o.name, fs.language,
       'de_identification_method',
       ps.de_identification_method_en, ps.de_identification_method_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN privacy_security ps ON ps.submission_id = fs.id

-- about_the_data
UNION ALL
SELECT fs.id, o.name, fs.language,
       'data_description',
       ad2.data_description_en, ad2.data_description_fr
FROM form_submissions fs
JOIN datasets d ON d.id = fs.dataset_id
JOIN organizations o ON o.id = d.organization_id
JOIN about_the_data ad2 ON ad2.submission_id = fs.id;
"""

CREATE_OCCURRENCES = """
CREATE TABLE ethical_term_occurrences (
    id                  SERIAL PRIMARY KEY,
    term_id             TEXT NOT NULL REFERENCES ethical_term_lexicon(id) ON DELETE CASCADE,
    term_en             TEXT NOT NULL,
    branch              TEXT NOT NULL,
    submission_id       INTEGER NOT NULL REFERENCES form_submissions(id) ON DELETE CASCADE,
    organization        TEXT NOT NULL,
    submission_language TEXT NOT NULL,
    field               TEXT NOT NULL,
    match_language      TEXT NOT NULL CHECK (match_language IN ('en', 'fr')),
    matched_variant     TEXT NOT NULL,
    context_before      TEXT,
    matched_text        TEXT NOT NULL,
    context_after       TEXT,
    sentence            TEXT,
    char_offset         INTEGER,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_eto_term_id   ON ethical_term_occurrences(term_id);
CREATE INDEX idx_eto_sub_id    ON ethical_term_occurrences(submission_id);
CREATE INDEX idx_eto_branch    ON ethical_term_occurrences(branch);
CREATE INDEX idx_eto_match_lang ON ethical_term_occurrences(match_language);

COMMENT ON TABLE ethical_term_occurrences IS
  'Phase 2: one row per match of an ethical term variant in the AIA corpus. Stores KWIC context and sentence for concordance analysis.';
"""

CREATE_FREQUENCY = """
CREATE TABLE ethical_term_frequency (
    term_id             TEXT NOT NULL REFERENCES ethical_term_lexicon(id),
    term_en             TEXT NOT NULL,
    branch              TEXT NOT NULL,
    match_language      TEXT NOT NULL,
    organization        TEXT NOT NULL,
    field               TEXT NOT NULL,
    occurrence_count    INTEGER NOT NULL DEFAULT 0,
    submission_count    INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (term_id, match_language, organization, field)
);

COMMENT ON TABLE ethical_term_frequency IS
  'Phase 2 summary: occurrence and submission counts per term × language × organization × field.';
"""


# ── Helper functions ───────────────────────────────────────────────────────────

def variant_to_pattern(variant: str) -> str:
    """Convert a lexicon variant (which may end in * for prefix match) to a regex pattern."""
    # Escape everything first
    escaped = re.escape(variant.rstrip("*"))
    if variant.endswith("*"):
        # Prefix match: match the stem followed by any word characters
        return r"(?<!\w)" + escaped + r"\w*"
    else:
        # Exact word-boundary match (works for ASCII and most Unicode)
        return r"(?<!\w)" + escaped + r"(?!\w)"


def build_term_patterns(variants: list[str]) -> re.Pattern:
    """Compile a single pattern that matches any variant (case-insensitive, Unicode)."""
    sub_patterns = [variant_to_pattern(v) for v in variants]
    combined = "|".join(f"({p})" for p in sub_patterns)
    return re.compile(combined, re.IGNORECASE | re.UNICODE)


def extract_sentence(text: str, match_start: int, match_end: int) -> str:
    """Extract the sentence containing the match."""
    # Sentence boundaries: . ! ? followed by whitespace or end, or newline
    sentence_end_pattern = re.compile(r"[.!?]\s+|\n")

    # Find start of sentence: scan backwards from match_start
    seg_start = 0
    for m in sentence_end_pattern.finditer(text[:match_start]):
        seg_start = m.end()

    # Find end of sentence: scan forwards from match_end
    seg_end = len(text)
    forward_match = sentence_end_pattern.search(text, match_end)
    if forward_match:
        seg_end = forward_match.end()

    return text[seg_start:seg_end].strip()


def extract_kwic(text: str, match_start: int, match_end: int) -> tuple[str, str, str]:
    """Return (context_before, matched_text, context_after) for a KWIC window."""
    before_start = max(0, match_start - KWIC_WINDOW)
    after_end    = min(len(text), match_end + KWIC_WINDOW)

    before = text[before_start:match_start]
    matched = text[match_start:match_end]
    after  = text[match_end:after_end]

    # Trim to word boundaries so context doesn't start/end mid-word
    if before_start > 0 and before and not before[0].isspace():
        space_idx = before.find(" ")
        before = before[space_idx + 1:] if space_idx != -1 else before
    if after_end < len(text) and after and not after[-1].isspace():
        space_idx = after.rfind(" ")
        after = after[:space_idx] if space_idx != -1 else after

    return before.strip(), matched, after.strip()


@dataclass
class TermRecord:
    id: str
    term_en: str
    branch: str
    variants_en: list[str]
    variants_fr: list[str]
    pattern_en: re.Pattern = field(default=None, repr=False)
    pattern_fr: re.Pattern = field(default=None, repr=False)

    def __post_init__(self):
        self.pattern_en = build_term_patterns(self.variants_en)
        self.pattern_fr = build_term_patterns(self.variants_fr)


# ── Main extraction ────────────────────────────────────────────────────────────

def load_terms(conn) -> list[TermRecord]:
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT id, term_en, branch, variants_en, variants_fr FROM ethical_term_lexicon ORDER BY branch, id;")
        rows = cur.fetchall()
    terms = [TermRecord(
        id=r["id"], term_en=r["term_en"], branch=r["branch"],
        variants_en=r["variants_en"], variants_fr=r["variants_fr"]
    ) for r in rows]
    print(f"  Loaded {len(terms)} terms from ethical_term_lexicon")
    return terms


def load_corpus(conn) -> list[dict]:
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT submission_id, organization, submission_language, field, text_en, text_fr
            FROM corpus_text_fields
            WHERE text_en IS NOT NULL OR text_fr IS NOT NULL;
        """)
        rows = [dict(r) for r in cur.fetchall()]
    print(f"  Loaded {len(rows)} text-field rows from corpus_text_fields")
    return rows


def search_text(text: str, pattern: re.Pattern, match_lang: str,
                term: TermRecord, row: dict) -> list[dict]:
    """Find all matches of a term pattern in a text, return occurrence dicts."""
    if not text:
        return []

    occurrences = []
    for m in pattern.finditer(text):
        before, matched, after = extract_kwic(text, m.start(), m.end())
        sentence = extract_sentence(text, m.start(), m.end())

        occurrences.append({
            "term_id":             term.id,
            "term_en":             term.term_en,
            "branch":              term.branch,
            "submission_id":       row["submission_id"],
            "organization":        row["organization"],
            "submission_language": row["submission_language"],
            "field":               row["field"],
            "match_language":      match_lang,
            "matched_variant":     matched,
            "context_before":      before,
            "matched_text":        matched,
            "context_after":       after,
            "sentence":            sentence,
            "char_offset":         m.start(),
        })
    return occurrences


INSERT_OCCURRENCE = """
INSERT INTO ethical_term_occurrences (
    term_id, term_en, branch, submission_id, organization,
    submission_language, field, match_language,
    matched_variant, context_before, matched_text, context_after,
    sentence, char_offset
) VALUES (
    %(term_id)s, %(term_en)s, %(branch)s, %(submission_id)s, %(organization)s,
    %(submission_language)s, %(field)s, %(match_language)s,
    %(matched_variant)s, %(context_before)s, %(matched_text)s, %(context_after)s,
    %(sentence)s, %(char_offset)s
);
"""

BUILD_FREQUENCY = """
INSERT INTO ethical_term_frequency (
    term_id, term_en, branch, match_language, organization, field,
    occurrence_count, submission_count
)
SELECT
    term_id, term_en, branch, match_language, organization, field,
    COUNT(*)                    AS occurrence_count,
    COUNT(DISTINCT submission_id) AS submission_count
FROM ethical_term_occurrences
GROUP BY term_id, term_en, branch, match_language, organization, field
ON CONFLICT (term_id, match_language, organization, field)
DO UPDATE SET
    occurrence_count = EXCLUDED.occurrence_count,
    submission_count = EXCLUDED.submission_count;
"""


def run_extraction(conn, terms: list[TermRecord], corpus: list[dict]):
    total_matches = 0
    with conn.cursor() as cur:
        for row in corpus:
            for term in terms:
                # Search EN text
                if row["text_en"]:
                    hits = search_text(row["text_en"], term.pattern_en, "en", term, row)
                    for hit in hits:
                        cur.execute(INSERT_OCCURRENCE, hit)
                    total_matches += len(hits)

                # Search FR text
                if row["text_fr"]:
                    hits = search_text(row["text_fr"], term.pattern_fr, "fr", term, row)
                    for hit in hits:
                        cur.execute(INSERT_OCCURRENCE, hit)
                    total_matches += len(hits)

        conn.commit()
    print(f"  Inserted {total_matches} occurrence rows")
    return total_matches


def build_frequency_table(conn):
    with conn.cursor() as cur:
        cur.execute(BUILD_FREQUENCY)
        conn.commit()
    print("  Frequency table built")


# ── Reporting ──────────────────────────────────────────────────────────────────

def print_summary(conn):
    with conn.cursor() as cur:
        # Top-level counts
        cur.execute("""
            SELECT match_language, COUNT(*) AS total_occurrences,
                   COUNT(DISTINCT term_id) AS distinct_terms,
                   COUNT(DISTINCT submission_id) AS submissions_with_hits
            FROM ethical_term_occurrences
            GROUP BY match_language ORDER BY match_language;
        """)
        print("\n━━━ Corpus totals ━━━")
        for lang, occ, terms, subs in cur.fetchall():
            print(f"  [{lang.upper()}]  {occ:>5} occurrences  |  {terms:>2} distinct terms hit  |  {subs:>3} submissions")

        # Per-branch breakdown
        cur.execute("""
            SELECT branch, match_language,
                   COUNT(*) AS occurrences,
                   COUNT(DISTINCT term_id) AS distinct_terms
            FROM ethical_term_occurrences
            GROUP BY branch, match_language
            ORDER BY branch, match_language;
        """)
        print("\n━━━ By branch × language ━━━")
        for branch, lang, occ, terms in cur.fetchall():
            print(f"  {branch:<20} [{lang}]  {occ:>5} occurrences  |  {terms:>2} terms hit")

        # Top 15 terms by total occurrences
        cur.execute("""
            SELECT term_en, branch,
                   SUM(occurrence_count) FILTER (WHERE match_language = 'en') AS en_count,
                   SUM(occurrence_count) FILTER (WHERE match_language = 'fr') AS fr_count,
                   SUM(occurrence_count) AS total
            FROM ethical_term_frequency
            GROUP BY term_en, branch
            ORDER BY total DESC
            LIMIT 20;
        """)
        print("\n━━━ Top 20 terms by total occurrences ━━━")
        print(f"  {'Term':<25} {'Branch':<20} {'EN':>5} {'FR':>5} {'TOTAL':>7}")
        print(f"  {'-'*25} {'-'*20} {'-'*5} {'-'*5} {'-'*7}")
        for term_en, branch, en_c, fr_c, total in cur.fetchall():
            print(f"  {term_en:<25} {branch:<20} {(en_c or 0):>5} {(fr_c or 0):>5} {total:>7}")

        # Terms with ZERO occurrences in the corpus
        cur.execute("""
            SELECT l.id, l.term_en, l.branch
            FROM ethical_term_lexicon l
            LEFT JOIN ethical_term_occurrences o ON o.term_id = l.id
            WHERE o.id IS NULL
            ORDER BY l.branch, l.id;
        """)
        absent = cur.fetchall()
        if absent:
            print(f"\n━━━ Terms with NO corpus matches ({len(absent)}) ━━━")
            for tid, term_en, branch in absent:
                print(f"  {tid}  {term_en:<25}  [{branch}]")

        # EN/FR asymmetry: terms appearing much more in one language
        cur.execute("""
            SELECT term_en, branch,
                   COALESCE(SUM(occurrence_count) FILTER (WHERE match_language = 'en'), 0) AS en_count,
                   COALESCE(SUM(occurrence_count) FILTER (WHERE match_language = 'fr'), 0) AS fr_count
            FROM ethical_term_frequency
            GROUP BY term_en, branch
            HAVING COALESCE(SUM(occurrence_count) FILTER (WHERE match_language = 'en'), 0) > 0
               AND COALESCE(SUM(occurrence_count) FILTER (WHERE match_language = 'fr'), 0) = 0
            ORDER BY en_count DESC;
        """)
        en_only = cur.fetchall()
        if en_only:
            print(f"\n━━━ Terms appearing ONLY in EN text (EN present, FR=0) ━━━")
            for term_en, branch, en_c, fr_c in en_only:
                print(f"  {term_en:<25} [{branch}]  EN={en_c}")

        cur.execute("""
            SELECT term_en, branch,
                   COALESCE(SUM(occurrence_count) FILTER (WHERE match_language = 'en'), 0) AS en_count,
                   COALESCE(SUM(occurrence_count) FILTER (WHERE match_language = 'fr'), 0) AS fr_count
            FROM ethical_term_frequency
            GROUP BY term_en, branch
            HAVING COALESCE(SUM(occurrence_count) FILTER (WHERE match_language = 'en'), 0) = 0
               AND COALESCE(SUM(occurrence_count) FILTER (WHERE match_language = 'fr'), 0) > 0
            ORDER BY fr_count DESC;
        """)
        fr_only = cur.fetchall()
        if fr_only:
            print(f"\n━━━ Terms appearing ONLY in FR text (FR present, EN=0) ━━━")
            for term_en, branch, en_c, fr_c in fr_only:
                print(f"  {term_en:<25} [{branch}]  FR={fr_c}")

        # Organization breakdown for top 5 terms
        cur.execute("""
            SELECT term_en, organization, match_language,
                   SUM(occurrence_count) AS count
            FROM ethical_term_frequency
            WHERE term_en IN (
                SELECT term_en FROM ethical_term_frequency
                GROUP BY term_en ORDER BY SUM(occurrence_count) DESC LIMIT 5
            )
            GROUP BY term_en, organization, match_language
            ORDER BY term_en, count DESC;
        """)
        print("\n━━━ Organization breakdown for top 5 terms ━━━")
        cur_term = None
        for term_en, org, lang, count in cur.fetchall():
            if term_en != cur_term:
                print(f"\n  [{term_en}]")
                cur_term = term_en
            org_short = org[:35] if org else "—"
            print(f"    {lang}  {org_short:<36} {count:>4}")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    print(f"Phase 2: Ethical Term Corpus Extraction")
    print(f"Database: {DB_NAME}\n")

    conn = psycopg2.connect(dbname=DB_NAME)
    try:
        with conn.cursor() as cur:
            print("Setting up schema...")
            cur.execute(DROP_TABLES)
            cur.execute(CREATE_VIEW)
            cur.execute(CREATE_OCCURRENCES)
            cur.execute(CREATE_FREQUENCY)
            conn.commit()
            print("  Schema ready")

        terms  = load_terms(conn)
        corpus = load_corpus(conn)

        print(f"\nRunning extraction ({len(terms)} terms × {len(corpus)} text rows)...")
        run_extraction(conn, terms, corpus)

        print("\nBuilding frequency summary table...")
        build_frequency_table(conn)

        print_summary(conn)

    finally:
        conn.close()

    print("\nPhase 2 complete.")
    print("  Tables: ethical_term_occurrences, ethical_term_frequency")
    print("  View:   corpus_text_fields")


if __name__ == "__main__":
    main()
