# Architecture Research

## Component Map

Six Copilot extension points are relevant to the wiki template. Each has a distinct role, load trigger, and surface coverage.

| Component | File Location | Load Trigger | Surfaces | Role in Wiki |
|-----------|--------------|--------------|----------|--------------|
| Custom instructions | `.github/copilot-instructions.md` | Automatic — every request | VS Code ✓, CLI ✓, GitHub.com ✓, JetBrains P | Core librarian identity: conventions, structure, operation summaries |
| Prompt files | `.github/prompts/*.prompt.md` | Manual — user picks via Attach Context | VS Code ✓, Visual Studio ✓, JetBrains P | Deep workflow prompts: ingest, query, lint (VS Code only) |
| Custom agents | `.github/agents/librarian.agent.md` | Manual or by inference | VS Code ✓, CLI ✓, GitHub.com ✓ | Dedicated librarian persona for agentic CLI sessions |
| Agent skills | `.github/skills/<name>/SKILL.md` | Automatic — Copilot picks when relevant | VS Code ✓, CLI ✓, GitHub.com ✓ | Bundled step-by-step workflows with assets; preferred for CLI/Cloud Agent |
| Hooks | `.github/hooks/*.json` | Automatic at lifecycle events | CLI ✓, GitHub.com P | Optional: audit logging, pre-write validation |
| AGENTS.md | `AGENTS.md` (repo root) | Automatic — agent-compatible runtimes | Cross-vendor (Claude, Gemini, Codex) | Compatibility alias for copilot-instructions.md |

> Source: `.planning/research/STACK.md` + `customization-cheat-sheet.md`

---

## Component Responsibilities

Each component has a lane. Overlap creates bloat and inconsistency.

**`copilot-instructions.md` — Identity layer**
- What the wiki is and who the librarian is (2-3 sentences)
- Directory structure (raw/, wiki/, sub-dirs)
- Non-negotiable conventions: filenames, link format, page endings, log format
- Trigger phrases for operations (e.g. "ingest X", "query:", "lint the wiki")
- Pointers to prompt files / skills for detail (not the detail itself)
- **Hard limit: ≤ 2 pages (Copilot quality degrades past ~1,000 lines; this file loads on EVERY request)**

**`.github/prompts/*.prompt.md` — Workflow depth layer (VS Code)**
- `ingest.prompt.md`: full step-by-step ingest flow with edge case handling
- `query.prompt.md`: query + file-the-answer loop
- `lint.prompt.md`: full health-check checklist
- Can reference other files: `#file:.github/copilot-instructions.md`

**`.github/agents/librarian.agent.md` — CLI persona layer**
- Description field for automatic inference
- Full librarian instructions optimized for CLI agentic sessions
- Tool restrictions (e.g. deny writes to raw/)
- Used with: `copilot --agent librarian -p "ingest X"`

**`.github/skills/` — Portable workflow layer**
- `wiki-ingest/SKILL.md`: ingest workflow, cross-runtime (VS Code + CLI + Cloud Agent)
- `wiki-lint/SKILL.md`: lint workflow
- Skills are loaded just-in-time — don't pollute main context
- Preferred for complex multi-step work that should survive context resets

**`scripts/intake.sh`** — Programmatic layer
- Wraps `copilot -p "..." --allow-all-tools`
- Accepts file path or URL argument
- Handles batch mode: scan raw/ for unprocessed files

---

## Data Flow

### Ingest
```
User: "ingest raw/article.md"
  → copilot-instructions.md loads (Copilot sees librarian identity)
  → Copilot triggers wiki-ingest skill (if via CLI/Cloud Agent)
    OR user uses ingest.prompt.md (if VS Code Chat)
  → LLM reads raw/article.md in full
  → Extracts key takeaways, entities, concepts
  → Discusses with user (interactive) OR proceeds (batch/programmatic)
  → Writes wiki/sources/<slug>.md
  → Creates/updates wiki/entities/, wiki/concepts/, wiki/comparisons/ pages
  → Updates wiki/index.md (sorted, one-line entries)
  → Appends to wiki/log.md (## [YYYY-MM-DD] ingest | title)
  → Reports: sources ingested, pages created, pages updated
```

