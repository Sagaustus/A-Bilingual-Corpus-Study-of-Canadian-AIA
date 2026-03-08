"""
Populates the 12 AIA section tables from JSON form files.

One row per form_submission per section table.
Scored fields → raw integer extracted from item code (e.g. "item2-3" → 3).
Text fields   → EN from data.*, FR from translationsOnResult.*.
Multi-select  → comma-joined list of item codes.

Outputs (one CSV per section table, ready for DB import):
  etl/output/section/project_details.csv
  etl/output/section/reasons_for_automation.csv
  etl/output/section/risk_profile.csv
  etl/output/section/project_authority.csv
  etl/output/section/about_the_algorithm.csv
  etl/output/section/about_the_decision.csv
  etl/output/section/individual_impacts.csv
  etl/output/section/about_the_data.csv
  etl/output/section/consultation.csv
  etl/output/section/data_quality_bias.csv
  etl/output/section/fairness.csv
  etl/output/section/privacy_security.csv
"""

import csv
import json
import re
from pathlib import Path

RESOURCES = Path(__file__).parent.parent / "resources"
SUB_CSV   = Path(__file__).parent / "output" / "form_submissions.csv"
OUT       = Path(__file__).parent / "output" / "section"
OUT.mkdir(parents=True, exist_ok=True)

# ── helpers ───────────────────────────────────────────────────────────────────

def score(val) -> int | None:
    """Extract trailing integer from an item code: 'item2-3' → 3."""
    if not isinstance(val, str):
        return None
    m = re.search(r"-(\d+)$", val)
    return int(m.group(1)) if m else None


def multi(val) -> str:
    """Normalise a multi-select value (list or string) to comma-joined string."""
    if isinstance(val, list):
        return ",".join(str(v) for v in val)
    return str(val) if val else ""


def txt(data: dict, key: str) -> str:
    v = data.get(key, "")
    return str(v).strip() if v and str(v) not in ("-", "N/A", "NA") else ""


def tr(trans: dict, key: str) -> str:
    v = trans.get(key, "")
    return str(v).strip() if v and str(v) not in ("-", "N/A", "NA") else ""


def write_csv(name: str, fieldnames: list[str], rows: list[dict]) -> None:
    p = OUT / f"{name}.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  {len(rows):>4} rows → section/{name}.csv")


# ── load submission id map (source_file → submission id) ─────────────────────

with open(SUB_CSV, encoding="utf-8") as f:
    subs = list(csv.DictReader(f))

# Map (dataset_id, source_file) → submission id for JSON files only
json_sub_map: dict[tuple[str, str], str] = {
    (s["dataset_id"], s["source_file"]): s["id"]
    for s in subs
    if s["source_format"] == "json"
}

# ── accumulators ──────────────────────────────────────────────────────────────

proj_rows:    list[dict] = []
reasons_rows: list[dict] = []
risk_rows:    list[dict] = []
auth_rows:    list[dict] = []
algo_rows:    list[dict] = []
decision_rows:list[dict] = []
impact_rows:  list[dict] = []
data_rows:    list[dict] = []
consult_rows: list[dict] = []
dqbias_rows:  list[dict] = []
fairness_rows:list[dict] = []
privacy_rows: list[dict] = []

# ── process each JSON file ────────────────────────────────────────────────────

