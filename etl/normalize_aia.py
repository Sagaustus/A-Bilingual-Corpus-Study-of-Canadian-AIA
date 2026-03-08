"""
ETL script: AIA.csv → normalized relational tables
Outputs CSV files ready for import into a relational database.
"""

import csv
import os
from pathlib import Path

SRC = Path(__file__).parent.parent / "AIA.csv"
OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────

def clean(val: str) -> str | None:
    """Return None for blank / dash placeholders, else strip whitespace."""
    v = val.strip()
    return None if v in ("", "-") else v


def split_multi(val: str) -> list[str]:
    """Split comma-separated multi-value field; skip blanks and dashes."""
    return [item.strip() for item in val.split(",") if item.strip() not in ("", "-")]


def write_csv(name: str, fieldnames: list[str], rows: list[dict]) -> None:
    path = OUT / f"{name}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {len(rows):>4} rows → {path.name}")


# ── load & deduplicate ────────────────────────────────────────────────────────

with open(SRC, encoding="utf-8-sig") as f:
    raw = list(csv.DictReader(f))

seen_ids: set[str] = set()
unique: list[dict] = []
for row in raw:
    if row["ID"] not in seen_ids:
        seen_ids.add(row["ID"])
        unique.append(row)

print(f"Raw rows: {len(raw)}  →  unique datasets: {len(unique)}")

# ── lookup-table builders ─────────────────────────────────────────────────────

def build_lookup(items: list[str]) -> dict[str, int]:
    """Assign a stable integer id to each unique string value."""
    return {v: i + 1 for i, v in enumerate(sorted(set(items)))}


# Collect all values for each multi-value lookup
all_subjects:       list[str] = []
all_keywords:       list[str] = []
all_resource_types: list[str] = []
all_languages:      list[str] = []
all_formats:        list[str] = []
all_orgs:           list[str] = []

for r in unique:
    all_subjects       += split_multi(r["Subject"])
    all_keywords       += split_multi(r["Keywords"])
    all_resource_types += split_multi(r["Resource Type"])
    all_languages      += split_multi(r["Language"])
    all_formats        += split_multi(r["Format"])
    all_orgs           += split_multi(r["Organization"])

subjects_lut       = build_lookup(all_subjects)
keywords_lut       = build_lookup(all_keywords)
resource_types_lut = build_lookup(all_resource_types)
languages_lut      = build_lookup(all_languages)
formats_lut        = build_lookup(all_formats)
orgs_lut           = build_lookup(all_orgs)

# ── write lookup tables ───────────────────────────────────────────────────────

write_csv("organizations",   ["id", "name"],
          [{"id": v, "name": k} for k, v in sorted(orgs_lut.items(), key=lambda x: x[1])])

write_csv("subjects",        ["id", "name"],
          [{"id": v, "name": k} for k, v in sorted(subjects_lut.items(), key=lambda x: x[1])])

write_csv("keywords",        ["id", "name"],
          [{"id": v, "name": k} for k, v in sorted(keywords_lut.items(), key=lambda x: x[1])])

write_csv("resource_types",  ["id", "name"],
          [{"id": v, "name": k} for k, v in sorted(resource_types_lut.items(), key=lambda x: x[1])])

write_csv("languages",       ["id", "name"],
          [{"id": v, "name": k} for k, v in sorted(languages_lut.items(), key=lambda x: x[1])])

write_csv("formats",         ["id", "name"],
          [{"id": v, "name": k} for k, v in sorted(formats_lut.items(), key=lambda x: x[1])])

# ── datasets (core table) ─────────────────────────────────────────────────────
# Dropped columns:
#   - Automated translation fields  (all null)
#   - Spatial Representation Type   (all null)
#   - Maintainer                    (all null)
#   - Relationship Type             (all null)
#   - Data Includes URIs and Links  (all null)
#   - Spatial                       (all null)
#   - Time Period Coverage End      (all null)
#   - Topic category                (all null)
#   - Name                          (= ID)
#   - Collection Type               (constant: 'Algorithmic Impact Assessment')
#   - Jurisdiction                  (constant: 'Federal')
#   - Licence                       (constant: 'Open Government Licence - Canada')
#   - Access Restrictions           (constant: 'unrestricted')
#   - Portal Type                   (constant: 'Open Information')
#   - Formats                       (duplicate of Format)
#   - Organization                  (dup of Publisher name; FK used instead)
#   - Publisher - Organization Name at Publication (same as Organization)

datasets: list[dict] = []
for r in unique:
    # Resolve org FK — take first org if somehow multiple (data is consistent)
    org_name = split_multi(r["Organization"])
    org_id   = orgs_lut[org_name[0]] if org_name else None

    datasets.append({
        "id":                    r["ID"],
        "title":                 clean(r["Title"]),
        "organization_id":       org_id,
        "publisher_section":     clean(r["Publisher - Organization Section Name"]),
        "update_frequency":      clean(r["Update Frequency"]),
        "contact_email":         clean(r["Contact Email"]),
        "metadata_created":      clean(r["Metadata Created"]),
        "metadata_modified":     clean(r["Metadata Modified"]),
        "homepage":              clean(r["Homepage"]),
        "related_record_type":   clean(r["Related Record Type"]),
        "time_period_start":     clean(r["Time Period Coverage Start"]),
    })

write_csv("datasets",
          ["id", "title", "organization_id", "publisher_section",
           "update_frequency", "contact_email", "metadata_created",
           "metadata_modified", "homepage", "related_record_type",
           "time_period_start"],
          datasets)

# ── junction tables ───────────────────────────────────────────────────────────

def build_junction(lut: dict[str, int], field: str, table_name: str,
                   col_a: str, col_b: str) -> None:
    rows: list[dict] = []
    seen: set[tuple] = set()
    for r in unique:
        for val in split_multi(r[field]):
            if val in lut:
                pair = (r["ID"], lut[val])
                if pair not in seen:
                    seen.add(pair)
                    rows.append({col_a: r["ID"], col_b: lut[val]})
    write_csv(table_name, [col_a, col_b], rows)


build_junction(subjects_lut,       "Subject",       "dataset_subjects",
               "dataset_id", "subject_id")
build_junction(keywords_lut,       "Keywords",      "dataset_keywords",
               "dataset_id", "keyword_id")
build_junction(resource_types_lut, "Resource Type", "dataset_resource_types",
               "dataset_id", "resource_type_id")
build_junction(languages_lut,      "Language",      "dataset_languages",
               "dataset_id", "language_id")
build_junction(formats_lut,        "Format",        "dataset_formats",
               "dataset_id", "format_id")

# ── resources (download URLs) ─────────────────────────────────────────────────
# Each URL is an independent downloadable file.
# Size and Date Published counts don't align with URL counts across datasets,
# so they are stored at the dataset level, not per-resource.

resources: list[dict] = []
resource_id = 1
for r in unique:
    urls = split_multi(r["Download URL"])
    for url in urls:
        resources.append({
            "id":         resource_id,
            "dataset_id": r["ID"],
            "url":        url,
        })
        resource_id += 1

write_csv("resources", ["id", "dataset_id", "url"], resources)

# ── summary ───────────────────────────────────────────────────────────────────

print("\nDone. Output directory:", OUT)
print(f"\nConstants encoded in schema (not in tables):")
print(f"  collection_type    = 'Algorithmic Impact Assessment'")
print(f"  jurisdiction       = 'Federal'")
print(f"  licence            = 'Open Government Licence - Canada'")
print(f"  access_restrictions= 'unrestricted'")
print(f"  portal_type        = 'Open Information'")
