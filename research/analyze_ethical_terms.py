#!/usr/bin/env python3
"""
Phase 3 + 4: Philosophical Origin vs Corpus Usage Analysis
          + Cross-Linguistic Conceptual Divergence Analysis

For each term in ethical_term_lexicon (that has corpus occurrences):
  - Collects sampled EN and FR sentences from ethical_term_occurrences
  - Sends one structured LLM call (Llama-3.3-70B via IONOS)
  - Produces:
      Phase 3a: How EN submissions use the term vs its philosophical origin
      Phase 3b: How FR submissions use the term vs its philosophical origin
      Phase 4:  How EN and FR conceptualize the term differently from each other

Results are stored in ethical_term_analysis.
"""

import json
import os
import random
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
from openai import OpenAI

load_dotenv()

DB_NAME        = "aia_corpus"
MODEL          = os.getenv("IONOS_RAG_MODEL_ID", "meta-llama/Llama-3.3-70B-Instruct")
LLM_API_KEY    = os.getenv("IONOS_RAG_API_KEY", os.getenv("OPENAI_API_KEY", ""))
PROMPT_VERSION = "v1.0"
MAX_SENTENCES  = 18   # max sentences per language per term sent to the model
MAX_RETRIES    = 3
RETRY_DELAY    = 5    # seconds between retries

# IONOS endpoint: strip /chat/completions so the SDK can append it
_raw_endpoint = os.getenv("IONOS_RAG_CHAT_ENDPOINT",
                           "https://openai.inference.de-txl.ionos.com/v1/chat/completions")
if _raw_endpoint.endswith("/chat/completions"):
    LLM_BASE_URL = _raw_endpoint.rsplit("/chat/completions", 1)[0]
else:
    LLM_BASE_URL = _raw_endpoint

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

# ── Schema ─────────────────────────────────────────────────────────────────────

DROP_TABLE = "DROP TABLE IF EXISTS ethical_term_analysis CASCADE;"

CREATE_TABLE = """
CREATE TABLE ethical_term_analysis (
    id                              SERIAL PRIMARY KEY,
    term_id                         TEXT NOT NULL REFERENCES ethical_term_lexicon(id),
    term_en                         TEXT NOT NULL,
    branch                          TEXT NOT NULL,

    -- Phase 3: philosophical context
    philosophical_origin_summary    TEXT,

    -- Phase 3a: EN corpus analysis
    en_corpus_sentence_count        INTEGER,
    en_usage_summary                TEXT,
    en_drift_type                   TEXT,
    en_drift_description            TEXT,
    en_representative_examples      JSONB,
    en_notable_observations         TEXT,

    -- Phase 3b: FR corpus analysis
    fr_corpus_sentence_count        INTEGER,
    fr_usage_summary                TEXT,
    fr_drift_type                   TEXT,
    fr_drift_description            TEXT,
    fr_representative_examples      JSONB,
    fr_notable_observations         TEXT,

    -- Phase 4: EN/FR cross-linguistic divergence
    en_fr_divergence_type           TEXT,
    en_fr_divergence_description    TEXT,
    en_fr_key_contrast              TEXT,
    en_fr_philosophical_significance TEXT,

    -- Catalogue synthesis
    key_finding                     TEXT,

    -- Metadata
    model_id                        TEXT NOT NULL,
    prompt_version                  TEXT NOT NULL,
    raw_llm_response                JSONB NOT NULL,
    created_at                      TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (term_id, prompt_version)
);

COMMENT ON TABLE ethical_term_analysis IS
  'Phase 3+4: LLM analysis of each ethical term — philosophical origin vs corpus usage (EN+FR) and cross-linguistic divergence.';
"""

