#!/usr/bin/env python3
"""
scripts/lint-wiki.py

Comprehensive deterministic linter for the LLM Wiki.
Validates:
1. Index synchronization (invokes scripts/build-index.py --check)
2. Explicit relationships (closed taxonomy, valid markdown links)
3. Broken links across all wiki markdown files
4. Archive link violations (active pages linking directly to wiki/archive/)
5. Claim provenance in Key Facts sections
6. Source freshness and Volatility Classes (high: 30d, medium: 90d, low: 365d)
7. Missing 'See Also' sections

Usage:
    python scripts/lint-wiki.py [--strict]
"""

import sys
import re
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
SOURCES_DIR = WIKI_DIR / "sources"

VALID_RELATIONSHIP_TYPES = {
    "depends-on",
    "implements",
    "part-of",
    "supersedes",
    "contradicts",
    "related-to",
}

VOLATILITY_CYCLES = {
    "high": 30,    # APIs, schemas, pricing tables
    "medium": 90,  # Architecture specs, system overviews
    "low": 365,    # Invariant math, RFCs, foundational principles
}

EXCLUDED_FILENAMES = {"index.md", "README.md", ".gitkeep", "log.md", "overview.md"}
CANONICAL_SILOS = {"entities", "concepts", "comparisons", "sources", "qa", "archive"}


def resolve_markdown_link(source_file: Path, target_href: str) -> bool:
    """Check if target_href resolves to an existing file."""
    clean_href = target_href.split("#")[0].split("?")[0].strip()
    if not clean_href or clean_href.startswith("http://") or clean_href.startswith("https://") or clean_href.startswith("mailto:"):
        return True

    # 1. Resolve relative to source file directory
    cand1 = (source_file.parent / clean_href).resolve()
    if cand1.exists():
        return True

    # 2. Resolve relative to REPO_ROOT (for links starting with wiki/...)
    cand2 = (REPO_ROOT / clean_href).resolve()
    if cand2.exists():
        return True

    # 3. Resolve relative to WIKI_DIR
    cand3 = (WIKI_DIR / clean_href).resolve()
    if cand3.exists():
        return True

    return False


def check_source_freshness(source_file: Path, today: datetime) -> Tuple[str, str]:
    """
    Parses a source file for Last Verified / Ingested date and Volatility.
    Returns (status, message) where status is 'current', 'aging', or 'stale'.
    """
    content = source_file.read_text(encoding="utf-8")
    date_str = None
    volatility = "medium"

    # Match Last Verified or Ingested
    last_verified_match = re.search(r'\*\*Last Verified\*\*:\s*(\d{4}-\d{2}-\d{2})', content)
    if last_verified_match:
        date_str = last_verified_match.group(1)
    else:
        ingested_match = re.search(r'\*\*Ingested\*\*:\s*(\d{4}-\d{2}-\d{2})', content)
        if ingested_match:
            date_str = ingested_match.group(1)

    vol_match = re.search(r'\*\*Volatility\*\*:\s*(high|medium|low)', content, re.IGNORECASE)
    if vol_match:
        volatility = vol_match.group(1).lower()

    if not date_str:
        return "unknown", f"No Ingested or Last Verified date found in {source_file.name}"

    try:
        verified_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return "unknown", f"Invalid date format in {source_file.name}: {date_str}"

    cycle_days = VOLATILITY_CYCLES.get(volatility, 90)
    days_elapsed = (today - verified_date).days

    if days_elapsed > cycle_days:
        return "stale", f"🔴 Stale ({days_elapsed}d > {cycle_days}d cycle, volatility={volatility}): {source_file.name} - needs reingest"
    elif days_elapsed > int(cycle_days * 0.75):
        return "aging", f"🟡 Aging ({days_elapsed}d / {cycle_days}d cycle, volatility={volatility}): {source_file.name}"
    else:
        return "current", f"🟢 Current ({days_elapsed}d / {cycle_days}d cycle, volatility={volatility}): {source_file.name}"


