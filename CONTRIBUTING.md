# Contributing to Copilot LLM Wiki

Thank you for your interest in contributing to **Copilot LLM Wiki**! Whether you are improving the template architecture, creating new prompt files, fixing automation scripts, adding adapters, or expanding documentation, your contributions are welcome.

---

## Code of Conduct

This project is governed by the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## Two Ways to Contribute

There are two primary categories of contributions:

1. **Improving the Open-Source Template & Tooling**:
   - Enhancing prompt files in `.github/prompts/`
   - Improving the Librarian CLI agent in `.github/agents/librarian.agent.md`
   - Enhancing intake automation scripts in `.github/skills/wiki-ingest/scripts/`
   - Adding and refining adapters in `adapters/` (e.g., `adapters/okf/` for Open Knowledge Format v0.2 bundle export)
   - Adding integrations (Obsidian, Logseq, Cursor, JetBrains)
   - Enhancing documentation and guides

2. **Contributing Knowledge to an Instantiated Wiki**:
   - Ingesting curated sources into `raw/`
   - Expanding `wiki/entities/`, `wiki/concepts/`, and `wiki/comparisons/`

---

## 🛠️ Contributing to Template & Tooling

### Development Workflow
1. **Fork the repository** on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/<your-username>/copilot-llm-wiki.git
   cd copilot-llm-wiki
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-enhancement
   ```
4. **Make and test your changes**:
   - Test prompt files in VS Code with GitHub Copilot Chat.
   - Test batch scripts with both PowerShell (`intake.ps1`) and Bash (`intake.sh`).
   - If modifying adapters, verify export scripts (e.g. `python adapters/okf/export.py`).
   - Ensure you do not break existing SEO keywords (e.g. `copilot llm wiki`, `compounding knowledge pattern`).
5. **Commit with conventional commit messages**:
   ```bash
   git commit -m "feat(prompts): add specialized synthesis prompt"
   ```
6. **Push and open a Pull Request** against the `main` branch.

---

## 📥 Contributing Knowledge (Wiki Ingestion Workflow)

If you are contributing knowledge to a shared knowledge base repository:

1. **Drop your source**: Place your raw markdown source files in `raw/`.
2. **Run Ingest**:
   - In VS Code Chat, type `/ingest raw/<filename>.md`
   - Or run the batch intake script:
     - PowerShell: `.\.github\skills\wiki-ingest\scripts\intake.ps1`
     - Bash: `./.github/skills/wiki-ingest/scripts/intake.sh`
3. **Review the AI's Output**:
   - Verify that new pages were created in `wiki/entities/` and `wiki/concepts/`.
   - Ensure the new source is indexed in `wiki/index.md` (alphabetically).
   - Ensure the operation was logged in `wiki/log.md`.
4. **Lint the Wiki**:
   - In VS Code Chat, run `/lint` (or use `lint.prompt.md`).
   - Fix any broken links or orphan pages.
5. **Handle Contradictions**:
   - If new sources contradict existing knowledge, do not overwrite silently. Update the existing page, cite both sources, and document the change in `wiki/log.md`.

---

## 📐 Conventions

- **Filenames**: Always use `lowercase-kebab-case.md`. No spaces or uppercase characters.
- **Links**: Use plain relative markdown links: `[Page Name](wiki/entities/page.md)`.
- **See Also**: Every wiki content page must end with a `## See Also` section with cross-links.
- **Append-Only Log**: Never modify past entries in `wiki/log.md`.
- **Read-Only Sources**: Files in `raw/` are immutable sources of truth.

---

## Questions or Ideas?

Feel free to open a [Feature Request](https://github.com/SriSatyaLokesh/copilot-llm-wiki/issues/new?template=feature_request.yml) or start a discussion on GitHub!
