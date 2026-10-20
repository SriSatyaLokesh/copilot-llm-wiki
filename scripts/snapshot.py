#!/usr/bin/env python3
"""
scripts/snapshot.py

Creates a named semantic snapshot of the wiki via Git tags and logs it
in wiki/meta/snapshots.md and wiki/log.md.

Usage:
    python scripts/snapshot.py <name> [description] [--auto-commit]
"""

import sys
import re
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
META_DIR = WIKI_DIR / "meta"
SNAPSHOTS_LOG = META_DIR / "snapshots.md"
WIKI_LOG = WIKI_DIR / "log.md"


def run_git(args, check=True, capture=True):
    cmd = ["git"] + args
    res = subprocess.run(cmd, cwd=str(REPO_ROOT), text=True, capture_output=capture)
    if check and res.returncode != 0:
        raise RuntimeError(f"Git command failed: {' '.join(cmd)}\n{res.stderr.strip()}")
    return res


def create_snapshot(name: str, description: str = "", auto_commit: bool = True) -> int:
    # 1. Validate snapshot name
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', name):
        print(f"Error: Invalid snapshot name '{name}'. Use alphanumeric characters, hyphens, dots, or underscores.", file=sys.stderr)
        return 1

    tag_name = f"snapshot-{name}"

    # 2. Check if tag already exists
    tags_res = run_git(["tag", "-l", tag_name])
    if tag_name in tags_res.stdout.splitlines():
        print(f"Error: Snapshot tag '{tag_name}' already exists. Choose a different name or delete the old tag.", file=sys.stderr)
        return 1

    # 3. Check for uncommitted changes
    status_res = run_git(["status", "--porcelain"])
    dirty_files = [line for line in status_res.stdout.splitlines() if line.strip()]

    if dirty_files:
        if auto_commit:
            print(f"[*] Uncommitted changes detected. Auto-committing before snapshotting...")
            run_git(["add", "wiki/"])
            # Check if there are staged changes in wiki
            diff_res = run_git(["diff", "--cached", "--quiet"], check=False)
            if diff_res.returncode != 0:
                run_git(["commit", "-m", f"chore(snapshot): save wiki state before snapshot '{name}'"])
        else:
            print(f"Error: Working directory has uncommitted changes. Please commit or stash them, or pass --auto-commit.", file=sys.stderr)
            return 1

    # 4. Create annotated Git tag
    tag_msg = f"Wiki snapshot: {name}" + (f" - {description}" if description else "")
    run_git(["tag", "-a", tag_name, "-m", tag_msg])
    print(f"  [OK] Created Git tag '{tag_name}'")

    now_utc = datetime.now(timezone.utc)
    now_iso = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    now_date = now_utc.strftime("%Y-%m-%d")
    desc_clean = description.strip() if description else "Manual snapshot"

    # 5. Append to wiki/meta/snapshots.md
    META_DIR.mkdir(parents=True, exist_ok=True)
    if not SNAPSHOTS_LOG.exists():
        SNAPSHOTS_LOG.write_text(
            "# Wiki Snapshots Log\n\nThis ledger tracks semantic snapshots and rollback operations for automated auditing and recovery.\n\n| Snapshot Name | Git Tag | Created At (UTC) | Description | Status |\n|---------------|---------|------------------|-------------|--------|\n",
            encoding="utf-8"
        )

    log_entry = f"| {name} | {tag_name} | {now_iso} | {desc_clean} | Active |\n"
    with open(SNAPSHOTS_LOG, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"  [OK] Recorded snapshot in {SNAPSHOTS_LOG.relative_to(REPO_ROOT)}")

    # 6. Append to wiki/log.md
    if WIKI_LOG.exists():
        log_block = f"\n## [{now_date}] snapshot | Created snapshot '{name}' - {desc_clean}\n"
        with open(WIKI_LOG, "a", encoding="utf-8") as f:
            f.write(log_block)
        print(f"  [OK] Recorded operation in {WIKI_LOG.relative_to(REPO_ROOT)}")

    print(f"\n[SUCCESS] Snapshot '{name}' created successfully.")
    print(f"To rollback to this state at any time, run:")
    print(f"  python scripts/rollback.py {name}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Create a named semantic snapshot of the wiki.")
    parser.add_argument("name", help="Alphanumeric name for the snapshot (e.g. pre-batch-ingest, v1.0)")
    parser.add_argument("description", nargs="?", default="", help="Optional description of the snapshot")
    parser.add_argument("--no-auto-commit", dest="auto_commit", action="store_false", help="Do not automatically commit uncommitted changes")
    args = parser.parse_args()

    sys.exit(create_snapshot(args.name, args.description, auto_commit=args.auto_commit))


if __name__ == "__main__":
    main()
