---
agent: 'agent'
description: 'Lint the wiki for structural issues'
---

Run a complete lint pass on the wiki using the **Lint workflow** in `.github/copilot-instructions.md`.

Check each of the following in order. Report results as a structured checklist with one section per check. For passing checks, show `✔ No issues`. For failures, list the file path and a short description of each issue found.

**Checks:**
1. **Orphan pages** -- files in `wiki/` that have no corresponding entry in `index.md`
2. **Broken cross-links** -- markdown links in wiki pages pointing to files that do not exist
3. **Missing See Also** -- wiki pages that lack a `## See Also` section
4. **Entities without pages** -- entity or concept names mentioned across multiple pages but lacking their own dedicated page
5. **Stale claims** -- facts in older pages that are contradicted by more recently ingested sources (compare dates in `log.md`)
6. **Contradictions** -- claims on one wiki page that directly contradict claims on another page

After reporting all six checks, offer to fix any issues found.
