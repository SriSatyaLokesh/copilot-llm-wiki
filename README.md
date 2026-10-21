# GitHub Copilot LLM Wiki: Compounding Knowledge Engine

**A production-grade, zero-dependency, LLM-first personal knowledge engine implementing Andrej Karpathy's Compounding Knowledge Pattern.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B%20(Stdlib%20Only)-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Multi-LLM](https://img.shields.io/badge/LLMs-Copilot%20%7C%20Claude%20%7C%20Gemini%20%7C%20Cursor-orange.svg)](#-multi-llm-environment-adapters)
[![Knowledge Graph](https://img.shields.io/badge/Graph-Directed%20Property%20Graph-8957e5.svg)](#-directed-property-graph-wikigraphjson)
[![Semantic Retrieval](https://img.shields.io/badge/Retrieval-Local%20Dense%20Index-0969da.svg)](#-lightweight-semantic-index-wikisemantic-indexjson)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 💡 The Philosophy: LLM-First Compounding Knowledge

Traditional RAG (Retrieval-Augmented Generation) chops unstructured text into disjointed chunks and embeds them into opaque vector databases. Every query searches for statistical cosine similarity, leaving the knowledge base static, fragile, and disconnected from document hierarchy.

This project implements the **Compounding Knowledge Pattern** popularized by [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), purpose-built as an **LLM-First Knowledge Engine**:

- **Humans query the LLM**: You don't waste time hunting through notes, browsing folder trees, or reading markdown files manually. You ask your AI coding assistant (GitHub Copilot, Claude Code, Gemini CLI, Cursor).
- **The LLM maintains the Wiki**: Your AI assistant acts as an autonomous librarian. It reads raw sources, creates canonical entities and concepts, tags claim citations, preserves historical provenance, and traverses semantic edges.
- **Compounding returns**: Every ingested document and every synthesized architectural answer permanently enriches the wiki. Instead of starting from scratch on every query, the LLM builds upon accumulated knowledge.
- **Zero infrastructure overhead**: **100% Python standard library**. No vector database servers, no cloud API keys for storage, no Docker containers, and no complex external runtime dependencies. Runs directly inside any cloned git repository on Windows, Linux, and macOS.

```
                     ┌────────────────────────────────┐
                     │          HUMAN USER            │
                     └───────────────┬────────────────┘
                                     │ Natural Language Queries
                                     ▼
                     ┌────────────────────────────────┐
                     │    AI ASSISTANT / AGENT        │
                     │ (Copilot, Claude, Gemini, etc) │
                     └───────┬────────────────▲───────┘
          Deterministic Tool │                │ Progressive Context
               & Graph Calls │                │ Retrieval
                             ▼                │
┌────────────────────────────────────────────────────────────────────────┐
│                        KNOWLEDGE ENGINE CORE                           │
│                                                                        │
│  ┌───────────────────────┐  compiles  ┌─────────────────────────────┐  │
│  │   raw/ (Immutable)    │ ─────────► │ wiki/                       │  │
│  │   - Primary Sources   │            │   - entities/   - concepts/ │  │
│  │   - Archived Deltas   │            │   - comparisons/- sources/  │  │
│  │                       │            │   - qa/         - archive/  │  │
│  └───────────────────────┘            └──────────────┬──────────────┘  │
│                                                      │                 │
│         ┌────────────────────────────────────────────┴──────────┐      │
│         ▼                                                       ▼      │
│  ┌───────────────────────────────┐     ┌────────────────────────────┐  │
│  │ wiki/semantic-index.json      │     │ wiki/graph.json            │  │
│  │ (Dense summaries & keywords)  │     │ (Nodes & directed edges)   │  │
│  └───────────────────────────────┘     └────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🌟 What This Repository Offers

### 1. 🔍 Sub-Cent Query Routing (`wiki/semantic-index.json`)
Large wikis (200+ pages) quickly saturate LLM context windows if agents load arbitrary markdown files. The engine generates a dense, file-based semantic index containing entity summaries, high-signal keyword maps (with built-in stopword filtering), and outbound link lists.
- Agents inspect `wiki/semantic-index.json` or query via CLI (`python scripts/build-semantic-index.py --query "<query>"`) to pinpoint exact candidate notes in milliseconds before reading file contents.
- **Zero cloud embeddings or vector DBs required.**

### 2. 🕸️ Directed Property Graph (`wiki/graph.json`)
The entire wiki is modeled as a formal directed property graph. Every entity and concept declares typed, single-direction relationships adhering to a closed taxonomy:
- `depends-on`: Architectural or functional dependency
- `implements`: Realizes a specification, concept, or protocol
- `part-of`: Hierarchical component or subsystem membership
- `supersedes`: Replaces an older entity or document (pairs with archiving)
- `contradicts`: Flags unresolved trade-offs or source conflicts
- `related-to`: Lateral association

The manifest generator compiles all nodes and relationships into `wiki/graph.json` with sub-second execution, automatically detecting graph orphans and disconnected components.

### 3. 📂 Hierarchical Progressive Disclosure Indexes
To scale beyond context limits, indexes are deterministically compiled by `scripts/build-index.py`:
- **Root Routing Index (`wiki/index.md`)**: Contains high-level page counts and links to silo indexes.
- **Silo Sub-Indexes (`wiki/<silo>/index.md`)**: Alphabetical catalogs with one-line descriptions for `entities/`, `concepts/`, `comparisons/`, `sources/`, `qa/`, and `archive/`.

### 4. 🤖 Multi-LLM Environment Adapters
Dedicated instruction files tuned for each major AI coding assistant, synchronized from authoritative schemas to eliminate prompt drift:
- **GitHub Copilot**: `.github/copilot-instructions.md` & `AGENTS.md`
- **Claude Code (Anthropic)**: `CLAUDE.md` (optimized for Claude Opus/Sonnet, tool invocation, subagent delegation)
- **Google Antigravity & Gemini CLI**: `.gemini/GEMINI.md` (tuned for multi-tool workflows, directed graph navigation)
- **Cursor IDE**: `.cursorrules` & `.cursor/rules/wiki.mdc` (context indexing with `@wiki/semantic-index.json` and `@wiki/graph.json`)
- **Drift Synchronization Engine**: `python scripts/sync-adapters.py --check` ensures zero-drift across all platforms.

### 5. 🔌 Pluggable Source Intake Architecture (`adapters/`)
Normalize diverse external formats into clean, standardized markdown in `raw/<slug>.md`:
- **Web Pages (`adapters/url_adapter.py`)**: Fetches HTML, strips scripts/nav/styles, and formats semantic markdown.
- **PDF Documents (`adapters/pdf_adapter.py`)**: Extracts multi-page text using `pypdf` or built-in stream decoding fallback.
- **Tabular Data (`adapters/csv_adapter.py`)**: Converts CSV files and raw tables into GitHub Flavored Markdown tables.
- **GitHub Issues/PRs (`adapters/github_issues_adapter.py`)**: Pulls titles, descriptions, labels, and discussion threads via `gh` CLI or JSON exports.
- **Automatic Intake Router**: `python scripts/intake.py <source>` automatically selects the right adapter.

### 6. 🕒 Living Source Freshness & Volatility Classes
Knowledge decays at different rates. Every ingested source document specifies an explicit **Volatility Class**:
- **High Volatility (30-day cycle)**: Microservice APIs, schemas, pricing tables, active product specs.
- **Medium Volatility (90-day cycle)**: System architecture, integration workflows, team processes.
- **Low Volatility (365-day cycle)**: Invariant math, RFC protocols, foundational design principles.

The linter (`scripts/lint-wiki.py`) automatically evaluates `Last Verified` timestamps and warns when documents enter aging or stale status.

### 7. 🔄 3-Way Delta Reingest Engine (`scripts/reingest.py`)
When a primary source changes:
- Prior raw snapshots are archived to `raw/archive/<slug>-<timestamp>.md`.
- A 3-way delta evaluation compares the prior source vs. the updated source against existing wiki pages.
- **Reference-Counted Attribution**: If an old assertion is removed from this source but backed by another active source, it remains cited. If no sources back it, it is safely moved to `### Deprecated / Historical Claims` rather than silently erased.

### 8. 📸 Git-Backed Semantic Snapshots & Instant Rollback
Perform batch operations and experimental ingests with complete safety:
- **Snapshot**: `python scripts/snapshot.py <name> [description]` creates a lightweight Git tag (`snapshot-<name>`) and records an entry in `wiki/meta/snapshots.md`.
- **Rollback**: `python scripts/rollback.py <name>` performs a semantic rollback of the `wiki/` directory while preserving uncommitted work safety.

### 9. 🛡️ Strict Deterministic Linter (`scripts/lint-wiki.py`)
Run `python scripts/lint-wiki.py --strict` to validate:
- Index synchronization across all 7 catalogs
- Graph manifest integrity and isolated orphan node detection
- Semantic index freshness and keyword mapping
- Multi-LLM instruction adapter synchronization
- Broken markdown links and archive link violations
- Claim provenance footnotes across all `## Key Facts`
- Source staleness based on volatility cycles

---

## 📁 Repository Structure

```
copilot-llm-wiki/
├── raw/                             ← Primary sources (IMMUTABLE: read-only)
│   └── archive/                     ← Previous source snapshots for delta reingest
├── wiki/                            ← Persistent knowledge layer (LLM-MAINTAINED)
│   ├── index.md                     ← Root routing index
│   ├── log.md                       ← Append-only chronological audit log
│   ├── overview.md                  ← Top-level orientation and domain overview
│   ├── graph.json                   ← Auto-generated directed property graph
│   ├── semantic-index.json          ← Dense local keyword & candidate routing index
│   ├── entities/                    ← Named things: actors, systems, APIs, services
│   ├── concepts/                    ← Core abstractions: protocols, lifecycles, rules
│   ├── comparisons/                 ← Side-by-side matrices and trade-off tables
│   ├── sources/                     ← Summaries and volatility metadata of ingested docs
│   ├── qa/                          ← Synthesized answers to multi-page queries
│   └── archive/                     ← Deprecated and superseded knowledge documents
├── adapters/                        ← Pluggable intake adapter framework
│   ├── base.py                      ← Abstract BaseSourceAdapter
│   ├── url_adapter.py               ← Web page scraper and markdown converter
│   ├── pdf_adapter.py               ← PDF text extractor
│   ├── csv_adapter.py               ← CSV to Markdown table converter
│   ├── github_issues_adapter.py     ← GitHub Issue/PR parser
│   └── registry.py                  ← Protocol and extension routing registry
├── scripts/                         ← Deterministic automation CLI tools (Python + Shell + PS1)
│   ├── build-index.py               ← Hierarchical sub-index & root catalog compiler
│   ├── build-graph.py               ← Directed property graph compiler
│   ├── build-semantic-index.py      ← Semantic candidate index compiler
│   ├── intake.py                    ← Multi-format intake router
│   ├── reingest.py                  ← Delta reingestion & archive engine
│   ├── lint-wiki.py                 ← Strict comprehensive wiki linter
│   ├── snapshot.py                  ← Git tag-based snapshot capture
│   ├── rollback.py                  ← Instant semantic rollback
│   └── sync-adapters.py             ← Multi-LLM adapter synchronizer
├── tests/                           ← Comprehensive stdlib test suite (23 tests)
├── .github/copilot-instructions.md  ← Authoritative GitHub Copilot instruction schema
├── AGENTS.md                        ← Cross-vendor unified agent instructions
├── CLAUDE.md                        ← Claude Code environment instructions
├── .gemini/GEMINI.md                ← Google Antigravity & Gemini CLI instructions
├── .cursorrules                     ← Cursor IDE root instructions
└── .cursor/rules/wiki.mdc           ← Cursor rules file format
```

---

## ⚡ Quickstart Guide

### 1. Clone & Set Up
```bash
git clone https://github.com/SriSatyaLokesh/copilot-llm-wiki.git my-wiki
cd my-wiki
```
*No virtual environments or pip installs required for core operations. Python 3.10+ standard library is all you need.*

### 2. Ingesting New Material
Tell your LLM assistant:
> *"Ingest https://docs.github.com/en/copilot/overview"*
> or
> *"Add data/pricing.csv to the wiki"*

Or run the intake router from your terminal:
```bash
# Normalize any URL, PDF, CSV, or GitHub issue into raw/<slug>.md
python scripts/intake.py https://docs.github.com/en/copilot/overview
```

The LLM will:
1. Normalize and read the source into `raw/<slug>.md`.
2. Present key takeaways and outline pages to create or update.
3. Check for contradictions against existing wiki notes.
4. Write a source summary in `wiki/sources/<slug>.md` with its Volatility Class.
5. Create or update entity and concept pages with explicit `## Relationships` and provenance footnotes.
6. Rebuild all indexes, graph manifests, and semantic indexes via `python scripts/build-index.py`.
7. Append an audit entry to `wiki/log.md`.

### 3. Querying Accumulated Knowledge
Ask your AI assistant:
> *"What systems participate in change order provisioning and what are their dependencies?"*

The LLM will:
1. Consult `wiki/semantic-index.json` or `scripts/build-semantic-index.py --query "..."` to locate exact candidate files in milliseconds without scanning the whole repository.
2. Traverse typed edges in `wiki/graph.json` to follow related entities.
3. Synthesize an answer with explicit file and source citations.
4. Offer to save the synthesized answer as a new document in `wiki/qa/`.

### 4. Health & Consistency Linting
Verify your knowledge base anytime:
```bash
python scripts/lint-wiki.py --strict
# Or use cross-platform runners:
./scripts/lint.sh
.\scripts\lint.ps1
```

### 5. Capturing Snapshots & Rolling Back
```bash
# Capture a snapshot before a batch ingest
python scripts/snapshot.py pre-ingest "Before importing 10 RFC specs"

# Rollback anytime if an ingest is unsatisfactory
python scripts/rollback.py pre-ingest
```

---

## 🛠️ CLI Tool Reference

All scripts provide cross-platform Bash (`.sh`) and PowerShell (`.ps1`) wrappers:

| Command | Description |
|---|---|
| `python scripts/intake.py <src>` | Ingests URL, PDF, CSV, or GitHub Issue into `raw/<slug>.md` |
| `python scripts/build-index.py` | Recompiles all 6 silo sub-indexes, root `index.md`, graph, and semantic index |
| `python scripts/build-graph.py` | Generates `wiki/graph.json` and reports isolated orphan nodes |
| `python scripts/build-semantic-index.py` | Generates `wiki/semantic-index.json` for fast keyword query routing |
| `python scripts/lint-wiki.py --strict` | Runs strict validation (indexes, graph, links, citations, freshness, adapters) |
| `python scripts/snapshot.py <name>` | Creates a semantic Git snapshot of the wiki |
| `python scripts/rollback.py <name>` | Reverts `wiki/` to a previously captured snapshot |
| `python scripts/reingest.py <slug>` | Archives prior source and triggers 3-way delta evaluation |
| `python scripts/sync-adapters.py` | Synchronizes `CLAUDE.md`, `.gemini/GEMINI.md`, and Cursor instructions |
| `python -m unittest discover tests` | Runs the full test suite (23 tests, sub-second execution) |

---

## 🔒 Cardinal Rules & Invariants

1. **`raw/` is immutable**: Never edit or delete files in `raw/`. It serves as the untampered source of truth for claim citations and delta reingestion.
2. **`wiki/log.md` is append-only**: Never modify or truncate historical log entries.
3. **Index-first routing**: LLMs must check `wiki/semantic-index.json` or `wiki/index.md` before loading or creating notes.
4. **Zero-contradiction guarantee**: Any conflict between new sources and existing wiki pages must be explicitly surfaced to the user before committing.
5. **Deterministic indexing**: LLMs never edit `index.md`, `graph.json`, or `semantic-index.json` manually; they are compiled deterministically by scripts.

---

## 🤝 Contributing & Community

Contributions are warmly welcomed! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md).

- Found a bug or edge case? Open a [Bug Report](https://github.com/SriSatyaLokesh/copilot-llm-wiki/issues/new?template=bug_report.yml).
- Have an idea for a source adapter or optimization? Submit a [Feature Request](https://github.com/SriSatyaLokesh/copilot-llm-wiki/issues/new?template=feature_request.yml).
- Join the conversation in [GitHub Discussions](https://github.com/SriSatyaLokesh/copilot-llm-wiki/discussions).

---

## 📜 Citation & License

```bibtex
@software{copilot_llm_wiki_2026,
  author = {Sri Satya Lokesh},
  title = {GitHub Copilot LLM Wiki: Compounding Knowledge Engine},
  url = {https://github.com/SriSatyaLokesh/copilot-llm-wiki},
  year = {2026}
}
```

This project is open-source software licensed under the [MIT License](LICENSE).

---
*Built on Andrej Karpathy's Compounding Knowledge Pattern. Engineered for the multi-LLM era.*
