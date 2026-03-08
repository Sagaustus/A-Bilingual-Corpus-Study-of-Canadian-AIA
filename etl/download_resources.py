"""
Download all AIA resources listed in etl/output/resources.csv.

Output layout:
  resources/
    {dataset_id}/
      {filename}.pdf
      {filename}.json
      ...

Features:
  - Skips files already downloaded (resume-safe)
  - Polite delay between requests
  - Logs outcomes to etl/output/download_log.csv
"""

import csv
import time
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs

RESOURCES_CSV = Path(__file__).parent / "output" / "resources.csv"
OUT_DIR       = Path(__file__).parent.parent / "resources"
LOG_PATH      = Path(__file__).parent / "output" / "download_log.csv"

DELAY_SECS    = 0.5   # pause between requests — be polite
TIMEOUT_SECS  = 30
HEADERS       = {"User-Agent": "AIA-Corpus-Research/1.0 (academic use)"}

# ── helpers ───────────────────────────────────────────────────────────────────

def derive_filename(url: str, dataset_id: str, row_id: str) -> str:
    """Return a safe local filename for a given URL."""
    parsed = urlparse(url)
    name   = Path(parsed.path).name

    if name and "." in name:
        return name

    # Fallback for URLs like /aia-eia-js/?lang=en
    lang = parse_qs(parsed.query).get("lang", [""])[0]
    suffix = f"_{lang}" if lang else f"_{row_id}"
    return f"page{suffix}.html"


def download(url: str, dest: Path) -> tuple[str, str]:
    """
    Download url → dest.
    Returns (status, detail) where status is 'ok'|'skip'|'error'.
    """
    if dest.exists():
        return "skip", f"already exists ({dest.stat().st_size} bytes)"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECS, stream=True)
        resp.raise_for_status()

        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                f.write(chunk)

        size = dest.stat().st_size
        return "ok", f"{size:,} bytes"

    except requests.HTTPError as e:
        return "error", f"HTTP {e.response.status_code}"
    except requests.RequestException as e:
        return "error", str(e)


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    with open(RESOURCES_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    log_rows: list[dict] = []
    counts   = {"ok": 0, "skip": 0, "error": 0}

    print(f"Downloading {len(rows)} resources → {OUT_DIR}/\n")

    for row in rows:
        row_id     = row["id"]
        dataset_id = row["dataset_id"]
        url        = row["url"]
        filename   = derive_filename(url, dataset_id, row_id)
        dest       = OUT_DIR / dataset_id / filename

        status, detail = download(url, dest)
        counts[status] += 1

        icon = {"ok": "✓", "skip": "–", "error": "✗"}[status]
        print(f"  [{row_id:>3}] {icon}  {filename:<55} {detail}")

        log_rows.append({
            "id":         row_id,
            "dataset_id": dataset_id,
            "url":        url,
            "filename":   filename,
            "status":     status,
            "detail":     detail,
        })

        if status != "skip":
            time.sleep(DELAY_SECS)

    # Write log
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id","dataset_id","url","filename","status","detail"])
        w.writeheader()
        w.writerows(log_rows)

    print(f"\nDone.  ✓ {counts['ok']} downloaded  – {counts['skip']} skipped  ✗ {counts['error']} errors")
    print(f"Log written → {LOG_PATH}")


if __name__ == "__main__":
    main()