for path in sorted(RESOURCES.rglob("*.json")):
    dataset_id = path.parent.name
    key = (dataset_id, path.name)
    if key not in json_sub_map:
        continue
    sid = json_sub_map[key]

    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        print(f"  WARN {path.name}: {e}")
        continue

    d = raw.get("data", {})
    t = raw.get("translationsOnResult", {})

    # ── 1. project_details ────────────────────────────────────────────────────
    phase_val = d.get("projectDetailsPhase", "")
    proj_rows.append({
        "submission_id":      sid,
        "respondent":         txt(d, "projectDetailsRespondent"),
        "job_title":          txt(d, "projectDetailsJob"),
        "department":         txt(d, "projectDetailsDepartment-NS"),
        "branch":             txt(d, "projectDetailsBranch"),
        "project_title_en":   txt(d, "projectDetailsTitle"),
        "project_title_fr":   tr(t,  "projectDetailsTitle"),
        "project_id_it_plan": txt(d, "projectDetailsID"),
        "program":            txt(d, "projectDetailsProgram"),
        "phase":              phase_val,
        "phase_score":        score(phase_val) if isinstance(phase_val, str) else "",
        "description_en":     txt(d, "projectDetailsDescription"),
        "description_fr":     tr(t,  "projectDetailsDescription"),
        "system_capabilities":multi(d.get("aboutSystem1", "")),
    })

    # ── 2. reasons_for_automation ─────────────────────────────────────────────
    reasons_rows.append({
        "submission_id":               sid,
        "motivation_types":            multi(d.get("businessDrivers1", "")),
        "motivation_other_en":         txt(d, "motivation-other"),
        "motivation_other_fr":         tr(t,  "motivation-other"),
        "client_needs_en":             txt(d, "businessDrivers3"),
        "client_needs_fr":             tr(t,  "businessDrivers3"),
        "public_benefits_en":          txt(d, "businessDrivers4"),
        "public_benefits_fr":          tr(t,  "businessDrivers4"),
        "effectiveness_score":         score(d.get("businessDrivers5")),
        "expected_improvements_en":    txt(d, "businessDrivers6"),
        "expected_improvements_fr":    tr(t,  "businessDrivers6"),
        "system_confinement_en":       txt(d, "businessDrivers7"),
        "system_confinement_fr":       tr(t,  "businessDrivers7"),
        "trade_offs_en":               txt(d, "businessDrivers8"),
        "trade_offs_fr":               tr(t,  "businessDrivers8"),
        "alternatives_considered":     score(d.get("businessDrivers9")),
        "why_automation_preferred_en": txt(d, "businessDrivers10"),
        "why_automation_preferred_fr": tr(t,  "businessDrivers10"),
        "no_deploy_consequence_types": multi(d.get("businessDrivers11", "")),
        "no_deploy_consequence_en":    txt(d, "businessDrivers12"),
        "no_deploy_consequence_fr":    tr(t,  "businessDrivers12"),
    })

    # ── 3. risk_profile ───────────────────────────────────────────────────────
    scores_rp = [
        score(d.get("riskProfile1")),
        score(d.get("riskProfile2")),
        score(d.get("riskProfile3")),
        score(d.get("riskProfile4")),
        score(d.get("riskProfile5")),
    ]
    risk_rows.append({
        "submission_id":             sid,
        "public_scrutiny_score":     scores_rp[0],
        "vulnerable_clients_score":  scores_rp[1],
        "high_stakes_score":         scores_rp[2],
        "staff_impact_score":        scores_rp[3],
        "disability_barriers_score": scores_rp[4],
        "risk_total":                sum(s for s in scores_rp if s is not None),
    })

    # ── 4. project_authority ──────────────────────────────────────────────────
    auth_rows.append({
        "submission_id":              sid,
        "new_policy_authority_score": score(d.get("projectAuthority1")),
    })

    # ── 5. about_the_algorithm ────────────────────────────────────────────────
    algo_rows.append({
        "submission_id":          sid,
        "is_trade_secret_score":    score(d.get("aboutAlgorithm1")),
        "is_hard_to_explain_score": score(d.get("aboutAlgorithm2")),
    })

    # ── 6. about_the_decision ─────────────────────────────────────────────────
    desc_en = " ".join(filter(None, [txt(d, "decisionSector2"), txt(d, "decisionSector3")]))
    desc_fr = " ".join(filter(None, [tr(t, "decisionSector2"),  tr(t, "decisionSector3")]))
    decision_rows.append({
        "submission_id":               sid,
        "decision_description_en":     desc_en,
        "decision_description_fr":     desc_fr,
        "decision_sectors":            multi(d.get("decisionSector1", "")),
        "automation_type_score":       score(d.get("impact22")),
        "system_role_en":              txt(d, "impact4"),
        "system_role_fr":              tr(t,  "impact4"),
        "requires_judgement_score":    score(d.get("impact5")),
        "evaluation_criteria_en":      txt(d, "impact6"),
        "evaluation_criteria_fr":      tr(t,  "impact6"),
        "system_output_en":            txt(d, "impact7"),
        "system_output_fr":            tr(t,  "impact7"),
        "superhuman_task_score":       score(d.get("impact3")),
        "used_by_different_org_score": score(d.get("impact30")),
        "impacts_reversible_score":    score(d.get("impact9")),
        "impact_duration_score":       score(d.get("impact8")),
    })

    # ── 7. individual_impacts ─────────────────────────────────────────────────
    impact_rows.append({
        "submission_id":           sid,
        "rights_freedoms_score":   score(d.get("impact11")),
        "rights_freedoms_en":      txt(d, "impact12"),
        "rights_freedoms_fr":      tr(t,  "impact12"),
        "equality_dignity_score":  score(d.get("impact13")),
        "equality_dignity_en":     txt(d, "impact14"),
        "equality_dignity_fr":     tr(t,  "impact14"),
        "health_wellbeing_score":  score(d.get("impact15")),
        "health_wellbeing_en":     txt(d, "impact16"),
        "health_wellbeing_fr":     tr(t,  "impact16"),
        "economic_interests_score":score(d.get("impact24")),
        "economic_interests_en":   txt(d, "impact25"),
        "economic_interests_fr":   tr(t,  "impact25"),
    })

    # ── 8. about_the_data ────────────────────────────────────────────────────
    data_rows.append({
        "submission_id":                   sid,
        "uses_personal_info":              score(d.get("aboutDataSource1")),
        "pib_bank_numbers":                txt(d, "aboutDataSource12"),
        "security_classification_score":   score(d.get("aboutDataSource6")),
        "data_controller_score":           score(d.get("aboutDataSource7")),
        "multiple_sources":                score(d.get("aboutDataSource2")),
        "internet_connected_input":        score(d.get("aboutDataSource3")),
        "interfaces_other_systems":        score(d.get("aboutDataSource4")),
        "training_data_collector_score":   score(d.get("aboutDataSource8")),
        "input_data_collector_score":      score(d.get("aboutDataSource9")),
        "data_description_en":             txt(d, "aboutDataSource13"),
        "data_description_fr":             tr(t,  "aboutDataSource13"),
        "uses_unstructured_data":          score(d.get("aboutDataSource5")),
        "unstructured_data_types":         multi(d.get("aboutDataType2", "")),
    })

    # ── 9. consultation ───────────────────────────────────────────────────────
    # Use Implementation keys (most forms); fall back to Design keys
    def ci(key): return d.get(f"consultationImplementation{key}", d.get(f"consultationDesign{key}"))
    def cit(key): return t.get(f"consultationImplementation{key}-other", t.get(f"consultationDesign{key}-other", ""))
    def cie(key): return d.get(f"consultationImplementation{key}-other", d.get(f"consultationDesign{key}-other", ""))

    consult_rows.append({
        "submission_id":                   sid,
        "internal_stakeholders_engaged":   score(ci("1")),
        "internal_stakeholders_list":      multi(ci("2") or ""),
        "internal_stakeholders_other_en":  txt(d, "consultationImplementation2-other") or txt(d, "consultationDesign2-other"),
        "internal_stakeholders_other_fr":  cit("2"),
        "external_stakeholders_engaged":   score(ci("3")),
        "external_stakeholders_list":      multi(ci("4") or ""),
        "external_stakeholders_other_en":  txt(d, "consultationImplementation4-other") or txt(d, "consultationDesign4-other"),
        "external_stakeholders_other_fr":  cit("4"),
    })

    # ── 10. data_quality_bias ────────────────────────────────────────────────
    def dq(n): return score(d.get(f"dataQualityImplementation{n}", d.get(f"dataQualityDesign{n}")))
    dqbias_rows.append({
        "submission_id":                    sid,
        "bias_testing_documented":          dq(1),
        "bias_testing_public":              dq(2),
        "data_quality_process_documented":  dq(3),
        "data_quality_process_public":      dq(4),
        "gba_plus_conducted":               dq(5),
        "gba_plus_public":                  dq(6),
        "accountability_assigned":          dq(7),
        "outdated_data_process":            dq(8),
        "outdated_data_process_public":     dq(9),
        "data_on_open_gov_portal":          dq(10),
    })

    # ── 11. fairness ─────────────────────────────────────────────────────────
    def fi(n): return score(d.get(f"fairnessImplementation{n}", d.get(f"fairnessDesign{n}")))
    fairness_rows.append({
        "submission_id":                sid,
        "audit_identifies_authority":   fi(1),
        "audit_records_all_decisions":  fi(2),
        "audit_key_decision_points":    fi(3),
        "decision_points_linked_law":   fi(4),
        "change_log_maintained":        fi(5),
        "audit_all_system_decisions":   fi(6),
        "audit_generates_notification": fi(7),
        "audit_identifies_version":     fi(8),
        "audit_shows_decision_maker":   fi(9),
        "can_produce_reasons":          fi(10),
        "access_permission_process":    fi(11),
        "user_feedback_mechanism":      fi(12),
        "client_recourse_process":      fi(13),
        "human_override_enabled":       fi(14),
        "override_log_process":         fi(15),
        "audit_records_changes":        fi(16),
        "gc_earb_reviewed":             fi(17),
    })

    # ── 12. privacy_security ─────────────────────────────────────────────────
    def pi(n): return score(d.get(f"privacyImplementation{n}", d.get(f"privacyDesign{n}")))
    privacy_rows.append({
        "submission_id":              sid,
        "pia_conducted":              pi(1),
        "pia_description_en":         txt(d, "privacyImplementation5") or txt(d, "privacyDesign4"),
        "pia_description_fr":         tr(t, "privacyImplementation5") or tr(t, "privacyDesign4"),
        "privacy_by_design":          pi(2),
        "closed_system":              pi(3),
        "data_sharing_agreement":     pi(4),
        "de_identification_applied":  pi(7),
        "de_identification_method_en":txt(d, "privacyImplementation8"),
        "de_identification_method_fr":tr(t, "privacyImplementation8"),
    })