def lint_wiki(strict: bool = False) -> int:
    errors = []
    warnings = []
    today = datetime.now()

    print("[*] Running deterministic wiki linter...\n")

    # 1. Index Synchronization check
    build_index_script = REPO_ROOT / "scripts" / "build-index.py"
    if build_index_script.exists():
        res = subprocess.run([sys.executable, str(build_index_script), "--check"], capture_output=True, text=True)
        if res.returncode != 0:
            errors.append(f"Index Synchronization: Wiki indexes are out of sync.\n{res.stdout.strip()}")
        else:
            print("  [OK] Index Synchronization: All sub-indexes and root index up-to-date")

    # 1b. Knowledge Graph & Semantic Index Synchronization
    build_graph_script = REPO_ROOT / "scripts" / "build-graph.py"
    if build_graph_script.exists():
        res = subprocess.run([sys.executable, str(build_graph_script), "--check"], capture_output=True, text=True)
        if res.returncode != 0:
            errors.append(f"Knowledge Graph: wiki/graph.json is out of sync.\n{res.stdout.strip()}")
        else:
            print("  [OK] Knowledge Graph: wiki/graph.json is up-to-date")

        try:
            import importlib
            if str(REPO_ROOT / "scripts") not in sys.path:
                sys.path.insert(0, str(REPO_ROOT / "scripts"))
            bg_mod = importlib.import_module("build-graph")
            graph_data = bg_mod.generate_graph(WIKI_DIR)
            orphans = bg_mod.find_isolated_nodes(graph_data)
            if orphans:
                for o in orphans:
                    warnings.append(f"Graph Orphan: Node '{o}' has 0 inbound and 0 outbound relationships/links")
            else:
                print("  [OK] Knowledge Graph: 0 isolated orphan nodes detected")
        except Exception as e:
            warnings.append(f"Could not perform graph orphan analysis: {e}")

    build_semantic_script = REPO_ROOT / "scripts" / "build-semantic-index.py"
    if build_semantic_script.exists():
        res = subprocess.run([sys.executable, str(build_semantic_script), "--check"], capture_output=True, text=True)
        if res.returncode != 0:
            errors.append(f"Semantic Index: wiki/semantic-index.json is out of sync.\n{res.stdout.strip()}")
        else:
            print("  [OK] Semantic Index: wiki/semantic-index.json is up-to-date")

    # 1c. Multi-LLM Instruction Adapters check
    sync_adapters_script = REPO_ROOT / "scripts" / "sync-adapters.py"
    if sync_adapters_script.exists():
        res = subprocess.run([sys.executable, str(sync_adapters_script), "--check"], capture_output=True, text=True)
        if res.returncode != 0:
            errors.append(f"Instruction Adapters: LLM instructions are out of sync.\n{res.stdout.strip()}")
        else:
            print("  [OK] Instruction Adapters: All multi-LLM instructions up-to-date")

    # 2. Source Freshness check
    if SOURCES_DIR.exists():
        source_files = [f for f in SOURCES_DIR.glob("*.md") if f.name not in EXCLUDED_FILENAMES]
        print(f"  [OK] Checking freshness for {len(source_files)} primary source documents...")
        for sf in source_files:
            status, msg = check_source_freshness(sf, today)
            if status == "stale":
                warnings.append(msg)
            elif status == "aging":
                warnings.append(msg)

    # 3. Scan all Markdown files in canonical silos
    all_md_files = []
    for silo in CANONICAL_SILOS:
        silo_dir = WIKI_DIR / silo
        if silo_dir.exists():
            for f in silo_dir.rglob("*.md"):
                if f.name not in EXCLUDED_FILENAMES:
                    all_md_files.append(f)

    print(f"  [OK] Scanning {len(all_md_files)} canonical knowledge documents...")

    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    rel_bullet_pattern = re.compile(r'^\s*[-*]\s+\*\*([a-zA-Z0-9_\-]+)\*\*:\s*(.+)$')

    for md_file in all_md_files:
        rel_path = md_file.relative_to(REPO_ROOT).as_posix()
        is_archive = "wiki/archive" in rel_path
        content = md_file.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Check for '## See Also'
        if not is_archive and not any("## See Also" in l for l in lines):
            warnings.append(f"Missing '## See Also': {rel_path}")

        # Check Relationships and Key Facts
        in_relationships = False
        in_key_facts = False

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("## "):
                heading = stripped[3:].strip().lower()
                in_relationships = (heading == "relationships")
                in_key_facts = ("key facts" in heading)
                continue

            # Validate Relationships
            if in_relationships and (stripped.startswith("- ") or stripped.startswith("* ")):
                match = rel_bullet_pattern.match(stripped)
                if match:
                    rel_type = match.group(1).lower()
                    rel_target = match.group(2)
                    if rel_type not in VALID_RELATIONSHIP_TYPES:
                        errors.append(f"Invalid relationship type '**{rel_type}**' in {rel_path}. Allowed: {sorted(list(VALID_RELATIONSHIP_TYPES))}")
                else:
                    warnings.append(f"Malformed relationship format in {rel_path}: '{stripped}' (expected: - **type**: [Target](path))")

            # Validate Provenance in Key Facts
            if in_key_facts and (stripped.startswith("- ") or stripped.startswith("* ")):
                has_footnote = bool(re.search(r'\[\^[a-zA-Z0-9_\-]+\]', stripped))
                has_parenthetical = bool(re.search(r'\(Source:|\(source:|\^\[source:', stripped, re.IGNORECASE))
                if not has_footnote and not has_parenthetical:
                    if strict:
                        errors.append(f"Unattributed fact in {rel_path}: '{stripped[:80]}...'")
                    else:
                        warnings.append(f"Unattributed fact in {rel_path}: '{stripped[:80]}...'")

            # Check links
            for link_match in link_pattern.finditer(stripped):
                anchor_text = link_match.group(1)
                href = link_match.group(2)

                # Check for active pages linking into wiki/archive/
                if not is_archive and ("wiki/archive" in href or "../archive" in href):
                    if not in_relationships or "supersedes" not in stripped:
                        warnings.append(f"Archive link violation in {rel_path}: links to archived page '{href}' instead of active note")

                # Check for broken links
                if not resolve_markdown_link(md_file, href):
                    errors.append(f"Broken link in {rel_path}: [{anchor_text}]({href}) does not exist")

    # Output report
    print("\n" + "=" * 60)
    print("                WIKI LINT REPORT")
    print("=" * 60)

    if warnings:
        print(f"\n[!] {len(warnings)} Warnings:")
        for w in warnings[:15]:
            print(f"  - {w}")
        if len(warnings) > 15:
            print(f"  ... and {len(warnings) - 15} more warnings.")

    if errors:
        print(f"\n[FAIL] {len(errors)} Errors found:")
        for e in errors:
            print(f"  - {e}")
        return 1
    else:
        print("\n[PASS] No critical lint errors found.")
        return 0


def main():
    parser = argparse.ArgumentParser(description="Deterministic wiki linter.")
    parser.add_argument("--strict", action="store_true", help="Treat missing claim provenance as errors")
    args = parser.parse_args()

    sys.exit(lint_wiki(strict=args.strict))


if __name__ == "__main__":
    main()
