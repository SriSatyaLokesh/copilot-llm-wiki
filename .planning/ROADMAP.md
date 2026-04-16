# Roadmap: LLM Wiki

**Milestone:** v1.0 — Copilot-native LLM wiki template
**Requirements:** .planning/REQUIREMENTS.md
**Config:** Standard granularity, YOLO mode, parallel execution

---

## Overview

Five phases that build from the inside out: schema and wiki structure first (the foundation every Copilot surface reads), then VS Code prompt files (the primary user-facing surface), then CLI agent and skills (the terminal surface), then the intake script (automation layer), and finally the fork-ready packaging that makes the whole thing shareable.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Schema & Wiki Scaffold** - Define librarian schema and initialize the wiki directory structure that all Copilot surfaces read
- [x] **Phase 2: VS Code Prompt Files** - Build ingest, query, and lint prompt files for VS Code Chat
- [x] **Phase 3: CLI Agent & Skills** - Build the librarian agent and wiki skills for Copilot CLI and Cloud Agent
- [x] **Phase 4: CLI Intake Script** - Write the shell intake script for programmatic and batch ingestion
- [x] **Phase 5: Fork-Ready Template** - Package the template with README, placeholders, and customization guide
- [x] **Phase 6: Master Blueprint** - Generate detailed PRD and TRD for full project recreation

## Phase Details

### Phase 1: Schema & Wiki Scaffold
**Goal**: The librarian schema is defined and the wiki scaffold exists so Copilot knows its role, constraints, and where everything lives
**Depends on**: Nothing (first phase)
**Requirements**: SCHEMA-01, SCHEMA-02, SCHEMA-03, SCHEMA-04, WIKI-01, WIKI-02, WIKI-03, WIKI-04, WIKI-05
**Success Criteria** (what must be TRUE):
  1. User can open `docs/PRD.md` and see the librarian role, directory layout, naming conventions, and trigger phrases — all within 2 pages
  2. A unified `docs/PRD.md` explaining the vision, rules, and prompt library.
  3. A unified `docs/TRD.md` detailing every file spec, tool mapping, and workflow logic.
  4. User can see an explicit prohibition list in the schema (no writes to raw/, no editing past log entries, no writing without checking index)
  5. User can see that contradiction check is listed as a mandatory step before any ingest write
  6. User can open `AGENTS.md` at repo root and see the same librarian instructions mirrored for cross-vendor compatibility
  7. User can see a complete `wiki/` scaffold with index.md, log.md, overview.md, and empty subdirectories (entities/, concepts/, comparisons/, sources/, qa/) — plus `raw/` with `.gitkeep`
**Plans:** 3 plans

Plans:
- [x] 01-01-PLAN.md — Refine docs/PRD.md: add Prohibitions, Contradiction check step, Trigger phrases, Page formats table, qa/ to tree
- [x] 01-02-PLAN.md — Create AGENTS.md as literal copy of final docs/PRD.md
- [x] 01-03-PLAN.md — Complete wiki scaffold: create qa/ dir, add QA section to index.md, add format-spec comment to log.md

---

### Phase 2: VS Code Prompt Files
**Goal**: Users can invoke ingest, query, and lint from VS Code Chat by attaching the relevant prompt file
**Depends on**: Phase 1
**Requirements**: INGEST-01, INGEST-03, INGEST-04, QUERY-01, QUERY-02, LINT-01
**Success Criteria** (what must be TRUE):
  1. User can attach `ingest.prompt.md` in VS Code Chat and have Copilot run the full ingest flow: read source, check log, state takeaways, write source summary, create/update entity and concept pages, update index, append to log
  2. User can run ingest on a URL and see the raw content saved to `raw/<slug>.md` before any wiki pages are written
  3. User can run ingest on a source already in log.md and see Copilot skip or flag it rather than duplicate
  4. User can attach `query.prompt.md` and get an answer that cites specific wiki pages consulted, with an offer to file the synthesis as `wiki/qa/<slug>.md`
  5. User can attach `lint.prompt.md` and get a report listing orphan pages, broken links, missing See Also sections, and contradictions
**Plans:** 2 plans

