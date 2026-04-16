# Contributing to [YOUR DOMAIN] Wiki

Thank you for your interest in contributing! This wiki is a persistent knowledge base maintained by GitHub Copilot. Contributions help our shared knowledge compound over time.

## Workflow for Contributions

1.  **Drop your source**: Place your raw source material (markdown files) in the `raw/` directory.
2.  **Run Ingest**: Use the `/ingest` prompt in VS Code Chat or run `scripts/intake.sh`.
3.  **Review the Changes**: Copilot will automatically create/update `wiki/` pages. Review these for accuracy.
4.  **Lint the Wiki**: Run `/lint` to ensure no broken links or orphan pages were introduced.
5.  **Submit a PR**: Push your changes (including the new `raw/` file and the updated `wiki/` files) and open a Pull Request.

## Conventions

- **Filenames**: Always use `lowercase-kebab-case.md`.
- **Links**: Use plain relative markdown links: `[Page Name](wiki/entities/page.md)`.
- **Citations**: Ensure every new page or section has a `## See Also` section linking to related knowledge.
- **Agentic Maintainer**: Rely on the **Librarian agent** to perform structural updates. Avoid manual editing of the `wiki/index.md` or `wiki/log.md` unless fixing a significant AI error.

## Contradiction Handling

If your new source contradicts an existing wiki page, Copilot will flag it. Please resolve these contradictions by:
- Updating the existing page to reflect the new truth (and citing the source).
- Adding a "Historical View" section if the contradiction represents evolving information.

---
*Happy Ingesting!*
