---
name: wiki-lint
description: Lint the LLM-maintained wiki for structural and content consistency.
---

# Wiki Lint Skill

When this skill is triggered, follow the **Lint workflow** defined in `.github/copilot-instructions.md`.

## Checklist

1. **Orphan Pages**: Identify `.md` files in `wiki/` (excluding `index.md` and `log.md`) that are missing from `wiki/index.md`.
2. **Broken Links**: Find `[Link](wiki/...)` paths that point to non-existent files.
3. **Missing "See Also"**: Ensure every concept page ends with a `## See Also` section.
4. **Missing Entity Pages**: Identify entities mentioned in pages that don't have their own page yet.
5. **Stale Claims**: Compare older pages against recent `log.md` entries for potential obsolescence.
6. **Contradictions**: Identify conflicting claims across different wiki pages.
7. **OKF Conformance**:
   - Every concept `.md` (not `index.md` or `log.md`) has parseable YAML frontmatter.
   - Every frontmatter has a non-empty `type` field.
   - `generated.by` follows the actor convention (`copilot-librarian/1.0`, `human:<id>`, or `process:<id>`).
   - `generated.at` is an ISO 8601 datetime string (e.g., `2026-08-02T13:00:00Z`), not a bare date.
   - `verified[].by` follows the same actor convention.
   - Any `stale_after` dates that have already passed are flagged.
   - Subdirectory `index.md` files exist for `entities/`, `concepts/`, `comparisons/`, `sources/`, and `qa/`.

## Report Format

Always provide a structured report using a checklist format (`✔` or `✘`). Offer to automatically fix errors if tools are available.