print(f"Processed {len(proj_rows)} JSON submissions\n")

# ── write all 12 section CSVs ─────────────────────────────────────────────────

write_csv("project_details", [
    "submission_id","respondent","job_title","department","branch",
    "project_title_en","project_title_fr","project_id_it_plan","program",
    "phase","phase_score","description_en","description_fr","system_capabilities",
], proj_rows)

write_csv("reasons_for_automation", [
    "submission_id",
    "motivation_types","motivation_other_en","motivation_other_fr",
    "client_needs_en","client_needs_fr",
    "public_benefits_en","public_benefits_fr",
    "effectiveness_score",
    "expected_improvements_en","expected_improvements_fr",
    "system_confinement_en","system_confinement_fr",
    "trade_offs_en","trade_offs_fr",
    "alternatives_considered",
    "why_automation_preferred_en","why_automation_preferred_fr",
    "no_deploy_consequence_types",
    "no_deploy_consequence_en","no_deploy_consequence_fr",
], reasons_rows)

write_csv("risk_profile", [
    "submission_id",
    "public_scrutiny_score","vulnerable_clients_score","high_stakes_score",
    "staff_impact_score","disability_barriers_score","risk_total",
], risk_rows)

write_csv("project_authority", [
    "submission_id","new_policy_authority_score",
], auth_rows)

