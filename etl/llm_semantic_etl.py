#!/usr/bin/env python3
"""
LLM Semantic Interpretation ETL

Reads respondent answers from the aia_corpus section tables, sends structured
prompts to an LLM (IONOS Llama 3.3 70B), and writes derived interpretation
rows back into PostgreSQL.

Usage:
    python3 etl/llm_semantic_etl.py --analysis all
    python3 etl/llm_semantic_etl.py --analysis justification --limit 3 --dry-run
    python3 etl/llm_semantic_etl.py --analysis themes
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DB_DSN = os.getenv("DATABASE_URL", "dbname=aia_corpus")

# IONOS OpenAI-compatible endpoint
LLM_BASE_URL = os.getenv("IONOS_RAG_CHAT_ENDPOINT",
                          "https://openai.inference.de-txl.ionos.com/v1/chat/completions")
# The openai library appends /chat/completions, so strip it from base_url
if LLM_BASE_URL.endswith("/chat/completions"):
    LLM_BASE_URL = LLM_BASE_URL.rsplit("/chat/completions", 1)[0]

LLM_API_KEY = os.getenv("IONOS_RAG_API_KEY", os.getenv("OPENAI_API_KEY", ""))
MODEL = os.getenv("IONOS_RAG_MODEL_ID", "meta-llama/Llama-3.3-70B-Instruct")
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
RATE_LIMIT_DELAY = float(os.getenv("LLM_RATE_LIMIT_SECONDS", "1.5"))
TEXT_TRUNCATE = 500  # max chars per text field in prompt

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

SYSTEM_MSG = (
    "You are a public policy analyst specializing in Canadian federal "
    "algorithmic governance under the Directive on Automated Decision-Making. "
    "Respond with valid JSON only — no markdown fences, no commentary."
)

# ---------------------------------------------------------------------------
# Prompt templates  (bump version when changing prompts)
# ---------------------------------------------------------------------------

PROMPT_V = {
    "justification": "1.0.0",
    "risk":          "1.0.0",
    "divergence":    "1.0.0",
    "safeguard":     "1.0.0",
    "themes":        "1.0.0",
}

PROMPT_JUSTIFICATION = """\
Analyze this Canadian Algorithmic Impact Assessment submission for its \
automation justification.

## Project Context
- Department: {department}
- Project Title (EN): {project_title_en}
- Project Title (FR): {project_title_fr}
- Phase: {phase}
- Description (EN): {description_en}

## Automation Rationale
- Client Needs (EN): {client_needs_en}
- Public Benefits (EN): {public_benefits_en}
- Expected Improvements (EN): {expected_improvements_en}
- Trade-offs (EN): {trade_offs_en}
- Why Automation Preferred (EN): {why_automation_preferred_en}
- System Confinement (EN): {system_confinement_en}

## Decision Context
- Automation Type Score: {automation_type_score} (0=support, 2=partial, 4=full)
- System Role (EN): {system_role_en}
- Evaluation Criteria (EN): {evaluation_criteria_en}

Produce a JSON object with these exact keys:
{{
  "justification_theme": "<primary theme: efficiency|client_service|cost_reduction|compliance|modernization|other>",
  "strength_score": <1-5 integer, 5=very strong justification>,
  "public_benefit_clarity": "<1-3 sentence assessment>",
  "trade_off_adequacy": "<1-3 sentence assessment>",
  "confinement_assessment": "<1-3 sentence assessment>"
}}"""

PROMPT_RISK = """\
Analyze this AIA submission's risk profile and individual rights impact.

## Risk Scores (0=none, 4=severe)
- Public Scrutiny: {public_scrutiny_score}
- Vulnerable Clients: {vulnerable_clients_score}
- High Stakes: {high_stakes_score}
- Staff Impact: {staff_impact_score}
- Disability Barriers: {disability_barriers_score}
- Risk Total: {risk_total}

## Individual Impact Descriptions
- Rights & Freedoms (score {rights_freedoms_score}): {rights_freedoms_en}
- Equality & Dignity (score {equality_dignity_score}): {equality_dignity_en}
- Health & Wellbeing (score {health_wellbeing_score}): {health_wellbeing_en}
- Economic Interests (score {economic_interests_score}): {economic_interests_en}

