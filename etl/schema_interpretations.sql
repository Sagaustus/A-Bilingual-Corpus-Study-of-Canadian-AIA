-- ============================================================
-- Semantic Interpretation & Derived Tables
-- LLM-generated analysis of AIA form responses
-- Dialect: PostgreSQL
-- ============================================================
--
-- These tables store structured interpretations produced by
-- sending respondent answers to an LLM (Llama 3.3 70B via IONOS).
-- Each row links back to form_submissions via submission_id.
-- All tables store the raw LLM response, model ID, and prompt
-- version for reproducibility and audit.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Automation Justification Analysis
--    Sources: project_details, reasons_for_automation, about_the_decision
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS interp_automation_justification (
    submission_id        INT         PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    justification_theme  TEXT        NOT NULL,
    strength_score       INT         CHECK (strength_score BETWEEN 1 AND 5),
    public_benefit_clarity TEXT      NOT NULL,
    trade_off_adequacy   TEXT        NOT NULL,
    confinement_assessment TEXT      NOT NULL,
    raw_llm_response     JSONB      NOT NULL,
    model_id             TEXT        NOT NULL,
    prompt_version       TEXT        NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ------------------------------------------------------------
-- 2. Risk & Rights Impact Interpretation
--    Sources: risk_profile, individual_impacts, about_the_decision
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS interp_risk_rights_impact (
    submission_id            INT         PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    risk_level_label         TEXT        NOT NULL,
    dominant_risk_dimension  TEXT        NOT NULL,
    rights_concern_summary   TEXT        NOT NULL,
    proportionality_assessment TEXT      NOT NULL,
    reversibility_concern    TEXT,
    raw_llm_response         JSONB      NOT NULL,
    model_id                 TEXT        NOT NULL,
    prompt_version           TEXT        NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ------------------------------------------------------------
-- 3. Bilingual Divergence Analysis
--    Sources: all section tables with _en/_fr field pairs
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS interp_bilingual_divergence (
    submission_id            INT         PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    has_divergence           BOOLEAN     NOT NULL,
    divergence_count         INT         NOT NULL DEFAULT 0,
    divergent_fields         JSONB       NOT NULL,
    overall_divergence_type  TEXT,
    semantic_fidelity_score  INT         CHECK (semantic_fidelity_score BETWEEN 0 AND 5),
    untranslatable_concepts  JSONB,
    raw_llm_response         JSONB       NOT NULL,
    model_id                 TEXT        NOT NULL,
    prompt_version           TEXT        NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ------------------------------------------------------------
-- 4. Safeguard Compliance Assessment
--    Sources: consultation, data_quality_bias, fairness, privacy_security
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS interp_safeguard_compliance (
    submission_id              INT         PRIMARY KEY REFERENCES form_submissions(id) ON DELETE CASCADE,
    overall_compliance_label   TEXT        NOT NULL,
    overall_compliance_score   INT         CHECK (overall_compliance_score BETWEEN 1 AND 5),
    consultation_assessment    TEXT        NOT NULL,
    bias_mitigation_assessment TEXT        NOT NULL,
    fairness_assessment        TEXT        NOT NULL,
    privacy_assessment         TEXT        NOT NULL,
    gaps_identified            JSONB       NOT NULL,
    raw_llm_response           JSONB       NOT NULL,
    model_id                   TEXT        NOT NULL,
    prompt_version             TEXT        NOT NULL,
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ------------------------------------------------------------
-- 5. Cross-Submission Thematic Patterns
--    Run after all per-submission interpretations are complete
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS interp_thematic_patterns (
    id                SERIAL      PRIMARY KEY,
    pattern_type      TEXT        NOT NULL,
    theme_label       TEXT        NOT NULL,
    theme_description TEXT        NOT NULL,
    submission_ids    INT[]       NOT NULL,
    prevalence        NUMERIC(4,2) NOT NULL,
    notable_outliers  JSONB,
    raw_llm_response  JSONB       NOT NULL,
    model_id          TEXT        NOT NULL,
    prompt_version    TEXT        NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (pattern_type, theme_label, prompt_version)
);


-- ------------------------------------------------------------
-- Run log for tracking ETL execution
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS interp_run_log (
    id                    SERIAL      PRIMARY KEY,
    run_started_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    run_finished_at       TIMESTAMPTZ,
    analysis_type         TEXT        NOT NULL,
    submissions_processed INT        NOT NULL DEFAULT 0,
    submissions_skipped   INT        NOT NULL DEFAULT 0,
    errors                INT        NOT NULL DEFAULT 0,
    model_id              TEXT        NOT NULL,
    prompt_version        TEXT        NOT NULL,
    notes                 TEXT
);
