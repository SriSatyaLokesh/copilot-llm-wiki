# Claude Code Instructions — GitHub Copilot LLM Wiki

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
