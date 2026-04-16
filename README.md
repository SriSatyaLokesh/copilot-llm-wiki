# GitHub Copilot Wiki Template

**A forkable template for building LLM-maintained personal knowledge bases using GitHub Copilot.**

Instead of starting from scratch on every query, Copilot incrementally builds and maintains a persistent, interlinked wiki of markdown files that compounds with every source ingested.

This project is an implementation of the **LLM-Wiki** concept popularized by [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), designed to create a "Compounding Knowledge Pattern" through purely file-based local storage.

## 🏗️ Architecture: The Three Layers
The system is divided into three distinct layers of responsibility:

![Three-Layer Architecture Continuous Ingest Loop](docs/assets/architecture-loop.jpg)

1.  **Raw Sources (`raw/`)**: Your collection of source documents. These are **immutable**—the AI reads them but never modifies them.
2.  **The Wiki (`wiki/`)**: Generating interlinked markdown files. The AI **owns** this layer—it writes it; you read it.
3.  **The Schema (`.github/copilot-instructions.md`)**: The "brain" or configuration layer. It tells the AI how to be a disciplined wiki maintainer rather than a generic chatbot.

## 🚀 10-Minute Setup Guide

1.  **Fork this repository**: Click the "Fork" button to create your own copy.
2.  **Clone and Open in VS Code**: Open the repo in an environment with GitHub Copilot installed.
3.  **Enable Prompt Files**:
    - Open VS Code Settings (`Ctrl+,`).
    - Search for `github.copilot.chat.promptFiles`.
    - Set it to `true`.
4.  **Drop your first source**: Put a markdown file or a URL reference in the `raw/` directory.
5.  **Run Ingest**:
    - **In VS Code Chat**: Type `/ingest` (or use the paperclip icon to attach `.github/prompts/ingest.prompt.md`) and provide- **Batch Mode**: Drop multiple markdown files in `raw/` and run:
  - Bash: `./.github/skills/wiki-ingest/scripts/intake.sh`
  - PowerShell: `.\.github\skills\wiki-ingest\scripts\intake.ps1`
).

## 🧠 Core Workflows

### 📥 Ingest
Tell Copilot to "ingest <source>". It will:
- Fetch and save the source to `raw/`.
- Extract key facts.
- Create/update pages in `wiki/entities/` and `wiki/concepts/`.
- Update the `wiki/index.md` and `wiki/log.md`.

### 🔍 Query
Ask a question about your knowledge domain. Copilot will:
- Read `wiki/index.md` to find relevant pages.
- Consult the interlinked wiki pages.
- Answer with citations.
- Offer to file the answer as a new QA page in `wiki/qa/`.

### 🧹 Lint
Run "lint the wiki" via `lint.prompt.md` or the `librarian` agent to check for orphans, broken links, or contradictions.

## 🛠️ Customization

1.  Open `.github/copilot-instructions.md`.
2.  Find the `[YOUR DOMAIN]` placeholders and replace them with your specific domain (e.g., "Medical Research", "Codebase Documentation", "Legal Case Files").
3.  Customize the `wiki/overview.md` to reflect your project's goals.

## 🤖 Librarian Agent (CLI)

If you have the GitHub Copilot CLI installed, you can invoke the dedicated librarian agent:

```bash
copilot --agent librarian -p "ingest raw/new-data.md"
```

The librarian agent automatically decides between direct ingestion and using the intake scripts based on the complexity of your request.

## 📊 Visualization (Obsidian Recommended)
To get the most out of your LLM Wiki, we highly recommend using **[Obsidian](https://obsidian.md/)** to view your `wiki/` directory.

- **Knowledge Graph**: Use Obsidian's "Graph View" to see how your entities and concepts are interconnected.
- **Easy Navigation**: Clickable links, back-links, and local previews make exploring your knowledge base feel like a "second brain."
- **Markdown-Native**: Since the wiki is 100% standard markdown, Obsidian handles it natively without any conversion needed.

---
*Inspired by Andrej Karpathy's [llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Built by the community.*
