"""
Builds etl/output/questions.csv — the canonical AIA question catalog.

Each row defines one question/field from the AIA form, mapping:
  - a stable question_id  (e.g. PD-01, IA-13, MQ-09)
  - the JSON data.* key   (e.g. riskProfile1, fairnessImplementation9)
  - section, subsection, question text, answer type, max_score
"""

import csv
from pathlib import Path

OUT = Path(__file__).parent / "output" / "questions.csv"

# answer_type values:
#   text        – free text, no score
#   scored      – single item code  "itemR-S" → score = S
#   multi       – list of item codes (not scored individually)
#   multi_scored– list of item codes each contributing a score (rare)
#   boolean     – Yes/No coded as scored (score 0 or >0)

QUESTIONS = [
    # ── Project Details (PD) ────────────────────────────────────────────────
    # section_code, section_name, subsection, q_num, question_text, answer_type, json_key, max_score, scores_section
    ("PD", "Project Details", "Admin",          1,  "Name of Respondent",                                              "text",    "projectDetailsRespondent",     0,  "none"),
    ("PD", "Project Details", "Admin",          2,  "Job Title",                                                       "text",    "projectDetailsJob",            0,  "none"),
    ("PD", "Project Details", "Admin",          3,  "Department",                                                      "text",    "projectDetailsDepartment-NS",  0,  "none"),
    ("PD", "Project Details", "Admin",          4,  "Branch",                                                          "text",    "projectDetailsBranch",         0,  "none"),
    ("PD", "Project Details", "Admin",          5,  "Project Title",                                                   "text",    "projectDetailsTitle",          0,  "none"),
    ("PD", "Project Details", "Admin",          6,  "Project ID from IT Plan",                                         "text",    "projectDetailsID",             0,  "none"),
    ("PD", "Project Details", "Admin",          7,  "Departmental Program",                                            "text",    "projectDetailsProgram",        0,  "none"),
    ("PD", "Project Details", "Admin",          8,  "Project Phase",                                                   "scored",  "projectDetailsPhase",          4,  "none"),
    ("PD", "Project Details", "Admin",          9,  "Project Description",                                             "text",    "projectDetailsDescription",    0,  "none"),
    ("PD", "Project Details", "System",        10,  "System capabilities (check all that apply)",                      "multi",   "aboutSystem1",                 0,  "none"),

    # ── Section 3.1 – Impact Questions (IA) ────────────────────────────────
    # Reasons for Automation
    ("IA", "Impact Assessment", "Reasons for Automation",  1,  "What is motivating your team to introduce automation? (multi-select)",          "multi",   "businessDrivers1",  0,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation",  2,  "Motivation – other (describe)",                                                   "text",    "motivation-other",  0,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation",  3,  "What client needs will the system address and how will it meet them?",            "text",    "businessDrivers3",  0,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation",  4,  "Describe any public benefits the system is expected to have",                     "text",    "businessDrivers4",  0,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation",  5,  "How effective will the system likely be in meeting client needs?",                "scored",  "businessDrivers5",  4,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation",  6,  "Describe improvements, benefits, or advantages expected from automation",         "text",    "businessDrivers6",  0,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation",  7,  "Describe how you will ensure the system is confined to identified client needs",  "text",    "businessDrivers7",  0,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation",  8,  "Describe trade-offs between client interests and program objectives considered",  "text",    "businessDrivers8",  0,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation",  9,  "Have alternative non-automated processes been considered?",                       "boolean", "businessDrivers9",  4,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation", 10,  "If considered, why was automation identified as the preferred option?",           "text",    "businessDrivers10", 0,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation", 11,  "What would be the consequence of not deploying the system? (multi-select)",       "multi",   "businessDrivers11", 0,  "impact"),
    ("IA", "Impact Assessment", "Reasons for Automation", 12,  "Consequence of not deploying – describe",                                         "text",    "businessDrivers12", 0,  "impact"),

    # Risk Profile
    ("IA", "Impact Assessment", "Risk Profile",  13, "Is the project under intense public scrutiny and/or frequent litigation?",            "scored", "riskProfile1", 4, "impact"),
    ("IA", "Impact Assessment", "Risk Profile",  14, "Are clients in this line of business particularly vulnerable?",                       "scored", "riskProfile2", 4, "impact"),
    ("IA", "Impact Assessment", "Risk Profile",  15, "Are the stakes of the decisions very high?",                                          "scored", "riskProfile3", 4, "impact"),
    ("IA", "Impact Assessment", "Risk Profile",  16, "Will this project have major impacts on staff in terms of numbers or roles?",         "scored", "riskProfile4", 4, "impact"),
    ("IA", "Impact Assessment", "Risk Profile",  17, "Will use of the system create or exacerbate barriers for persons with disabilities?", "scored", "riskProfile5", 4, "impact"),

    # Project Authority
    ("IA", "Impact Assessment", "Project Authority", 18, "Will you require new policy authority for this project?", "boolean", "projectAuthority1", 4, "impact"),

    # About the Algorithm
    ("IA", "Impact Assessment", "About the Algorithm", 19, "The algorithm used will be a (trade) secret",                      "boolean", "aboutAlgorithm1", 4, "impact"),
    ("IA", "Impact Assessment", "About the Algorithm", 20, "The algorithmic process will be difficult to interpret or explain", "boolean", "aboutAlgorithm2", 4, "impact"),

    # About the Decision
    ("IA", "Impact Assessment", "About the Decision", 21, "Describe the decision(s) that will be automated",                                 "text",    "decisionSector2",  0, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 22, "Describe additional decision detail",                                              "text",    "decisionSector3",  0, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 23, "What sector does the decision fall under? (multi-select, scored)",                 "multi",   "decisionSector1",  0, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 24, "Which best describes the type of automation planned?",                            "scored",  "impact22",         4, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 25, "Describe the role of the system in the decision-making process",                  "text",    "impact4",          0, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 26, "Will the system make assessments requiring judgement or discretion?",             "boolean", "impact5",          4, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 27, "Describe the criteria used to evaluate client data",                              "text",    "impact6",          0, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 28, "Describe the system output and how to interpret it",                              "text",    "impact7",          0, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 29, "Will the system perform operations a human could not complete in reasonable time?","boolean", "impact3",          4, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 30, "Is the system used by a different part of the org than who developed it?",        "scored",  "impact30",         4, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 31, "Are the impacts resulting from the decision reversible?",                         "scored",  "impact9",          4, "impact"),
    ("IA", "Impact Assessment", "About the Decision", 32, "How long will impacts from the decision last?",                                   "scored",  "impact8",          4, "impact"),

    # Impact on individuals
    ("IA", "Impact Assessment", "Individual Impacts", 33, "Impacts on rights or freedoms of individuals",                    "scored", "impact11", 4, "impact"),
    ("IA", "Impact Assessment", "Individual Impacts", 34, "Describe – rights or freedoms",                                   "text",   "impact12", 0, "impact"),
    ("IA", "Impact Assessment", "Individual Impacts", 35, "Impacts on equality, dignity, privacy, and autonomy",             "scored", "impact13", 4, "impact"),
    ("IA", "Impact Assessment", "Individual Impacts", 36, "Describe – equality, dignity, privacy, autonomy",                 "text",   "impact14", 0, "impact"),
    ("IA", "Impact Assessment", "Individual Impacts", 37, "Impacts on health and well-being",                                "scored", "impact15", 4, "impact"),
    ("IA", "Impact Assessment", "Individual Impacts", 38, "Describe – health and well-being",                               "text",   "impact16", 0, "impact"),
    ("IA", "Impact Assessment", "Individual Impacts", 39, "Impacts on economic interests",                                   "scored", "impact24", 4, "impact"),
    ("IA", "Impact Assessment", "Individual Impacts", 40, "Describe – economic interests",                                   "text",   "impact25", 0, "impact"),

    # About the Data
    ("IA", "Impact Assessment", "About the Data", 41, "Will the system use personal information as input data?",                     "boolean", "aboutDataSource1",  4, "impact"),
    ("IA", "Impact Assessment", "About the Data", 42, "List relevant PIB Bank Numbers",                                              "text",    "aboutDataSource12", 0, "impact"),
    ("IA", "Impact Assessment", "About the Data", 43, "Highest security classification of input data",                              "scored",  "aboutDataSource6",  4, "impact"),
    ("IA", "Impact Assessment", "About the Data", 44, "Who controls the data?",                                                      "scored",  "aboutDataSource7",  4, "impact"),
    ("IA", "Impact Assessment", "About the Data", 45, "Will the system use data from multiple different sources?",                   "boolean", "aboutDataSource2",  4, "impact"),
    ("IA", "Impact Assessment", "About the Data", 46, "Will the system require input from an internet- or telephony-connected device?","boolean","aboutDataSource3", 4, "impact"),
    ("IA", "Impact Assessment", "About the Data", 47, "Will the system interface with other IT systems?",                            "boolean", "aboutDataSource4",  4, "impact"),
    ("IA", "Impact Assessment", "About the Data", 48, "Who collected the training data?",                                            "scored",  "aboutDataSource8",  4, "impact"),
    ("IA", "Impact Assessment", "About the Data", 49, "Who collected the input data?",                                               "scored",  "aboutDataSource9",  4, "impact"),
    ("IA", "Impact Assessment", "About the Data", 50, "Describe input data, its source and method of collection",                    "text",    "aboutDataSource13", 0, "impact"),
    ("IA", "Impact Assessment", "About the Data", 51, "Will the system require analysis of unstructured data?",                      "boolean", "aboutDataSource5",  4, "impact"),
    ("IA", "Impact Assessment", "About the Data", 52, "What types of unstructured data? (multi-select)",                             "multi",   "aboutDataType2",    0, "impact"),
    ("IA", "Impact Assessment", "About the Data", 53, "Data type – other (describe)",                                                "text",    "aboutDataSource11", 0, "impact"),

    # ── Section 3.2 – Mitigation Questions (MQ) ────────────────────────────
    # Consultation
    ("MQ", "Mitigation Questions", "Consultation",  1,  "Have you engaged internal stakeholders?",                                        "boolean", "consultationImplementation1",       1, "mitigation"),
    ("MQ", "Mitigation Questions", "Consultation",  2,  "Which internal stakeholders have you engaged?",                                  "multi",   "consultationImplementation2",       0, "mitigation"),
    ("MQ", "Mitigation Questions", "Consultation",  3,  "Internal stakeholders – other (describe)",                                       "text",    "consultationImplementation2-other", 0, "mitigation"),
    ("MQ", "Mitigation Questions", "Consultation",  4,  "Have you engaged external stakeholders?",                                        "boolean", "consultationImplementation3",       1, "mitigation"),
    ("MQ", "Mitigation Questions", "Consultation",  5,  "Which external stakeholders have you engaged?",                                  "multi",   "consultationImplementation4",       0, "mitigation"),
    ("MQ", "Mitigation Questions", "Consultation",  6,  "External stakeholders – other (describe)",                                       "text",    "consultationImplementation4-other", 0, "mitigation"),

    # Data Quality & Bias
    ("MQ", "Mitigation Questions", "Data Quality & Bias",  7,  "Documented processes to test datasets for bias and unexpected outcomes?",   "boolean", "dataQualityImplementation1",  2, "mitigation"),
    ("MQ", "Mitigation Questions", "Data Quality & Bias",  8,  "Is that information publicly available?",                                  "boolean", "dataQualityImplementation2",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Data Quality & Bias",  9,  "Process to document how data quality issues were resolved during design?",  "boolean", "dataQualityImplementation3",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Data Quality & Bias", 10,  "Is that information publicly available?",                                  "boolean", "dataQualityImplementation4",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Data Quality & Bias", 11,  "Have you undertaken a Gender-Based Analysis Plus of the data?",            "boolean", "dataQualityImplementation5",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Data Quality & Bias", 12,  "Is that information publicly available?",                                  "boolean", "dataQualityImplementation6",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Data Quality & Bias", 13,  "Have you assigned institutional accountability for the system?",           "boolean", "dataQualityImplementation7",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Data Quality & Bias", 14,  "Documented process to manage outdated or unreliable data?",                "boolean", "dataQualityImplementation8",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Data Quality & Bias", 15,  "Is that information publicly available?",                                  "boolean", "dataQualityImplementation9",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Data Quality & Bias", 16,  "Is the data used for this system posted on the Open Government Portal?",   "boolean", "dataQualityImplementation10", 1, "mitigation"),

    # Fairness / Bias Checks
    ("MQ", "Mitigation Questions", "Fairness",  17, "Does the audit trail identify the legislative authority?",                         "boolean", "fairnessImplementation1",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  18, "Does the system provide an audit trail of all recommendations/decisions?",         "boolean", "fairnessImplementation2",  2, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  19, "Are all key decision points identifiable in the audit trail?",                     "boolean", "fairnessImplementation3",  2, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  20, "Are decision points linked to relevant legislation, policy, or procedures?",       "boolean", "fairnessImplementation4",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  21, "Do you maintain a change log for all model/system modifications?",                 "boolean", "fairnessImplementation5",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  22, "Does the audit trail record all decision points made by the system?",              "boolean", "fairnessImplementation6",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  23, "Can the audit trail generate a decision notification to clients?",                 "boolean", "fairnessImplementation7",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  24, "Does the audit trail identify which system version was used per decision?",        "boolean", "fairnessImplementation8",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  25, "Does the audit trail show who the authorized decision-maker is?",                  "boolean", "fairnessImplementation9",  1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  26, "Can the system produce reasons for its decisions when required?",                  "boolean", "fairnessImplementation10", 2, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  27, "Is there a process to grant, monitor, and revoke access permissions?",             "boolean", "fairnessImplementation11", 1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  28, "Is there a mechanism to capture feedback from users of the system?",               "boolean", "fairnessImplementation12", 1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  29, "Is there a recourse process for clients wishing to challenge the decision?",       "boolean", "fairnessImplementation13", 2, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  30, "Does the system enable human override of system decisions?",                       "boolean", "fairnessImplementation14", 2, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  31, "Is there a process to log instances when overrides were performed?",               "boolean", "fairnessImplementation15", 1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  32, "Does the audit trail record changes to system operation or performance?",          "boolean", "fairnessImplementation16", 1, "mitigation"),
    ("MQ", "Mitigation Questions", "Fairness",  33, "Has the system been reviewed by the GC Enterprise Architecture Review Board?",     "boolean", "fairnessImplementation17", 1, "mitigation"),

    # Privacy & Security
    ("MQ", "Mitigation Questions", "Privacy & Security",  34, "Has a Privacy Impact Assessment been undertaken or updated?",                            "boolean", "privacyImplementation1", 2, "mitigation"),
    ("MQ", "Mitigation Questions", "Privacy & Security",  35, "PIA title, scope, and how the automation project is covered (describe)",                  "text",    "privacyImplementation5", 0, "mitigation"),
    ("MQ", "Mitigation Questions", "Privacy & Security",  36, "Has security and privacy been designed in from the concept stage?",                       "boolean", "privacyImplementation2", 1, "mitigation"),
    ("MQ", "Mitigation Questions", "Privacy & Security",  37, "Is information used within a closed system (no internet/intranet connections)?",          "boolean", "privacyImplementation3", 1, "mitigation"),
    ("MQ", "Mitigation Questions", "Privacy & Security",  38, "If personal information is shared, is there a data-sharing agreement with safeguards?",   "boolean", "privacyImplementation4", 1, "mitigation"),
    ("MQ", "Mitigation Questions", "Privacy & Security",  39, "Will personal information be de-identified at any point in the lifecycle?",               "boolean", "privacyImplementation7", 1, "mitigation"),
    ("MQ", "Mitigation Questions", "Privacy & Security",  40, "Describe the de-identification method(s)",                                                 "text",    "privacyImplementation8", 0, "mitigation"),
]

FIELDNAMES = [
    "question_id", "section_code", "section_name", "subsection",
    "question_number", "question_text", "answer_type",
    "json_key", "max_score", "scores_section",
]

rows = []
for (sc, sn, sub, num, qt, at, jk, ms, ss) in QUESTIONS:
    qid = f"{sc}-{num:02d}"
    rows.append({
        "question_id":     qid,
        "section_code":    sc,
        "section_name":    sn,
        "subsection":      sub,
        "question_number": num,
        "question_text":   qt,
        "answer_type":     at,
        "json_key":        jk,
        "max_score":       ms,
        "scores_section":  ss,
    })

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDNAMES)
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} questions → {OUT}")
sections = {}
for r in rows:
    key = (r["section_code"], r["subsection"])
    sections.setdefault(key, 0)
    sections[key] += 1
print()
for (sc, sub), count in sections.items():
    print(f"  [{sc}] {sub}: {count} questions")
