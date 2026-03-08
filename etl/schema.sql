-- ============================================================
-- AIA Bilingual Corpus – Relational Schema
-- Dialect: PostgreSQL (adapt types for SQLite/MySQL as needed)
-- ============================================================
--
-- Columns removed from source CSV (reason):
--   Automated translation fields    – always null
--   Spatial Representation Type     – always null
--   Maintainer                      – always null
--   Relationship Type               – always null
--   Data Includes URIs and Links    – always null
--   Spatial                         – always null
--   Time Period Coverage End        – always null
--   Topic category                  – always null
--   Name                            – duplicate of ID
--   Formats                         – duplicate of Format
--   Organization                    – same as Publisher org; replaced by FK
--
-- Constants (uniform across all 32 records, documented here):
--   collection_type     = 'Algorithmic Impact Assessment'
--   jurisdiction        = 'Federal'
--   licence             = 'Open Government Licence - Canada'
--   access_restrictions = 'unrestricted'
--   portal_type         = 'Open Information'
-- ============================================================


-- ------------------------------------------------------------
-- Lookup / reference tables
-- ------------------------------------------------------------

CREATE TABLE organizations (
    id   SERIAL      PRIMARY KEY,
    name TEXT        NOT NULL UNIQUE
);

CREATE TABLE subjects (
    id   SERIAL      PRIMARY KEY,
    name TEXT        NOT NULL UNIQUE
);

CREATE TABLE keywords (
    id   SERIAL      PRIMARY KEY,
    name TEXT        NOT NULL UNIQUE
);

CREATE TABLE resource_types (
    id   SERIAL      PRIMARY KEY,
    name TEXT        NOT NULL UNIQUE
);

CREATE TABLE languages (
    id   SERIAL      PRIMARY KEY,
    name TEXT        NOT NULL UNIQUE
);

CREATE TABLE formats (
    id   SERIAL      PRIMARY KEY,
    name TEXT        NOT NULL UNIQUE
);


-- ------------------------------------------------------------
-- Core entity: one row per AIA dataset
-- ------------------------------------------------------------

CREATE TABLE datasets (
    id                  UUID        PRIMARY KEY,   -- open.canada.ca dataset GUID
    title               TEXT        NOT NULL,
    organization_id     INT         REFERENCES organizations(id),
    publisher_section   TEXT,                      -- sub-unit within org
    update_frequency    TEXT,                      -- e.g. 'Continual', 'Not Planned'
    contact_email       TEXT,
    metadata_created    TIMESTAMPTZ,
    metadata_modified   TIMESTAMPTZ,
    homepage            TEXT,
    related_record_type TEXT,                      -- sparse; e.g. 'Open Information'
    time_period_start   DATE
);


-- ------------------------------------------------------------
-- Junction tables  (many-to-many)
-- ------------------------------------------------------------

CREATE TABLE dataset_subjects (
    dataset_id  UUID  NOT NULL REFERENCES datasets(id)  ON DELETE CASCADE,
    subject_id  INT   NOT NULL REFERENCES subjects(id)  ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, subject_id)
);

CREATE TABLE dataset_keywords (
    dataset_id  UUID  NOT NULL REFERENCES datasets(id)  ON DELETE CASCADE,
    keyword_id  INT   NOT NULL REFERENCES keywords(id)  ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, keyword_id)
);

CREATE TABLE dataset_resource_types (
    dataset_id       UUID  NOT NULL REFERENCES datasets(id)       ON DELETE CASCADE,
    resource_type_id INT   NOT NULL REFERENCES resource_types(id) ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, resource_type_id)
);

CREATE TABLE dataset_languages (
    dataset_id  UUID  NOT NULL REFERENCES datasets(id)  ON DELETE CASCADE,
    language_id INT   NOT NULL REFERENCES languages(id) ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, language_id)
);

CREATE TABLE dataset_formats (
    dataset_id UUID  NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    format_id  INT   NOT NULL REFERENCES formats(id)  ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, format_id)
);


-- ------------------------------------------------------------
-- Resources: individual downloadable files per dataset
-- ------------------------------------------------------------

CREATE TABLE resources (
    id          SERIAL  PRIMARY KEY,
    dataset_id  UUID    NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    url         TEXT    NOT NULL
);

CREATE INDEX idx_resources_dataset ON resources(dataset_id);


-- ============================================================
-- AIA Form Structure – Questions, Submissions & Answers
-- ============================================================

-- ------------------------------------------------------------
-- Question catalog: one row per AIA form question (103 total)
-- ------------------------------------------------------------

