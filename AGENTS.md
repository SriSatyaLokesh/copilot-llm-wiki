# GitHub Copilot Wiki

You are the maintainer of this wiki — a persistent, LLM-maintained knowledge base about GitHub Copilot. Read this file before every operation.

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

**raw/** holds the source material. The primary source is the GitHub Copilot docs:
- https://docs.github.com/en/copilot
- Repository: https://github.com/github/docs (`content/copilot/`)

When ingesting a URL, save its markdown content to `raw/` before processing. Never edit files in `raw/`.

**wiki/** is your persistent knowledge layer. You own it entirely. Pages are organized by category:

- **entities/** — named things in the Copilot ecosystem: features (Copilot Chat, inline suggestions, agent mode, code review, Copilot CLI, Spark, Spaces), plans (Free, Pro, Pro+, Business, Enterprise), AI models (GPT-4o, Claude Sonnet, Gemini), IDEs and environments (VS Code, JetBrains, Visual Studio, Xcode, NeoVim, GitHub.com, mobile, terminal)
- **concepts/** — foundational ideas: how completions work, context, prompting, MCP, rate limits, billing, content exclusion, responsible use, custom instructions
- **comparisons/** — side-by-side tables: plans, AI models, IDE feature support
- **sources/** — one summary page per ingested raw document
- **qa/** — filed answers from multi-page query syntheses
- **overview.md** — top-level synthesis: what Copilot is, its capabilities, its plan tiers, a map to the rest of the wiki

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
# GitHub Copilot Wiki — Index

## Entities
- [Copilot Chat](wiki/entities/copilot-chat.md) — AI chat assistant across IDE, GitHub.com, mobile, and terminal
- [Copilot Enterprise](wiki/entities/copilot-enterprise.md) — Enterprise plan with knowledge bases and fine-tuned models

## Concepts
- [Context](wiki/concepts/context.md) — What Copilot sends with each request and how to shape it

## Comparisons
- [Plans](wiki/comparisons/plans.md) — All six Copilot plans side by side

## Sources
- [What is GitHub Copilot](wiki/sources/what-is-github-copilot.md) — ingested 2026-04-09

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

Triggered by: "ingest X", "add X to the wiki", "process this", "add this source"

1. **Read the source** in full. If it's a URL, save the content to `raw/<slug>.md` first.
2. **State key takeaways** before writing anything: important facts, new entities/concepts to create, existing pages to update.
3. **Contradiction check.** Read any existing pages the source touches. If a claim contradicts an existing page, flag it to the user and do not write until resolved.
4. **Write a source summary** at `wiki/sources/<slug>.md` — key takeaways, notable details, cross-links to pages created or updated.
5. **Create or update entity/concept pages.** A single source typically touches 5–15 pages. New pages start as stubs; fill in what the source supports. Existing pages get new sections or updated facts.
   If the source materially changes the top-level picture (new plan tier, new capability, new product area), update `wiki/overview.md` as well.
6. **Update index.md** — add new pages, refresh stale descriptions, keep sections sorted.
7. **Append to log.md.**

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
| overview | ## What Is GitHub Copilot?, ## Core Capabilities, ## Plans at a Glance, ## See Also |
