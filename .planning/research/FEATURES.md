# Features Research

**Domain:** LLM-maintained personal knowledge base (Copilot-native wiki template)
**Researched:** 2026-04-10
**Mode:** Ecosystem

---

## Table Stakes

Features users expect. Missing = the pattern fails or the template gets forked and immediately gutted.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Ingest workflow | Core value — without it, the wiki never grows | Low | One source at a time is the right default; discuss takeaways before writing |
| Query workflow | Reason users open the wiki at all | Low | Index-first navigation, citations required; filing back answers compounds value |
| Lint workflow | Without it, orphans and broken links accumulate until the wiki is untrustworthy | Medium | Check orphans, broken links, missing cross-refs, contradictions |
| `index.md` as catalog | LLM's navigation layer — without it, Copilot reads every file blindly | Low | One-line per page, alphabetically sorted per section, updated on every ingest |
| `log.md` as append-only audit trail | Provenance — users need to see what changed and when | Low | Never edit past entries; parseable with standard tools |
| Source summary pages (`sources/`) | Traceability from wiki claim back to origin document | Low | One page per ingested source; links to pages created/updated |
| Entity pages (`entities/`) | Named things recur across sources — consolidation prevents duplication | Low-Med | Single source of truth per entity; updated incrementally |
| Concept pages (`concepts/`) | Foundational ideas need explanation, not just repeated assertion | Low-Med | Cross-linked to every entity and source that uses the concept |
| `See Also` section on every page | Navigation glue — wiki pages without outbound links are dead ends | Low | Required convention; LLM must enforce it on every page write |
| Consistent filename conventions | Diffable, predictable, toolable | Trivial | Lowercase kebab-case; no spaces |
| `raw/` immutability rule | Source integrity — once corrupted, provenance is gone | Trivial | Read-only by convention; LLM instructed never to modify |
| Batch / no-argument ingest | Users want to drop multiple files in `raw/` and process all at once | Medium | The Claude intake command already handles this; Copilot equivalent needed |
| Pre-write takeaway discussion | Prevents silent hallucination; forces LLM to show reasoning before committing to disk | Low | "State key takeaways before writing anything" — already in schema |
| Fork-ready scaffold | Template is useless if forking requires more than 10 minutes of setup | Low | Empty wiki structure with stubs and placeholder conventions |

---

## Differentiators

What makes this pattern better than RAG / NotebookLM / "upload and ask."

### 1. Compiled, Compounding Knowledge

RAG re-derives answers from raw documents on every query. This wiki compiles knowledge once and keeps it current. A question answered today enriches the wiki for tomorrow. Each ingest touches 10-15 existing pages, creating a cross-referenced knowledge structure that grows denser over time.

**Consequence for the template:** The query workflow must include "offer to file the answer as a wiki page" — this is the compound-interest mechanism. Without it, the wiki only grows on ingest, not on use.

### 2. Filing Loop (Query-Driven Growth)

When a query synthesizes across multiple pages in a reusable way, the LLM files the synthesis as a new wiki page. Karpathy identified this as the key differentiator: knowledge base grows automatically from usage patterns, not just from manual source ingestion. Users don't have to explicitly decide to write something down — the act of asking a good question creates the entry.

**Consequence for the template:** Query workflow must prompt the LLM to offer filing after every multi-page synthesis.

### 3. Interpretable Retrieval

RAG is a black box — you get an answer but not which documents were consulted or why. This wiki surfaces exactly which pages the LLM read and in what order. Users can audit the answer path, verify reasoning, and trust the output more.

**Consequence for the template:** Every query answer must end with a citations block listing pages consulted. This is non-optional.

### 4. Zero Infrastructure

NotebookLM requires Google's cloud. RAG requires embeddings, vector stores, and a retrieval pipeline. This wiki requires a git repo and a Copilot subscription. The entire system is plain markdown — readable without any tooling, diffable, and collaborative with standard git workflows.

**Consequence for the template:** No build steps, no scripts required for core operation, no cloud dependencies. `copilot-instructions.md` as auto-loaded schema is the entire infrastructure.

### 5. Git as Knowledge History

