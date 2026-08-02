---
agent: 'agent'
description: 'Ingest a source into the wiki'
---

Read the **Ingest workflow** in `.github/copilot-instructions.md` and execute it now.

The user's message may contain a source (URL or path). If no source is present, scan the `raw/` folder for new markdown files and process them.

**CRITICAL Automation Reminders**:
- If the source is a URL, save its content to `raw/<slug>.md` **before** any wiki writes.
- Every concept page you create MUST have OKF frontmatter (`type`, `title`, `description`, `generated: { by: copilot-librarian/1.0, at: <ISO-8601 now> }`).
- Update root `wiki/index.md` using `* [Title](path) - description` (asterisk bullets). Also update the relevant subdirectory `index.md`.
- Prepend a new `## YYYY-MM-DD` section to `wiki/log.md` (newest first).
- **Cleanup (MUST USE TERMINAL)**: Delete the source file from `raw/` after successfully updating the log and index using `rm` or `Remove-Item`. Do NOT use standard file-editing tools for this step.
- Check `log.md` — if this source was already ingested, skip it to avoid duplicates.
- Run the contradiction check before writing.

