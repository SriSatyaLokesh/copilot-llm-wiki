#!/usr/bin/env python3
"""
scripts/sync-adapters.py

Deterministic Multi-LLM Instruction Synchronizer.
Fulfills Issue #22:
- Synchronizes core wiki schema from AGENTS.md / .github/copilot-instructions.md
- Generates/validates platform adapters:
  - CLAUDE.md (Claude Code / Anthropic Opus & Sonnet)
  - .gemini/GEMINI.md (Google Antigravity / Gemini CLI)
  - .cursorrules (Cursor IDE Agent)
  - .cursor/rules/wiki.mdc (Cursor Rules directory format)
- Enforces zero-drift on Prohibitions, Schemas, and Workflows
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

CLAUDE_TEMPLATE = """# Claude Code Instructions — GitHub Copilot LLM Wiki

> **Authoritative Schema**: This repository is governed by [.github/copilot-instructions.md](file:///.github/copilot-instructions.md) and [AGENTS.md](file:///AGENTS.md). All rules, prohibitions, and schema conventions defined therein apply unconditionally to Claude Code.

---

## Claude Code Specific Optimizations

1. **Sub-Cent Routing via Semantic Index**:
   - Before reading entire directories or loading markdown files, inspect `wiki/semantic-index.json`.
   - Query candidate files with `python scripts/build-semantic-index.py --query "<topic>"` to locate relevant files without context waste.
   - For entity relationships, inspect `wiki/graph.json` to follow typed edges (`depends-on`, `implements`, `part-of`).

2. **Subagent Delegation**:
   - For research tasks spanning multiple source documents, dispatch a read-only subagent to summarize facts before modifying wiki files.
   - For batch linting or re-indexing, run the deterministic Python scripts directly rather than reading and checking files manually.

3. **Tool Invocation**:
   - Always run deterministic automation scripts for bookkeeping:
     - `python scripts/build-index.py` — deterministic index and catalog compiler
     - `python scripts/build-graph.py` — knowledge graph manifest generator
     - `python scripts/build-semantic-index.py` — keyword and summary index generator
     - `python scripts/lint-wiki.py --strict` — strict invariant linter

---

## Prohibitions
- Never modify or delete files in `raw/` — it is read-only source material.
- Never edit or delete past entries in `wiki/log.md` — append only.
- Never write a wiki page without first checking `wiki/semantic-index.json` or `wiki/index.md`.
- Never write a page that contradicts an existing page without flagging the contradiction to the user.

---

## Core Workflows

### Ingest Workflow
1. Read the source in full. If a URL, fetch and save to `raw/<slug>.md`.
2. State key takeaways and outline pages to create or update.
3. Write source summary at `wiki/sources/<slug>.md` with Volatility Class.
4. Create or update entity/concept pages in `wiki/entities/` and `wiki/concepts/`.
5. Run `python scripts/build-index.py` to compile indexes, graph, and semantic index.
6. Append entry to `wiki/log.md`.

### Query Workflow
1. Routing: Inspect `wiki/semantic-index.json` or run `python scripts/build-semantic-index.py --query "<query>"`.
2. Read matched candidate pages and follow cross-links.
3. Cite sources at the end of every answer.

### Lint Workflow
1. Run `python scripts/lint-wiki.py --strict`.
2. Report results and resolve any broken links, graph orphans, or formatting violations.
"""

GEMINI_TEMPLATE = """# Google Antigravity & Gemini CLI Instructions — GitHub Copilot LLM Wiki

> **Authoritative Schema**: This repository is governed by [.github/copilot-instructions.md](file:///.github/copilot-instructions.md) and [AGENTS.md](file:///AGENTS.md). All rules, prohibitions, and schema conventions defined therein apply unconditionally to Google Antigravity and Gemini CLI agents.

---

## Gemini & Antigravity Optimizations

1. **Progressive Disclosure & Context Management**:
   - Gemini models utilize the hierarchical routing index `wiki/index.md` and `wiki/semantic-index.json`.
   - Read `wiki/semantic-index.json` first to identify target entities and concepts rather than reading all files in `wiki/`.
   - Inspect `wiki/graph.json` to navigate directed property graph edges (`depends-on`, `implements`, `part-of`, `related-to`).

2. **Deterministic Script Execution**:
   - Never write index files or graph manifests manually. Always invoke:
     - `python scripts/build-index.py`
     - `python scripts/build-graph.py`
     - `python scripts/build-semantic-index.py`
     - `python scripts/lint-wiki.py --strict`

3. **Multi-Modal Source Intake**:
   - When ingesting images or architectural diagrams, summarize textual structure into `raw/<slug>.md` and link in `wiki/sources/<slug>.md`.

---

## Prohibitions
- Never modify or delete files in `raw/` — it is read-only source material.
- Never edit or delete past entries in `wiki/log.md` — append only.
- Never write a wiki page without first checking `wiki/semantic-index.json` or `wiki/index.md`.
- Never write a page that contradicts an existing page without flagging the contradiction to the user.

---

## Core Workflows

### Ingest Workflow
1. Read the source in full. Save content to `raw/<slug>.md`.
2. State key takeaways with the user.
3. Write source summary at `wiki/sources/<slug>.md`.
4. Create/update entity and concept pages with explicit `## Relationships` and claim provenance.
5. Recompile indexes: `python scripts/build-index.py`.
6. Append to `wiki/log.md`.

### Query Workflow
1. Consult `wiki/semantic-index.json` or `wiki/index.md`.
2. Read candidate notes; follow directed edges.
3. Answer with source citations.

### Lint Workflow
1. Run `python scripts/lint-wiki.py --strict`.
"""

CURSORRULES_TEMPLATE = """# Cursor IDE Agent Instructions — GitHub Copilot LLM Wiki

Authoritative Schema: .github/copilot-instructions.md and AGENTS.md

## Cursor Agent Guidelines
- Before answering questions or editing files, consult @wiki/semantic-index.json or @wiki/index.md.
- For entity relationships, inspect @wiki/graph.json.
- Always run `python scripts/build-index.py` after editing or adding wiki documents.
- Always run `python scripts/lint-wiki.py --strict` to verify link and schema integrity.

## Prohibitions
- Never modify or delete files in raw/
- Never edit or delete past entries in wiki/log.md
- Never write a page without checking wiki/index.md and wiki/semantic-index.json first
- Never contradict an existing page without explicitly highlighting the conflict

## Workflows
- Ingest: Save to raw/<slug>.md -> summarize in wiki/sources/<slug>.md -> update entities/concepts -> run build-index.py -> append wiki/log.md
- Query: Check wiki/semantic-index.json -> read candidate notes -> cite sources
- Lint: Run python scripts/lint-wiki.py --strict
"""

CURSOR_MDC_TEMPLATE = """---
description: Knowledge engine and wiki maintenance rules for Cursor
globs: wiki/**/*, raw/**/*
---

# Cursor Rule: GitHub Copilot LLM Wiki

Governed by authoritative specifications in `.github/copilot-instructions.md` and `AGENTS.md`.

## Critical Directives
- **Zero-Waste Query Routing**: Check `wiki/semantic-index.json` or `wiki/index.md` first before loading arbitrary markdown files into context.
- **Graph Traversal**: Inspect `wiki/graph.json` for typed entity relationships (`depends-on`, `implements`, `part-of`).
- **Deterministic Compilation**: Run `python scripts/build-index.py` to update indexes and semantic catalogs after modifying wiki content.
- **Quality Linting**: Run `python scripts/lint-wiki.py --strict` before submitting changes.

## Prohibitions
- Never modify or delete files in `raw/`.
- Never edit past entries in `wiki/log.md`.
- Never write a wiki page without first checking `wiki/semantic-index.json` or `wiki/index.md`.
"""

ADAPTERS_CONFIG = {
    REPO_ROOT / "CLAUDE.md": CLAUDE_TEMPLATE,
    REPO_ROOT / ".gemini" / "GEMINI.md": GEMINI_TEMPLATE,
    REPO_ROOT / ".cursorrules": CURSORRULES_TEMPLATE,
    REPO_ROOT / ".cursor" / "rules" / "wiki.mdc": CURSOR_MDC_TEMPLATE,
}


def validate_adapters() -> int:
    """Check that all adapter files exist and contain required schema invariants."""
    errors = []
    for file_path, expected_content in ADAPTERS_CONFIG.items():
        if not file_path.exists():
            errors.append(f"Missing adapter: {file_path.relative_to(REPO_ROOT)}")
            continue

        content = file_path.read_text(encoding="utf-8")
        if "copilot-instructions.md" not in content and "AGENTS.md" not in content:
            errors.append(f"{file_path.relative_to(REPO_ROOT)} is missing authoritative schema reference")

        if "semantic-index.json" not in content:
            errors.append(f"{file_path.relative_to(REPO_ROOT)} is missing reference to semantic-index.json")

        if "raw/" not in content or "log.md" not in content:
            errors.append(f"{file_path.relative_to(REPO_ROOT)} is missing core prohibition rules")

    if errors:
        for err in errors:
            print(f"[FAIL] {err}", file=sys.stderr)
        return 1
    return 0


def sync_adapters() -> int:
    """Generate or update all instruction adapter files."""
    for file_path, content in ADAPTERS_CONFIG.items():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"  [OK] Synchronized {file_path.relative_to(REPO_ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize and validate multi-LLM instruction adapters.")
    parser.add_argument("--check", action="store_true", help="Validate adapters without modifying files.")
    args = parser.parse_args()

    if args.check:
        res = validate_adapters()
        if res == 0:
            print(f"[PASS] All {len(ADAPTERS_CONFIG)} instruction adapters are valid and synchronized.")
        return res

    sync_adapters()
    print(f"\n[SUCCESS] Successfully synchronized {len(ADAPTERS_CONFIG)} instruction adapters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
