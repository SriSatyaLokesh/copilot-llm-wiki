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
- **overview.md** — top-level synthesis: what [YOUR DOMAIN] is, its core aspects, a map to the rest of the wiki

---

## Prohibitions

- Never modify or delete files in `raw/` — it is read-only source material
- Never edit or delete past entries in `log.md` — append only
- Never write a wiki page without first reading `index.md` — check before creating
- Never write a page that contradicts an existing page without flagging the contradiction to the user

---

## index.md

The catalog of every wiki page. Updated on every ingest. The LLM reads this first when answering any query.

Format:
```markdown
# [YOUR DOMAIN] Wiki — Index

## Entities
- [Example Entity](wiki/entities/example.md) — Description

## Concepts
- [Example Concept](wiki/concepts/example.md) — Description

## Comparisons
- [Comparison Table](wiki/comparisons/example.md)

## Sources
- [Source Title](wiki/sources/example.md) — ingested YYYY-MM-DD

## Overview
- [Overview](wiki/overview.md) — Top-level orientation
```

One line per entry. Keep each section alphabetically sorted.

---

## log.md

Append-only. Never edit past entries.

Format: `## [YYYY-MM-DD] operation | description`

Operations: `init` `ingest` `query` `lint`

Example:
```
## [2026-04-09] init | Wiki initialized

## [2026-04-10] ingest | What is GitHub Copilot
Saved raw/what-is-github-copilot.md. Created wiki/sources/what-is-github-copilot.md,
wiki/entities/copilot-free.md, wiki/overview.md (updated). Updated index.md.

## [2026-04-10] query | What IDEs support agent mode?
Read entities/copilot-chat.md, comparisons/ide-support.md. Filed answer as wiki/comparisons/agent-mode-ides.md.
```

---

## Ingest workflow

Triggered by: "ingest X", "add X to the wiki", "process this", "add this source", or simply "ingest" (auto-detects files in `raw/`).

1. **Source Retrieval**: 
   - If a source is provided (URL or path), use it. 
   - If no source is provided, scan the `raw/` directory for any new markdown files (excluding `.gitkeep`).
   - If the source is a URL, save the content to `raw/<slug>.md` first.
2. **State key takeaways** before writing anything: important facts, new entities/concepts to create, existing pages to update.
3. **Contradiction check.** Read any existing pages the source touches. If a claim contradicts an existing page, flag it to the user and do not write until resolved.
4. **Write a source summary** at `wiki/sources/<slug>.md` — key takeaways, notable details, cross-links to pages created or updated.
5. **Create or update entity/concept pages.** A single source typically touches 5–15 pages. New pages start as stubs; fill in what the source supports. Existing pages get new sections or updated facts.
   If the source materially changes the top-level picture (new plan tier, new capability, new product area), update `wiki/overview.md` as well.
6. **Update index.md** — add new pages, refresh stale descriptions, keep sections sorted.
7. **Append to log.md.**
8. **Cleanup**: You MUST delete the source file from `raw/` after successfully updating the log and index. **Requirement**: Use the `execute` tool with a terminal command (like `rm` or `Remove-Item`) to perform the deletion; do NOT use standard file-editing tools for this step.

Discuss takeaways with the user before writing. Prefer ingesting one source at a time.

---

## Query workflow

Triggered by: any question about Copilot

1. Read `index.md` to find relevant pages.
2. Read those pages; follow cross-links as needed.
3. If the wiki can't answer, say which source would fill the gap and ask whether to ingest it.
4. Answer with citations: list the pages consulted at the end.
5. If the answer synthesizes across pages in a reusable way, offer to file it as a new wiki page.

---

## Lint workflow

Triggered by: "lint the wiki", "check the wiki", "find orphans"

Check for:
- Pages in `wiki/` with no entry in `index.md` (orphans)
- Cross-links pointing to pages that don't exist
- Concepts or entities mentioned across multiple pages but lacking their own page
- Claims in older pages contradicted by newer sources
- Missing cross-references between related pages

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

- Plain markdown links: `[Page Name](wiki/entities/copilot-chat.md)`
- Every page ends with a `## See Also` section
- Filenames: lowercase kebab-case, no spaces
- Don't editorialize — state what sources say; attribute version- or plan-specific claims
- log.md entries are never edited or deleted

### Page formats

| Type | Required sections |
|------|-------------------|
| entity | ## Overview, ## Key Facts, ## See Also |
| concept | ## Definition, ## How It Works, ## See Also |
| comparison | ## Summary Table, ## See Also |
| source | ## Key Takeaways, ## Pages Created/Updated, ## See Also |
| qa | ## Question, ## Answer, ## Pages Consulted, ## See Also |
| overview | ## What Is [YOUR DOMAIN]?, ## [CORE CATEGORY 1], ## [CORE CATEGORY 2], ## See Also |