INSERT_SQL = """
INSERT INTO ethical_term_analysis (
    term_id, term_en, branch,
    philosophical_origin_summary,
    en_corpus_sentence_count, en_usage_summary, en_drift_type,
    en_drift_description, en_representative_examples, en_notable_observations,
    fr_corpus_sentence_count, fr_usage_summary, fr_drift_type,
    fr_drift_description, fr_representative_examples, fr_notable_observations,
    en_fr_divergence_type, en_fr_divergence_description,
    en_fr_key_contrast, en_fr_philosophical_significance,
    key_finding, model_id, prompt_version, raw_llm_response
) VALUES (
    %(term_id)s, %(term_en)s, %(branch)s,
    %(philosophical_origin_summary)s,
    %(en_corpus_sentence_count)s, %(en_usage_summary)s, %(en_drift_type)s,
    %(en_drift_description)s, %(en_representative_examples)s, %(en_notable_observations)s,
    %(fr_corpus_sentence_count)s, %(fr_usage_summary)s, %(fr_drift_type)s,
    %(fr_drift_description)s, %(fr_representative_examples)s, %(fr_notable_observations)s,
    %(en_fr_divergence_type)s, %(en_fr_divergence_description)s,
    %(en_fr_key_contrast)s, %(en_fr_philosophical_significance)s,
    %(key_finding)s, %(model_id)s, %(prompt_version)s, %(raw_llm_response)s
)
ON CONFLICT (term_id, prompt_version) DO UPDATE SET
    philosophical_origin_summary    = EXCLUDED.philosophical_origin_summary,
    en_corpus_sentence_count        = EXCLUDED.en_corpus_sentence_count,
    en_usage_summary                = EXCLUDED.en_usage_summary,
    en_drift_type                   = EXCLUDED.en_drift_type,
    en_drift_description            = EXCLUDED.en_drift_description,
    en_representative_examples      = EXCLUDED.en_representative_examples,
    en_notable_observations         = EXCLUDED.en_notable_observations,
    fr_corpus_sentence_count        = EXCLUDED.fr_corpus_sentence_count,
    fr_usage_summary                = EXCLUDED.fr_usage_summary,
    fr_drift_type                   = EXCLUDED.fr_drift_type,
    fr_drift_description            = EXCLUDED.fr_drift_description,
    fr_representative_examples      = EXCLUDED.fr_representative_examples,
    fr_notable_observations         = EXCLUDED.fr_notable_observations,
    en_fr_divergence_type           = EXCLUDED.en_fr_divergence_type,
    en_fr_divergence_description    = EXCLUDED.en_fr_divergence_description,
    en_fr_key_contrast              = EXCLUDED.en_fr_key_contrast,
    en_fr_philosophical_significance = EXCLUDED.en_fr_philosophical_significance,
    key_finding                     = EXCLUDED.key_finding,
    model_id                        = EXCLUDED.model_id,
    prompt_version                  = EXCLUDED.prompt_version,
    raw_llm_response                = EXCLUDED.raw_llm_response,
    created_at                      = now();
"""

# ── Prompt ─────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a philosopher of ethics and a computational humanities researcher analyzing the Canadian Algorithmic Impact Assessment (AIA) corpus — a bilingual (English/French) collection of government submissions describing automated decision-making systems. Each AIA submission was filed by a federal department and describes how an algorithmic system is used, what risks it poses, and what safeguards are in place.

Your task is to analyze how ethical terms from philosophy (metaethics, normative ethics, applied ethics) appear in this corpus — and in what ways their use diverges from their philosophical origins.

You will receive:
1. A term's philosophical definition and tradition
2. A sample of English corpus sentences where the term appears
3. A sample of French corpus sentences where equivalent terms appear

You must return a single valid JSON object with this exact structure:
{
  "philosophical_origin_summary": "2-3 sentences: the term's philosophical meaning, which tradition it comes from, who the key thinkers are, and what moral work the concept does in its original philosophical context",
  "en_analysis": {
    "usage_summary": "2-3 sentences: how English AIA submissions actually use this term — what they mean by it, in what contexts, for what rhetorical or institutional purposes",
    "drift_type": "<one of: instrumentalized | hollowed | reframed | narrowed | bifurcated | legalized | faithful | expanded | unnamed | absent>",
    "drift_description": "2-3 sentences: specifically how and why the corpus usage diverges from (or aligns with) the philosophical origin — be precise about what is lost, added, or transformed",
    "representative_examples": ["exact sentence from corpus", "exact sentence from corpus"],
    "notable_observations": "1-2 sentences: any surprising, ironic, or especially revealing patterns in EN usage"
  },
  "fr_analysis": {
    "usage_summary": "2-3 sentences: how French AIA submissions use the term or its French equivalents",
    "drift_type": "<same taxonomy as above>",
    "drift_description": "2-3 sentences: how FR corpus usage diverges from or aligns with the philosophical origin",
    "representative_examples": ["exact sentence from corpus"],
    "notable_observations": "1-2 sentences: any surprising patterns in FR usage"
  },
  "en_fr_divergence": {
    "divergence_type": "<one of: terminological | conceptual_shift | omission | addition | register | faithful | asymmetric_emphasis>",
    "divergence_description": "2-3 sentences: how the English and French submissions conceptualize this term differently from each other — differences in what word is chosen, what meaning is carried, and what is foregrounded or erased",
    "key_contrast": "One precise sentence contrasting EN vs FR treatment (e.g. 'EN frames X as..., while FR frames it as...')",
    "philosophical_significance": "1-2 sentences: what this EN/FR divergence reveals about different governance philosophies, legal traditions, or political cultures at work in Canadian bilingual AI governance"
  },
  "key_finding": "One sentence — the single most important finding about this term for a catalogue of ethical terminologies in Canadian AI governance"
}

