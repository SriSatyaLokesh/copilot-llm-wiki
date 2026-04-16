# Pitfalls Research

## Instruction File Failures

**`copilot-instructions.md` is loaded on every Copilot request in the repo — including coding tasks unrelated to the wiki.** An overloaded schema doesn't just degrade wiki operations; it degrades the user's coding assistant. This is the #1 failure mode.

| Pitfall | Warning Sign | Prevention |
|---------|-------------|------------|
| Schema too long | Responses feel sluggish; Copilot ignores conventions | Hard cap at ~2 pages (the file loads on every request). Move workflow depth to skills/prompts |
| Vague conventions | LLM creates pages in different formats each session | Specify exactly: filename format, required sections, link syntax, how log entries are written |
| Missing prohibition list | LLM edits `raw/`, deletes old log entries, skips index update | Explicit "NEVER" list: never modify raw/, never edit past log entries, never write without checking index |
| No contradiction gate | New ingest silently overwrites correct claims | Make pre-write contradiction check explicit in ingest workflow ("before writing, check if any takeaway contradicts existing pages") |
| Instructions only describe happy path | LLM stalls on edge cases (empty wiki, single page, broken link) | Document at least: first-run behavior, source not found, page already exists |

---

## Wiki Degradation Patterns

LLM wikis rot when maintenance is inconsistent. Common degradation paths:

**Broken cross-links** — Pages reference other pages by name that later get renamed or deleted.
- Prevention: Use relative markdown links consistently; lint catches broken links
- Which phase: Phase 1 (establish link conventions), Phase 3 (lint skill checks them)

**Stale index.md** — New pages exist but aren't listed in index; old entries describe pages that have changed.
- Prevention: Ingest workflow must always end with an index update step; lint scans for orphans
- Warning sign: Index has fewer entries than wiki/ directory has files

**log.md becoming unreadable** — Unbounded growth; LLM can't efficiently find last ingest date.
- Prevention: Enforce `## [YYYY-MM-DD] operation | title` prefix. Parseable with grep.
- At scale: Add "last 30 days" view: `grep "^## \[" log.md | tail -30`

**Inconsistent page formats** — Each ingest session produces differently structured pages.
- Prevention: Require every page type to end with `## See Also`. Lint checks for missing sections.
- Deeper prevention: Include example page structure in the ingest skill (not copilot-instructions.md)

**Contradiction drift** — Newer source contradicts an older page; old page not updated.
- Prevention: Ingest step 2 must be "state contradictions before writing anything." Lint periodically scans.

**Summary pages replacing source pages** — LLM writes a summary that compresses away nuance; original raw source is the only recovery path.
- Prevention: raw/ is immutable. Always append to existing pages rather than rewriting from scratch.

---

## Fork/Adoption Failures

Templates fail at the seam between "author's domain" and "fork user's domain."

| Failure | Root Cause | Fix |
|---------|-----------|-----|
| Schema too domain-specific | copilot-instructions.md full of GitHub Copilot references; hard to adapt | Keep schema domain-agnostic. Use `[YOUR DOMAIN]` placeholders for domain-specific sections |
| No first-run experience | New user forks, opens VS Code, doesn't know what to do first | README must be a 10-minute walkthrough: fork → open in VS Code → enable prompt files → drop a source → run ingest |
| Dual-LLM confusion | Repo has both `.claude/commands/` and `.github/` Copilot tooling; fork users don't know which to use | README explicitly maps: Claude Code → use `.claude/commands/intake.md`; Copilot → use prompt files / skills / agent |
| Prompt files not working | User didn't enable `"chat.promptFiles": true` in VS Code settings | README includes the exact setting toggle (one-line JSON) as step 1 |
| Agent not found in CLI | User runs `copilot --agent librarian` but CLI was never restarted after adding agent file | Document: restart CLI after adding `.github/agents/*.agent.md` |
| Skills not triggering | Skill name or trigger description too vague | SKILL.md `description` field must contain specific trigger phrases matching how users naturally phrase ingest/lint requests |

---

## Copilot-Specific Gotchas

Confirmed from official Copilot docs in `D:\professional\code\learn\docs\content\copilot\`:

**Prompt files require explicit opt-in.**
`"chat.promptFiles": true` must be in workspace `settings.json`. The `.github/prompts/` folder is not scanned without it. Prompt files are VS Code only — not available in CLI or GitHub.com chat.

**Prompt files are NOT available in Copilot CLI or GitHub.com.**
They are a VS Code / Visual Studio feature. The skills layer (`.github/skills/`) is the cross-surface equivalent for CLI and Cloud Agent. Both are needed.

**Custom agents require a CLI restart to load.**
Adding `.github/agents/librarian.agent.md` during a session will not take effect until the CLI is restarted. Document this explicitly.

**copilot-instructions.md practical limit is ~1,000 lines.**
GitHub's own docs warn about quality degradation. Confirmed: the cheat sheet recommends keeping it under 2 pages and moving depth to skills.

**Skills are loaded just-in-time by Copilot, not by the user.**
The `SKILL.md` `description` field is what Copilot reads to decide whether to load the skill. If the description is vague, the skill won't trigger. Be specific: "Use this skill when the user asks to ingest a source, process a document, or add something to the wiki."

**Copilot Memory (agentic memory) is Pro/Pro+ only, and off by default for orgs.**
The wiki's log.md + index.md pattern must work WITHOUT Copilot Memory enabled. Memory is a nice-to-have enhancement, not a foundation.

**AGENTS.md at repo root provides cross-vendor compatibility (Claude, Gemini, Codex).**
Same content as copilot-instructions.md. Symlink or duplicate is an implementation choice. Helps forks work with other LLMs out of the box.

**Hooks require `.github/hooks/*.json` format** (not YAML). Format:
```json
{"version": 1, "hooks": {"preToolUse": [{"type": "command", "bash": "./scripts/hook.sh"}]}}
```
Hooks need `jq` in PATH. Only available on CLI (v) and GitHub.com (preview). Skip for v1.

---

## Intake Workflow Failures

**LLM touches too many files in one pass.**
A single rich source can legitimately update 10-15 wiki pages. This is expected and correct — but Copilot may stall or lose coherence on very long sessions.
- Prevention: Ingest one source at a time (default). Batch mode is explicitly "less supervised" and documented as such.

**Lost track of what's been ingested.**
Without log.md, re-ingesting a source creates duplicate summaries and conflicting page updates.
- Prevention: Ingest workflow step 1: check `wiki/log.md` to see if this source was already ingested. If yes, ask user whether to re-ingest.

**URL sources become stale.**
A URL ingested today may 404 next month.
- Prevention: Always save URL content to `raw/<slug>.md` before processing. The raw file is the permanent record.

**LLM summarizes instead of integrating.**
On large sources, LLM may write a summary page without creating individual entity/concept pages — missing the compounding value.
- Prevention: Ingest instructions must be explicit: "a single source typically touches 5-15 wiki pages." After writing the source summary, always list which entity/concept pages were created or updated.

**Contradictions silently resolved by recency.**
New source says X; old page says not-X. LLM updates old page without flagging the change.
- Prevention: Step 2 of ingest must surface contradictions before writing. The updated page should note the contradiction and which source is newer.