CREATE TABLE questions (
    question_id     TEXT        PRIMARY KEY,   -- e.g. PD-01, IA-13, MQ-09
    section_code    TEXT        NOT NULL,       -- PD | IA | MQ
    section_name    TEXT        NOT NULL,       -- human-readable section name
    subsection      TEXT        NOT NULL,       -- e.g. 'Risk Profile'
    question_number INT         NOT NULL,
    question_text   TEXT        NOT NULL,
    answer_type     TEXT        NOT NULL,       -- text | scored | boolean | multi | multi_scored
    json_key        TEXT,                       -- corresponding key in JSON data.*
    max_score       INT         DEFAULT 0,      -- max points this question can contribute
    scores_section  TEXT        NOT NULL        -- impact | mitigation | none
);

CREATE INDEX idx_questions_section ON questions(section_code, subsection);
CREATE INDEX idx_questions_json_key ON questions(json_key);


-- ------------------------------------------------------------
-- Form submissions: one row per downloaded form file
-- ------------------------------------------------------------

CREATE TABLE form_submissions (
    id                  SERIAL      PRIMARY KEY,
    dataset_id          UUID        NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    source_file         TEXT        NOT NULL,
    source_format       TEXT        NOT NULL,  -- json | pdf | html | csv | xlsx
    language            TEXT,                  -- en | fr | bilingual
    form_version        TEXT,                  -- e.g. 0.10.0
    -- Computed scores (populated from PDF; derived for JSON)
    impact_level        INT,
    current_score       INT,
    raw_impact_score    INT,
    mitigation_score    INT,
    UNIQUE (dataset_id, source_file)
);

CREATE INDEX idx_submissions_dataset ON form_submissions(dataset_id);


-- ============================================================
-- Section Tables  (one row per form_submission, one per section)
-- All share the same FK pattern: submission_id → form_submissions
-- Scored fields store the raw 0–4 integer from the item code.
-- Text fields carry both EN and FR where the JSON provides both.
-- ============================================================

-- ------------------------------------------------------------
-- 1. Project Details  (PD)
-- ------------------------------------------------------------
CREATE TABLE project_details (
    submission_id       INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    respondent          TEXT,
    job_title           TEXT,
    department          TEXT,
    branch              TEXT,
    project_title_en    TEXT,
    project_title_fr    TEXT,
    project_id_it_plan  TEXT,
    program             TEXT,
    phase               TEXT,                   -- e.g. Discovery | Design | Implementation
    phase_score         INT,                    -- 0–4
    description_en      TEXT,
    description_fr      TEXT,
    system_capabilities TEXT                    -- comma-separated selected capability codes
);

-- ------------------------------------------------------------
-- 2. Reasons for Automation  (IA – subsection 1)
-- ------------------------------------------------------------
CREATE TABLE reasons_for_automation (
    submission_id               INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    motivation_types            TEXT,           -- multi-select; comma-separated item codes
    motivation_other_en         TEXT,
    motivation_other_fr         TEXT,
    client_needs_en             TEXT,
    client_needs_fr             TEXT,
    public_benefits_en          TEXT,
    public_benefits_fr          TEXT,
    effectiveness_score         INT,            -- 0–4
    expected_improvements_en    TEXT,
    expected_improvements_fr    TEXT,
    system_confinement_en       TEXT,
    system_confinement_fr       TEXT,
    trade_offs_en               TEXT,
    trade_offs_fr               TEXT,
    alternatives_considered     INT,            -- 0 = No, >0 = Yes
    why_automation_preferred_en TEXT,
    why_automation_preferred_fr TEXT,
    no_deploy_consequence_types TEXT,           -- multi-select; comma-separated
    no_deploy_consequence_en    TEXT,
    no_deploy_consequence_fr    TEXT
);

-- ------------------------------------------------------------
-- 3. Risk Profile  (IA – subsection 2)
-- ------------------------------------------------------------
CREATE TABLE risk_profile (
    submission_id               INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    public_scrutiny_score       INT,            -- riskProfile1: 0–4
    vulnerable_clients_score    INT,            -- riskProfile2: 0–4
    high_stakes_score           INT,            -- riskProfile3: 0–4
    staff_impact_score          INT,            -- riskProfile4: 0–4
    disability_barriers_score   INT,            -- riskProfile5: 0–4
    risk_total                  INT             -- sum of the five scores above
);

-- ------------------------------------------------------------
-- 4. Project Authority  (IA – subsection 3)
-- ------------------------------------------------------------
CREATE TABLE project_authority (
    submission_id               INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    new_policy_authority_score  INT             -- projectAuthority1: 0 = No, >0 = Yes
);

-- ------------------------------------------------------------
-- 5. About the Algorithm  (IA – subsection 4)
-- ------------------------------------------------------------
CREATE TABLE about_the_algorithm (
    submission_id               INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    is_trade_secret_score       INT,            -- aboutAlgorithm1: 0 = No, >0 = Yes
    is_hard_to_explain_score    INT             -- aboutAlgorithm2: 0 = No, >0 = Yes
);

