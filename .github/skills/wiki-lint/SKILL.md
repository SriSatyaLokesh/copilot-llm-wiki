---
name: wiki-lint
description: Lint the LLM-maintained wiki for structural and content consistency.
---

# Wiki Lint Skill

When this skill is triggered, you will follow the **Lint workflow** defined in `.github/copilot-instructions.md`.

## Checklist

1. **Index Synchronization**: Run `python scripts/build-index.py --check` (or `.\scripts\build-index.ps1 -Check`) to verify all silo and root indexes are up-to-date.
2. **Orphan Pages**: Identify `.md` files in `wiki/` that are missing from their silo `index.md`.
3. **Broken Links**: Find `[Link](wiki/...)` paths that point to non-existent files.
4. **Archive Violations**: Flag active pages that link directly to archived pages in `wiki/archive/` (should link to superseding active page instead).
5. **Missing "See Also"**: Ensure every page ends with a `## See Also` section.
6. **Missing Entity Pages**: Identify entities mentioned in pages that don't have their own page yet.
7. **Stale Claims**: Compare older pages against recent `log.md` entries for potential obsolescence.
8. **Contradictions**: Identify conflicting claims across different wiki pages.

## Report Format

Always provide a structured report using a checklist format (`✔` or `✘`). Offer to automatically fix errors if tools are available.