### Query
```
User: "what does X do?" or "compare A and B"
  → copilot-instructions.md loads
  → Copilot reads wiki/index.md first
  → Reads relevant pages (follows cross-links as needed)
  → Answers with citations
  → If answer synthesizes usefully → offers to file as wiki/qa/<slug>.md
  → Updates wiki/index.md and wiki/log.md
```

### Lint
```
User: "lint the wiki" or "check the wiki"
  → Copilot triggers wiki-lint skill OR lint.prompt.md
  → Scans wiki/ for: orphans, broken links, stale claims, missing pages,
    entities mentioned without their own page, gaps for web search
  → Reports findings with fix suggestions
  → Optionally fixes in-place on user approval
```

---

## Build Order

Phase dependencies flow in this order — each layer depends on the one before.

```
Phase 1: Core schema + wiki scaffold
  ├── copilot-instructions.md (refined, production-ready)
  ├── wiki/ directory structure + placeholder pages
  ├── AGENTS.md (cross-vendor alias)
  └── .github/instructions/ (path-specific, optional)

Phase 2: VS Code workflow depth
  ├── .github/prompts/ingest.prompt.md
  ├── .github/prompts/query.prompt.md
  └── .github/prompts/lint.prompt.md
  (depends on Phase 1 schema being stable)

Phase 3: CLI / agentic layer
  ├── .github/agents/librarian.agent.md
  ├── .github/skills/wiki-ingest/SKILL.md
  └── .github/skills/wiki-lint/SKILL.md
  (depends on Phase 1 conventions, Phase 2 for workflow reference)

Phase 4: Intake script + automation
  ├── scripts/intake.sh
  └── Optional: .github/hooks/ for audit logging
  (depends on agent being stable)

Phase 5: Fork-ready template
  ├── README.md (fork guide, 10-minute setup)
  ├── Placeholder wiki/ pages stripped to domain-agnostic stubs
  └── TEMPLATE.md (customization instructions)
  (depends on all components being stable and tested)
```

---

## Fork Structure

What ships in the template repo when someone forks:

```
.
├── .github/
│   ├── copilot-instructions.md   ← librarian schema (EDIT: adapt to your domain)
│   ├── agents/
│   │   └── librarian.agent.md    ← CLI librarian agent (ready to use)
│   ├── prompts/
│   │   ├── ingest.prompt.md      ← VS Code Chat ingest workflow
│   │   ├── query.prompt.md       ← VS Code Chat query workflow
│   │   └── lint.prompt.md        ← VS Code Chat lint workflow
│   └── skills/
│       ├── wiki-ingest/
│       │   └── SKILL.md          ← ingest skill (VS Code + CLI + Cloud Agent)
│       └── wiki-lint/
│           └── SKILL.md          ← lint skill
├── AGENTS.md                     ← cross-vendor alias
├── README.md                     ← fork guide
├── scripts/
│   └── intake.sh                 ← CLI intake script
├── raw/
│   └── .gitkeep                  ← drop your sources here
└── wiki/
    ├── index.md                  ← starts empty, Copilot fills it
    ├── log.md                    ← starts empty, Copilot fills it
    ├── overview.md               ← stub, Copilot fills on first ingest
    ├── entities/                 ← directory only, Copilot creates pages
    ├── concepts/                 ← directory only
    ├── comparisons/              ← directory only
    ├── sources/                  ← directory only
    └── qa/                       ← directory only (filed query answers)
```

**User's only setup task:** Edit `copilot-instructions.md` to describe their domain and replace placeholder wiki structure comments. Then drop a source in `raw/` and run intake.

---

## Context Window Strategy

The wiki grows; context windows don't. The index.md pattern handles this.

| Scale | Strategy |
|-------|----------|
| < 50 pages | `index.md` alone is sufficient — read on every query |
| 50-200 pages | Read index first, then drill into relevant pages only |
| 200-500 pages | Consider splitting index into sub-indexes by category |
| 500+ pages | Add qmd (BM25/vector search CLI) or similar; LLM reads index + search results |

**Implemented patterns in the schema:**
- Query workflow always reads `index.md` first (not all pages)
- Ingest only reads pages it's updating (not the whole wiki)
- Lint can be scoped: "lint entities only" or "lint sources added this week"
- `log.md` stays parseable: `grep "^## \[" log.md | tail -20` for recent history
