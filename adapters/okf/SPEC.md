# Open Knowledge Format (OKF) v0.2 — Specification Reference

This document references the **Open Knowledge Format (OKF) v0.2** specification (introduced by Google Cloud in July 2026) for packaging wiki knowledge into machine-readable bundles for enterprise AI agents.

---

## 1. Bundle Structure

An OKF v0.2 bundle organizes knowledge into an interlinked directory structure with progressive disclosure indexes:

```
wiki/
├── index.md                 # Root catalog with okf_version: "0.2" frontmatter
├── log.md                   # Update log with newest-first ## YYYY-MM-DD headings
├── overview.md              # type: Overview concept
├── entities/                # type: Entity concepts
│   └── index.md             # Subdirectory index
├── concepts/                # type: Concept concepts
│   └── index.md             # Subdirectory index
├── comparisons/             # type: Comparison concepts
│   └── index.md             # Subdirectory index
├── sources/                 # type: Source concepts (one per raw document)
│   └── index.md             # Subdirectory index
└── qa/                      # type: Q&A concepts
    └── index.md             # Subdirectory index
```

---

## 2. OKF Frontmatter Requirements

Every concept page in an OKF bundle (excluding `index.md` and `log.md`) carries structured YAML frontmatter:

```yaml
---
type: <Type>              # REQUIRED — Entity | Concept | Comparison | Source | Q&A | Overview
title: "<Display name>"  # Recommended
description: "<One-line summary>"  # Recommended
tags: [<tag>, ...]        # Optional
status: draft             # draft | stable | deprecated (default: stable)
generated: { by: copilot-librarian/1.0, at: <ISO-8601 datetime> }
sources:                  # Include when the concept derives from external material
  - id: <slug>
    resource: <URL or bundle-relative path>
    title: "<Source title>"
    author: <actor>
    last_modified: <YYYY-MM-DD>
---
```

### Actor Conventions
For `generated.by` and `verified[].by`:
- **AI-generated**: `copilot-librarian/1.0`
- **Human-authored**: `human:<username>`
- **Automated process**: `process:<id>`

### Trust Tiers (Derived from `verified`)
- No `verified` field: **unverified**
- `verified` by non-`human:` actors only: **machine-confirmed**
- `verified` by a `human:<id>` actor: **human-reviewed**

---

## 3. Page Formats & Types

| Type | OKF `type` value | Required Frontmatter | Required Body Sections |
| :--- | :--- | :--- | :--- |
| **entity** | `Entity` | `type`, `title`, `description`, `generated` | `## Overview`, `## Key Facts`, `## See Also` |
| **concept** | `Concept` | `type`, `title`, `description`, `generated` | `## Definition`, `## How It Works`, `## See Also` |
| **comparison** | `Comparison` | `type`, `title`, `description`, `generated` | `## Summary Table`, `## See Also` |
| **source** | `Source` | `type`, `title`, `description`, `generated`, `sources` | `## Key Takeaways`, `## Pages Created/Updated`, `## See Also` |
| **qa** | `Q&A` | `type`, `title`, `description`, `generated` | `## Question`, `## Answer`, `## Pages Consulted`, `## See Also` |
| **overview** | `Overview` | `type`, `title`, `description`, `generated` | `## Overview`, `## Core Aspects`, `## See Also` |

---

## 4. Subdirectory Progressive Disclosure

Each content subdirectory maintains its own `index.md` listing local pages using asterisk bullets:
```markdown
# Entities

Named things in the ecosystem (features, products, people, systems).

* [Entity Name](entity-slug.md) - One-line summary
```
This enables agents to inspect a specific category without ingesting the entire global index.
