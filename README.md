# PyForge Testing Framework

A lightweight Python testing framework with decorator-based test collection and automatic discovery—designed for personal projects and learning.

[![PyPI version](https://img.shields.io/pypi/v/pyforge-test)](https://pypi.org/project/pyforge-test/)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue)](https://pypi.org/project/pyforge-test/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Quality](https://img.shields.io/badge/Pylint-9.89%2F10-brightgreen.svg)](pyproject.toml)
[![Type Checked](https://img.shields.io/badge/Type%20Checked-Pyright-blue.svg)](pyproject.toml)

> **Note**: PyForge is designed for **personal projects, learning, and small-scale testing**. It is **not** a substitute for production frameworks like pytest.

## Features

- 🎯 **Simple Decorators** — Mark tests with `@test`, automatic collection
- 🚀 **Zero Configuration** — Works out of the box
- 📦 **Zero Dependencies** — Pure Python, nothing to install but PyForge itself
- 🔍 **Auto-Discovery** — Finds and loads all `test*.py` files automatically
- ⚡ **Fast Execution** — Minimal overhead, quick feedback
- 🏷️ **Test Markers** — Organize tests by priority (`integration`, `slow`)
- 📊 **Parameterized Tests** — Run one test with multiple inputs
- ⊘ **Skip Tests** — Conditionally skip tests with clear reasons
- ✅ **Full Type Hints** — PEP 484 type annotations throughout
- 🎨 **Clean Output** — Color-coded results with minimal internal noise

## Installation

```bash
pip install pyforge-test
```

Or from GitHub:

```bash
pip install git+https://github.com/ertanturk/pyforge-test.git
```

## Quick Start

### 1. Create Test File

```bash
mkdir -p tests && touch tests/__init__.py
```

Create `tests/test_example.py`:

```python
from pyforge_test import test


@test
def test_addition() -> None:
    """Test basic arithmetic."""
    assert 2 + 2 == 4


@test
def test_strings() -> None:
    """Test string manipulation."""
    assert "hello".upper() == "HELLO"
```

### 2. Run Tests

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
  PASSED test_strings (Line 9)

------------------------------------------------------------------------
Summary: PASSED: 2/2  FAILED: 0/2  SKIPPED: 0/2  ERRORS: 0/2
Took 5 ms to execute all tests
------------------------------------------------------------------------
```

## CLI Options

```bash
pyforge              # Run all tests
pyforge -q           # Quiet: only failures
pyforge -v           # Verbose: full tracebacks
pyforge --fail-fast  # Stop on first failure
pyforge -k api       # Filter by test name
pyforge test_api.py  # Run specific file
```

## Test Features

### Basic Tests

```python
from pyforge_test import test


@test
def test_example() -> None:
    """Test function requirements:
    - Starts with 'test_'
    - No parameters
    - Return type -> None
    - Uses @test decorator
    """
    assert True
```

### Parameterized Tests

Run the same test with multiple inputs:

```python
from pyforge_test import test_parameterized


@test_parameterized([
    (2, 3, 5),
    (10, 5, 15),
    (100, 200, 300),
])
def test_addition(a: int, b: int, expected: int) -> None:
    """Generates: test_addition_0, test_addition_1, test_addition_2"""
    assert a + b == expected
```

### Test Markers

Execution priority: **Unmarked (0)** → **Integration (1)** → **Slow (2)**

```python
from pyforge_test import test, test_marker

# Fast unit test (runs first)
@test
def test_fast() -> None:
    assert 2 + 2 == 4

# Integration test (requires external resources)
@test_marker("integration")
@test
def test_database() -> None:
    db.connect()
    assert db.is_connected()

# Slow test (performance-intensive)
@test_marker("slow")
@test
def test_large_dataset() -> None:
    result = process_records(1_000_000)
    assert len(result) == 1_000_000
```

> **Important**: `@test_marker` must come **before** `@test`

### Skip Tests

```python
import sys
from pyforge_test import test, test_skip, test_skipif


@test_skip(reason="Not implemented yet")
def test_future() -> None:
    """Always skipped."""
    pass


@test_skipif(sys.platform == "win32", reason="Unix only")
def test_unix() -> None:
    """Skipped on Windows."""
    pass
```

## Project Structure

```
my-project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   ├── __init__.py            # Required (can be empty)
│   ├── test_main.py           # Auto-discovered
│   └── test_utils.py          # Auto-discovered
├── README.md
└── pyproject.toml
```

## Code Quality

PyForge is fully type-checked and linted:

- **Ruff**: All checks passing ✅
- **Pylint**: 9.89/10 score ✅
- **Pyright**: Strict type checking ✅
- **Type Hints**: Full PEP 484 compliance ✅

## Documentation

- **Complete Guide**: [docs/Documentation.md](docs/Documentation.md)
- **Development Guide**: [.github/instructions/pyforge.instructions.md](.github/instructions/pyforge.instructions.md)
- **Examples**: [tests/test_test.py](tests/test_test.py)
- **Roadmap**: [docs/FUTURE_UPDATES.md](docs/FUTURE_UPDATES.md)

## Development

Code standards:

- PEP 484 type hints on all functions
- Google-style docstrings
- Exception chaining: `raise ... from e`
- No bare `except` statements

## License

MIT — See [LICENSE](LICENSE)

## Contributing

Contributions welcome! Open an issue or PR on [GitHub](https://github.com/ertanturk/pyforge-test).

---

**Status**: Alpha (v0.2.0) | **Python**: 3.12+ | **Type Safe**: Yes | **Dependencies**: 0
