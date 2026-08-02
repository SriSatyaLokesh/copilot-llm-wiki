---
agent: 'agent'
description: 'Lint the wiki for structural issues'
---

Run a complete lint pass on the wiki using the **Lint workflow** in `.github/copilot-instructions.md`.

Check each of the following in order. Report results as a structured checklist with one section per check. For passing checks, show `✔ No issues`. For failures, list the file path and a short description of each issue found.

**Checks:**
1. **Orphan pages** — files in `wiki/` (excluding `index.md` and `log.md`) that have no entry in the root `wiki/index.md`
2. **Broken cross-links** — markdown links in wiki pages pointing to files that do not exist
3. **Missing See Also** — concept pages that lack a `## See Also` section
4. **Entities without pages** — entity or concept names mentioned across multiple pages but lacking their own dedicated page
5. **Stale claims** — facts in older pages contradicted by more recently ingested sources (compare dates in `log.md`)
6. **Contradictions** — claims on one wiki page that directly contradict claims on another page
7. **OKF conformance** — concept `.md` files missing YAML frontmatter or a non-empty `type` field
8. **OKF actor format** — `generated.by` or `verified[].by` values not following `<producer>/<version>`, `human:<id>`, or `process:<id>` convention
9. **OKF datetime format** — `generated.at` or `verified[].at` values that are bare dates (e.g., `2026-08-02`) instead of ISO 8601 datetimes (e.g., `2026-08-02T00:00:00Z`)
10. **Stale after** — concepts with a `stale_after` date that is today or in the past
11. **Subdirectory indexes** — missing `index.md` in `entities/`, `concepts/`, `comparisons/`, `sources/`, or `qa/`

After reporting all checks, offer to fix any issues found.

