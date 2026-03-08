"""
Populates the four new relational tables from downloaded resources:
  form_submissions  – one row per form file
  project_details   – admin header per submission
  form_answers      – one row per (submission × question)
  answer_items      – exploded multi-select items

Source data:
  - resources/**/*.json  → richest; has raw item codes + French translations
  - resources/**/*.pdf   → parsed text; fills scores + English narrative answers
  - etl/output/questions.csv → question catalog (json_key → question_id)

Outputs (CSV, ready for COPY or ORM bulk-insert):
  etl/output/form_submissions.csv
  etl/output/project_details.csv
  etl/output/form_answers.csv
  etl/output/answer_items.csv
"""

import csv
import json
import re
from pathlib import Path

import pdfplumber

RESOURCES   = Path(__file__).parent.parent / "resources"
OUT         = Path(__file__).parent / "output"
Q_CATALOG   = OUT / "questions.csv"

# ── Load question catalog ──────────────────────────────────────────────────

with open(Q_CATALOG, encoding="utf-8") as f:
    questions = list(csv.DictReader(f))

# json_key → question row
key_to_q: dict[str, dict] = {q["json_key"]: q for q in questions if q["json_key"]}
# question_id → question row
id_to_q: dict[str, dict] = {q["question_id"]: q for q in questions}

# ── Score helpers ──────────────────────────────────────────────────────────

def score_from_item(val) -> int | None:
    """Extract trailing digit from item code: 'item2-3' → 3, 'item1-0' → 0."""
    if not isinstance(val, str):
        return None
    m = re.search(r"-(\d+)$", val)
    return int(m.group(1)) if m else None


def raw_to_str(val) -> str:
    """Serialize any JSON value to a compact string."""
    if isinstance(val, list):
        return ",".join(str(v) for v in val)
    return str(val) if val is not None else ""

# ── Collectors ─────────────────────────────────────────────────────────────

submissions: list[dict] = []
proj_details: list[dict] = []
answers: list[dict] = []
answer_items_rows: list[dict] = []

sub_id_counter = 0
ans_id_counter = 0
item_id_counter = 0


def next_sub_id() -> int:
    global sub_id_counter
    sub_id_counter += 1
    return sub_id_counter


def next_ans_id() -> int:
    global ans_id_counter
    ans_id_counter += 1
    return ans_id_counter


def next_item_id() -> int:
    global item_id_counter
    item_id_counter += 1
    return item_id_counter


# ── Detect language from filename ──────────────────────────────────────────

def detect_lang(name: str) -> str:
    n = name.lower()
    if any(s in n for s in ["-fr", "_fr", "fra", "french", "francais"]):
        return "fr"
    if any(s in n for s in ["-en", "_en", "eng", "english"]):
        return "en"
    if "bilingual" in n:
        return "bilingual"
    return ""


# ── JSON processor ─────────────────────────────────────────────────────────

