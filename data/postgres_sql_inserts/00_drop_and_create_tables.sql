-- ============================================================================
-- DROP AND CREATE ALL TABLES FOR AIA GOVERNANCE DATABASE
-- ============================================================================
-- This script:
--   1. Drops existing tables (in reverse FK order)
--   2. Creates fresh tables matching the CSV schema exactly
--   3. Adds indexes for performance
--
-- Run this FIRST before loading INSERT statements
-- ============================================================================

-- ============================================================================
-- STEP 1: DROP EXISTING TABLES (reverse order due to foreign keys)
-- ============================================================================

DROP TABLE IF EXISTS mitigations CASCADE;
DROP TABLE IF EXISTS key_findings CASCADE;
DROP TABLE IF EXISTS risk_areas CASCADE;
DROP TABLE IF EXISTS stakeholders CASCADE;
DROP TABLE IF EXISTS governance CASCADE;
DROP TABLE IF EXISTS systems CASCADE;
DROP TABLE IF EXISTS projects CASCADE;

-- ============================================================================
-- STEP 2: CREATE TABLES (matches CSV schema exactly)
-- ============================================================================

-- TABLE: projects
-- Master table - one row per PDF document
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    pdf_filename TEXT NOT NULL,
    project_title TEXT,
    department TEXT,
    branch TEXT,
    project_phase TEXT,
    program TEXT,
    annual_decisions TEXT,
    language VARCHAR(2) CHECK (language IN ('en', 'fr')),
    created_at TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_projects_language ON projects(language);
CREATE INDEX idx_projects_department ON projects(department);
CREATE INDEX idx_projects_title ON projects(project_title);
CREATE INDEX idx_projects_pdf_filename ON projects(pdf_filename);

COMMENT ON TABLE projects IS 'Master table containing one record per AIA PDF document';
COMMENT ON COLUMN projects.project_id IS 'Unique identifier from CSV (matches across related tables)';
COMMENT ON COLUMN projects.language IS 'Document language: en (English) or fr (French)';

-- ============================================================================

-- TABLE: systems
-- AI system descriptions and technical details
CREATE TABLE systems (
    system_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    system_purpose TEXT,
    system_description TEXT,
    data_inputs TEXT,
    decision_outputs TEXT,
    affected_population TEXT
);

CREATE INDEX idx_systems_project_id ON systems(project_id);

COMMENT ON TABLE systems IS 'Technical descriptions of AI/automated systems';
COMMENT ON COLUMN systems.system_description IS 'How the AI system works';
COMMENT ON COLUMN systems.data_inputs IS 'What data the system processes';
COMMENT ON COLUMN systems.decision_outputs IS 'What decisions/outputs the system produces';

-- ============================================================================

-- TABLE: governance
-- Oversight, accountability, and transparency mechanisms
CREATE TABLE governance (
    governance_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    oversight_mechanism TEXT,
    appeal_process TEXT,
    transparency_measures TEXT,
    accountability_framework TEXT,
    external_audit TEXT
);

CREATE INDEX idx_governance_project_id ON governance(project_id);

COMMENT ON TABLE governance IS 'Governance mechanisms for AI systems (key for divergence analysis)';
COMMENT ON COLUMN governance.oversight_mechanism IS 'How the system is monitored/supervised';
COMMENT ON COLUMN governance.appeal_process IS 'How decisions can be challenged';
COMMENT ON COLUMN governance.accountability_framework IS 'Who is responsible for system outcomes';

-- ============================================================================

-- TABLE: stakeholders
-- Contact information for AIA respondents
CREATE TABLE stakeholders (
    stakeholder_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    respondent_name TEXT,
    respondent_title TEXT,
    respondent_email TEXT
);

CREATE INDEX idx_stakeholders_project_id ON stakeholders(project_id);

COMMENT ON TABLE stakeholders IS 'Contact information for AIA document respondents';

-- ============================================================================

-- TABLE: risk_areas
-- Identified risks and concerns
CREATE TABLE risk_areas (
    risk_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    risk_area TEXT,
    risk_description TEXT,
    severity TEXT,
    affected_groups TEXT
);

CREATE INDEX idx_risk_areas_project_id ON risk_areas(project_id);

COMMENT ON TABLE risk_areas IS 'Identified risks associated with AI systems';
COMMENT ON COLUMN risk_areas.severity IS 'Risk severity level';
COMMENT ON COLUMN risk_areas.affected_groups IS 'Populations impacted by the risk';

-- ============================================================================

-- TABLE: key_findings
-- Summary findings from impact assessments
CREATE TABLE key_findings (
    finding_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    biases_identified TEXT,
    fairness_issues TEXT,
    transparency_gaps TEXT,
    accountability_gaps TEXT
);

CREATE INDEX idx_key_findings_project_id ON key_findings(project_id);

COMMENT ON TABLE key_findings IS 'Summary findings from algorithmic impact assessments';
COMMENT ON COLUMN key_findings.biases_identified IS 'Algorithmic biases detected';
COMMENT ON COLUMN key_findings.fairness_issues IS 'Fairness concerns identified';

-- ============================================================================

-- TABLE: mitigations
-- Risk mitigation strategies
-- NOTE: This table has TWO foreign keys (project_id AND risk_id)
CREATE TABLE mitigations (
    mitigation_id INTEGER PRIMARY KEY,
    risk_id INTEGER REFERENCES risk_areas(risk_id) ON DELETE CASCADE,
    project_id INTEGER NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    mitigation_strategy TEXT,
    implementation_status TEXT
);

CREATE INDEX idx_mitigations_project_id ON mitigations(project_id);
CREATE INDEX idx_mitigations_risk_id ON mitigations(risk_id);

COMMENT ON TABLE mitigations IS 'Strategies to mitigate identified risks';
COMMENT ON COLUMN mitigations.risk_id IS 'Links to specific risk being mitigated (can be NULL)';
COMMENT ON COLUMN mitigations.implementation_status IS 'Current status of mitigation implementation';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- List all created tables
SELECT 
    table_name,
    (SELECT COUNT(*) 
     FROM information_schema.columns 
     WHERE table_name = t.table_name 
       AND table_schema = 'public') as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY 
    CASE table_name
        WHEN 'projects' THEN 1
        WHEN 'systems' THEN 2
        WHEN 'governance' THEN 3
        WHEN 'stakeholders' THEN 4
        WHEN 'risk_areas' THEN 5
        WHEN 'key_findings' THEN 6
        WHEN 'mitigations' THEN 7
    END;

-- Show foreign key relationships
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name;

-- ============================================================================
-- READY FOR DATA IMPORT
-- ============================================================================
-- Next steps:
--   1. Run projects_insert.sql
--   2. Run systems_insert.sql
--   3. Run governance_insert.sql
--   4. Run stakeholders_insert.sql
--   5. Run risk_areas_insert.sql
--   6. Run key_findings_insert.sql
--   7. Run mitigations_insert.sql
-- ============================================================================
