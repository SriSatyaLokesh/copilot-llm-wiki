---
name: wiki-ingest
description: Ingest a source (URL or file) into the LLM-maintained wiki.
---

# Wiki Ingest Skill

When this skill is triggered, follow the **Ingest workflow** defined in `.github/copilot-instructions.md`.

## Workflow Overview

1. **Source Retrieval**: If the source is a URL, fetch the content and save it to `raw/<slug>.md`.
2. **Analysis**: Extract key takeaways, entities, and concepts.
3. **Contradiction Check**: Verify if new findings contradict existing wiki pages. Flag to the user if they do.
4. **Source Page**: Create `wiki/sources/<slug>.md` as an OKF concept with:
   ```yaml
   ---
   type: Source
   title: "<Source title>"
   description: "<One-line summary>"
   tags: [...]
   status: draft
   generated: { by: copilot-librarian/1.0, at: <ISO-8601 now> }
   sources:
     - id: <slug>
       resource: <original URL or path>
       title: "<Source title>"
   ---
   ```
5. **Entity/Concept Updates**: Create or update pages in `wiki/entities/` and `wiki/concepts/`. Every new page MUST have OKF frontmatter (`type`, `title`, `description`, `generated`).
6. **Bookkeeping**:
   - Update root `wiki/index.md` using `* [Title](path) - description` (asterisk bullet) format.
   - Update the relevant subdirectory `index.md` (e.g., `wiki/entities/index.md`).
   - Prepend a new `## YYYY-MM-DD` section to `wiki/log.md` with `* **Ingest**: <description>` entries.
7. **Automated Cleanup**: Once ingestion is successful, delete the source file from `raw/`.
   - **IMPORTANT**: Use the `execute` tool (Terminal) to delete the file (e.g., `rm` or `Remove-Item`). Do NOT use file-edit based deletion tools.

## Operating Modes

- **Manual**: Use this skill when asked to "ingest X" or "add X to the wiki".
- **Batch**: If asked to "ingest everything in raw" or "process all sources", use the `execute` tool to run `.github/skills/wiki-ingest/scripts/intake.sh` or `.github/skills/wiki-ingest/scripts/intake.ps1`.

