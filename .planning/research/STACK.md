# Stack Research

**Project:** Copilot-native LLM wiki template
**Researched:** 2026-04-10
**Sources:** Local GitHub Copilot docs mirror at `D:\professional\code\learn\docs\content\copilot\`
**Confidence:** HIGH — all claims sourced directly from official Copilot documentation

---

## Copilot Extension Points (with exact formats)

### 1. `.github/copilot-instructions.md` — Repository-wide custom instructions

**What it is:** Always-on context injected into every Copilot interaction in the repo scope.
**When it loads:** Automatically on every request — chat, agent mode, CLI sessions, cloud agent. No user action needed.
**What it controls:** Global behavior: role, output style, wiki schema, workflow triggers, naming conventions.
**Scope:** All surfaces — VS Code, JetBrains (preview), Visual Studio, CLI, GitHub.com.
**Format:** Plain markdown. No frontmatter. Natural language only. Limit: 2 pages is the recommended practical cap (the cloud agent onboarding prompt explicitly targets this).

```markdown
# GitHub Copilot Wiki

You are the maintainer of this wiki...

## Structure
...

## Ingest workflow
Triggered by: "ingest X"
...
```

**Notes:**
- Copilot adds the file as a reference visible in chat (expandable "References" list)
- If both `copilot-instructions.md` and `AGENTS.md` exist at repo root, both are loaded
- Precedence (lowest to highest): org instructions → agent instructions (AGENTS.md) → repo-wide (copilot-instructions.md) → path-specific → personal instructions
- CLI flag `--no-custom-instructions` can suppress loading

---

### 2. `.github/instructions/*.instructions.md` — Path-specific custom instructions

**What it is:** Instructions that apply only when Copilot is working on files matching a glob pattern.
**When it loads:** Automatically when the file Copilot is editing matches the `applyTo` glob in frontmatter.
**What it controls:** Language-specific rules, framework conventions, or per-directory behavior.
**Scope:** VS Code, Visual Studio, CLI, GitHub.com (cloud agent and code review only as of 2026-04).
**Format:** Markdown with YAML frontmatter containing `applyTo` glob.

```markdown
---
applyTo: "**/*.py"
---

# Python Coding Conventions

- Use snake_case for variables
- Follow PEP 8
```

```markdown
---
applyTo: "**/tests/*.spec.ts"
---

