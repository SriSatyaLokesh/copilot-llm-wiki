# Technical Requirements Document (TRD): Copilot LLM Wiki

## 1. System Architecture

The wiki is a file-system based knowledge layer using structured Markdown. It relies on the GitHub Copilot ecosystem (Prompt Files, Agents, and Skills) to provide the compute logic.

### Directory Structure
```
/
├── .github/
│   ├── agents/
│   │   └── librarian.agent.md   # Persona & Decision Logic
│   ├── prompts/
│   │   ├── ingest.prompt.md     # VS Code Ingest trigger
│   │   ├── query.prompt.md      # VS Code Query trigger
│   │   └── lint.prompt.md       # VS Code Lint trigger
│   ├── skills/
│   │   ├── wiki-ingest/         # Portable ingest logic
│   │   │   ├── SKILL.md
│   │   │   └── scripts/         # Intake Automation (agentskills.io)
│   │   │       ├── intake.sh
│   │   │       └── intake.ps1
│   │   └── wiki-lint/           # Portable lint logic
│   └── copilot-instructions.md  # CORE SCHEMA (Source of Truth)
├── raw/                         # Immutable Source Store
└── wiki/                        # Maintenance Layer
    ├── index.md                 # Knowledge Map
    ├── log.md                   # Operation Audit
    ├── overview.md              # Domain orientation
    └── (entities|concepts|qa)/  # Content Silos
```

## 2. Implementation Specifications

### 2.1 Core Schema (`copilot-instructions.md`)
This file is the global context for all Copilot surfaces. It defines:
- **Trigger Phrases**: "ingest", "query", "lint".
- **Workflow Definitions**: Detailed step-by-step instructions for each operation.
- **Conventions**: Lowercase kebab-case filenames, mandatory `## See Also` sections.

### 2.2 Librarian Agent (`librarian.agent.md`)
A dedicated persona for CLI and Cloud Agent environments.

#### Agent Frontmatter Specification
```markdown
---
name: librarian
description: Automated maintainer for the LLM Wiki. Trigger keywords: "ingest", "wiki", "librarian", "lint".
tools: ["read", "edit", "search", "execute"]
---
```

#### Decision Logic Branching
1. **Source Discovery**: The agent must count files in `raw/` or sources in the prompt.
2. **Path A (Direct)**: If `count == 1`, the agent uses `read` and `edit` tools to follow the Ingest workflow manually.
3. **Path B (Scripted)**: If `count > 1`, the agent uses the `execute` tool to run the appropriate intake script (Bash or PowerShell).

### 2.3 Prompt Specifications (`.github/prompts/`)
Prompt files use standard Markdown with YAML frontmatter.

#### Interactive Variable Syntax
Used to capture user intent dynamically in VS Code:
- `${input:question:What is your question?}`
- `${input:source:Which file or URL should I ingest?}`

### 2.4 Intake Scripts (`scripts/`)
Designed for batch processing and environment compatibility.
- **Batch Logic**: Scans `raw/`, cross-references with `wiki/log.md`, and calls `copilot -p` for every new file.
- **Stability**: Includes a mandatory cleanup step at the end of every successful batch.

## 3. Tool-to-Workflow Mapping

| Workflow Step | Tool Used | Purpose |
|---------------|-----------|---------|
| Scan Directory | `read_dir` / `execute` | Identify new files in `raw/` |
| Read Source | `read_file` / `read_url` | Extract raw content |
| Check History | `read_file` | Verify `wiki/log.md` for duplicates |
| Create Pages | `write_to_file` | Generate new wiki content |
| Update Index | `edit_file` | Alphabetical insertion into `index.md` |
| Cleanup | `execute` | Terminal-based deletion (`rm` / `Remove-Item`) |

## 4. Detailed Workflow Logic

### 📥 Ingest Workflow (8 Steps)
1. **Source Discovery**: Auto-detects files in `raw/` if no argument provided.
2. **Key Takeaways**: Identifies facts and entities.
3. **Contradiction Check**: Reads existing pages to verify consistency.
4. **Source Summary**: Creates `wiki/sources/<slug>.md`.
5. **Knowledge Update**: Creates/updates `wiki/entities/` and `wiki/concepts/`.
6. **Index Update**: Adds new pages to `wiki/index.md` (alphabetical).
7. **Log Update**: Records the operation in `wiki/log.md`.
8. **Cleanup (CRITICAL) (PLATFORM WORKAROUND)**: Deletes the source from `raw/` using `rm` or `Remove-Item` via the `execute` tool. **NEVER use standard file-edit tools for this step.**

### 🔍 Query Workflow
1. Read `wiki/index.md`.
2. Follow cross-links to relevant `entities/` or `concepts/`.
3. Answer with **citations** (e.g., `Pages consulted: [foo.md]`).

## 5. Technical Constraints & Workarounds

### Patch Tool Bug Workaround
- **Issue**: Standard file deletion tools in some Copilot environments fail with "Duplicate Path" errors due to internal patch-tracking limitations.
- **Solution**: The system is explicitly instructed to use the **`execute`** tool (Terminal) for all file removals (`rm` or `Remove-Item`).

### File Naming
- All filenames MUST be lowercase-kebab-case.md.
- Special characters in `raw/` filenames are handled by the Librarian during slugs creation.

## 6. Deployment & Forking
To initialize a new instance:
1. Fork repository.
2. Enable `github.copilot.chat.promptFiles` in VS Code Chat.
3. Replace `[YOUR DOMAIN]` in `copilot-instructions.md`.
4. Run `init` in `wiki/log.md`.
