#!/usr/bin/env python3
"""
scripts/intake.py

CLI intake router for multi-format source documents.
Fulfills Issue #19:
- Automatically detects input format (URL, PDF, CSV, GitHub Issue/PR)
- Dispatches to appropriate adapter in adapters/
- Writes normalized markdown to raw/<slug>.md without modifying existing raw files
- Outputs next-step instructions for the LLM ingest workflow

Usage:
    python scripts/intake.py https://docs.github.com/en/copilot/overview
    python scripts/intake.py data/pricing.csv
    python scripts/intake.py docs/whitepaper.pdf --slug copilot-whitepaper
"""

import argparse
import sys
from pathlib import Path

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from adapters.registry import get_adapter_for

RAW_DIR = REPO_ROOT / "raw"


def intake_source(source: str, slug: str = None, raw_dir: Path = None) -> int:
    """Route source to adapter and write to raw/."""
    if raw_dir is None:
        raw_dir = RAW_DIR

    try:
        adapter = get_adapter_for(source)
    except ValueError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return 1

    print(f"[*] Selected adapter: {adapter.__class__.__name__}")
    print(f"[*] Ingesting: {source}")

    try:
        saved_path = adapter.save_to_raw(source, raw_dir=raw_dir, slug=slug)
        print(f"\n[OK] Source document normalized and saved to:")
        print(f"     {saved_path.relative_to(REPO_ROOT)}")
        print("\nNext steps for Ingest Workflow:")
        print(f"  1. Read {saved_path.relative_to(REPO_ROOT)}")
        print(f"  2. Discuss takeaways and propose new entities/concepts")
        print(f"  3. Create summary at wiki/sources/{saved_path.stem}.md")
        print(f"  4. Update wiki/entities/ and wiki/concepts/ with explicit relationships & citations")
        print(f"  5. Run 'python scripts/build-index.py' to compile indexes, graph, and semantic index")
        print(f"  6. Append entry to wiki/log.md")
        return 0
    except Exception as e:
        print(f"[FAIL] Error during source intake: {e}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-format source intake tool for GitHub Copilot LLM Wiki.")
    parser.add_argument("source", type=str, help="URL, local file path (PDF, CSV, JSON), or GitHub Issue URL.")
    parser.add_argument("--slug", "-s", type=str, default=None, help="Custom filename slug (without .md).")
    parser.add_argument("--raw-dir", "-o", type=Path, default=None, help="Custom output directory (default: raw/).")
    args = parser.parse_args()

    return intake_source(args.source, slug=args.slug, raw_dir=args.raw_dir)


if __name__ == "__main__":
    sys.exit(main())
