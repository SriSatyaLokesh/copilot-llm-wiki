# Gemini Adapter for Superpowers

> **Everything in this file is optional.**
> For core skills logic, see the `skills/` library.

This adapter provides tool-specific optimizations for Gemini models running Superpowers in Antigravity.

---

## Model Selection Guidance

| Model Type | Recommended Task | Why |
|------------|------------------|-----|
| **Gemini Pro** | Brainstorming, Planning, Architecture | Superior reasoning for high-level design |
| **Gemini Flash** | TDD loops, Small fixes, Task execution | High speed and efficiency for atomic changes |

---

## Tool Integration

### run_command
When using `run_command` within a Superpowers skill:
- Set `SafeToAutoRun: true` for idempotent, non-destructive commands (e.g., `git status`, `npm test`).
- Use `WaitMsBeforeAsync` appropriately for long-running test suites.

### browser_subagent
The `brainstorming` and `systematic-debugging` skills should leverage `browser_subagent` for:
- API documentation research.
- UI/UX verification using screenshots.
- Troubleshooting error codes found in web search.

---

## Context Management

Gemini's large context window is an advantage, but **Search-First** remains the primary discipline.
- Use `grep_search` or `find_by_name` before reading files.
- If a file is >300 lines, use `view_file_outline`.

---

*Part of the Superpowers for Antigravity integration.*
