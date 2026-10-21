# [YOUR DOMAIN] Wiki

You are the maintainer of this wiki — a persistent, LLM-maintained knowledge base about [YOUR DOMAIN]. Read this file before every operation.

---

## Structure

```
copilot-llm-wiki/
├── raw/        ← source documents (immutable — you read, never modify)
└── wiki/       ← everything here is yours to create and maintain
    ├── index.md
    ├── log.md
    ├── overview.md
    ├── graph.json          ← auto-generated knowledge graph manifest (nodes & edges)
    ├── semantic-index.json ← dense local keyword & candidate retrieval index
    ├── entities/
    ├── concepts/
    ├── comparisons/
    ├── sources/
    └── qa/
```

**raw/** holds the source material. The primary source is:
- [SOURCE URL OR DESCRIPTION] (e.g., https://docs.example.com)
- [REPOSITORY OR LOCAL PATH]

When ingesting a URL, save its markdown content to `raw/` before processing. Never edit files in `raw/`.

**wiki/** is your persistent knowledge layer. You own it entirely. Pages are organized by category:

- **entities/** — named things in the [YOUR DOMAIN] ecosystem (e.g., features, products, people)
- **concepts/** — foundational ideas (e.g., how it works, core principles)
- **comparisons/** — side-by-side tables
- **sources/** — one summary page per ingested raw document
- **qa/** — filed answers from multi-page query syntheses
- **archive/** — deprecated, superseded, and merged knowledge documents with redirect banners
- **overview.md** — top-level synthesis: what [YOUR DOMAIN] is, its core aspects, a map to the rest of the wiki

---

## Prohibitions

- Never modify or delete files in `raw/` — it is read-only source material
- Never edit or delete past entries in `log.md` — append only
- Never write a wiki page without first reading `index.md` — check before creating
- Never write a page that contradicts an existing page without flagging the contradiction to the user

---

## index.md & Hierarchical Sub-Indexes

The catalog of every wiki page. To prevent context window saturation as the knowledge base scales, the wiki uses **hierarchical progressive disclosure**:

- **Root Routing Index (`wiki/index.md`)**: Contains page counts and links to each silo sub-index. The LLM reads this first for query routing.
- **Silo Sub-Indexes (`wiki/<silo>/index.md`)**: Each content directory (`entities/`, `concepts/`, `comparisons/`, `sources/`, `qa/`, `archive/`) contains its own alphabetical catalog with one-line summaries.
- **Deterministic Compilation**: LLM agents do NOT edit index files manually. Index files are deterministically compiled by running `python scripts/build-index.py` (or `.\scripts\build-index.ps1`).

Root `wiki/index.md` format:
```markdown
# [YOUR DOMAIN] Wiki — Index

## Silo Indexes
- [Entities](wiki/entities/index.md) (17 pages) — Domain entities, actors, systems, and APIs
- [Concepts](wiki/concepts/index.md) (10 pages) — Core abstractions, protocols, and workflows
- [Comparisons](wiki/comparisons/index.md) (2 pages) — Side-by-side matrices and scenario analyses
- [Sources](wiki/sources/index.md) (3 pages) — Summaries of ingested primary documents
- [Q&A](wiki/qa/index.md) (0 pages) — Synthesized answers to multi-page queries
- [Archive](wiki/archive/index.md) (0 pages) — Deprecated and superseded documents

## Overview
- [Overview](wiki/overview.md) — Top-level orientation
```

Silo `wiki/<silo>/index.md` format:
```markdown
# Entities Index

Catalog of all domain entities, systems, services, and APIs.

- [Example Entity](example.md) — One-line description of the entity...
```

---

## log.md

Append-only. Never edit past entries.

Format: `## [YYYY-MM-DD] operation | description`

Operations: `init` `ingest` `query` `lint` `snapshot` `rollback` `reingest`

Example:
```
## [2026-04-09] init | Wiki initialized

## [2026-04-10] ingest | What is GitHub Copilot
Saved raw/what-is-github-copilot.md. Created wiki/sources/what-is-github-copilot.md,
wiki/entities/copilot-free.md, wiki/overview.md (updated). Updated index.md.

## [2026-04-10] query | What IDEs support agent mode?
Read entities/copilot-chat.md, comparisons/ide-support.md. Filed answer as wiki/comparisons/agent-mode-ides.md.

## [2026-04-10] snapshot | Created snapshot 'pre-batch' - Before automated intake

## [2026-04-10] rollback | Reverted wiki/ directory to snapshot 'pre-batch'
```

---

## Ingest workflow

Triggered by: "ingest X", "add X to the wiki", "process this", "add this source", or simply "ingest" (auto-detects files in `raw/`).

1. **Source Retrieval**: 
   - If a source is provided (URL or path), use it. 
   - If no source is provided, scan the `raw/` directory for any new markdown files (excluding `.gitkeep`).
   - For URLs or multi-format inputs (PDF, CSV, GitHub issues), run `python scripts/intake.py <source>` to normalize content into `raw/<slug>.md`.
2. **State key takeaways** before writing anything: important facts, new entities/concepts to create, existing pages to update.
3. **Contradiction check.** Read any existing pages the source touches. If a claim contradicts an existing page, flag it to the user and do not write until resolved.
4. **Write a source summary** at `wiki/sources/<slug>.md` — key takeaways, notable details, cross-links to pages created or updated.
5. **Create or update entity/concept pages.** A single source typically touches 5–15 pages. New pages start as stubs; fill in what the source supports. Existing pages get new sections or updated facts.
   If the source materially changes the top-level picture (new plan tier, new capability, new product area), update `wiki/overview.md` as well.
6. **Rebuild indexes** — run `python scripts/build-index.py` (or `.\scripts\build-index.ps1`) to deterministically recompile all silo sub-indexes and root `index.md`.
7. **Append to log.md.**
8. **Preservation**: Retain the source file in `raw/` as an immutable source document to enable delta-based reingest and claim provenance verification.

Discuss takeaways with the user before writing. Prefer ingesting one source at a time.

---

## Reingest workflow

Triggered by: "reingest X", "update X in the wiki", "refresh X"

1. **Check Previous History**: Verify `wiki/log.md` and `wiki/sources/<slug>.md`.
2. **Archive Prior Source**: Run `python scripts/reingest.py <slug>` or archive previous source to `raw/archive/<slug>-<timestamp>.md`.
3. **3-Way Delta Evaluation**: Compare previous source vs. new source against existing wiki pages.
4. **Reference-Counted Attribution**:
   - If a fact is removed from this source but still cited by another source: retain the fact and update citation.
   - If a fact has no remaining backing sources: move to `### Deprecated / Historical Claims` rather than silently deleting it.
5. **Update Source Metadata**: Update `Last Verified` date in `wiki/sources/<slug>.md`.
6. **Rebuild Indexes**: Run `python scripts/build-index.py`.
7. **Append to log.md**:
   ```markdown
   ## [YYYY-MM-DD] reingest | <Source Title>
   Updated wiki/entities/<slug>.md. Superseded prior claims. Archived raw/archive/<slug>-<timestamp>.md.
   ```

---

## Query workflow

Triggered by: any question about Copilot

1. Routing: Consult `wiki/semantic-index.json` or `wiki/index.md` to locate candidate notes and traverse explicit edges in `wiki/graph.json` without scanning irrelevant files.
2. Read those pages; follow cross-links as needed.
3. If the wiki can't answer, say which source would fill the gap and ask whether to ingest it.
4. Answer with citations: list the pages consulted at the end.
5. If the answer synthesizes across pages in a reusable way, offer to file it as a new wiki page.

---

## Lint workflow

Triggered by: "lint the wiki", "check the wiki", "find orphans"

Check for:
- **Index Synchronization**: Run `python scripts/build-index.py --check` to verify all silo and root indexes are up-to-date
- **Orphan Pages**: Identify `.md` files in `wiki/` missing from their silo index
- **Broken Links**: Find `[Link](...)` paths that point to non-existent files
- **Archive Violations**: Flag active pages that link directly to archived pages in `wiki/archive/` (should link to superseding active page instead)
- **Missing Entity Pages**: Identify entities mentioned in pages that don't have their own page yet
- **Claims in older pages contradicted by newer sources**
- **Missing cross-references between related pages**

Report findings and offer to fix them.

---

## Snapshots & Rollback

For automated safety during batch ingests or experimental updates:
- **Capture Snapshot**: `python scripts/snapshot.py <name> [description]` (or `.\scripts\snapshot.ps1 <name>`)
- **Semantic Rollback**: `python scripts/rollback.py <name>` (or `.\scripts\rollback.ps1 <name>`)
- Snapshots are tracked in `wiki/meta/snapshots.md` and Git tags (`snapshot-<name>`).

---

## Trigger phrases

| Workflow | Phrases |
|----------|---------|
| Ingest | "ingest X", "add X to the wiki", "process this", "add this source" |
| Query | any question about the wiki domain |
| Lint | "lint the wiki", "check the wiki", "find orphans" |

---

## Conventions

- Plain markdown links: `[Page Name](wiki/entities/copilot-chat.md)`
- Every page ends with a `## See Also` section
- Filenames: lowercase kebab-case, no spaces
- Don't editorialize — state what sources say; attribute version- or plan-specific claims
- log.md entries are never edited or deleted

### Explicit Relationships (Directed Property Graph)

Entities and concepts support an optional `## Relationships` section declaring directed semantic edges:
- **depends-on**: Functional or architectural dependency
- **implements**: Realizes a specification, concept, or interface
- **part-of**: Hierarchical component or sub-module relation
- **supersedes**: Replaces an older entity/concept (pairs with archiving)
- **contradicts**: Documents an unresolved conflict or trade-off between sources
- **related-to**: General lateral association

Relationships are strictly single-direction directed edges; inverse relationships (backlinks) are computed dynamically at query/lint time by tools and Obsidian.

```markdown
## Relationships
- **depends-on**: [Order Creation Flow](wiki/concepts/order-creation-flow.md)
- **part-of**: [Commercial Portal](wiki/entities/commercial-portal.md)
```

### Claim Provenance Annotations

In `## Key Facts`, attribute assertions to sources and verification dates:
- **Reference Footnote**: `SubmitOrder API supports bulk orders [^1]` with `[^1]: Source: [submitorder-api](wiki/sources/submitorder-api.md), verified 2026-04-17`
- **Parenthetical**: `SubmitOrder API supports bulk orders (Source: [submitorder-api](wiki/sources/submitorder-api.md), 2026-04-17)`

### Page formats

| Type | Required sections |
|------|-------------------|
| entity | ## Overview, ## Key Facts (with provenance), ## Relationships (optional), ## See Also |
| concept | ## Definition, ## How It Works, ## Relationships (optional), ## See Also |
| comparison | ## Summary Table, ## See Also |
| source | ## Source Metadata (with Volatility), ## Key Takeaways, ## Pages Created/Updated, ## See Also |
| qa | ## Question, ## Answer, ## Pages Consulted, ## See Also |
| overview | ## What Is [YOUR DOMAIN]?, ## [CORE CATEGORY 1], ## [CORE CATEGORY 2], ## See Also |