## Playwright test requirements
...
```

**Notes:**
- File name: `<descriptive-name>.instructions.md`, stored anywhere in `.github/instructions/`
- When `applyTo` matches AND `copilot-instructions.md` exists, both are loaded together
- Conflicts between them are resolved non-deterministically — avoid contradictions
- The `applyTo` value is a glob pattern relative to repo root (supports `**`, `{}` expansion)

---

### 3. `.github/prompts/*.prompt.md` — Prompt files (reusable prompt templates)

**What it is:** Reusable, manually-invoked prompt templates with optional input variables.
**When it loads:** Manual only — user selects via chat paperclip / "Prompt..." picker, or types `/prompt-name` in VS Code chat.
**What it controls:** A specific repeatable task run with different inputs each time.
**Scope:** VS Code (GA), Visual Studio (GA), JetBrains (preview). Not available in CLI or GitHub.com chat.
**Requires:** VS Code setting `"chat.promptFiles": true` must be enabled.
**Format:** Markdown. Supports optional YAML frontmatter with `agent` and `description` fields. Supports `${input:variable_name:prompt_text}` for user-supplied values.

```markdown
---
agent: 'agent'
description: 'Generate unit tests for selected functions or methods'
---

Analyze the selected function and generate focused unit tests.

Target function: ${input:function_name:Which function should be tested?}
Testing framework: ${input:framework:Which framework? (jest/vitest/pytest/etc)}
```

**Notes:**
- File name: `<name>.prompt.md` in `.github/prompts/`
- Can reference other files via markdown links `[name](../path/to/file.md)` or `#file:path` syntax
- Invocation: VS Code paperclip > "Prompt..." or `/name` in chat
- Not auto-loaded — always manual trigger

---

### 4. `.github/agents/*.agent.md` — Custom agents

**What it is:** A specialist "persona" with its own instructions, tool permissions, and optional MCP configuration.
**When it loads:** Manual (user selects from agent dropdown or uses `--agent` flag) or automatic inference by the main agent when task context matches the agent's description.
**What it controls:** Delegate work to a subagent with focused expertise and constrained toolset.
**Scope:** VS Code (GA), CLI (GA), GitHub.com cloud agent (GA), JetBrains (preview).
**Format:** Markdown with YAML frontmatter. Body = agent behavior instructions (max 30,000 chars).

```markdown
---
name: wiki-librarian
description: >
  Manages this repository's LLM-maintained wiki. Use this agent when the user
  asks to ingest a source, update the wiki, or run a lint check.
tools: ["read", "edit", "search", "execute"]
model: claude-sonnet-4-6
disable-model-invocation: false
---

You are the maintainer of the wiki in this repository.

Read `.github/copilot-instructions.md` before every operation.
Follow the ingest, query, and lint workflows defined there exactly.
```

**Frontmatter properties:**

| Property | Required | Description |
|---|---|---|
| `name` | No | Display name (defaults to filename minus `.agent.md`) |
| `description` | **Yes** | What expertise this agent has and when to use it. Drives automatic inference. |
| `target` | No | `vscode` or `github-copilot`. Defaults to both. |
| `tools` | No | List of tool names/aliases allowed. Omit = all tools. `[]` = no tools. |
| `model` | No | Override the model for this agent. |
| `disable-model-invocation` | No | `true` to require explicit selection; never auto-inferred. Default: `false`. |
| `user-invocable` | No | `false` = programmatic use only, not selectable in UI. Default: `true`. |
| `mcp-servers` | No | Additional MCP servers (CLI/cloud agent only, not VS Code). |

**Tool aliases available for `tools` field:**

| Alias | Maps to | Purpose |
|---|---|---|
| `read` | Read, NotebookRead | Read file contents |
| `edit` | Edit, MultiEdit, Write, NotebookEdit | Edit files |
| `search` | Grep, Glob | Search files/text |
| `execute` | shell, Bash, powershell | Run shell commands |
| `web` | WebSearch, WebFetch | Fetch URLs / search |
| `agent` | custom-agent, Task | Invoke another custom agent |
| `todo` | TodoWrite | Create task lists |

**Precedence:** User home `~/.copilot/agents/` overrides `.github/agents/` if same filename.
**Programmatic use:** `copilot --agent wiki-librarian --prompt "ingest README"`

---

### 5. `.github/skills/<skill-name>/SKILL.md` — Agent skills

**What it is:** A folder of instructions (and optionally scripts/assets) that Copilot loads as needed when a task matches the skill's purpose. An open standard shared across Claude, Copilot, and other AI systems (see [agentskills/agentskills](https://github.com/agentskills/agentskills)).
**When it loads:** Automatic — Copilot selects the skill when it determines the skill is relevant to the current task. Manual override: `/skill-name` slash command in CLI.
**What it controls:** "Just-in-time" domain expertise without permanently inflating the context window.
**Scope:** VS Code (GA), CLI (GA), GitHub.com cloud agent (GA). Not in Visual Studio or JetBrains.
**Search paths:**
- Project: `.github/skills/`, `.claude/skills/`, `.agents/skills/`
- Personal: `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/`

**Format:** Directory named for the skill, containing a `SKILL.md` file.

```
.github/skills/
├── intake/
│   └── SKILL.md
└── wiki-lint/
    └── SKILL.md
```

`SKILL.md` format — markdown with optional YAML frontmatter:

```markdown
---
name: intake
description: Ingest a raw source document into the wiki
---

# Intake Skill

When given a URL or file path to ingest:

1. Read the source in full. If it is a URL, fetch and save to `raw/<slug>.md`.
2. State key takeaways before writing anything.
3. Write `wiki/sources/<slug>.md` with key takeaways and cross-links.
4. Create or update entity/concept pages touched by this source.
5. Update `wiki/index.md` and append to `wiki/log.md`.
```

**Frontmatter fields:**
- `name` — skill identifier (used with `disabledSkills`). Defaults to directory name if omitted.
- `description` — what the skill does. Copilot uses this for automatic matching.

**Notes:**
- Skills can include additional files in the skill directory (scripts, templates, etc.)
- CLI commands: `/skills list`, `/skills info`, `/skills reload`, `/skills add`, `/skills remove`
- Prefer skills over custom instructions when behavior should be "sometimes needed, not always"

---

### 6. `.github/hooks/*.json` — Lifecycle hooks

**What it is:** Shell commands that run deterministically at agent lifecycle events.
**When it loads:** Automatic at configured lifecycle points.
**Scope:** CLI (preview), GitHub.com cloud agent (preview). Not VS Code or JetBrains.
**Format:** JSON file with `version: 1` and a `hooks` object.

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "type": "command",
        "bash": "./scripts/log-session.sh",
        "powershell": "./scripts/log-session.ps1",
        "cwd": ".",
        "timeoutSec": 10
      }
    ],
    "preToolUse": [
      {
        "type": "command",
        "bash": "./scripts/security-check.sh",
        "timeoutSec": 15
      }
    ]
  }
}
```

**Hook types:**

| Hook | When it fires | Can deny tool? |
|---|---|---|
| `sessionStart` | New or resumed session begins | No |
| `sessionEnd` | Session completes or is terminated | No |
| `userPromptSubmitted` | User submits a prompt | No |
| `preToolUse` | Before any tool executes | **Yes** |
| `postToolUse` | After tool completes | No |
| `agentStop` | Main agent finishes responding | No |
| `subagentStop` | Subagent completes | No |
| `errorOccurred` | Error during execution | No |

**`preToolUse` deny output format:**
```json
{"permissionDecision": "deny", "permissionDecisionReason": "Reason text"}
```

**Hook object properties:**

| Property | Required | Description |
|---|---|---|
| `type` | Yes | Must be `"command"` |
| `bash` | Yes (Unix) | Path to bash script |
| `powershell` | Yes (Windows) | Path to PowerShell script |
| `cwd` | No | Working directory, relative to repo root |
| `env` | No | Environment variable overrides |
| `timeoutSec` | No | Max execution time (default: 30) |

---

## Agent Skills Format (complete spec)

The Agent Skills open standard (`agentskills/agentskills` on GitHub) is supported by Copilot, Claude, and other AI systems.

**Minimal skill:**
```
.github/skills/my-skill/SKILL.md
```

**SKILL.md:**
```markdown
---
name: my-skill
description: One-sentence description that AI uses to decide when to apply this skill
---

# Skill Title

Body is plain markdown instructions injected into the session context when loaded.
```

**Discovery rules:**
1. Copilot looks in `.github/skills/`, `.claude/skills/`, `.agents/skills/` (project-level)
2. Also looks in `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/` (personal)
3. Project skills take precedence over personal skills when names conflict
4. CLI: `skillDirectories` option points to the parent directory; it auto-discovers all `SKILL.md` files in immediate subdirectories

**Key design rule:** Keep the skill directory flat (one level of subdirectories). The SDK's `skillDirectories` option expects the parent directory, not the skill directory itself.

---

## Custom Agent Format (complete spec)

**File:** `.github/agents/<agent-name>.agent.md`

**Complete example for a wiki librarian agent:**

```markdown
---
name: wiki-librarian
description: >
  Manages the LLM-maintained wiki in this repository. Use this agent when the
  user requests an ingest, wiki query, or lint operation. Trigger keywords:
  "ingest", "add to the wiki", "process this", "lint the wiki", "check the wiki".
tools: ["read", "edit", "search", "execute"]
model: claude-sonnet-4-6
disable-model-invocation: false
user-invocable: true
---

You are the sole maintainer of the wiki in this repository.

Before every operation, read `.github/copilot-instructions.md` in full.
Follow the workflows defined there exactly: ingest, query, lint.

Never modify files in `raw/`. Only write to `wiki/`.
Always append to `wiki/log.md` at the end of every operation — never edit past entries.
```

**Naming:**
- File name (minus `.agent.md`) is the CLI `--agent` selector
- Prefer lowercase kebab-case for programmatic use: `wiki-librarian.agent.md`

**Precedence when names conflict:**
- User home `~/.copilot/agents/` beats `.github/agents/` — same filename wins at user level
- Org/enterprise agents (in `.github-private` repo) can be overridden by repo-level agents

---

## Prompt File Format (complete spec)

**File:** `.github/prompts/<name>.prompt.md`

**Minimal prompt (no frontmatter required):**
```markdown
Review the selected code for security vulnerabilities.

Focus on:
- Exposed secrets or credentials
- SQL injection risk
- XSS vectors
```

**Prompt with frontmatter and input variables:**
```markdown
---
agent: 'agent'
description: 'Ingest a source document into the wiki'
---

Ingest the following source into the wiki following the workflow in
`.github/copilot-instructions.md`.

Source: ${input:source:URL or file path to ingest}
```

**Frontmatter fields:**
- `agent` — set to `'agent'` to run in agent mode (can use tools). Omit for chat-only.
- `description` — shown in the prompt picker UI.

**Input variable syntax:** `${input:variable_id:prompt_shown_to_user}`

**References to other files:**
```markdown
See the schema defined in [copilot-instructions.md](../.github/copilot-instructions.md).
```

**Invocation in VS Code:**
1. Paperclip icon > "Prompt..." > select file
2. Type `/name-of-prompt-file` in chat

---

## Complementary Tooling

These tools are worth knowing about for the wiki template ecosystem, with honest assessments of their fit.

### Markdown as the universal format (HIGH confidence)

Plain `.md` files are the correct and only format for all wiki content in this pattern. Every Copilot extension point reads markdown. No conversion layer needed.

### AGENTS.md / CLAUDE.md / GEMINI.md (HIGH confidence)

Third-party agent instruction files that Copilot also reads at session start. `AGENTS.md` is the cross-vendor standard (see [agentsmd/agents.md](https://github.com/agentsmd/agents.md)); Copilot reads it from repo root and any directory in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`. This is useful for templates that need to work across multiple AI agents (not just Copilot).

If both `AGENTS.md` and `.github/copilot-instructions.md` are present, Copilot loads both. Use `AGENTS.md` for cross-agent compatibility, `copilot-instructions.md` for Copilot-specific details.

### jq (HIGH confidence — runtime dependency for hooks)

All hook scripts in the docs use `jq` to parse the JSON stdin payload. It is a required runtime dependency for any bash-based hook. Must be in PATH.

### Obsidian (LOW confidence for this pattern)

Obsidian is a popular personal knowledge base with markdown files and AI plugins. It is NOT a good fit for this template:
- Designed for human-navigated, local-first PKM
- Copilot does not have a native Obsidian integration
- Vault format adds `.obsidian/` config that creates noise in a git repo
- AI plugins (Smart Connections, Copilot for Obsidian) are separate tools, not the Copilot in this pattern

Use if the user explicitly wants a human-browsable Obsidian vault alongside the LLM wiki — but that is a separate concern from the template itself.

### Quarto / qmd (LOW confidence for this pattern)

Quarto is a scientific publishing system using `.qmd` files (markdown + code chunks). Not relevant unless the wiki needs to render notebooks or produce PDF/HTML reports. The overhead of a Quarto project (`_quarto.yml`, render pipeline) is unjustified for a plain markdown wiki maintained by an LLM.

### Marp (LOW confidence for this pattern)

Marp converts markdown to slides. Not relevant to a wiki template. Mention only if the user wants to generate presentation output from wiki content.

### MCP servers (MEDIUM confidence — optional enhancement)

The Model Context Protocol allows Copilot agents to call external APIs as tools. Relevant additions for a wiki template:

- **GitHub MCP server** — built-in, read-only GitHub API access. Useful for ingesting issues, PRs, or release notes as sources.
- **Playwright MCP server** — built-in, browser automation. Could be used for crawling URLs during ingest.
- **Filesystem MCP server** — allows structured file operations. Less needed since Copilot agents already have read/edit tools.

MCP configuration lives in `.mcp.json` (project-level) or `~/.copilot/mcp-config.json` (user-level).

### GitHub Actions (MEDIUM confidence — automation layer)

Actions can trigger `copilot -p "ingest X" --allow-all-tools` on a schedule or when new files appear in `raw/`. This creates a fully automated pipeline. The `COPILOT_HOME` and `COPILOT_CACHE_HOME` environment variables allow CI to use a custom config directory.

Not needed for the initial template, but worth documenting as an advanced pattern.

---

## What NOT to Use and Why

### Vector databases / embeddings (NOT recommended for this pattern)

Tools like Pinecone, Chroma, or Weaviate are commonly suggested for "AI knowledge bases." Do not use them here. The Copilot librarian pattern works through structured markdown and a maintained `index.md` — the LLM reads the index to navigate, then reads relevant pages. This is intentionally simpler and more transparent than semantic search. Adding a vector DB would require:
- A separate ingestion pipeline
- An external service dependency
- Code outside the wiki repo itself
- A query tool that Copilot does not natively use

The whole point of this pattern is that Copilot reads its own wiki like a human would — by following an index and cross-links.

### SQLite / databases for wiki content (NOT recommended)

Same argument as above. Markdown files are the storage layer. They are version-controlled, diff-able, and directly readable by Copilot without any tools.

### LangChain / LlamaIndex (NOT recommended)

Framework overhead for agentic pipelines that is unnecessary when Copilot itself is the agent. These frameworks are for building custom LLM applications, not for extending Copilot.

### Automatic commit bots / GitHub Apps (NOT recommended initially)

Tools like Renovate or custom GitHub Apps that auto-commit to the wiki create merge conflict risk and break the "Copilot as sole maintainer" contract. The human should remain in the loop via `/intake` triggers, not background automation.

### Obsidian Sync / iCloud / Dropbox sync (NOT recommended)

Any sync layer that operates outside of git will create file conflicts and break the append-only `log.md` contract. Git is the only sync mechanism.

### `copilot-instructions.md` as a dumping ground (NOT recommended)

The docs explicitly cap repository-wide instructions at 2 pages. Overloading it with detailed workflow instructions for every scenario degrades response quality because all instructions compete for attention on every single request. The right pattern:
- `copilot-instructions.md` → schema, structure, role, workflow triggers (2 pages max)
- `.github/skills/intake/SKILL.md` → detailed ingest workflow
- `.github/skills/wiki-lint/SKILL.md` → detailed lint workflow
- `.github/agents/wiki-librarian.agent.md` → specialist agent for programmatic use

---

## Summary: What the Template Actually Needs

| File | Purpose | Priority |
|---|---|---|
| `.github/copilot-instructions.md` | Schema, role, workflow triggers — the brain | Essential |
| `.github/skills/intake/SKILL.md` | Detailed ingest steps | Essential |
| `.github/skills/wiki-lint/SKILL.md` | Lint / consistency check steps | Recommended |
| `.github/agents/wiki-librarian.agent.md` | Programmatic / CLI use | Recommended |
| `.github/prompts/intake.prompt.md` | VS Code chat shortcut for ingest | Optional |
| `.github/hooks/audit.json` | Session/tool logging | Optional |
| `AGENTS.md` | Cross-agent compatibility (Claude, Gemini) | Optional |
| `wiki/` | The actual wiki content (Copilot owns this) | Essential |
| `raw/` | Immutable source documents | Essential |
