#!/usr/bin/env python3
"""
Phase 1: Build Ethical Term Lexicon in PostgreSQL.
Reads ethical_term_lexicon.json and populates the ethical_term_lexicon table.
"""

import json
import psycopg2
from pathlib import Path

LEXICON_FILE = Path(__file__).parent / "ethical_term_lexicon.json"
DB_NAME = "aia_corpus"

CREATE_TABLE_SQL = """
DROP TABLE IF EXISTS ethical_term_lexicon CASCADE;

CREATE TABLE ethical_term_lexicon (
    id                      TEXT PRIMARY KEY,
    term_en                 TEXT NOT NULL,
    term_fr                 TEXT[] NOT NULL,
    branch                  TEXT NOT NULL CHECK (branch IN ('metaethics', 'normative_ethics', 'applied_ethics')),
    tradition               TEXT[] NOT NULL,
    key_philosophers        TEXT[] NOT NULL,
    canonical_definition_en TEXT NOT NULL,
    canonical_definition_fr TEXT NOT NULL,
    aia_relevance           TEXT,
    expected_drift          TEXT,
    variants_en             TEXT[] NOT NULL,
    variants_fr             TEXT[] NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE ethical_term_lexicon IS
  'Phase 1 catalogue: master lexicon of ethical terms across metaethics, normative ethics, and applied ethics. Each row represents one term with its philosophical grounding and expected corpus behaviour.';

COMMENT ON COLUMN ethical_term_lexicon.expected_drift IS
  'Predicted divergence between philosophical origin and corpus usage, or between EN and FR versions. One of: hollowed, reframed, instrumentalized, narrowed, bifurcated, absent, faithful, cross-linguistic shift.';
"""

INSERT_SQL = """
INSERT INTO ethical_term_lexicon (
    id, term_en, term_fr, branch, tradition, key_philosophers,
    canonical_definition_en, canonical_definition_fr,
    aia_relevance, expected_drift, variants_en, variants_fr
) VALUES (
    %(id)s, %(term_en)s, %(term_fr)s, %(branch)s, %(tradition)s, %(key_philosophers)s,
    %(canonical_definition_en)s, %(canonical_definition_fr)s,
    %(aia_relevance)s, %(expected_drift)s, %(variants_en)s, %(variants_fr)s
);
"""


def load_lexicon():
    with open(LEXICON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded lexicon: {data['metadata']['total_terms']} terms, version {data['metadata']['version']}")
    return data["terms"]


def build_table(conn, terms):
    with conn.cursor() as cur:
        print("Creating ethical_term_lexicon table...")
        cur.execute(CREATE_TABLE_SQL)

        print(f"Inserting {len(terms)} terms...")
        for term in terms:
            cur.execute(INSERT_SQL, {
                "id":                      term["id"],
                "term_en":                 term["term_en"],
                "term_fr":                 term["term_fr"],
                "branch":                  term["branch"],
                "tradition":               term["tradition"],
                "key_philosophers":        term["key_philosophers"],
                "canonical_definition_en": term["canonical_definition_en"],
                "canonical_definition_fr": term["canonical_definition_fr"],
                "aia_relevance":           term.get("aia_relevance"),
                "expected_drift":          term.get("expected_drift"),
                "variants_en":             term["variants_en"],
                "variants_fr":             term["variants_fr"],
            })

        conn.commit()
        print("Done.")


def verify(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT branch, COUNT(*) FROM ethical_term_lexicon GROUP BY branch ORDER BY branch;")
        rows = cur.fetchall()
        print("\n--- Lexicon summary by branch ---")
        total = 0
        for branch, count in rows:
            print(f"  {branch:<20} {count:>3} terms")
            total += count
        print(f"  {'TOTAL':<20} {total:>3} terms")

        cur.execute("""
            SELECT id, term_en, branch, expected_drift
            FROM ethical_term_lexicon
            ORDER BY branch, id;
        """)
        rows = cur.fetchall()
        print("\n--- Full term list ---")
        current_branch = None
        for tid, term_en, branch, drift in rows:
            if branch != current_branch:
                print(f"\n  [{branch.upper()}]")
                current_branch = branch
            drift_short = (drift or "").split(":")[0][:40]
            print(f"    {tid}  {term_en:<25}  drift: {drift_short}")


def main():
    print(f"Connecting to database: {DB_NAME}")
    conn = psycopg2.connect(dbname=DB_NAME)
    try:
        terms = load_lexicon()
        build_table(conn, terms)
        verify(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
