# Template Customization Guide

This guide explains how to adapt the **LLM Wiki Template** to your specific domain.

---

## 1. Core Schema (`.github/copilot-instructions.md`)

This is the "brain" of your wiki. Copilot reads this on every request.

- **Domain Definition**: Replace `[YOUR DOMAIN]` with your topic.
- **Key Entities**: Update the list of example entities in the `## Structure - entities/` section to match your domain.
- **Concepts**: Update the foundational ideas in `## Structure - concepts/`.

---

## 2. Page Formats & Ontologies

### Entity Template
```markdown
# [Entity Name]

## Overview
[One-to-two paragraph definition of the actor, system, component, or API.]

## Key Facts
- First grounded assertion [^1]
- Second grounded assertion (Source: [source-slug](wiki/sources/source-slug.md), YYYY-MM-DD)

## Relationships
- **depends-on**: [Component Name](wiki/entities/component.md)
- **part-of**: [Parent System](wiki/entities/parent.md)
- **implements**: [Concept Name](wiki/concepts/concept.md)

## See Also
- [Related Page](wiki/entities/related.md)

[^1]: Source: [source-slug](wiki/sources/source-slug.md), verified YYYY-MM-DD
```

### Concept Template
```markdown
# [Concept Name]

## Definition
[One-paragraph formal definition of the concept or rule.]

## How It Works
[Detailed explanation, steps, or workflow.]

## Relationships
- **implements**: [Specification](wiki/entities/spec.md)
- **related-to**: [Another Concept](wiki/concepts/other.md)

## See Also
- [Related Page](wiki/concepts/related.md)
```

### Standardized Relationship Taxonomy
- `depends-on`: Functional or architectural dependency
- `implements`: Realizes a specification, concept, or interface
- `part-of`: Hierarchical component or sub-module relation
- `supersedes`: Replaces an older entity/concept (pairs with archiving)
- `contradicts`: Documents an unresolved conflict or trade-off between sources
- `related-to`: General lateral association

*(Note: Relationships form a directed acyclic property graph; do not write reciprocal inverse links manually)*.

---

## 3. The `raw/` Directory

Keep the `raw/` directory clean. It is meant to be an immutable record of where your knowledge came from.
- **Single files**: Just drop them in and type `ingest <filename>`.
- **URLs**: You can simply give Copilot the URL. It is instructed to fetch and save it to `raw/` first.

---

## 4. Automation & Tooling

- **Index Compilation**: Run `python scripts/build-index.py` (or `.\scripts\build-index.ps1`) to regenerate all silo sub-indexes deterministically.
- **Linting**: Run `python scripts/lint-wiki.py` (or `.\scripts\lint.ps1`) to check for broken links, relationship violations, and provenance.
- **Snapshots & Rollback**:
  - `python scripts/snapshot.py <name> [description]`
  - `python scripts/rollback.py <name>`

---

## 5. Visualization & Deployment

Since the wiki is entirely markdown:
- **[Obsidian](https://obsidian.md/) (Highly Recommended)**: Open the root folder as an Obsidian Vault. Use the **Graph View** to visualize your interlinked entities and concepts as a second brain.
- **GitHub Pages**: Use any static site generator (like [Quartz](https://quartz.jzhao.xyz/) or MkDocs) to publish the `wiki/` directory as a website.

---
*Follow the conventions. Trust the process. Build your knowledge.*