def process_json(path: Path, dataset_id: str) -> None:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    data  = raw.get("data", {})
    trans = raw.get("translationsOnResult", {})
    lang  = detect_lang(path.name) or "bilingual"

    sid = next_sub_id()

    # -- form_submissions row --
    submissions.append({
        "id":             sid,
        "dataset_id":     dataset_id,
        "source_file":    path.name,
        "source_format":  "json",
        "language":       lang,
        "form_version":   raw.get("version", ""),
        "impact_level":   "",   # not directly in JSON; computed externally
        "current_score":  "",
        "raw_impact_score": "",
        "mitigation_score": "",
    })

    # -- project_details row --
    phase_val = data.get("projectDetailsPhase", "")
    proj_details.append({
        "submission_id":      sid,
        "respondent":         data.get("projectDetailsRespondent", ""),
        "job_title":          data.get("projectDetailsJob", ""),
        "department":         data.get("projectDetailsDepartment-NS", ""),
        "branch":             data.get("projectDetailsBranch", ""),
        "project_title_en":   data.get("projectDetailsTitle", ""),
        "project_title_fr":   trans.get("projectDetailsTitle", ""),
        "project_id_it_plan": data.get("projectDetailsID", ""),
        "program":            data.get("projectDetailsProgram", ""),
        "phase":              phase_val,
        "phase_score":        score_from_item(phase_val) if isinstance(phase_val, str) else "",
        "description_en":     data.get("projectDetailsDescription", ""),
        "description_fr":     trans.get("projectDetailsDescription", ""),
        "system_capabilities": raw_to_str(data.get("aboutSystem1", "")),
    })

    # -- form_answers: iterate through catalog --
    for q in questions:
        jk  = q["json_key"]
        qid = q["question_id"]
        if not jk or jk not in data:
            continue

        val = data[jk]
        is_list = isinstance(val, list)

        raw_str = raw_to_str(val)
        score   = score_from_item(val) if not is_list else None

        # For translations: check translationsOnResult
        text_fr = trans.get(jk, "")

        aid = next_ans_id()
        answers.append({
            "id":            aid,
            "submission_id": sid,
            "question_id":   qid,
            "answer_raw":    raw_str,
            "answer_score":  score if score is not None else "",
            "answer_text_en": raw_str if q["answer_type"] == "text" else "",
            "answer_text_fr": text_fr if q["answer_type"] == "text" else "",
            "is_list":       "true" if is_list else "false",
        })

        # Explode lists into answer_items
        if is_list:
            for order, item in enumerate(val):
                answer_items_rows.append({
                    "id":         next_item_id(),
                    "answer_id":  aid,
                    "item_code":  str(item),
                    "item_order": order,
                })


# ── PDF processor ──────────────────────────────────────────────────────────

_SCORE_PAT     = re.compile(r"Impact Level\s*[:\-–]\s*(\d+)", re.I)
_CURR_PAT      = re.compile(r"Current\s*Score\s*[:\-–]?\s*(\d+)", re.I)
_RAW_PAT       = re.compile(r"Raw\s*Impact\s*Score\s*[:\-–]?\s*(\d+)", re.I)
_MIT_PAT       = re.compile(r"Mitigation\s*Score\s*[:\-–]?\s*(\d+)", re.I)
_VER_PAT       = re.compile(r"Version\s*[:\-–]\s*([\d.]+)", re.I)

# Section 3 Q&A question+answer pattern
_QA_PAT = re.compile(
    r"^(\d+)\.\s+(.+?)(?=\n\d+\.\s|\nSection |\Z)",
    re.MULTILINE | re.DOTALL,
)

