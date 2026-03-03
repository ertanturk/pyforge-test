# Future Improvements - PyForge Test

PyForge Test is a personal testing framework built for use in my own projects.
It is not intended to compete with pytest or other full-scale frameworks.
The focus is simplicity, control, and long-term maintainability.

---

## Phase 1 – Core Stability & CLI UX (Required Before Everything)

These improvements make the framework reliable and pleasant to use.

- [ ] Centralized Stats Tracker (passed, failed, skipped, errors, duration)
- [ ] Proper Exit Codes (0 = success, 1 = failures, 2 = internal error)
- [ ] Verbosity Levels (`-q`, default, `-v`)
- [ ] Selective Running
  - File path filtering
  - `-k` substring filtering
- [ ] Colorized Output
- [ ] Fail-Fast Option (`--fail-fast`)
- [ ] Per-Test Duration Tracking

Goal:
Stable, predictable behavior suitable for daily development.

---

## Phase 2 – Developer Efficiency

Add only what improves productivity in real projects.

- [ ] JSON Report Output (for automation or CI use)
- [ ] Marker-Based Execution (`-m slow`)
- [ ] Max Failures Option (`--max-failures N`)
- [ ] Improved Traceback Formatting (clean, readable errors)
- [ ] Basic Fixture Injection System (minimal and explicit)
- [ ] `--list` / `--collect-only` mode

Goal:
Reduce friction during debugging and larger test suites.

---

## Phase 3 – Scaling (Only If Needed)

These features will only be implemented if future projects require them.

- [ ] Parallel Test Execution (process-based)
- [ ] Configurable Test Timeouts
- [ ] Randomized Test Order with Seed Control

These add complexity and will not be implemented unless there is a real need.

---

## Design Principles

- Keep the surface area small.
- Avoid unnecessary abstraction.
- Do not reimplement full pytest functionality.
- Prefer clarity over cleverness.
- Every new feature must solve a real problem in an actual project.

---

## Versioning Philosophy

This project follows pragmatic versioning:

- v0.x → Internal evolution
- v1.0.0 → Only after it has been used successfully in multiple real projects without architectural changes

No rushed 1.0 release.
Stability comes from usage, not ambition.hanges

No rushed 1.0 release.
Stability comes from usage, not ambition.

discuss potential improvements.

Stability comes from usage, not ambition.

discuss potential improvements.
.

Stability comes from usage, not ambition.

discuss potential improvements.
