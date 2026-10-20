#!/usr/bin/env python3
"""
scripts/reingest.py

Manages source versioning and delta re-ingestion for living documents (Issue #13).
Preserves prior raw source snapshots in raw/archive/<slug>-<timestamp>.md,
updates Last Verified metadata, and logs the reingest delta operation in wiki/log.md.

Usage:
    python scripts/reingest.py <source-slug-or-file>
"""

import sys
import re
import shutil
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "raw"
RAW_ARCHIVE_DIR = RAW_DIR / "archive"
WIKI_DIR = REPO_ROOT / "wiki"
SOURCES_DIR = WIKI_DIR / "sources"
WIKI_LOG = WIKI_DIR / "log.md"


def reingest_source(source_identifier: str) -> int:
    slug = Path(source_identifier).stem
    raw_source = RAW_DIR / f"{slug}.md"
    wiki_source = SOURCES_DIR / f"{slug}.md"

    if not wiki_source.exists():
        print(f"Error: Source documentation page not found at {wiki_source.relative_to(REPO_ROOT)}.", file=sys.stderr)
        print("Use regular 'ingest' for new documents.", file=sys.stderr)
        return 1

    now_utc = datetime.now(timezone.utc)
    timestamp = now_utc.strftime("%Y%m%d%H%M%S")
    today_date = now_utc.strftime("%Y-%m-%d")

    # 1. Archive prior raw file if it exists
    RAW_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    if raw_source.exists():
        archive_dest = RAW_ARCHIVE_DIR / f"{slug}-{timestamp}.md"
        shutil.copy2(raw_source, archive_dest)
        print(f"  [OK] Archived prior source to {archive_dest.relative_to(REPO_ROOT)}")

    # 2. Update Last Verified in wiki/sources/<slug>.md
    source_content = wiki_source.read_text(encoding="utf-8")
    if "**Last Verified**:" in source_content:
        updated_content = re.sub(
            r'\*\*Last Verified\*\*:\s*\d{4}-\d{2}-\d{2}',
            f"**Last Verified**: {today_date}",
            source_content
        )
    else:
        # Insert Last Verified after Ingested
        if "**Ingested**:" in source_content:
            updated_content = re.sub(
                r'(\*\*Ingested\*\*:\s*\d{4}-\d{2}-\d{2})',
                r'\1\n- **Last Verified**: ' + today_date,
                source_content
            )
        else:
            updated_content = f"- **Last Verified**: {today_date}\n" + source_content

    wiki_source.write_text(updated_content, encoding="utf-8")
    print(f"  [OK] Refreshed 'Last Verified' to {today_date} in {wiki_source.relative_to(REPO_ROOT)}")

    # 3. Log reingest operation in wiki/log.md
    if WIKI_LOG.exists():
        log_entry = (
            f"\n## [{today_date}] reingest | {slug}\n"
            f"Reingested living document and updated verification timestamp.\n"
            f"Archived previous snapshot in raw/archive/.\n"
        )
        with open(WIKI_LOG, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"  [OK] Appended reingest record to {WIKI_LOG.relative_to(REPO_ROOT)}")

    # 4. Rebuild indexes
    indexer = REPO_ROOT / "scripts" / "build-index.py"
    if indexer.exists():
        subprocess.run([sys.executable, str(indexer)], check=True, cwd=str(REPO_ROOT))
        print(f"  [OK] Recompiled wiki indexes")

    print(f"\n[SUCCESS] Reingest completed for '{slug}'.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Reingest living document and archive prior version.")
    parser.add_argument("source", help="Slug or filename of the source document")
    args = parser.parse_args()

    sys.exit(reingest_source(args.source))


if __name__ == "__main__":
    main()