## Decision Context
- Automation Type: {automation_type_score} (0=support, 2=partial, 4=full)
- Reversibility: {impacts_reversible_score} (0=irreversible, 4=easily reversible)
- Duration: {impact_duration_score} (0=long-term, 4=brief)

Produce a JSON object:
{{
  "risk_level_label": "<low|moderate|high|very_high>",
  "dominant_risk_dimension": "<which of the 5 risk dimensions is highest and why>",
  "rights_concern_summary": "<2-4 sentences on which rights are most at stake>",
  "proportionality_assessment": "<is the automation level proportional to the risk?>",
  "reversibility_concern": "<concern about irreversibility, or null if not applicable>"
}}"""

PROMPT_DIVERGENCE = """\
You are a bilingual policy analyst comparing English and French versions of \
the SAME Canadian AIA submission. These are not separate documents — they \
are the EN and FR fields from one form.

Compare each field pair for semantic equivalence vs. divergence.

## Field Pairs
{field_pairs_block}

For each pair where both EN and FR are non-empty, assess:
- Is the FR a faithful translation of the EN?
- Are there conceptual additions, omissions, or reframings?
- Do different legal/cultural assumptions appear?

Produce a JSON object:
{{
  "has_divergence": <true|false>,
  "divergence_count": <integer>,
  "divergent_fields": [
    {{
      "field": "<field name>",
      "type": "<translation|omission|addition|reframing|terminological>",
      "severity": "<minor|moderate|significant>",
      "explanation": "<1-2 sentences>"
    }}
  ],
  "overall_divergence_type": "<linguistic|legal|cultural|professional|none>",
  "semantic_fidelity_score": <1-5, 5=perfect translation>,
  "untranslatable_concepts": ["<concept>", ...]
}}"""

PROMPT_SAFEGUARD = """\
Assess the safeguard compliance posture of this AIA submission.

## Consultation (0=No, 1=Yes)
- Internal stakeholders engaged: {internal_stakeholders_engaged}
- External stakeholders engaged: {external_stakeholders_engaged}

## Data Quality & Bias (0=No, 1=Yes)
- Bias testing documented: {bias_testing_documented}
- Bias testing public: {bias_testing_public}
- GBA+ conducted: {gba_plus_conducted}
- GBA+ public: {gba_plus_public}
- Accountability assigned: {accountability_assigned}
- Data on Open Gov portal: {data_on_open_gov_portal}

## Fairness (0=No, 1=Yes)
- Audit identifies authority: {audit_identifies_authority}
- Records all decisions: {audit_records_all_decisions}
- Can produce reasons: {can_produce_reasons}
- Human override enabled: {human_override_enabled}
- Client recourse process: {client_recourse_process}
- User feedback mechanism: {user_feedback_mechanism}
- GC EARB reviewed: {gc_earb_reviewed}
- Change log maintained: {change_log_maintained}

## Privacy & Security (0=No, 1=Yes)
- PIA conducted: {pia_conducted}
- Privacy by design: {privacy_by_design}
- De-identification applied: {de_identification_applied}
- Data sharing agreement: {data_sharing_agreement}

Produce a JSON object:
{{
  "overall_compliance_label": "<strong|adequate|weak|minimal>",
  "overall_compliance_score": <1-5>,
  "consultation_assessment": "<1-2 sentences>",
  "bias_mitigation_assessment": "<1-2 sentences>",
  "fairness_assessment": "<1-2 sentences>",
  "privacy_assessment": "<1-2 sentences>",
  "gaps_identified": ["<gap description>", ...]
}}"""

PROMPT_THEMES = """\
You are analyzing {n} Canadian federal AIA submissions to identify \
thematic patterns in their "{pattern_type}" dimension.

## Per-Submission Summaries
{summaries_block}

Identify 3-7 recurring themes across these submissions.

Produce a JSON array:
[
  {{
    "theme_label": "<short label>",
    "theme_description": "<2-3 sentence description>",
    "submission_ids": [<int>, ...],
    "prevalence": <0.00-1.00>,
    "notable_outliers": [{{
      "submission_id": <int>,
      "reason": "<why it deviates>"
    }}]
  }}
]"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def t(val):
    """Truncate a text value for prompt inclusion."""
    if val is None:
        return "(not provided)"
    s = str(val).strip()
    return s[:TEXT_TRUNCATE] if s else "(empty)"


