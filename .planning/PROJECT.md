# LLM Wiki

## What This Is

A forkable template for building LLM-maintained personal knowledge bases using GitHub Copilot as the AI backbone. Instead of re-deriving knowledge from raw documents on every query (RAG), Copilot incrementally builds and maintains a persistent, interlinked wiki of markdown files that compounds with every ingest and every question asked. Users fork the repo, drop in their sources, and Copilot handles all the bookkeeping.

## Core Value

A Copilot librarian that ingests any source, integrates it into a structured wiki, and answers questions from accumulated knowledge — so the wiki gets richer over time instead of starting from scratch on every query.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Copilot-native librarian schema (`copilot-instructions.md`) — precise, testable instructions for ingest, query, and lint workflows that any Copilot surface reads automatically
- [ ] VS Code Chat prompt files (`.github/prompts/`) — reusable `ingest.prompt.md`, `query.prompt.md`, `lint.prompt.md` usable via Copilot Chat attach context
- [ ] Copilot CLI custom librarian agent (`.github/agents/librarian.agent.md`) — dedicated agent for agentic wiki operations from the terminal
- [ ] Agent skills (`.github/skills/`) — specialized skills for wiki tasks (ingest, cross-reference, lint) that Copilot CLI loads automatically
- [ ] CLI intake script (`scripts/intake.sh`) — programmatic ingestion via `copilot -p` for batch or scripted use cases
- [ ] Fork-ready wiki scaffold — empty but well-structured `wiki/` with placeholder pages and clear conventions, ready to use for any domain
- [ ] README and fork guide — step-by-step for anyone forking the pattern to their own domain

### Out of Scope

- Ingesting any specific content domain — users bring their own sources, the template is domain-agnostic
- Claude-specific tooling — this targets Copilot; `.claude/` artifacts are secondary/bonus
- RAG infrastructure (embeddings, vector stores, retrieval pipelines) — index.md + log.md is the intentional navigation layer at moderate scale
- Web scraping automation — manual curation is a deliberate design choice (humans pick sources)
- Backend services, databases, or hosted infrastructure — everything is plain markdown in a git repo

## Context

**Existing state of this repo:**
- `.github/copilot-instructions.md` — librarian schema already written (good starting point, needs refinement and hardening)
- `.claude/commands/intake.md` — Claude Code intake command exists; Copilot equivalent needs to be built
- `wiki/index.md`, `wiki/log.md`, `wiki/overview.md` — 3 stub pages initialized
- `raw/copilot/` — 435 Copilot docs (this project's own domain content, not part of the template)

**Copilot tooling surface:**
- `copilot-instructions.md` — auto-loaded by VS Code Chat, Copilot CLI, Cloud Agent on every request
- `.github/prompts/*.prompt.md` — VS Code Chat prompt files, accessible via Attach Context
- `.github/agents/*.agent.md` — custom CLI agents, invoked with `/agent` or `--agent` flag
- `.github/skills/*.md` — agent skills, loaded by Copilot CLI and Cloud Agent when relevant
- Programmatic CLI: `copilot -p "task" --allow-all-tools` for scripted ingestion

**Conceptual model:** The Vannevar Bush Memex pattern — private, curated, associatively linked knowledge store. Humans curate sources and ask questions. Copilot does all maintenance (summaries, cross-references, contradictions, filing). The wiki is the codebase; Copilot is the programmer; Obsidian is the IDE.

## Constraints

- **Copilot compatibility**: All tooling must work within GitHub Copilot's documented extension points (no Claude/OpenAI-specific primitives)
- **Zero infrastructure**: Works entirely in a cloned git repo — no build tools, servers, or cloud dependencies required
- **Markdown only**: All wiki content is plain markdown — readable without any tooling, diffable, collaborative
- **Forkable by design**: Any user with GitHub Copilot should be able to fork and run this in under 10 minutes

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| `.github/copilot-instructions.md` as primary schema | Auto-loaded by all Copilot surfaces (VS Code, CLI, Cloud Agent) without any user setup | — Pending |
| VS Code prompt files over slash commands | Prompt files work in VS Code Chat with full file context; slash commands require CLI | — Pending |
| Custom librarian agent for CLI | CLI agent gets its own context window — cleaner than stuffing everything into copilot-instructions.md | — Pending |
| index.md + log.md as navigation layer | Avoids embedding/RAG infrastructure; works well up to ~hundreds of pages per Copilot's context window | — Pending |
| No RAG — compiled wiki pattern | Knowledge compiled once, compounding; avoids re-deriving on every query | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-10 after initialization*