Every ingest, every page update, every lint fix is a git commit. Users get time-travel across their knowledge base — they can see what was known on any date, trace which source triggered a belief, and roll back mistakes. No wiki platform offers this natively.

**Consequence for the template:** The log.md append-only pattern reinforces git history but should not replace it. Commit hygiene matters.

### 6. LLM as Maintainer, Not Search Engine

The wiki's maintenance burden (updating cross-references, detecting contradictions, filing new pages) is the part that causes humans to abandon wikis. LLMs don't get bored, don't forget to update a backlink, and can touch 15 files in one pass. This flips the abandonment dynamic: the cost of maintenance is near zero.

**Consequence for the template:** Lint must be comprehensive enough that "lint the wiki" is a complete health-check, not just an orphan finder. Contradiction detection and missing cross-references are first-class lint checks.

---

## Anti-Features

Features to deliberately NOT build, with rationale.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| RAG / embeddings / vector store | Adds infrastructure, breaks "zero infra" constraint, obscures retrieval | index.md + context window is sufficient to ~400K words; flag scale limit clearly |
| Automatic web scraping | Removes human curation — the intentional filter that keeps the wiki signal-rich | Users use Obsidian Web Clipper or manual copy; source selection stays human |
| Multi-user real-time sync | Adds conflict resolution complexity; the pattern is personal-first | Git branching/PRs handles team collaboration if needed; don't bake in |
| Hosted publishing pipeline | External publishing (GitHub Pages, MkDocs) is meaningful but out of scope for v1 | Document it as an optional enhancement; don't make it required infrastructure |
| Automatic ingestion triggers | Auto-ingesting on file drop removes the discuss-before-write step that prevents hallucination | Keep ingest explicitly user-triggered |
| Confidence scores / metadata frontmatter | Adds schema overhead users must maintain; degrades readability in Obsidian | Use source attribution in page prose instead ("per [source-slug]...") |
| Synthesis / reflection as a scheduled job | Event-driven compilation requires infrastructure; "reflect" is a manual operation for now | Users invoke `/query` or `/lint` when they want synthesis; don't automate |
| Fine-tuning / model weights updates | Requires retraining infrastructure — explicitly out of scope | The compiled wiki IS the persistent memory layer |
| Claude-specific primitives in core schema | Project targets Copilot; Claude tooling is secondary | `.claude/commands/` can exist but `copilot-instructions.md` is authoritative |
| Glossary / FAQ as required page types | These emerge naturally from concepts/ pages; forcing them adds friction without value for all domains | Let the domain drive taxonomy; provide them as optional scaffold examples |

---

## Page Type Taxonomy

All wiki page categories, with purpose and format notes. Organized by whether they are required (always present), standard (common across domains), or optional (domain-specific).

### Required Pages

These must exist in every fork from day one.

| Page | Path | Purpose | Format Notes |
|------|------|---------|--------------|
| Index | `wiki/index.md` | Master catalog; LLM reads this first on every query | One line per page, sections by category, alphabetically sorted |
| Log | `wiki/log.md` | Chronological audit trail of every operation | Append-only; `## [YYYY-MM-DD] operation \| description` format |
| Overview | `wiki/overview.md` | Top-level synthesis: what is this domain, what are the major pillars | Free-form synthesis; updated when major new entities/concepts land |

### Standard Page Types

Present in most domains. The core taxonomy.

| Page Type | Path | Purpose | Format Notes |
|-----------|------|---------|--------------|
| Source summary | `wiki/sources/<slug>.md` | One page per ingested document; key takeaways, cross-links | Header with source URL/date; bullet takeaways; "Pages created/updated" section; See Also |
| Entity | `wiki/entities/<name>.md` | Named things: features, products, people, organizations, plans, models | Factual prose; version/plan-specific claims attributed; See Also required |
| Concept | `wiki/concepts/<name>.md` | Foundational ideas, mechanisms, patterns | Definition first; how it relates to entities; See Also required |
| Comparison | `wiki/comparisons/<slug>.md` | Side-by-side tables for things that are often conflated | Markdown tables preferred; note when comparison was last validated; See Also |

### Optional Page Types