-- ------------------------------------------------------------
-- 6. About the Decision  (IA – subsection 5)
-- ------------------------------------------------------------
CREATE TABLE about_the_decision (
    submission_id               INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    decision_description_en     TEXT,           -- decisionSector2 + decisionSector3
    decision_description_fr     TEXT,
    decision_sectors            TEXT,           -- multi-select; comma-separated item codes
    automation_type_score       INT,            -- impact22: 0 = support, 2 = partial, 4 = full
    system_role_en              TEXT,           -- impact4
    system_role_fr              TEXT,
    requires_judgement_score    INT,            -- impact5: 0 = No, >0 = Yes
    evaluation_criteria_en      TEXT,           -- impact6
    evaluation_criteria_fr      TEXT,
    system_output_en            TEXT,           -- impact7
    system_output_fr            TEXT,
    superhuman_task_score       INT,            -- impact3: 0 = No, >0 = Yes
    used_by_different_org_score INT,            -- impact30: 0–4
    impacts_reversible_score    INT,            -- impact9: 0 = irreversible → 4 = easily reversible
    impact_duration_score       INT             -- impact8: 0 = long-term → 4 = brief
);

-- ------------------------------------------------------------
-- 7. Individual Impacts  (IA – subsection 6)
-- ------------------------------------------------------------
CREATE TABLE individual_impacts (
    submission_id               INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    rights_freedoms_score       INT,            -- impact11: 0–4
    rights_freedoms_en          TEXT,           -- impact12
    rights_freedoms_fr          TEXT,
    equality_dignity_score      INT,            -- impact13: 0–4
    equality_dignity_en         TEXT,           -- impact14
    equality_dignity_fr         TEXT,
    health_wellbeing_score      INT,            -- impact15: 0–4
    health_wellbeing_en         TEXT,           -- impact16
    health_wellbeing_fr         TEXT,
    economic_interests_score    INT,            -- impact24: 0–4
    economic_interests_en       TEXT,           -- impact25
    economic_interests_fr       TEXT
);

-- ------------------------------------------------------------
-- 8. About the Data  (IA – subsection 7)
-- ------------------------------------------------------------
CREATE TABLE about_the_data (
    submission_id                   INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    uses_personal_info              INT,        -- aboutDataSource1: 0 = No, >0 = Yes
    pib_bank_numbers                TEXT,       -- aboutDataSource12
    security_classification_score   INT,        -- aboutDataSource6: 0=unclassified → 4=Top Secret
    data_controller_score           INT,        -- aboutDataSource7: who controls data
    multiple_sources                INT,        -- aboutDataSource2: 0 = No, >0 = Yes
    internet_connected_input        INT,        -- aboutDataSource3: 0 = No, >0 = Yes
    interfaces_other_systems        INT,        -- aboutDataSource4: 0 = No, >0 = Yes
    training_data_collector_score   INT,        -- aboutDataSource8: who collected training data
    input_data_collector_score      INT,        -- aboutDataSource9: who collected input data
    data_description_en             TEXT,       -- aboutDataSource13
    data_description_fr             TEXT,
    uses_unstructured_data          INT,        -- aboutDataSource5: 0 = No, >0 = Yes
    unstructured_data_types         TEXT        -- aboutDataType2: multi-select
);

-- ------------------------------------------------------------
-- 9. Consultation  (MQ – subsection 1)
-- ------------------------------------------------------------
CREATE TABLE consultation (
    submission_id                   INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    internal_stakeholders_engaged   INT,        -- consultationImplementation1: 0/1
    internal_stakeholders_list      TEXT,       -- consultationImplementation2: multi-select
    internal_stakeholders_other_en  TEXT,       -- consultationImplementation2-other
    internal_stakeholders_other_fr  TEXT,
    external_stakeholders_engaged   INT,        -- consultationImplementation3: 0/1
    external_stakeholders_list      TEXT,       -- consultationImplementation4: multi-select
    external_stakeholders_other_en  TEXT,       -- consultationImplementation4-other
    external_stakeholders_other_fr  TEXT
);

