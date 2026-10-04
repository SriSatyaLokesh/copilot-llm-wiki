---
name: wiki-lint
description: Lint the LLM-maintained wiki for structural and content consistency.
---

# Wiki Lint Skill

When this skill is triggered, you will follow the **Lint workflow** defined in `.github/copilot-instructions.md`.

## Checklist

1. **Orphan Pages**: Identify `.md` files in `wiki/` that are missing from `wiki/index.md`.
2. **Broken Links**: Find `[Link](wiki/...)` paths that point to non-existent files.
3. **Missing "See Also"**: Ensure every page ends with a `## See Also` section.
4. **Missing Entity Pages**: Identify entities mentioned in pages that don't have their own page yet.
5. **Stale Claims**: Compare older pages against recent `log.md` entries for potential obsolescence.
6. **Contradictions**: Identify conflicting claims across different wiki pages.

## Report Format

Always provide a structured report using a checklist format (`✔` or `✘`). Offer to automatically fix errors if tools are available.