def s(val):
    """Format a score value."""
    return str(val) if val is not None else "N/A"


def parse_llm_json(text, expect_object=True):
    """Extract JSON from LLM response, tolerating markdown fences and trailing data."""
    text = text.strip()
    # Strip markdown code fences
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()

    # Use the JSON decoder to parse just the first valid JSON value
    decoder = json.JSONDecoder()
    # Find the start of JSON
    for i, ch in enumerate(text):
        if ch in ('{', '['):
            obj, _ = decoder.raw_decode(text, i)
            # If we expect an object but got a list, unwrap single-element lists
            if expect_object and isinstance(obj, list):
                if len(obj) == 1:
                    return obj[0]
                # For multi-element lists, return as-is (caller handles)
                return obj
            return obj

    return json.loads(text)


def call_llm(user_prompt, retries=2, expect_object=True):
    """Call the LLM API and return parsed JSON + raw text."""
    last_error = None
    for attempt in range(1 + retries):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_MSG},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            )
            raw = resp.choices[0].message.content.strip()
            parsed = parse_llm_json(raw, expect_object=expect_object)
            usage = {
                "prompt_tokens": resp.usage.prompt_tokens,
                "completion_tokens": resp.usage.completion_tokens,
            }
            return parsed, raw, usage
        except json.JSONDecodeError as e:
            last_error = e
            if attempt < retries:
                time.sleep(RATE_LIMIT_DELAY)
                continue
        except Exception as e:
            last_error = e
            break

    raise RuntimeError(f"LLM call failed after {1 + retries} attempts: {last_error}")


def already_processed(cur, table, submission_id, prompt_version):
    """Check if this submission was already interpreted at this prompt version."""
    cur.execute(
        f"SELECT 1 FROM {table} WHERE submission_id = %s AND prompt_version = %s",
        (submission_id, prompt_version),
    )
    return cur.fetchone() is not None


# ---------------------------------------------------------------------------
# Analysis pipelines
# ---------------------------------------------------------------------------

def run_justification(conn, limit=None, dry_run=False):
    """Automation justification analysis."""
    pv = PROMPT_V["justification"]
    table = "interp_automation_justification"
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT pd.submission_id, pd.department, pd.project_title_en,
               pd.project_title_fr, pd.phase, pd.description_en,
               ra.client_needs_en, ra.public_benefits_en,
               ra.expected_improvements_en, ra.trade_offs_en,
               ra.why_automation_preferred_en, ra.system_confinement_en,
               ad.automation_type_score, ad.system_role_en,
               ad.evaluation_criteria_en
        FROM project_details pd
        JOIN reasons_for_automation ra USING (submission_id)
        JOIN about_the_decision ad USING (submission_id)
        ORDER BY pd.submission_id
    """)
    rows = cur.fetchall()
    if limit:
        rows = rows[:limit]

    processed, skipped, errors = 0, 0, 0
    for row in rows:
        sid = row["submission_id"]
        if already_processed(cur, table, sid, pv):
            skipped += 1
            continue

        prompt = PROMPT_JUSTIFICATION.format(
            department=t(row["department"]),
            project_title_en=t(row["project_title_en"]),
            project_title_fr=t(row["project_title_fr"]),
            phase=t(row["phase"]),
            description_en=t(row["description_en"]),
            client_needs_en=t(row["client_needs_en"]),
            public_benefits_en=t(row["public_benefits_en"]),
            expected_improvements_en=t(row["expected_improvements_en"]),
            trade_offs_en=t(row["trade_offs_en"]),
            why_automation_preferred_en=t(row["why_automation_preferred_en"]),
            system_confinement_en=t(row["system_confinement_en"]),
            automation_type_score=s(row["automation_type_score"]),
            system_role_en=t(row["system_role_en"]),
            evaluation_criteria_en=t(row["evaluation_criteria_en"]),
        )

        if dry_run:
            print(f"\n--- Submission {sid} ---")
            print(prompt[:400] + "...\n")
            processed += 1
            continue

        try:
            parsed, raw, usage = call_llm(prompt)
            parsed["usage"] = usage
            wcur = conn.cursor()
            wcur.execute(
                f"""INSERT INTO {table}
                    (submission_id, justification_theme, strength_score,
                     public_benefit_clarity, trade_off_adequacy,
                     confinement_assessment, raw_llm_response,
                     model_id, prompt_version)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    sid,
                    parsed["justification_theme"],
                    parsed["strength_score"],
                    parsed["public_benefit_clarity"],
                    parsed["trade_off_adequacy"],
                    parsed["confinement_assessment"],
                    psycopg2.extras.Json(parsed),
                    MODEL, pv,
                ),
            )
            conn.commit()
            processed += 1
            print(f"  [justification] submission {sid}: "
                  f"theme={parsed['justification_theme']}, "
                  f"strength={parsed['strength_score']}")
        except Exception as e:
            conn.rollback()
            errors += 1
            print(f"  [justification] submission {sid}: ERROR — {e}")

        time.sleep(RATE_LIMIT_DELAY)

    return processed, skipped, errors


