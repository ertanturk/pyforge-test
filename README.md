# PyForge Test

A lightweight Python unit testing framework for personal projects and learning — zero configuration, decorator-based tests, automatic discovery.

[![PyPI version](https://img.shields.io/pypi/v/pyforge-test)](https://pypi.org/project/pyforge-test/)
[![Python 3.12+](https://img.shields.io/pypi/pyversions/pyforge-test)](https://pypi.org/project/pyforge-test/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Note**: PyForge is designed for personal projects, learning, and small-scale testing. It is **not** a competitor to production-grade frameworks like pytest or unittest.

## When to Use PyForge

✓ Personal projects and hobby development  
✓ Learning Python testing concepts  
✓ Quick prototyping without framework overhead  
✓ Single-module or small-package testing

**Not recommended for:** production applications, large organizational projects, or CI/CD pipelines with complex requirements.

## Features

- **Decorator-based** — `@test` marks a function as a test
- **Automatic discovery** — Finds and loads all `test*.py` files in `tests/`
- **Zero configuration** — Works in any project structure
- **Zero dependencies** — Pure Python, no external packages
- **Parameterized tests** — Run one test function with many input sets
- **Skip & markers** — `@test_skip`, `@test_skipif`, `@test_marker`
- **Clean tracebacks** — Internal framework frames filtered out; location shown in normal mode, full colorized traceback in verbose mode
- **Type-safe** — Full PEP 484 type hints throughout
- **Python 3.12+** — Modern Python support

## Installation

```bash
pip install pyforge-test
```

Or install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/ertanturk/pyforge-test.git
```

Or for local development:

```bash
git clone https://github.com/ertanturk/pyforge-test.git
cd pyforge-test
pip install -e .
```

## Quick Start

### 1. Create test directory

```bash
mkdir -p tests && touch tests/__init__.py
```

### 2. Create test file

Create `tests/test_example.py`:

```python
from pyforge_test import test


@test
def test_addition() -> None:
    assert 2 + 2 == 4


@test
def test_string_concat() -> None:
    assert "Hello" + " World" == "Hello World"
```

### 3. Run tests

```bash
pyforge
```

Expected output:

```
Discovering test modules in '/path/to/tests'...
Loaded: test_example.py

Loaded 1 test module(s).

Executing 2 test(s).


PyForge Test Results
------------------------------------------------------------------------

test_example.py
  PASSED test_addition (Line 4)
  PASSED test_string_concat (Line 9)

------------------------------------------------------------------------
Summary: PASSED: 2/2  FAILED: 0/2  SKIPPED: 0/2  ERRORS: 0/2
Took 1 ms to execute all tests
------------------------------------------------------------------------
```

## CLI Options

```bash
pyforge                    # Run all tests (normal output)
pyforge -q                 # Quiet: only show failures and summary
pyforge -v                 # Verbose: show full colorized tracebacks
pyforge --fail-fast        # Stop at first failure
pyforge -k basic           # Run tests with 'basic' in their name
pyforge test_utils.py      # Run tests from a specific file
pyforge -k api -v          # Combine options freely
```

## Test Features

### Parameterized Tests

```python
from pyforge_test import test_parameterized


@test_parameterized([
    (2, 3, 5),
    (10, 5, 15),
])
def test_addition(a: int, b: int, expected: int) -> None:
    assert a + b == expected
# Generates: test_addition_0, test_addition_1
```

### Markers

```python
from pyforge_test import test, test_marker


@test_marker("integration")   # runs after unmarked tests
@test
def test_database() -> None:
    ...


@test_marker("slow")          # runs last
@test
def test_performance() -> None:
    ...
```

Execution order: **unmarked (0)** → **integration (1)** → **slow (2)**

> `@test_marker` must come **before** `@test`.

### Skip

```python
from pyforge_test import test, test_skip, test_skipif
import sys


@test_skip(reason="Not implemented yet")
def test_future() -> None:
    ...


@test_skipif(sys.platform == "win32", reason="Unix only")
def test_unix() -> None:
    ...
```

## Project Structure

```
my-project/
├── src/
│   └── mypackage/
├── tests/
│   ├── __init__.py          # Required (can be empty)
│   ├── test_core.py
│   └── test_utils.py
└── pyproject.toml
```

## Documentation

Full documentation: [Documentation.md](Documentation.md)  
Roadmap: [FUTURE_UPDATES.md](FUTURE_UPDATES.md)

## Development

Code standards:

- PEP 484 type hints on all functions
- Google-style docstrings
- Exception chaining: `raise ... from e`
- No bare `except` statements

## License

MIT — See [LICENSE](LICENSE) for details

## Contributing

Contributions welcome! Open an issue or pull request on [GitHub](https://github.com/ertanturk/pyforge-test).

---

**Status**: Alpha (v0.1.0)