Plans:
- [x] 02-01-PLAN.md — Create VS Code workspace settings and ingest prompt file (thin trigger for ingest workflow with edge case reminders)
- [x] 02-02-PLAN.md — Create query and lint prompt files (trailing citation format, conditional filing offer, 6-check structured lint checklist)

---

### Phase 3: CLI Agent & Skills
**Goal**: Users can run ingest and lint from Copilot CLI using the librarian agent or individual wiki skills
**Depends on**: Phase 1
**Requirements**: AGENT-01, AGENT-02, AGENT-03, INGEST-02, LINT-02
**Success Criteria** (what must be TRUE):
  1. User can invoke the librarian agent from Copilot CLI and have it handle ingest, query, and lint requests using the agent's own context window
  2. User can have Copilot CLI auto-infer the librarian agent from natural language requests because the agent description contains specific trigger phrases
  3. User can confirm that the agent prohibits writes to `raw/` (either via tool restriction or explicit instruction)
  4. User can trigger wiki ingest from CLI using the `wiki-ingest` skill, with the same edge case handling as the VS Code prompt
  5. User can trigger wiki lint from CLI using the `wiki-lint` skill with the same checklist as the VS Code prompt
**Plans**: TBD

Plans:
- [x] 03-01: Write `librarian.agent.md` — agent definition with persona, trigger phrases, ingest/query/lint capability, and raw/ write prohibition
- [x] 03-02: Write `wiki-ingest/SKILL.md` — ingest skill for CLI/Cloud Agent with trigger phrases and full ingest workflow including edge cases
- [x] 03-03: Write `wiki-lint/SKILL.md` — lint skill for CLI/Cloud Agent with trigger phrases and full lint checklist

---

### Phase 4: CLI Intake Script
**Goal**: Users can ingest a single source or batch-process all unprocessed sources in raw/ by running a shell script
**Depends on**: Phase 3
**Requirements**: CLI-01, CLI-02, CLI-03
**Success Criteria** (what must be TRUE):
  1. User can run `scripts/intake.sh <file-or-url>` and have it invoke `copilot -p "ingest <arg>" --allow-all-tools` automatically
  2. User can run `scripts/intake.sh` with no arguments and have it scan `raw/` for files not yet listed in `wiki/log.md`, processing each in sequence
  3. User can run the script on macOS, Linux, and WSL without modification
**Plans**: TBD

Plans:
- [x] 04-01: Write `scripts/intake.sh` — single-source mode, batch mode, cross-platform compatibility (macOS/Linux/WSL)

---

### Phase 5: Fork-Ready Template
**Goal**: Any user with GitHub Copilot can fork the repo, follow the README, and have a working wiki in under 10 minutes
**Depends on**: Phase 4
**Requirements**: FORK-01, FORK-02, FORK-03, FORK-04
**Success Criteria** (what must be TRUE):
  1. User can follow the README step-by-step (fork → open in VS Code → enable prompt files → drop first source in raw/ → run ingest) and complete the flow in under 10 minutes
  2. User can find the exact VS Code setting (`"chat.promptFiles": true`) and the CLI agent restart note in the README
  3. User can search `docs/PRD.md` for `[YOUR DOMAIN]` and find every section that needs domain-specific customization clearly marked
  4. User can open `TEMPLATE.md` and see a clear list of what to change (schema domain sections, placeholder wiki pages) versus what to leave alone (ingest/query/lint logic, index/log format)
**Plans**: TBD

Plans:
- [x] 05-01: Write `README.md` — 10-minute fork guide with exact VS Code setting, CLI restart note, and step-by-step walkthrough
- [x] 05-02: Add `[YOUR DOMAIN]` placeholder comments to `docs/PRD.md`; write `TEMPLATE.md` customization guide

---

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Schema & Wiki Scaffold | 3/3 | Complete | 2026-04-10 |
| 2. VS Code Prompt Files | 2/2 | Complete | 2026-04-10 |
| 3. CLI Agent & Skills | 3/3 | Complete | 2026-04-16 |
| 4. CLI Intake Script | 1/1 | Complete | 2026-04-16 |
| 5. Fork-Ready Template | 2/2 | Complete | 2026-04-16 |