Drift type definitions:
- instrumentalized: term used as a metric, score, or checkbox rather than a moral concept
- hollowed: term is present but the concept it carries (who is accountable to whom, etc.) is evacuated
- reframed: term repurposed to serve institutional efficiency or compliance rather than ethics
- narrowed: term restricted to a subset of its philosophical meaning (e.g. only procedural fairness, not substantive)
- bifurcated: term used in two incompatible senses simultaneously (e.g. autonomy as both system-autonomy and human self-governance)
- legalized: term's meaning collapsed into its legal definition, losing philosophical depth
- faithful: term used in approximate alignment with its philosophical meaning
- expanded: term carries more meaning than in its philosophical origin
- unnamed: the concept is operationalized without being named (e.g. non-maleficence as risk mitigation)
- absent: term variants appear but in a completely unrelated sense (false positive matches)

Divergence type definitions:
- terminological: different word, essentially same concept across EN/FR
- conceptual_shift: different word, meaningfully different concept (the most interesting case)
- omission: concept articulated in one language but largely absent from the other
- addition: one language introduces an ethical concept the other omits
- register: same concept but one language uses bureaucratic register, the other moral/philosophical
- faithful: EN and FR treat the term similarly
- asymmetric_emphasis: both languages use the term, but one language foregrounds it much more heavily

Be direct, analytically precise, and grounded in the actual sentences. Do not generalize beyond what the evidence supports. If a language has very few sentences, note that and be appropriately hedged."""


def build_user_prompt(term: dict, en_sentences: list[str], fr_sentences: list[str]) -> str:
    tradition_str = ", ".join(term["tradition"])
    philosophers_str = "; ".join(term["key_philosophers"])
    term_fr_str = " / ".join(term["term_fr"])
    variants_en_str = ", ".join(term["variants_en"])
    variants_fr_str = ", ".join(term["variants_fr"])

    en_block = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(en_sentences)) if en_sentences else "  [No English corpus sentences found for this term]"
    fr_block = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(fr_sentences)) if fr_sentences else "  [No French corpus sentences found for this term]"

    return f"""TERM TO ANALYZE: "{term['term_en']}" (FR equivalents: {term_fr_str})

BRANCH: {term['branch'].replace('_', ' ').title()}
TRADITION(S): {tradition_str}
KEY PHILOSOPHERS: {philosophers_str}

CANONICAL PHILOSOPHICAL DEFINITION (EN):
{term['canonical_definition_en']}

CANONICAL PHILOSOPHICAL DEFINITION (FR):
{term['canonical_definition_fr']}

EN SEARCH VARIANTS: {variants_en_str}
FR SEARCH VARIANTS: {variants_fr_str}

AIA RELEVANCE NOTE:
{term.get('aia_relevance', 'N/A')}

PREDICTED DRIFT (from lexicon — for your reference only, do not be bound by it):
{term.get('expected_drift', 'N/A')}

─────────────────────────────────────
ENGLISH CORPUS SENTENCES ({len(en_sentences)} sentences):
{en_block}

─────────────────────────────────────
FRENCH CORPUS SENTENCES ({len(fr_sentences)} sentences):
{fr_block}

─────────────────────────────────────
Now produce the JSON analysis as specified in the system prompt."""


# ── Data loading ───────────────────────────────────────────────────────────────

def load_terms(conn) -> list[dict]:
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT id, term_en, term_fr, branch, tradition, key_philosophers,
                   canonical_definition_en, canonical_definition_fr,
                   aia_relevance, expected_drift, variants_en, variants_fr
            FROM ethical_term_lexicon
            ORDER BY branch, id;
        """)
        return [dict(r) for r in cur.fetchall()]


