# Contributing to [YOUR DOMAIN] Wiki

Thank you for your interest in contributing! This wiki is an **OKF v0.2** knowledge bundle maintained by GitHub Copilot. Contributions help our shared knowledge compound over time.

## Workflow for Contributions

1.  **Drop your source**: Place your raw source material (markdown files) in the `raw/` directory.
2.  **Run Ingest**: Use the `/ingest` prompt in VS Code Chat or run `scripts/intake.sh`.
3.  **Review the Changes**: Copilot will automatically create/update `wiki/` pages with OKF frontmatter. Review these for accuracy. Consider updating `status: draft` to `status: stable` and adding a `verified` entry for pages you've confirmed.
4.  **Lint the Wiki**: Run `/lint` to ensure no broken links, orphan pages, or OKF conformance issues were introduced.
5.  **Submit a PR**: Push your changes (including the updated `wiki/` files) and open a Pull Request.

## Conventions

- **Filenames**: Always use `lowercase-kebab-case.md`.
- **OKF Frontmatter**: Every concept page MUST have frontmatter with `type`, `title`, `description`, and `generated`. See the Page formats table in `.github/copilot-instructions.md`.
- **Links**: Use bundle-relative links: `[Page Name](/wiki/entities/page.md)`.
- **Citations**: Every new page ends with a `## See Also` section. Use markdown footnotes (`[^source-id]`) for per-claim attribution to `sources[]` entries.
- **Agentic Maintainer**: Rely on the **Librarian agent** to perform structural updates. Avoid manual editing of `wiki/index.md` or `wiki/log.md` unless fixing a significant AI error.

## Human Verification

After reviewing a page's accuracy, you can mark it human-reviewed by adding a `verified` entry:

```yaml
verified: { by: human:<your-username>, at: 2026-08-02T09:00:00Z }
```

This upgrades the page's trust tier from "unverified" or "machine-confirmed" to "human-reviewed."

## Contradiction Handling

If your new source contradicts an existing wiki page, Copilot will flag it. Please resolve these contradictions by:
- Updating the existing page to reflect the new truth (and citing the source).
- Adding a "Historical View" section if the contradiction represents evolving information.

---
*Happy Ingesting!*