-- ------------------------------------------------------------
-- 10. Data Quality & Bias  (MQ – subsection 2)
-- ------------------------------------------------------------
CREATE TABLE data_quality_bias (
    submission_id                   INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    bias_testing_documented         INT,        -- dataQualityImplementation1: 0/1
    bias_testing_public             INT,        -- dataQualityImplementation2: 0/1
    data_quality_process_documented INT,        -- dataQualityImplementation3: 0/1
    data_quality_process_public     INT,        -- dataQualityImplementation4: 0/1
    gba_plus_conducted              INT,        -- dataQualityImplementation5: 0/1
    gba_plus_public                 INT,        -- dataQualityImplementation6: 0/1
    accountability_assigned         INT,        -- dataQualityImplementation7: 0/1
    outdated_data_process           INT,        -- dataQualityImplementation8: 0/1
    outdated_data_process_public    INT,        -- dataQualityImplementation9: 0/1
    data_on_open_gov_portal         INT         -- dataQualityImplementation10: 0/1
);

-- ------------------------------------------------------------
-- 11. Fairness  (MQ – subsection 3)
-- ------------------------------------------------------------
CREATE TABLE fairness (
    submission_id                   INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    audit_identifies_authority      INT,        -- fairnessImplementation1: 0/1
    audit_records_all_decisions     INT,        -- fairnessImplementation2: 0/1
    audit_key_decision_points       INT,        -- fairnessImplementation3: 0/1
    decision_points_linked_law      INT,        -- fairnessImplementation4: 0/1
    change_log_maintained           INT,        -- fairnessImplementation5: 0/1
    audit_all_system_decisions      INT,        -- fairnessImplementation6: 0/1
    audit_generates_notification    INT,        -- fairnessImplementation7: 0/1
    audit_identifies_version        INT,        -- fairnessImplementation8: 0/1
    audit_shows_decision_maker      INT,        -- fairnessImplementation9: 0/1
    can_produce_reasons             INT,        -- fairnessImplementation10: 0/1
    access_permission_process       INT,        -- fairnessImplementation11: 0/1
    user_feedback_mechanism         INT,        -- fairnessImplementation12: 0/1
    client_recourse_process         INT,        -- fairnessImplementation13: 0/1
    human_override_enabled          INT,        -- fairnessImplementation14: 0/1
    override_log_process            INT,        -- fairnessImplementation15: 0/1
    audit_records_changes           INT,        -- fairnessImplementation16: 0/1
    gc_earb_reviewed                INT         -- fairnessImplementation17: 0/1
);

-- ------------------------------------------------------------
-- 12. Privacy & Security  (MQ – subsection 4)
-- ------------------------------------------------------------
CREATE TABLE privacy_security (
    submission_id               INT     PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    pia_conducted               INT,            -- privacyImplementation1: 0/1
    pia_description_en          TEXT,           -- privacyImplementation5
    pia_description_fr          TEXT,
    privacy_by_design           INT,            -- privacyImplementation2: 0/1
    closed_system               INT,            -- privacyImplementation3: 0/1
    data_sharing_agreement      INT,            -- privacyImplementation4: 0/1
    de_identification_applied   INT,            -- privacyImplementation7: 0/1
    de_identification_method_en TEXT,           -- privacyImplementation8
    de_identification_method_fr TEXT
);


-- ------------------------------------------------------------
-- Useful views
-- ------------------------------------------------------------

-- Flat view matching the original denormalised format
CREATE VIEW v_datasets_flat AS
SELECT
    d.id,
    d.title,
    o.name                                          AS organization,
    d.publisher_section,
    d.update_frequency,
    d.contact_email,
    d.metadata_created,
    d.metadata_modified,
    d.homepage,
    d.related_record_type,
    d.time_period_start,
    string_agg(DISTINCT s.name,  ', ' ORDER BY s.name)  AS subjects,
    string_agg(DISTINCT k.name,  ', ' ORDER BY k.name)  AS keywords,
    string_agg(DISTINCT rt.name, ', ' ORDER BY rt.name) AS resource_types,
    string_agg(DISTINCT l.name,  ', ' ORDER BY l.name)  AS languages,
    string_agg(DISTINCT f.name,  ', ' ORDER BY f.name)  AS formats
FROM datasets d
LEFT JOIN organizations          o  ON o.id  = d.organization_id
LEFT JOIN dataset_subjects       ds ON ds.dataset_id = d.id
LEFT JOIN subjects               s  ON s.id  = ds.subject_id
LEFT JOIN dataset_keywords       dk ON dk.dataset_id = d.id
LEFT JOIN keywords               k  ON k.id  = dk.keyword_id
LEFT JOIN dataset_resource_types dr ON dr.dataset_id = d.id
LEFT JOIN resource_types         rt ON rt.id = dr.resource_type_id
LEFT JOIN dataset_languages      dl ON dl.dataset_id = d.id
LEFT JOIN languages              l  ON l.id  = dl.language_id
LEFT JOIN dataset_formats        df ON df.dataset_id = d.id
LEFT JOIN formats                f  ON f.id  = df.format_id
GROUP BY d.id, o.name;
