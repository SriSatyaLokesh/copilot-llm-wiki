#!/usr/bin/env python3
"""
scripts/rollback.py

Reverts the wiki/ directory to a previously captured named snapshot.
Verifies git tag existence, restores files, rebuilds indexes, and logs the rollback.

Usage:
    python scripts/rollback.py <name> [--force]
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


def rollback_to_snapshot(name: str, force: bool = False) -> int:
    tag_name = f"snapshot-{name}" if not name.startswith("snapshot-") else name
    snapshot_label = name.replace("snapshot-", "")

    # 1. Check if tag exists
    tags_res = run_git(["tag", "-l", tag_name])
    if tag_name not in tags_res.stdout.splitlines():
        print(f"Error: Snapshot tag '{tag_name}' does not exist.", file=sys.stderr)
        print("Available snapshots:", file=sys.stderr)
        all_snapshots = [t.replace("snapshot-", "") for t in tags_res.stdout.splitlines() if t.startswith("snapshot-")]
        for s in all_snapshots:
            print(f"  - {s}", file=sys.stderr)
        return 1

    # 2. Check for uncommitted changes
    status_res = run_git(["status", "--porcelain", "wiki/"])
    if status_res.stdout.strip() and not force:
        print("Error: Uncommitted changes detected in wiki/ directory.", file=sys.stderr)
        print("To overwrite local changes and force rollback, run with --force.", file=sys.stderr)
        return 1

    print(f"[*] Reverting wiki/ directory to snapshot '{snapshot_label}' ({tag_name})...")

    # 3. Checkout wiki/ from snapshot tag
    run_git(["checkout", tag_name, "--", "wiki/"])

    # 4. Clean untracked files in wiki/ that did not exist in the snapshot
    run_git(["clean", "-fd", "wiki/"])
    print("  [OK] Restored wiki/ files to snapshot state")

    # 5. Rebuild indexes to guarantee synchronization
    indexer = REPO_ROOT / "scripts" / "build-index.py"
    if indexer.exists():
        subprocess.run([sys.executable, str(indexer)], cwd=str(REPO_ROOT), check=True)
        print("  [OK] Recompiled wiki indexes")

    now_utc = datetime.now(timezone.utc)
    now_date = now_utc.strftime("%Y-%m-%d")

    # 6. Append to wiki/log.md
    if WIKI_LOG.exists():
        log_block = f"\n## [{now_date}] rollback | Reverted wiki/ directory to snapshot '{snapshot_label}'\n"
        with open(WIKI_LOG, "a", encoding="utf-8") as f:
            f.write(log_block)
        print(f"  [OK] Recorded operation in {WIKI_LOG.relative_to(REPO_ROOT)}")

    print(f"\n[SUCCESS] Wiki successfully rolled back to snapshot '{snapshot_label}'.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Revert wiki/ to a named snapshot.")
    parser.add_argument("name", help="Name of the snapshot to roll back to")
    parser.add_argument("--force", action="store_true", help="Force rollback even if uncommitted changes exist in wiki/")
    args = parser.parse_args()

    sys.exit(rollback_to_snapshot(args.name, force=args.force))


if __name__ == "__main__":
    main()
