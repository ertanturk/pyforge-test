# Future Improvements - PyForge Test

---

## Phase 1 – Core Stability & CLI UX

These improvements make the framework reliable and pleasant to use.

- [x] Centralized Stats Tracker (passed, failed, skipped, errors, duration)
- [x] Proper Exit Codes (0 = success, 1 = failures, 2 = internal error)
- [x] Verbosity Levels (`-q`, default, `-v`)
- [x] Selective Running
  - File path filtering
  - `-k` substring filtering
- [x] Colorized Output
- [x] Fail-Fast Option (`--fail-fast`)

Goal:
Stable, predictable behavior suitable for daily development.

---

## Phase 2 – Developer Efficiency

Add only what improves productivity in real projects.

- [x] Improved Traceback Formatting (clean, readable errors)
- [ ] JSON Report Output (for automation or CI use)
- [ ] Max Failures Option (`--max-failures N`)

Goal:
Reduce friction during debugging and larger test suites.

---

## Phase 3 – Scaling (Only If Needed)

These features will only be implemented if future projects require them.

- [ ] Parallel Test Execution (process-based)
- [ ] Configurable Test Timeouts

These add complexity and will not be implemented unless there is a real need.

---
