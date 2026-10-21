# Google Antigravity & Gemini CLI Instructions — GitHub Copilot LLM Wiki

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
