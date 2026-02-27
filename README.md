# PyForge Test

A lightweight Python unit testing framework built from scratch, designed for simplicity and ease of use. Works seamlessly in any project - no configuration required!

## Features

- **Simple Decorator-Based Tests** - Use the `@collecter` decorator to define tests
- **Automatic Discovery** - Finds and executes all test files in `tests/` directory
- **Zero Configuration** - Automatic path setup, works in any project structure
- **Minimal Dependencies** - Zero external dependencies, pure Python implementation
- **Clear Reporting** - Human-readable test results and failure messages
- **Type-Safe** - Full PEP 484 type hints, Google-style docstrings
- **Python 3.12+** - Modern Python support with latest language features

## Installation

```bash
pip install git+https://github.com/ertanturk/pyforge-test.git
```

Or from local development:

```bash
pip install -e /path/to/pyforge-test
```

## Quick Start

### 1. Create test directory

```bash
mkdir -p tests
touch tests/__init__.py  # Creates empty __init__.py
```

### 2. Create a test file

Create `tests/test_example.py`:

```python
"""Example tests for PyForge."""

from core.collector import collecter


@collecter
def test_addition() -> None:
    """Test basic addition."""
    assert 2 + 2 == 4


@collecter
def test_string_concat() -> None:
    """Test string concatenation."""
    assert "Hello" + " World" == "Hello World"
```

### 3. Run tests

From your project directory:

```bash
pyforge
```

Output:

```
Discovering test modules in '/path/to/tests'...
✓ Loaded: test_example.py

Loaded 1 test module(s).

Test Results:
test_addition: Passed
test_string_concat: Passed
```

## How It Works

PyForge automatically:

1. **Discovers** - Finds all `test_*.py` files in your `tests/` directory
2. **Loads** - Executes test modules (triggering `@collecter` decorators)
3. **Registers** - Collects all decorated test functions
4. **Executes** - Runs tests and captures results
5. **Reports** - Displays pass/fail/error results

## Documentation

For comprehensive usage guide, see [QUICK_START.md](QUICK_START.md).

For future planned features, see [FUTURE_UPDATES.md](FUTURE_UPDATES.md).

## Project Structure

```
pyforge-test/
├── src/
│   ├── __init__.py          # Package marker
│   └── core/
│       ├── __init__.py
│       ├── main.py          # CLI entry point
│       ├── collector.py     # @collecter decorator
│       ├── registry.py      # Test registry storage
│       ├── runner.py        # Test executor
│       └── reporter.py      # Results formatter
├── tests/
│   ├── __init__.py          # Auto-configures paths
│   └── test_basic.py        # Example test file
├── pyproject.toml           # Package configuration
├── QUICK_START.md           # User guide
├── README.md                # This file
└── LICENSE                  # MIT License
```

## Test File Requirements

Test files must follow these conventions:

✓ Located in `tests/` directory  
✓ Named `test_*.py` or `*_test.py`  
✓ Functions start with `test_` prefix  
✓ Functions have no parameters  
✓ Functions decorated with `@collecter`  
✓ Functions have return type hint `-> None`  
✓ Use standard `assert` statements

## Usage Examples

### Multiple Test Files

Organize tests by feature:

```
tests/
├── __init__.py
├── test_auth.py
├── test_database.py
├── test_api.py
└── test_integration.py
```

All files are automatically discovered and executed.

### Test Results

Tests report as:

- **Passed** - Assertion succeeded
- **Failed** - Assertion failed
- **Error: <message>** - Unexpected exception

### Different Project Layouts

PyForge works with any project structure:

**Simple structure:**

```
my-project/
├── tests/
│   ├── __init__.py
│   └── test_example.py
```

**With src/ directory:**

```
my-project/
├── src/
│   └── my_module.py
└── tests/
    ├── __init__.py
    └── test_my_module.py
```

**With package structure:**

```
my-project/
├── src/
│   ├── core/
│   │   └── main.py
│   └── utils/
│       └── helpers.py
└── tests/
    ├── __init__.py
    ├── test_core.py
    └── test_utils.py
```

## Running Tests

From your project root:

```bash
# Using CLI (recommended)
pyforge

# Using Python module
python3 -m core.main

# During development (from pyforge source)
python3 src/core/main.py
```

## Development Instructions

For developers contributing to PyForge, see [.github/instructions/pyforge.instructions.md](.github/instructions/pyforge.instructions.md).

Coding standards:

- PEP 484 type hints on all functions
- Google-style docstrings
- Exception chaining with `raise ... from e`
- Proper error handling (no bare `except`)

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contributing

Contributions welcome! PyForge aims to be a simple, maintainable testing framework.

---

**Status**: Alpha (v0.0.1) - Core functionality complete, ready for feedback and improvements.
