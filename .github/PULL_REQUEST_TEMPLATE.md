## Summary of Changes

<!-- Please provide a clear summary of what this pull request modifies or adds. -->

### Type of Change
- [ ] **Knowledge Base Ingest**: Added new sources to `raw/` and updated `wiki/`
- [ ] **Template / Tooling**: Improvements to prompts, scripts, or agents
- [ ] **Documentation / SEO**: Updates to README, guides, or specifications
- [ ] **Bug Fix**: Resolving an issue with ingest, lint, or automation

---

### 📥 If Ingesting Knowledge (`wiki/` changes)
- **Source(s) added to `raw/`**: [List files or URLs]
- **Wiki pages Created**: [List new .md files]
- **Wiki pages Updated**: [List updated .md files]

#### Wiki Health Check
- [ ] Ingested via GitHub Copilot (Librarian agent, `/ingest` prompt, or intake script)
- [ ] `wiki/log.md` updated correctly (appended only, no historical edits)
- [ ] `wiki/index.md` updated and remains alphabetically sorted
- [ ] Ran `/lint` (or `lint.prompt.md`) with 0 orphan pages and 0 broken links
- [ ] All new pages include a `## See Also` section
- [ ] All filenames follow strict `lowercase-kebab-case.md` format
- [ ] Checked for knowledge contradictions against existing pages

---

### 🛠️ If Modifying Tooling, Prompts, or Scripts
- [ ] Tested in VS Code with GitHub Copilot Chat
- [ ] Tested CLI librarian agent / intake scripts (PowerShell and/or Bash)
- [ ] Maintained backward compatibility with existing `copilot-instructions.md` schema
- [ ] Preserved all core ranking keywords (`copilot llm wiki`, etc.)

---

### 🔗 Related Issues
<!-- Link related issues, e.g. Fixes #1 or Resolves #2 -->
Closes #