def load_sentences(conn, term_id: str, lang: str, max_n: int) -> list[str]:
    """
    Load up to max_n sentences for a term in a given language.
    Samples for diversity: up to 3 per organization, prioritizing different fields.
    Deduplicates identical sentences.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT ON (sentence)
                sentence, organization, field
            FROM ethical_term_occurrences
            WHERE term_id = %s
              AND match_language = %s
              AND sentence IS NOT NULL
              AND LENGTH(sentence) > 15
            ORDER BY sentence, organization, field;
        """, (term_id, lang))
        rows = cur.fetchall()

    if not rows:
        return []

    # Group by organization and sample for diversity
    from collections import defaultdict
    by_org: dict[str, list] = defaultdict(list)
    for sentence, org, field in rows:
        by_org[org].append((sentence, field))

    sampled = []
    per_org = max(3, max_n // max(len(by_org), 1))

    for org, items in by_org.items():
        seen_fields: set[str] = set()
        org_count = 0
        for sentence, field in items:
            if len(sampled) >= max_n or org_count >= per_org:
                break
            if field not in seen_fields or len(items) <= 2:
                sampled.append(sentence.strip())
                seen_fields.add(field)
                org_count += 1

    # Fill up to max_n with any remaining unique sentences
    all_sentences = [r[0].strip() for r in rows]
    for sentence in all_sentences:
        if sentence not in sampled and len(sampled) < max_n:
            sampled.append(sentence)

    return sampled[:max_n]


# ── LLM call ───────────────────────────────────────────────────────────────────

def call_llm(user_prompt: str) -> dict:
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_prompt},
                ],
                temperature=0.15,
                max_tokens=2048,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"    JSON parse error (attempt {attempt+1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"    API error (attempt {attempt+1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                raise
    raise RuntimeError(f"LLM call failed after {MAX_RETRIES} attempts")


# ── Parsing LLM response ───────────────────────────────────────────────────────

def safe_get(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d


def parse_response(raw: dict, term: dict,
                   en_count: int, fr_count: int) -> dict:
    en = raw.get("en_analysis", {})
    fr = raw.get("fr_analysis", {})
    div = raw.get("en_fr_divergence", {})

    return {
        "term_id":   term["id"],
        "term_en":   term["term_en"],
        "branch":    term["branch"],

        "philosophical_origin_summary": raw.get("philosophical_origin_summary"),

        "en_corpus_sentence_count":    en_count,
        "en_usage_summary":            en.get("usage_summary"),
        "en_drift_type":               en.get("drift_type"),
        "en_drift_description":        en.get("drift_description"),
        "en_representative_examples":  json.dumps(en.get("representative_examples", [])),
        "en_notable_observations":     en.get("notable_observations"),

        "fr_corpus_sentence_count":    fr_count,
        "fr_usage_summary":            fr.get("usage_summary"),
        "fr_drift_type":               fr.get("drift_type"),
        "fr_drift_description":        fr.get("drift_description"),
        "fr_representative_examples":  json.dumps(fr.get("representative_examples", [])),
        "fr_notable_observations":     fr.get("notable_observations"),

        "en_fr_divergence_type":              div.get("divergence_type"),
        "en_fr_divergence_description":       div.get("divergence_description"),
        "en_fr_key_contrast":                 div.get("key_contrast"),
        "en_fr_philosophical_significance":   div.get("philosophical_significance"),

        "key_finding":    raw.get("key_finding"),
        "model_id":       MODEL,
        "prompt_version": PROMPT_VERSION,
        "raw_llm_response": json.dumps(raw),
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("Phase 3 + 4: Ethical Term Analysis")
    print(f"Model: {MODEL}")
    print(f"Database: {DB_NAME}\n")

    conn = psycopg2.connect(dbname=DB_NAME)
    try:
        # Set up table
        with conn.cursor() as cur:
            cur.execute(DROP_TABLE)
            cur.execute(CREATE_TABLE)
            conn.commit()
        print("Table ethical_term_analysis created.\n")

        terms = load_terms(conn)
        print(f"Processing {len(terms)} terms...\n")

        success = 0
        skipped = 0

        for i, term in enumerate(terms, 1):
            tid = term["id"]
            tname = term["term_en"]

            en_sentences = load_sentences(conn, tid, "en", MAX_SENTENCES)
            fr_sentences = load_sentences(conn, tid, "fr", MAX_SENTENCES)

            total = len(en_sentences) + len(fr_sentences)
            print(f"[{i:02d}/{len(terms)}] {tid}  {tname:<25}  EN={len(en_sentences):>3}  FR={len(fr_sentences):>3}", end="  ")

            if total == 0:
                # No corpus sentences — still record a philosophical entry with the absence noted
                raw_stub = {
                    "philosophical_origin_summary": term["canonical_definition_en"][:400],
                    "en_analysis": {
                        "usage_summary": "No corpus sentences found.",
                        "drift_type": "absent",
                        "drift_description": "This term did not appear in the corpus — itself a significant finding confirming the predicted absence.",
                        "representative_examples": [],
                        "notable_observations": "Absence from corpus is analytically significant."
                    },
                    "fr_analysis": {
                        "usage_summary": "No corpus sentences found.",
                        "drift_type": "absent",
                        "drift_description": "This term did not appear in the French corpus.",
                        "representative_examples": [],
                        "notable_observations": "Absence from corpus is analytically significant."
                    },
                    "en_fr_divergence": {
                        "divergence_type": "faithful",
                        "divergence_description": "Both languages equally omit this concept.",
                        "key_contrast": "Neither EN nor FR submissions engage with this term.",
                        "philosophical_significance": "The shared absence reflects a mutual gap in philosophical grounding across both language communities."
                    },
                    "key_finding": f"'{tname}' is entirely absent from the AIA corpus in both languages, confirming that this philosophical concept has no purchase in bureaucratic AI governance discourse."
                }
                row = parse_response(raw_stub, term, 0, 0)
                with conn.cursor() as cur:
                    cur.execute(INSERT_SQL, row)
                    conn.commit()
                print("→ absent (no corpus data, stub recorded)")
                skipped += 1
                continue

            user_prompt = build_user_prompt(term, en_sentences, fr_sentences)

            try:
                raw = call_llm(user_prompt)
                row = parse_response(raw, term, len(en_sentences), len(fr_sentences))
                with conn.cursor() as cur:
                    cur.execute(INSERT_SQL, row)
                    conn.commit()
                drift_en = (row.get("en_drift_type") or "?")[:15]
                drift_fr = (row.get("fr_drift_type") or "?")[:15]
                div_type = (row.get("en_fr_divergence_type") or "?")[:20]
                print(f"→ EN:{drift_en:<15} FR:{drift_fr:<15} DIV:{div_type}")
                success += 1
            except Exception as e:
                print(f"→ ERROR: {e}")
                conn.rollback()

        print(f"\n{'━'*60}")
        print(f"Done. {success} terms analyzed, {skipped} absent stubs recorded.")
        print_final_summary(conn)

    finally:
        conn.close()


def print_final_summary(conn):
    with conn.cursor() as cur:
        print("\n━━━ Drift types across all terms ━━━")
        cur.execute("""
            SELECT en_drift_type, COUNT(*) AS n
            FROM ethical_term_analysis
            WHERE en_drift_type IS NOT NULL
            GROUP BY en_drift_type ORDER BY n DESC;
        """)
        print("  EN drift types:")
        for dtype, n in cur.fetchall():
            print(f"    {dtype:<20} {n:>3}")

        cur.execute("""
            SELECT fr_drift_type, COUNT(*) AS n
            FROM ethical_term_analysis
            WHERE fr_drift_type IS NOT NULL
            GROUP BY fr_drift_type ORDER BY n DESC;
        """)
        print("  FR drift types:")
        for dtype, n in cur.fetchall():
            print(f"    {dtype:<20} {n:>3}")

        print("\n━━━ EN/FR divergence types ━━━")
        cur.execute("""
            SELECT en_fr_divergence_type, COUNT(*) AS n
            FROM ethical_term_analysis
            WHERE en_fr_divergence_type IS NOT NULL
            GROUP BY en_fr_divergence_type ORDER BY n DESC;
        """)
        for dtype, n in cur.fetchall():
            print(f"  {dtype:<25} {n:>3}")

        print("\n━━━ Key findings per term ━━━")
        cur.execute("""
            SELECT term_en, branch, en_drift_type, fr_drift_type,
                   en_fr_divergence_type, key_finding
            FROM ethical_term_analysis
            ORDER BY branch, term_id;
        """)
        cur_branch = None
        for term_en, branch, en_d, fr_d, div, finding in cur.fetchall():
            if branch != cur_branch:
                print(f"\n  [{branch.upper().replace('_',' ')}]")
                cur_branch = branch
            print(f"  {term_en:<22} EN:{(en_d or '?'):<14} FR:{(fr_d or '?'):<14} DIV:{div or '?'}")
            if finding:
                print(f"    → {finding[:110]}")


if __name__ == "__main__":
    main()