def run_risk(conn, limit=None, dry_run=False):
    """Risk & rights impact interpretation."""
    pv = PROMPT_V["risk"]
    table = "interp_risk_rights_impact"
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT rp.submission_id,
               rp.public_scrutiny_score, rp.vulnerable_clients_score,
               rp.high_stakes_score, rp.staff_impact_score,
               rp.disability_barriers_score, rp.risk_total,
               ii.rights_freedoms_score, ii.rights_freedoms_en,
               ii.equality_dignity_score, ii.equality_dignity_en,
               ii.health_wellbeing_score, ii.health_wellbeing_en,
               ii.economic_interests_score, ii.economic_interests_en,
               ad.automation_type_score, ad.impacts_reversible_score,
               ad.impact_duration_score
        FROM risk_profile rp
        JOIN individual_impacts ii USING (submission_id)
        JOIN about_the_decision ad USING (submission_id)
        ORDER BY rp.submission_id
    """)
    rows = cur.fetchall()
    if limit:
        rows = rows[:limit]

    processed, skipped, errors = 0, 0, 0
    for row in rows:
        sid = row["submission_id"]
        if already_processed(cur, table, sid, pv):
            skipped += 1
            continue

        prompt = PROMPT_RISK.format(
            public_scrutiny_score=s(row["public_scrutiny_score"]),
            vulnerable_clients_score=s(row["vulnerable_clients_score"]),
            high_stakes_score=s(row["high_stakes_score"]),
            staff_impact_score=s(row["staff_impact_score"]),
            disability_barriers_score=s(row["disability_barriers_score"]),
            risk_total=s(row["risk_total"]),
            rights_freedoms_score=s(row["rights_freedoms_score"]),
            rights_freedoms_en=t(row["rights_freedoms_en"]),
            equality_dignity_score=s(row["equality_dignity_score"]),
            equality_dignity_en=t(row["equality_dignity_en"]),
            health_wellbeing_score=s(row["health_wellbeing_score"]),
            health_wellbeing_en=t(row["health_wellbeing_en"]),
            economic_interests_score=s(row["economic_interests_score"]),
            economic_interests_en=t(row["economic_interests_en"]),
            automation_type_score=s(row["automation_type_score"]),
            impacts_reversible_score=s(row["impacts_reversible_score"]),
            impact_duration_score=s(row["impact_duration_score"]),
        )

        if dry_run:
            print(f"\n--- Submission {sid} ---")
            print(prompt[:400] + "...\n")
            processed += 1
            continue

        try:
            parsed, raw, usage = call_llm(prompt)
            parsed["usage"] = usage
            wcur = conn.cursor()
            wcur.execute(
                f"""INSERT INTO {table}
                    (submission_id, risk_level_label, dominant_risk_dimension,
                     rights_concern_summary, proportionality_assessment,
                     reversibility_concern, raw_llm_response,
                     model_id, prompt_version)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    sid,
                    parsed["risk_level_label"],
                    parsed["dominant_risk_dimension"],
                    parsed["rights_concern_summary"],
                    parsed["proportionality_assessment"],
                    parsed.get("reversibility_concern"),
                    psycopg2.extras.Json(parsed),
                    MODEL, pv,
                ),
            )
            conn.commit()
            processed += 1
            print(f"  [risk] submission {sid}: "
                  f"level={parsed['risk_level_label']}")
        except Exception as e:
            conn.rollback()
            errors += 1
            print(f"  [risk] submission {sid}: ERROR — {e}")

        time.sleep(RATE_LIMIT_DELAY)

    return processed, skipped, errors