Not every domain needs these, but they are domain-agnostic and commonly valuable. Include as scaffold stubs where the domain warrants.

| Page Type | Path | Purpose | Format Notes |
|-----------|------|---------|--------------|
| Decision | `wiki/decisions/<slug>.md` | Records a choice made and its rationale (ADR-style) | Status, Context, Decision, Consequences sections; immutable once "accepted" |
| Timeline | `wiki/timelines/<slug>.md` | Chronological history of a feature, product, or domain | Reverse-chronological (newest first); cite sources for each event |
| FAQ / Q&A | `wiki/qa/<slug>.md` | Answers to recurring questions, filed after query workflow | Question as title; answer as prose; pages consulted as citations; See Also |
| Relationship map | `wiki/relationships/<slug>.md` | Explicit mapping of how entities relate to each other | Prose or table; useful for complex ecosystems with many interacting components |
| Glossary | `wiki/glossary.md` | Single-page term definitions for the domain | Alphabetical; one-liner per term; links to full concept/entity pages |

### Missing from Existing Schema (Gaps Found in Research)

The current `copilot-instructions.md` lacks these page types that community implementations have found valuable:

1. **`decisions/`** — Architecture Decision Records are domain-agnostic and valuable for any evolving technical domain. The copilot-instructions.md schema currently has no equivalent. Add as optional but document the format.

2. **`timelines/`** — Chronological histories are natural for versioned products (Copilot plans, model releases, feature rollouts). Currently implicit in entity pages but deserves its own type when a domain has significant version history.

3. **`qa/`** (filed answers) — The "filing loop" (filing query answers back into the wiki) is identified as the key differentiator. Without a designated home for filed answers, they end up as unstructured additions to entity/concept pages. A `qa/` directory gives them a home, keeps them indexed, and preserves the citation chain.

4. **`archive/`** — When pages are superseded or merged, they need a home with redirect pointers rather than deletion. Deletion breaks backlinks; archiving preserves provenance.

---

## Librarian Instruction Patterns

What makes a great `copilot-instructions.md` for a wiki. Based on GitHub's documented best practices plus patterns from community LLM wiki implementations.

### Structural Patterns

**1. Role Statement First**
Lead with a single-sentence identity: "You are the maintainer of this wiki." This anchors every subsequent instruction and prevents Copilot from treating it as a generic coding assistant.

**2. Workflow Trigger Phrases**
Each operation needs explicit trigger phrases, not just descriptions. `"Triggered by: 'ingest X', 'add X to the wiki', 'process this'"` tells the LLM exactly when to activate a workflow without the user needing to remember a slash command.

**3. Numbered Steps, Not Prose**
Each workflow must be a numbered list of concrete steps, not a paragraph. The ingest workflow in the existing schema is excellent: 6 numbered steps, imperative verbs, clear file paths. This is the right pattern.

**4. State Before Write**
The pre-write takeaway step is the most important single instruction in the schema. It forces the LLM to reason in public before committing to disk, creating a human checkpoint against hallucination. It must appear in every write-producing workflow.

**5. Explicit Cross-Link Mandate**
"A single source typically touches 5-15 pages" is a scope instruction. Without a concrete number, the LLM may only update 2-3 pages and miss integration. Keep this quantified expectation in the ingest workflow.

**6. Convention Specificity**
Generic "use good style" fails. Specific conventions work: "Plain markdown links (not wiki-style `[[]]`)", "Every page ends with `## See Also`", "Filenames: lowercase kebab-case, no spaces." Each convention needs its own line.

**7. Immutability Rules Are Load-Bearing**
"Never edit files in `raw/`" and "log.md entries are never edited or deleted" are safety constraints. State them as absolute prohibitions, not suggestions. They belong in the Conventions section, not buried in workflow steps.

### Content Patterns

**8. Schema Length Discipline**
GitHub's documented limit is ~1,000 lines before quality degrades. The current `copilot-instructions.md` is ~138 lines — healthy. Adding every optional page type, edge case, and example risks bloating it past utility. Keep the schema lean; move domain-specific detail to prompt files.