def process_pdf(path: Path, dataset_id: str) -> None:
    pages_text = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    pages_text.append(t)
    except Exception:
        return

    text = "\n".join(pages_text)
    lang = detect_lang(path.name)
    if not lang:
        lang = "en"

    def find(pat) -> str:
        m = pat.search(text)
        return m.group(1).strip() if m else ""

    sid = next_sub_id()

    submissions.append({
        "id":               sid,
        "dataset_id":       dataset_id,
        "source_file":      path.name,
        "source_format":    "pdf",
        "language":         lang,
        "form_version":     find(_VER_PAT),
        "impact_level":     find(_SCORE_PAT),
        "current_score":    find(_CURR_PAT),
        "raw_impact_score": find(_RAW_PAT),
        "mitigation_score": find(_MIT_PAT),
    })

    # Project details from PDF header
    def after_label(label: str) -> str:
        m = re.search(rf"{re.escape(label)}[^\n]*\n(.+?)(?=\n\d+\.|\Z)", text, re.I | re.DOTALL)
        return m.group(1).strip()[:500] if m else ""

    proj_details.append({
        "submission_id":      sid,
        "respondent":         after_label("Name of Respondent"),
        "job_title":          after_label("Job Title"),
        "department":         after_label("Department"),
        "branch":             after_label("Branch"),
        "project_title_en":   after_label("Project Title") if lang == "en" else "",
        "project_title_fr":   after_label("Project Title") if lang == "fr" else "",
        "project_id_it_plan": after_label("Project ID"),
        "program":            after_label("Departmental Program"),
        "phase":              "",
        "phase_score":        "",
        "description_en":     "",
        "description_fr":     "",
        "system_capabilities": "",
    })

    # Extract Section 3 Q&A into form_answers
    # Map PDF question number within each subsection to question_id
    # Build lookup: subsection → ordered list of question_ids that are non-text scored
    ia_scored = [q for q in questions if q["section_code"] == "IA" and q["answer_type"] in ("scored","boolean")]
    mq_scored = [q for q in questions if q["section_code"] == "MQ" and q["answer_type"] in ("scored","boolean")]

    # Find Section 3.1 and 3.2 blocks
    ia_match = re.search(r"Section 3\.1[:\s]+.+?\n(.+?)(?=Section 3\.2|Section 4|\Z)", text, re.DOTALL | re.I)
    mq_match = re.search(r"Section 3\.2[:\s]+.+?\n(.+?)(?=Section 4|\Z)", text, re.DOTALL | re.I)

    def extract_qa_block(block_text: str, q_list: list[dict]) -> None:
        """Parse numbered Q&A text and store as form_answers keyed by question_id."""
        # Match entries like "13. Question text\nAnswer text [ Points: +N ]"
        entries = re.findall(
            r"(\d+)\.\s+(.+?)(?=\n\d+\.\s|\Z)",
            block_text, re.DOTALL
        )
        for num_str, body in entries:
            num = int(num_str)
            # Find the question with this number in q_list
            matched = next((q for q in q_list if q["question_number"] == num), None)
            if not matched:
                continue
            body = body.strip()
            # Extract points if present
            pts_m = re.search(r"\[\s*Points:\s*\+?(-?\d+)\s*\]", body)
            score_val = int(pts_m.group(1)) if pts_m else None
            # Clean answer text
            answer_clean = re.sub(r"\[\s*Points:[^\]]+\]", "", body).strip()[:2000]

            aid = next_ans_id()
            row = {
                "id":            aid,
                "submission_id": sid,
                "question_id":   matched["question_id"],
                "answer_raw":    answer_clean,
                "answer_score":  score_val if score_val is not None else "",
                "is_list":       "false",
            }
            row["answer_text_en"] = answer_clean if lang == "en" else ""
            row["answer_text_fr"] = answer_clean if lang == "fr" else ""
            answers.append(row)

    if ia_match:
        extract_qa_block(ia_match.group(1), ia_scored)
    if mq_match:
        extract_qa_block(mq_match.group(1), mq_scored)


# ── Walk resources dir ─────────────────────────────────────────────────────

processed = {"json": 0, "pdf": 0, "skipped": 0}

for path in sorted(RESOURCES.rglob("*")):
    if not path.is_file():
        continue
    dataset_id = path.parent.name
    ext = path.suffix.lower()

    if ext == ".json":
        try:
            process_json(path, dataset_id)
            processed["json"] += 1
        except Exception as e:
            print(f"  WARN JSON {path.name}: {e}")

    elif ext == ".pdf":
        try:
            process_pdf(path, dataset_id)
            processed["pdf"] += 1
        except Exception as e:
            print(f"  WARN PDF {path.name}: {e}")

    else:
        processed["skipped"] += 1

print(f"Processed: {processed}")

# ── Write CSVs ─────────────────────────────────────────────────────────────

def write(name: str, fieldnames: list[str], rows: list[dict]) -> None:
    p = OUT / f"{name}.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {len(rows):>5} rows → {p.name}")


write("form_submissions", [
    "id","dataset_id","source_file","source_format","language",
    "form_version","impact_level","current_score","raw_impact_score","mitigation_score",
], submissions)

write("project_details", [
    "submission_id","respondent","job_title","department","branch",
    "project_title_en","project_title_fr","project_id_it_plan","program",
    "phase","phase_score","description_en","description_fr","system_capabilities",
], proj_details)

write("form_answers", [
    "id","submission_id","question_id","answer_raw",
    "answer_score","answer_text_en","answer_text_fr","is_list",
], answers)

write("answer_items", [
    "id","answer_id","item_code","item_order",
], answer_items_rows)

print("\nDone.")