def run_divergence(conn, limit=None, dry_run=False):
    """Bilingual divergence analysis."""
    pv = PROMPT_V["divergence"]
    table = "interp_bilingual_divergence"
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Collect all bilingual field pairs per submission
    cur.execute("""
        SELECT pd.submission_id,
               pd.project_title_en, pd.project_title_fr,
               pd.description_en, pd.description_fr,
               ra.motivation_other_en, ra.motivation_other_fr,
               ra.client_needs_en, ra.client_needs_fr,
               ra.public_benefits_en, ra.public_benefits_fr,
               ra.expected_improvements_en, ra.expected_improvements_fr,
               ra.system_confinement_en, ra.system_confinement_fr,
               ra.trade_offs_en, ra.trade_offs_fr,
               ra.why_automation_preferred_en, ra.why_automation_preferred_fr,
               ra.no_deploy_consequence_en, ra.no_deploy_consequence_fr,
               ad.decision_description_en, ad.decision_description_fr,
               ad.system_role_en, ad.system_role_fr,
               ad.evaluation_criteria_en, ad.evaluation_criteria_fr,
               ad.system_output_en, ad.system_output_fr,
               ii.rights_freedoms_en, ii.rights_freedoms_fr,
               ii.equality_dignity_en, ii.equality_dignity_fr,
               ii.health_wellbeing_en, ii.health_wellbeing_fr,
               ii.economic_interests_en, ii.economic_interests_fr,
               atd.data_description_en, atd.data_description_fr,
               ps.pia_description_en, ps.pia_description_fr,
               ps.de_identification_method_en, ps.de_identification_method_fr
        FROM project_details pd
        JOIN reasons_for_automation ra USING (submission_id)
        JOIN about_the_decision ad USING (submission_id)
        JOIN individual_impacts ii USING (submission_id)
        JOIN about_the_data atd USING (submission_id)
        JOIN privacy_security ps USING (submission_id)
        ORDER BY pd.submission_id
    """)
    rows = cur.fetchall()
    if limit:
        rows = rows[:limit]

    # Define bilingual field pairs (base name -> en/fr column names)
    FIELD_PAIRS = [
        ("project_title",          "project_title_en",          "project_title_fr"),
        ("description",            "description_en",            "description_fr"),
        ("client_needs",           "client_needs_en",           "client_needs_fr"),
        ("public_benefits",        "public_benefits_en",        "public_benefits_fr"),
        ("expected_improvements",  "expected_improvements_en",  "expected_improvements_fr"),
        ("system_confinement",     "system_confinement_en",     "system_confinement_fr"),
        ("trade_offs",             "trade_offs_en",             "trade_offs_fr"),
        ("why_automation_preferred","why_automation_preferred_en","why_automation_preferred_fr"),
        ("decision_description",   "decision_description_en",   "decision_description_fr"),
        ("system_role",            "system_role_en",            "system_role_fr"),
        ("evaluation_criteria",    "evaluation_criteria_en",    "evaluation_criteria_fr"),
        ("system_output",          "system_output_en",          "system_output_fr"),
        ("rights_freedoms",        "rights_freedoms_en",        "rights_freedoms_fr"),
        ("equality_dignity",       "equality_dignity_en",       "equality_dignity_fr"),
        ("health_wellbeing",       "health_wellbeing_en",       "health_wellbeing_fr"),
        ("economic_interests",     "economic_interests_en",     "economic_interests_fr"),
        ("data_description",       "data_description_en",       "data_description_fr"),
        ("pia_description",        "pia_description_en",        "pia_description_fr"),
        ("de_identification_method","de_identification_method_en","de_identification_method_fr"),
    ]

    processed, skipped, errors = 0, 0, 0
    for row in rows:
        sid = row["submission_id"]
        if already_processed(cur, table, sid, pv):
            skipped += 1
            continue

        # Build field pairs block, only include pairs where at least one side is non-empty
        lines = []
        pair_count = 0
        for label, en_col, fr_col in FIELD_PAIRS:
            en_val = (row.get(en_col) or "").strip()
            fr_val = (row.get(fr_col) or "").strip()
            if en_val or fr_val:
                pair_count += 1
                lines.append(f"### {label}")
                lines.append(f"EN: {en_val[:TEXT_TRUNCATE] if en_val else '(empty)'}")
                lines.append(f"FR: {fr_val[:TEXT_TRUNCATE] if fr_val else '(empty)'}")
                lines.append("")

        if pair_count == 0:
            skipped += 1
            continue

        prompt = PROMPT_DIVERGENCE.format(field_pairs_block="\n".join(lines))

        if dry_run:
            print(f"\n--- Submission {sid} ({pair_count} pairs) ---")
            print(prompt[:500] + "...\n")
            processed += 1
            continue

        try:
            parsed, raw, usage = call_llm(prompt)
            parsed["usage"] = usage
            wcur = conn.cursor()
            wcur.execute(
                f"""INSERT INTO {table}
                    (submission_id, has_divergence, divergence_count,
                     divergent_fields, overall_divergence_type,
                     semantic_fidelity_score, untranslatable_concepts,
                     raw_llm_response, model_id, prompt_version)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    sid,
                    parsed["has_divergence"],
                    parsed["divergence_count"],
                    psycopg2.extras.Json(parsed.get("divergent_fields", [])),
                    parsed.get("overall_divergence_type"),
                    parsed.get("semantic_fidelity_score"),
                    psycopg2.extras.Json(parsed.get("untranslatable_concepts", [])),
                    psycopg2.extras.Json(parsed),
                    MODEL, pv,
                ),
            )
            conn.commit()
            processed += 1
            div = "YES" if parsed["has_divergence"] else "no"
            print(f"  [divergence] submission {sid}: "
                  f"divergence={div}, fidelity={parsed.get('semantic_fidelity_score')}")
        except Exception as e:
            conn.rollback()
            errors += 1
            print(f"  [divergence] submission {sid}: ERROR — {e}")

        time.sleep(RATE_LIMIT_DELAY)

    return processed, skipped, errors


def run_safeguard(conn, limit=None, dry_run=False):
    """Safeguard compliance assessment."""
    pv = PROMPT_V["safeguard"]
    table = "interp_safeguard_compliance"
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT c.submission_id,
               c.internal_stakeholders_engaged, c.external_stakeholders_engaged,
               dqb.bias_testing_documented, dqb.bias_testing_public,
               dqb.gba_plus_conducted, dqb.gba_plus_public,
               dqb.accountability_assigned, dqb.data_on_open_gov_portal,
               f.audit_identifies_authority, f.audit_records_all_decisions,
               f.can_produce_reasons, f.human_override_enabled,
               f.client_recourse_process, f.user_feedback_mechanism,
               f.gc_earb_reviewed, f.change_log_maintained,
               ps.pia_conducted, ps.privacy_by_design,
               ps.de_identification_applied, ps.data_sharing_agreement
        FROM consultation c
        JOIN data_quality_bias dqb USING (submission_id)
        JOIN fairness f USING (submission_id)
        JOIN privacy_security ps USING (submission_id)
        ORDER BY c.submission_id
    """)
    rows = cur.fetchall()
    if limit:
        rows = rows[:limit]

    processed, skipped, errors = 0, 0, 0
    for row in rows:
        sid = row["submission_id"]
        if already_processed(cur, table, sid, pv):
            skipped += 1
            continue

        prompt = PROMPT_SAFEGUARD.format(
            internal_stakeholders_engaged=s(row["internal_stakeholders_engaged"]),
            external_stakeholders_engaged=s(row["external_stakeholders_engaged"]),
            bias_testing_documented=s(row["bias_testing_documented"]),
            bias_testing_public=s(row["bias_testing_public"]),
            gba_plus_conducted=s(row["gba_plus_conducted"]),
            gba_plus_public=s(row["gba_plus_public"]),
            accountability_assigned=s(row["accountability_assigned"]),
            data_on_open_gov_portal=s(row["data_on_open_gov_portal"]),
            audit_identifies_authority=s(row["audit_identifies_authority"]),
            audit_records_all_decisions=s(row["audit_records_all_decisions"]),
            can_produce_reasons=s(row["can_produce_reasons"]),
            human_override_enabled=s(row["human_override_enabled"]),
            client_recourse_process=s(row["client_recourse_process"]),
            user_feedback_mechanism=s(row["user_feedback_mechanism"]),
            gc_earb_reviewed=s(row["gc_earb_reviewed"]),
            change_log_maintained=s(row["change_log_maintained"]),
            pia_conducted=s(row["pia_conducted"]),
            privacy_by_design=s(row["privacy_by_design"]),
            de_identification_applied=s(row["de_identification_applied"]),
            data_sharing_agreement=s(row["data_sharing_agreement"]),
        )

        if dry_run:
            print(f"\n--- Submission {sid} ---")
            print(prompt[:400] + "...\n")
            processed += 1
            continue

        try:
            parsed, raw, usage = call_llm(prompt)
            parsed["usage"] = usage
            wcur = conn.cursor()
            wcur.execute(
                f"""INSERT INTO {table}
                    (submission_id, overall_compliance_label,
                     overall_compliance_score, consultation_assessment,
                     bias_mitigation_assessment, fairness_assessment,
                     privacy_assessment, gaps_identified,
                     raw_llm_response, model_id, prompt_version)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    sid,
                    parsed["overall_compliance_label"],
                    parsed["overall_compliance_score"],
                    parsed["consultation_assessment"],
                    parsed["bias_mitigation_assessment"],
                    parsed["fairness_assessment"],
                    parsed["privacy_assessment"],
                    psycopg2.extras.Json(parsed.get("gaps_identified", [])),
                    psycopg2.extras.Json(parsed),
                    MODEL, pv,
                ),
            )
            conn.commit()
            processed += 1
            print(f"  [safeguard] submission {sid}: "
                  f"compliance={parsed['overall_compliance_label']} "
                  f"({parsed['overall_compliance_score']}/5)")
        except Exception as e:
            conn.rollback()
            errors += 1
            print(f"  [safeguard] submission {sid}: ERROR — {e}")

        time.sleep(RATE_LIMIT_DELAY)

    return processed, skipped, errors


def run_themes(conn, dry_run=False):
    """Cross-submission thematic pattern analysis."""
    pv = PROMPT_V["themes"]
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    analyses = {
        "justification": {
            "table": "interp_automation_justification",
            "summary_cols": "submission_id, justification_theme, strength_score, "
                            "public_benefit_clarity",
        },
        "risk": {
            "table": "interp_risk_rights_impact",
            "summary_cols": "submission_id, risk_level_label, "
                            "dominant_risk_dimension, rights_concern_summary",
        },
        "divergence": {
            "table": "interp_bilingual_divergence",
            "summary_cols": "submission_id, has_divergence, divergence_count, "
                            "overall_divergence_type, semantic_fidelity_score",
        },
        "safeguard": {
            "table": "interp_safeguard_compliance",
            "summary_cols": "submission_id, overall_compliance_label, "
                            "overall_compliance_score, gaps_identified",
        },
    }

    processed, errors = 0, 0
    for pattern_type, cfg in analyses.items():
        # Check if source data exists
        cur.execute(f"SELECT COUNT(*) FROM {cfg['table']}")
        count = cur.fetchone()["count"]
        if count == 0:
            print(f"  [themes] skipping {pattern_type}: no source interpretations")
            continue

        # Check if themes already generated for this version
        cur.execute(
            "SELECT 1 FROM interp_thematic_patterns "
            "WHERE pattern_type = %s AND prompt_version = %s",
            (pattern_type, pv),
        )
        if cur.fetchone():
            print(f"  [themes] skipping {pattern_type}: already generated at v{pv}")
            continue

        cur.execute(f"SELECT {cfg['summary_cols']} FROM {cfg['table']}")
        rows = cur.fetchall()

        summaries = []
        for row in rows:
            parts = [f"Submission {row['submission_id']}:"]
            for k, v in row.items():
                if k == "submission_id":
                    continue
                val = str(v)[:200] if v is not None else "N/A"
                parts.append(f"  {k}: {val}")
            summaries.append("\n".join(parts))

        prompt = PROMPT_THEMES.format(
            n=len(rows),
            pattern_type=pattern_type,
            summaries_block="\n\n".join(summaries),
        )

        if dry_run:
            print(f"\n--- Themes: {pattern_type} ({len(rows)} submissions) ---")
            print(prompt[:600] + "...\n")
            processed += 1
            continue

        try:
            parsed, raw, usage = call_llm(prompt, expect_object=False)
            if not isinstance(parsed, list):
                parsed = [parsed]

            wcur = conn.cursor()
            for theme in parsed:
                theme["usage"] = usage
                wcur.execute(
                    """INSERT INTO interp_thematic_patterns
                        (pattern_type, theme_label, theme_description,
                         submission_ids, prevalence, notable_outliers,
                         raw_llm_response, model_id, prompt_version)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (pattern_type, theme_label, prompt_version)
                        DO NOTHING""",
                    (
                        pattern_type,
                        theme["theme_label"],
                        theme["theme_description"],
                        theme["submission_ids"],
                        theme["prevalence"],
                        psycopg2.extras.Json(theme.get("notable_outliers")),
                        psycopg2.extras.Json(theme),
                        MODEL, pv,
                    ),
                )
            conn.commit()
            processed += 1
            print(f"  [themes] {pattern_type}: {len(parsed)} themes identified")
        except Exception as e:
            conn.rollback()
            errors += 1
            print(f"  [themes] {pattern_type}: ERROR — {e}")

        time.sleep(RATE_LIMIT_DELAY)

    return processed, 0, errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

PIPELINES = {
    "justification": run_justification,
    "risk":          run_risk,
    "divergence":    run_divergence,
    "safeguard":     run_safeguard,
}


def main():
    parser = argparse.ArgumentParser(
        description="LLM Semantic Interpretation ETL for AIA Corpus"
    )
    parser.add_argument(
        "--analysis",
        choices=["justification", "risk", "divergence", "safeguard", "themes", "all"],
        default="all",
        help="Which analysis to run (default: all)",
    )
    parser.add_argument("--limit", type=int, default=None,
                        help="Process only N submissions (for testing)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print prompts without calling LLM")
    args = parser.parse_args()

    # Connect to database
    conn = psycopg2.connect(DB_DSN)
    print(f"Connected to database: {DB_DSN}")
    print(f"Model: {MODEL}")
    print(f"Base URL: {LLM_BASE_URL}")
    if args.dry_run:
        print("DRY RUN — no API calls or DB writes\n")

    # Create interpretation tables
    schema_path = Path(__file__).resolve().parent / "schema_interpretations.sql"
    with open(schema_path) as f:
        conn.cursor().execute(f.read())
    conn.commit()
    print("Interpretation tables ready.\n")

    # Determine which analyses to run
    if args.analysis == "all":
        to_run = list(PIPELINES.keys()) + ["themes"]
    else:
        to_run = [args.analysis]

    # Run per-submission analyses
    total_stats = {}
    for name in to_run:
        if name == "themes":
            continue  # run after per-submission analyses
        print(f"\n{'='*60}")
        print(f"  Running: {name}")
        print(f"{'='*60}")

        # Log run start
        log_cur = conn.cursor()
        log_cur.execute(
            """INSERT INTO interp_run_log
                (analysis_type, model_id, prompt_version)
                VALUES (%s, %s, %s) RETURNING id""",
            (name, MODEL, PROMPT_V[name]),
        )
        run_id = log_cur.fetchone()[0]
        conn.commit()

        p, s_count, e = PIPELINES[name](conn, limit=args.limit, dry_run=args.dry_run)
        total_stats[name] = (p, s_count, e)

        # Update run log
        if not args.dry_run:
            log_cur.execute(
                """UPDATE interp_run_log
                   SET run_finished_at = NOW(),
                       submissions_processed = %s,
                       submissions_skipped = %s,
                       errors = %s
                   WHERE id = %s""",
                (p, s_count, e, run_id),
            )
            conn.commit()

        print(f"\n  Result: {p} processed, {s_count} skipped, {e} errors")

    # Run themes if requested
    if "themes" in to_run:
        print(f"\n{'='*60}")
        print(f"  Running: thematic patterns")
        print(f"{'='*60}")
        p, _, e = run_themes(conn, dry_run=args.dry_run)
        total_stats["themes"] = (p, 0, e)
        print(f"\n  Result: {p} pattern types processed, {e} errors")

    # Summary
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    for name, (p, sk, e) in total_stats.items():
        print(f"  {name:20s}  processed={p}  skipped={sk}  errors={e}")

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