**9. Index-First Navigation**
Every query workflow must start with "Read `index.md` to find relevant pages." This is the retrieval mechanism. Without it, Copilot either reads everything (slow, hits context limits) or guesses (unreliable). It must be step 1, not a suggestion.

**10. Contradiction Detection Is Active, Not Passive**
The lint workflow lists "claims in older pages contradicted by newer sources" as a check. For ingest, add an explicit step: "Before writing, check whether any takeaway contradicts an existing wiki claim; if so, flag the contradiction before updating." This makes contradiction detection a pre-write gate, not just a periodic health-check.

**11. Attribution Over Editorializing**
"Don't editorialize — state what sources say; attribute version- or plan-specific claims." This is essential for technical domains where things change between versions. The rule prevents the wiki from drifting into LLM opinion. It belongs in Conventions with emphasis.

**12. Failure Modes to Explicitly Forbid**
Instruction files should state what NOT to do for critical failure modes:
- Never modify `raw/` files
- Never delete `log.md` entries
- Never write a wiki page without checking for an existing page on the same topic first (prevents duplicates)
- Never answer a query without citing which pages were consulted

### Prompt File Patterns (Supplementing copilot-instructions.md)

The global schema handles always-on conventions. Prompt files handle task-specific workflows where more detail is appropriate without bloating the global schema.

**`ingest.prompt.md`** — Full ingest workflow with examples of good source summaries, entity page stubs, and index entries. Attach when ingesting.

**`query.prompt.md`** — Query workflow with examples of citation format and the offer-to-file prompt. Attach when asking domain questions.

**`lint.prompt.md`** — Full lint checklist, detailed contradiction-detection heuristics, and repair instructions. Attach when running health checks.

The split: `copilot-instructions.md` defines the schema (always loaded, always enforced). Prompt files provide depth for each workflow (loaded on demand).

### Agent Skill Patterns

Agent skills (`.github/skills/`) are portable across VS Code, CLI, and Copilot Cloud Agent. They follow the same SKILL.md format regardless of surface. For a wiki template, skills should correspond to the three operations:

- `ingest.skill.md` — triggered by "ingest" context; includes the ingest steps as skill instructions
- `lint.skill.md` — triggered by "lint" or "check" context; includes the full lint checklist
- `query.skill.md` — triggered by domain questions; enforces index-first navigation and citation format

Skills are portable and can be shared across forks, making them better candidates for community contribution than the schema itself.

---

## Operations Beyond Ingest / Query / Lint

Research found several operations that implementations have added. Assessment of each for this template:

| Operation | Value | Verdict | Notes |
|-----------|-------|---------|-------|
| **Bulk / batch ingest** | High | Include | Process all unprocessed files in `raw/` — already in Claude intake; needed for Copilot equivalent |
| **Reflect / synthesize** | Medium | Include as manual | Cross-source synthesis produces new concept pages; valuable but user-triggered, not automated |
| **Merge / deduplicate** | Medium | Defer | Consolidates duplicate concept pages; real need at scale; complexity not warranted in v1 |
| **Archive** | Medium | Include as convention | Superseded pages need a home; add `wiki/archive/` and document the pattern; no separate workflow needed |
| **Export / publish** | Low | Exclude from core | MkDocs/GitHub Pages is real value but adds infrastructure; document as optional enhancement |
| **Import existing vault** | Low | Exclude | Obsidian vault migration is one-time and user-specific; a prompt file could handle it; not template-core |
| **Recall / full-text search** | Low | Exclude | Git grep and Obsidian search cover this without adding infrastructure |
| **Bootstrap / init** | High | Include | The `scripts/intake.sh` and the fork guide together constitute bootstrap; make it explicit |

### Bulk Ingest Pattern (Specifically)

One-at-a-time ingest is the right default (discuss takeaways with user before writing). But batch mode is needed for initial setup and for users who drop 10 sources at once. The resolution:

- Default: interactive ingest with takeaway discussion per source
- Batch: scan `raw/` for files not yet in `log.md` as ingested; process each with a summary but skip the interactive discussion step; produce a batch summary at the end

The existing Claude intake command already implements this pattern correctly. The Copilot equivalent must match it.

