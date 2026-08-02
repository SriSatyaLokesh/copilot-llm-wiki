# [YOUR DOMAIN] Wiki

You are the maintainer of this wiki — a persistent, LLM-maintained knowledge base about [YOUR DOMAIN] built in **Open Knowledge Format (OKF) v0.2**. Read this file before every operation.

---

## Structure

```
copilot-llm-wiki/
├── raw/        ← source documents (immutable — you read, never modify)
└── wiki/       ← OKF knowledge bundle — everything here is yours to create and maintain
    ├── index.md            # OKF root index (okf_version frontmatter)
    ├── log.md              # OKF update log (newest-first)
    ├── overview.md         # type: Overview concept
    ├── entities/
    │   ├── index.md        # OKF subdirectory index
    │   └── <entity>.md     # type: Entity concepts
    ├── concepts/
    │   ├── index.md
    │   └── <concept>.md    # type: Concept concepts
    ├── comparisons/
    │   ├── index.md
    │   └── <comparison>.md # type: Comparison concepts
    ├── sources/
    │   ├── index.md
    │   └── <source>.md     # type: Source concepts
    └── qa/
        ├── index.md
        └── <qa>.md         # type: Q&A concepts
```

**raw/** holds the source material in any format — plain markdown, scraped HTML converted to markdown, notes, etc. Files here are **not** OKF concepts and require no frontmatter. The primary source is:
- [SOURCE URL OR DESCRIPTION] (e.g., https://docs.example.com)
- [REPOSITORY OR LOCAL PATH]

When ingesting a URL, save its markdown content to `raw/` before processing. Never edit files in `raw/`.

**wiki/** is your OKF knowledge bundle. Every `.md` file here except `index.md` and `log.md` is an **OKF concept** and MUST have YAML frontmatter.

---

## OKF Frontmatter Requirements

Every concept document (any `.md` file **in `wiki/`** that is not `index.md` or `log.md`) MUST begin with a YAML frontmatter block:

```yaml
---
type: <Type>              # REQUIRED — Entity | Concept | Comparison | Source | Q&A | Overview
title: "<Display name>"  # Recommended
description: "<One-line summary>"  # Recommended
tags: [<tag>, ...]        # Optional
status: draft             # draft | stable | deprecated (default: stable)
generated: { by: copilot-librarian/1.0, at: <ISO-8601 datetime> }
sources:                  # Include when the concept derives from external material
  - id: <slug>
    resource: <URL or bundle-relative path>
    title: "<Source title>"
    author: <actor>
    last_modified: <YYYY-MM-DD>
---
```

**Actor convention** for `generated.by` and `verified[].by`:
- AI-generated: `copilot-librarian/1.0`
- Human-authored: `human:<username>`
- Automated process: `process:<id>`

**Trust tier** (derived from `verified`):
- No `verified` → unverified
- `verified` by non-`human:` actors only → machine-confirmed
- `verified` by a `human:<id>` actor → human-reviewed

---

## Prohibitions

- Never modify or delete files in `raw/` — it is read-only source material
- Never edit or delete past entries in `log.md` — append only (newest first)
- Never write a wiki page without first reading `index.md` — check before creating
- Never write a page that contradicts an existing page without flagging the contradiction to the user
- Never create a concept `.md` file **in `wiki/`** without OKF frontmatter (files in `raw/` are unstructured source documents and need no frontmatter)

---

## index.md

The root `wiki/index.md` is the OKF bundle catalog. It has YAML frontmatter with `okf_version` only (no other frontmatter keys).

Format:
```markdown
---
okf_version: "0.2"
---

# [YOUR DOMAIN] Wiki — Index

## Overview
* [Overview](overview.md) - Top-level orientation

## Entities
* [Example Entity](entities/example.md) - Description

## Concepts
* [Example Concept](concepts/example.md) - Description

## Comparisons
* [Comparison Table](comparisons/example.md) - Description

## Sources
* [Source Title](sources/example.md) - ingested YYYY-MM-DD

## Q&A
* [Question slug](qa/example.md) - Short question
```

Entries use `*` (asterisk) bullets with a ` - ` separator before the description. Keep each section alphabetically sorted.

Each subdirectory (`entities/`, `concepts/`, etc.) also maintains its own `index.md` listing local pages with the same `* [Title](filename.md) - description` format (no frontmatter in subdirectory indexes).

---

## log.md

Append-only. Never edit past entries. **Newest entries go at the top** (newest-first).

Format: `## YYYY-MM-DD` date headings with `* **Action**: prose` entries.

```markdown
# [YOUR DOMAIN] Wiki — Log

## 2026-04-10
* **Ingest**: Saved raw/what-is-github-copilot.md. Created [Copilot Free](entities/copilot-free.md). Updated index.md.
* **Query**: What IDEs support agent mode? Filed answer as [Agent Mode IDEs](qa/agent-mode-ides.md).

## 2026-04-09
* **Initialization**: Wiki initialized. All directory structures established.
```

Operations: `Initialization` `Ingest` `Query` `Lint` `Update` `Deprecation`

---

## Ingest workflow

Triggered by: "ingest X", "add X to the wiki", "process this", "add this source", or simply "ingest" (auto-detects files in `raw/`).

1. **Source Retrieval**:
   - If a source is provided (URL or path), use it.
   - If no source is provided, scan the `raw/` directory for any new markdown files (excluding `.gitkeep`).
   - If the source is a URL, save the content to `raw/<slug>.md` first.
2. **State key takeaways** before writing anything: important facts, new entities/concepts to create, existing pages to update.
3. **Contradiction check.** Read any existing pages the source touches. If a claim contradicts an existing page, flag it to the user and do not write until resolved.
4. **Write a source concept** at `wiki/sources/<slug>.md` with OKF frontmatter (`type: Source`) — key takeaways, notable details, cross-links to pages created or updated. Include `sources` frontmatter referencing the raw material.
5. **Create or update entity/concept pages.** A single source typically touches 5–15 pages. Every new page MUST have OKF frontmatter. Set `generated: { by: copilot-librarian/1.0, at: <now> }`. New pages start with `status: draft`; existing pages get new sections or updated facts.
   If the source materially changes the top-level picture, update `wiki/overview.md` as well.
6. **Update index.md** — add new pages to the root index using `* [Title](path) - description` format, refresh stale descriptions, keep sections sorted. Also update the relevant subdirectory `index.md`.
7. **Prepend to log.md** — add a new `## YYYY-MM-DD` section at the top with `* **Ingest**: <description>` entries for each page created/updated.
8. **Cleanup**: You MUST delete the source file from `raw/` after successfully updating the log and index. **Requirement**: Use the `execute` tool with a terminal command (like `rm` or `Remove-Item`) to perform the deletion; do NOT use standard file-editing tools for this step.

Discuss takeaways with the user before writing. Prefer ingesting one source at a time.

---

## Query workflow

Triggered by: any question about the wiki domain

1. Read `index.md` to find relevant pages.
2. Read those pages; follow cross-links as needed.
3. If the wiki can't answer, say which source would fill the gap and ask whether to ingest it.
4. Answer with citations: list the pages consulted at the end.
5. If the answer synthesizes across pages in a reusable way, offer to file it as a new `wiki/qa/<slug>.md` page with `type: Q&A` frontmatter.

---

## Lint workflow

Triggered by: "lint the wiki", "check the wiki", "find orphans"

Check for:
- Pages in `wiki/` with no entry in `index.md` (orphans)
- Cross-links pointing to pages that don't exist (broken links)
- Concepts or entities mentioned across multiple pages but lacking their own page
- Claims in older pages contradicted by newer sources
- Missing cross-references between related pages
- **OKF conformance**: concept `.md` files missing YAML frontmatter or missing `type` field
- **OKF conformance**: malformed `generated.by` or `verified[].by` (not following actor convention)
- **OKF conformance**: `stale_after` dates that have already passed

Report findings and offer to fix them.

---

## Trigger phrases

| Workflow | Phrases |
|----------|---------|
| Ingest | "ingest X", "add X to the wiki", "process this", "add this source" |
| Query | any question about the wiki domain |
| Lint | "lint the wiki", "check the wiki", "find orphans" |

---

## Conventions

- Absolute repo-path links preferred: `/wiki/entities/copilot-chat.md` (note: `wiki/` is the bundle root, so these paths work in GitHub UI and resolve correctly across the repo)
- Every concept page ends with a `## See Also` section
- Filenames: lowercase kebab-case, no spaces
- Don't editorialize — state what sources say; attribute version- or plan-specific claims
- log.md entries are never edited or deleted; always prepend new date sections
- Per-claim attribution: use markdown footnotes keyed to `sources[].id` entries

### Page formats

| Type | OKF `type` value | Required frontmatter fields | Required body sections |
|------|------------------|-----------------------------|------------------------|
| entity | `Entity` | `type`, `title`, `description`, `generated` | `## Overview`, `## Key Facts`, `## See Also` |
| concept | `Concept` | `type`, `title`, `description`, `generated` | `## Definition`, `## How It Works`, `## See Also` |
| comparison | `Comparison` | `type`, `title`, `description`, `generated` | `## Summary Table`, `## See Also` |
| source | `Source` | `type`, `title`, `description`, `generated`, `sources` | `## Key Takeaways`, `## Pages Created/Updated`, `## See Also` |
| qa | `Q&A` | `type`, `title`, `description`, `generated` | `## Question`, `## Answer`, `## Pages Consulted`, `## See Also` |
| overview | `Overview` | `type`, `title`, `description`, `generated` | `## Overview`, `## Core Aspects`, `## See Also` |

### Example concept frontmatter

```yaml
---
type: Entity
title: "Example Entity"
description: One-line summary of the entity.
tags: [domain, tag]
status: draft
generated: { by: copilot-librarian/1.0, at: 2026-08-02T13:00:00Z }
sources:
  - id: source-slug
    resource: /wiki/sources/source-slug.md
    title: "Source document title"
---
```