write_csv("about_the_algorithm", [
    "submission_id","is_trade_secret_score","is_hard_to_explain_score",
], algo_rows)

write_csv("about_the_decision", [
    "submission_id",
    "decision_description_en","decision_description_fr",
    "decision_sectors",
    "automation_type_score",
    "system_role_en","system_role_fr",
    "requires_judgement_score",
    "evaluation_criteria_en","evaluation_criteria_fr",
    "system_output_en","system_output_fr",
    "superhuman_task_score","used_by_different_org_score",
    "impacts_reversible_score","impact_duration_score",
], decision_rows)

write_csv("individual_impacts", [
    "submission_id",
    "rights_freedoms_score","rights_freedoms_en","rights_freedoms_fr",
    "equality_dignity_score","equality_dignity_en","equality_dignity_fr",
    "health_wellbeing_score","health_wellbeing_en","health_wellbeing_fr",
    "economic_interests_score","economic_interests_en","economic_interests_fr",
], impact_rows)

write_csv("about_the_data", [
    "submission_id",
    "uses_personal_info","pib_bank_numbers",
    "security_classification_score","data_controller_score",
    "multiple_sources","internet_connected_input","interfaces_other_systems",
    "training_data_collector_score","input_data_collector_score",
    "data_description_en","data_description_fr",
    "uses_unstructured_data","unstructured_data_types",
], data_rows)

write_csv("consultation", [
    "submission_id",
    "internal_stakeholders_engaged","internal_stakeholders_list",
    "internal_stakeholders_other_en","internal_stakeholders_other_fr",
    "external_stakeholders_engaged","external_stakeholders_list",
    "external_stakeholders_other_en","external_stakeholders_other_fr",
], consult_rows)

write_csv("data_quality_bias", [
    "submission_id",
    "bias_testing_documented","bias_testing_public",
    "data_quality_process_documented","data_quality_process_public",
    "gba_plus_conducted","gba_plus_public",
    "accountability_assigned",
    "outdated_data_process","outdated_data_process_public",
    "data_on_open_gov_portal",
], dqbias_rows)

write_csv("fairness", [
    "submission_id",
    "audit_identifies_authority","audit_records_all_decisions",
    "audit_key_decision_points","decision_points_linked_law",
    "change_log_maintained","audit_all_system_decisions",
    "audit_generates_notification","audit_identifies_version",
    "audit_shows_decision_maker","can_produce_reasons",
    "access_permission_process","user_feedback_mechanism",
    "client_recourse_process","human_override_enabled",
    "override_log_process","audit_records_changes","gc_earb_reviewed",
], fairness_rows)

write_csv("privacy_security", [
    "submission_id",
    "pia_conducted","pia_description_en","pia_description_fr",
    "privacy_by_design","closed_system","data_sharing_agreement",
    "de_identification_applied",
    "de_identification_method_en","de_identification_method_fr",
], privacy_rows)

print("\nDone. All 12 section tables written to etl/output/section/")
