---
agent: 'agent'
description: 'Ingest a source into the wiki'
---

Read the **Ingest workflow** in `.github/copilot-instructions.md` and execute it now.

The user's message may contain a source (URL or path). If no source is present, scan the `raw/` folder for new markdown files and process them.

**CRITICAL Automation Reminders**:
- If the source is a URL, save its content to `raw/<slug>.md` **before** any wiki writes.
- **Cleanup (MUST USE TERMINAL)**: You MUST delete the source file from `raw/` after successfully updating the log and index. **Requirement**: Use the `execute` tool with a terminal command (like `rm` or `Remove-Item`) to perform the deletion; do NOT use standard file-editing tools for this step to avoid platform-specific patch errors.
- Check `log.md` -- if this source was already ingested, skip it to avoid duplicates.
- Run the contradiction check before writing.
