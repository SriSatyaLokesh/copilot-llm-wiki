# Product Requirements Document (PRD): Copilot LLM Wiki

## 1. Project Vision
The **Copilot LLM Wiki** is a domain-agnostic, LLM-maintained knowledge base designed to solve the "Zero-Context" problem in AI coding. Most LLM interactions are stateless, starting from scratch each time. This project implements Andrej Karpathy's "Compounding Knowledge Pattern," where the AI acts as a **Librarian**, incrementally building a persistent, interlinked wiki from every source it encounters.

## 2. Core Personas
### The Librarian
- **Role**: Active maintainer of the wiki.
- **Responsibility**: Ingesting sources, updating the index/log, cross-referencing knowledge, and ensuring structural health (linting).
- **Tone**: objective, precise, academic, and systematic.

## 3. Core Features
### 📥 Automated Ingestion
- Programmatic and manual ingestion of URLs or markdown files.
- Automated creation of "Entity" and "Concept" pages.
- Mandatory "Contradiction Check" to ensure knowledge integrity.
- Post-ingestion cleanup of source files.

### 🔍 Knowledge Querying
- CITATION-FIRST answering. Every response must link back to specific wiki pages.
- Synthesis of multiple pages into new "QA" pages to capture complex insights.

### 🧹 Wiki Health (Linting)
- Automated detection of orphan pages (missing from index).
- Broken link detection.
- Cross-reference suggestions for related but unlinked concepts.

## 4. Prompt & Keyword Library

### VS Code Chat (Prompt Files)
Direct triggers for the primary user-facing surface:
- `/ingest` -> Ingests a specific file or URL.
- `/query` -> Asks a question using the "Librarian" context.
- `/lint` -> Runs a structural health check on the `wiki/` folder.

### CLI Agent triggers
Implicit triggers that allow the CLI to infer the librarian persona:
- "Ingest the files in raw"
- "Tell me what the wiki says about [Topic]"
- "Check the wiki for broken links"

## 5. Wiki Content Templates
To ensure consistency across different LLM sessions, the following templates must be used:

### Entity Template (`wiki/entities/*.md`)
```markdown
# [Entity Name]

## Overview
High-level description of what the entity is.

## Key Facts
- Bulleted list of verified facts from sources.

## See Also
- [Related Concept](wiki/concepts/related.md)
```

### Concept Template (`wiki/concepts/*.md`)
```markdown
# [Concept Name]

## Definition
The core meaning or theory behind this concept.

## How It Works
Detailed explanation of mechanics or principles.

## See Also
- [Entity Name](wiki/entities/entity.md)
```

## 6. Fundamental Rules (The "Librarian's Code")

- **Immutable Sources**: Files in the `raw/` directory are source material; they are read-only and never modified by the librarian (except for cleanup after ingestion).
- **Append-Only Logging**: The `wiki/log.md` is an immutable record of operations. Past entries are never edited or deleted.
- **Index-First Architecture**: The librarian MUST read `wiki/index.md` before any query or update to maintain a consistent mental map of the knowledge base.
- **No Silent Contradictions**: If a new source contradicts an existing page, the Librarian MUST flag it to the user and resolve it before writing.
- **Lowercase Kebab-Case**: All filenames MUST be lowercase with hyphens (e.g., `github-copilot.md`).

## 7. Implementation Phases
To build this project from scratch, follow these phases in order:

### Phase 1: Schema & Wiki Scaffold
- **Goal**: Establish the foundation that all Copilot surfaces read.
- **Key Task**: Create `copilot-instructions.md` and the `wiki/` directory structure.

### Phase 2: VS Code Prompt Files
- **Goal**: Enable the primary user-facing Chat interface.
- **Key Task**: Create `.github/prompts/` (ingest, query, lint).

### Phase 3: CLI Agent & Skills
- **Goal**: Enable terminal-based agentic operations.
- **Key Task**: Create `librarian.agent.md` and portable skills.

### Phase 4: CLI Intake Script
- **Goal**: automate batch processing and programmatic ingestion.
- **Key Task**: Create `scripts/intake.sh` and `scripts/intake.ps1`.

### Phase 5: Fork-Ready Template
- **Goal**: Package the system for domain-agnostic use.
- **Key Task**: Add `README.md`, `TEMPLATE.md`, and `[YOUR DOMAIN]` placeholders.

## 8. Success Metrics
- **Zero-Friction Ingest**: Single-command ingestion of any source.
- **Searchability**: Finding any fact within the wiki in under 2 chat turns.
- **Self-Maintenance**: The Librarian can identify and fix its own structural errors using the `lint` workflow.
