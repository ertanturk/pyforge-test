# PyForge Test

A lightweight Python unit testing framework for personal projects and learning — zero configuration, decorator-based tests, automatic discovery.

> **Note**: PyForge is designed for personal projects, learning, and small-scale testing. It is **not** a competitor to production-grade frameworks like pytest, unittest, or testing infrastructure in organizations using PyTorch, TensorFlow, or similar platforms.

## When to Use PyForge

✓ Personal projects and hobby development  
✓ Learning Python testing concepts  
✓ Quick prototyping without framework overhead  
✓ Single-module or small-package testing

**Not recommended for:**

- Production applications (use pytest, unittest)
- Data science pipelines (use pytest + specialized tools)
- Large organizational projects (use established frameworks)
- CI/CD pipelines with complex requirements

## Features

- **Decorator-based** — Use `@test` to define tests
- **Automatic discovery** — Finds and executes all tests in `tests/` directory
- **Zero configuration** — Works in any project structure
- **Zero dependencies** — Pure Python, no external packages
- **Type-safe** — Full PEP 484 type hints and Google-style docstrings
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
pip install -e /path/to/pyforge-test
```

## Quick Start

### 1. Create test directory

```bash
mkdir -p tests && touch tests/__init__.py
```

### 2. Create test file

Create `tests/test_example.py`:

```python
"""Example tests."""

from pyforge_test.core.collector import test


@test
def test_addition() -> None:
    """Test basic addition."""
    assert 2 + 2 == 4


@test
def test_string_concat() -> None:
    """Test string concatenation."""
    assert "Hello" + " World" == "Hello World"
```

### 3. Run tests

```bash
pyforge
```

Expected output:

```
Discovering test modules in '/path/to/tests'...
✓ Loaded: test_example.py

Loaded 1 test module(s).

Test Results:
test_addition: Passed
test_string_concat: Passed
```

## Test Requirements

Test files must follow these conventions:

- Location: `tests/` directory
- Naming: `test_*.py` or `*_test.py`
- Functions: `test_*()`, no parameters, return type `-> None`
- Decoration: Use `@test` decorator
- Assertions: Standard `assert` statements

## Project Structure

```
pyforge-test/
├── src/pyforge_test/
│   └── core/
│       ├── collector.py     # @test decorator
│       ├── main.py          # CLI entry point
│       ├── registry.py      # Test registry
│       ├── runner.py        # Test executor
│       └── reporter.py      # Results formatter
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── pyproject.toml
└── LICENSE
```

## Running

From project root:

```bash
pyforge                              # Using CLI
python3 -m pyforge_test.core.main    # Using Python module
```

## Documentation

- [Full Guide](QUICK_START.md) — Comprehensive usage documentation
- [Planned Features](FUTURE_UPDATES.md) — Roadmap for future releases
- [Development Guide](.github/instructions/pyforge.instructions.md) — Contributing guidelines

## Development

Code standards:

- PEP 484 type hints on all functions
- Google-style docstrings
- Exception chaining: `raise ... from e`
- No bare `except` statements

## License

MIT — See [LICENSE](LICENSE) for details

## Contributing

Contributions welcome! PyForge aims to be a simple, maintainable testing framework.

---

**Status**: Alpha (v0.1.0)