---

## UX Patterns: What Makes Wikis Actually Used vs Abandoned

Research consensus from multiple sources on the human side of the pattern:

**What kills wikis:**
- Outdated information (78% of engineers cite this as reason they don't trust internal docs)
- Invisible maintenance work that accumulates faster than value accrues
- Context-switching to a documentation platform outside the user's primary workflow
- No structural incentive to keep things current

**What keeps wikis alive with LLM maintenance:**
- LLM handles bookkeeping that humans abandon (cross-references, index updates, log entries)
- The "filing loop" — answers become wiki entries, so using the wiki improves the wiki
- Git history as audit trail — users trust the wiki because they can see its provenance
- Obsidian as the reading interface — knowledge graph visualization is free; no extra tooling
- Pre-write discussion — users see reasoning before it's committed; hallucinations get caught

**Friction points specific to Copilot-native wiki:**
- Copilot is primarily invoked for coding; context-switching to "librarian mode" requires explicit prompt discipline
- `copilot-instructions.md` is always loaded — a verbose schema degrades all Copilot interactions in the repo, not just wiki ones
- No persistent session memory across VS Code Copilot Chat sessions — each query starts fresh from `index.md`
- Prompt files require manual attach; users may not know to use `ingest.prompt.md` vs. just typing "ingest this"

**Mitigations built into the design:**
- Trigger phrases ("ingest X") in the schema activate the right workflow without requiring the user to attach a prompt file every time
- Schema size discipline (under 1,000 lines) prevents Copilot quality degradation
- index.md as the persistent memory layer — LLM reads it on every query, reconstructing context from state rather than session

---

## MVP Recommendation

What the template must ship with to be useful vs. what can wait.

**Must have (day one):**
1. `copilot-instructions.md` with all three workflows (ingest, query, lint) fully specified
2. `wiki/` scaffold: `index.md`, `log.md`, `overview.md`, `entities/`, `concepts/`, `comparisons/`, `sources/`
3. Ingest prompt file (`ingest.prompt.md`) — the workflow users run most
4. Lint prompt file (`lint.prompt.md`) — health-check that builds trust
5. CLI intake script (`scripts/intake.sh`) — batch ingest for programmatic use
6. README with fork guide (10-minute setup target)

**Nice to have (v1.1):**
1. Query prompt file (`query.prompt.md`) — useful but query is the simplest workflow; schema alone handles it
2. Agent skills (`ingest.skill.md`, `lint.skill.md`) — portable to CLI/Cloud Agent; adds value but requires Copilot skill support
3. Optional page type scaffolds: `decisions/`, `timelines/`, `qa/`, `archive/`
4. Librarian agent file (`librarian.agent.md`) — dedicated CLI agent for agentic wiki operations

**Defer (v2+):**
1. Batch-compiled static site export (MkDocs/GitHub Pages)
2. Obsidian vault import workflow
3. Cross-wiki merge/federation

---

## Sources

- Karpathy LLM Wiki gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (HIGH confidence — primary pattern source)
- LLM Wiki v2 extensions: https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2 (MEDIUM confidence — community extension)
- Self-Improving KB pattern: https://louiswang524.github.io/blog/llm-knowledge-base/ (MEDIUM confidence — detailed implementation)
- Glen Rhodes Obsidian + LLM workflow: https://glenrhodes.com/andrej-karpathys-llm-powered-personal-knowledge-base-workflow-using-markdown-wikis-and-obsidian/ (MEDIUM confidence)
- GitHub Copilot custom instructions best practices: https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/ (HIGH confidence — official GitHub blog)
- VS Code agent skills docs: https://code.visualstudio.com/docs/copilot/customization/agent-skills (HIGH confidence — official docs)
- Prompt files vs instruction files: https://devblogs.microsoft.com/dotnet/prompt-files-and-instructions-files-explained/ (HIGH confidence — official Microsoft blog)
- Wiki abandonment research: https://fullscale.io/blog/build-a-technical-wiki-engineers-actually-use/ (MEDIUM confidence)
- MindStudio LLM wiki breakdown: https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code (MEDIUM confidence)
