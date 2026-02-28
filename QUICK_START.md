# PyForge Testing Framework - User Guide

This guide shows how to use PyForge in your projects without any manual configuration.

## Installation

Install PyForge from GitHub:

```bash
pip install git+https://github.com/ertanturk/pyforge-test.git
```

Or from local development:

```bash
pip install -e /path/to/pyforge-test
```

## Quick Start (3 Steps)

### Step 1: Create Test Directory

```bash
mkdir -p tests
touch tests/__init__.py  # Create empty __init__.py
```

### Step 2: Create Test File

Create `tests/test_example.py`:

```python
from core.collector import test

@test
def test_addition() -> None:
    assert 2 + 2 == 4

@test
def test_subtraction() -> None:
    assert 5 - 3 == 2
```

### Step 3: Run Tests

From your project directory:

```bash
pyforge
```

That's it! Tests automatically discovered and executed.

## Running Tests

### Option 1: CLI Command (Recommended)

```bash
pyforge
```

### Option 2: Python Module

```bash
python3 -m core.main
```

### Option 3: Direct Script (Development)

```bash
python3 src/core/main.py
```

## Test File Requirements

- Create files in `tests/` directory
- Name them `test_*.py` or `*_test.py`
- Create empty `tests/__init__.py`
- Functions must start with `test_`
- Functions must have no parameters
- Use `@test` decorator
- Add return type hint `-> None`

## Example Test File

```python
"""Tests for my features."""

from core.collector import test


@test
def test_addition() -> None:
    """Test basic arithmetic."""
    assert 2 + 2 == 4


@test
def test_string_concat() -> None:
    """Test string operations."""
    assert "Hello" + " World" == "Hello World"


@test
def test_list_sum() -> None:
    """Test list operations."""
    numbers: list[int] = [1, 2, 3, 4, 5]
    assert sum(numbers) == 15
```

## Recommended Project Structure

```
my-project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   ├── __init__.py              # Required (can be empty)
│   ├── test_main.py             # Automatically discovered
│   ├── test_utils.py            # Automatically discovered
│   └── test_integration.py      # Automatically discovered
└── pyproject.toml (optional)
```

## How PyForge Finds Tests

1. Looks for `tests/` directory in current working directory
2. If not found, checks parent directory
3. Falls back to pyforge installation directory
4. Recursively loads all files matching `test*.py` pattern
5. Collects all functions decorated with `@test`
6. Executes tests in order and displays results

## Test Results Format

- **Passed** - Assertion succeeded
- **Failed** - Assertion failed (AssertionError)
- **Error: <message>** - Unexpected exception

## Auto Path Configuration

PyForge automatically:

1. Adds your project's `src/` directory to Python path (if it exists)
2. Configures `tests/__init__.py` for proper imports
3. No manual `sys.path.insert()` needed!

Your tests can simply do:

```python
from core.collector import test  # No setup needed!
```

## Troubleshooting

### Tests not running

- Verify `tests/` directory exists in current directory
- Check that `tests/__init__.py` exists (can be empty)
- Ensure test filenames match `test_*.py` pattern
- Verify test functions start with `test_` prefix
- Confirm test functions have no parameters

### Import errors

- Make sure `tests/__init__.py` exists
- Verify the test can import `core.collector`
- If importing custom code, place it in `src/` directory
- Check that dependencies are installed

### Entry point error

- Run `pyforge` from your project root directory
- Verify `tests/` subdirectory exists
- Reinstall package if needed: `pip install --force-reinstall git+https://github.com/ertanturk/pyforge-test.git`

## Multiple Test Files

Organize tests into multiple files:

```
tests/
├── __init__.py
├── test_auth.py           # Authentication tests
├── test_database.py       # Database tests
├── test_api.py            # API tests
└── test_integration.py    # Integration tests
```

Tests execute in alphabetical order by filename.

## Advanced: Custom Test Organization

Control execution order with naming:

```
tests/
├── test_01_critical.py    # Runs first
├── test_02_features.py    # Runs second
└── test_03_integration.py # Runs last
```

## Platform Support

- ✅ Linux
- ✅ macOS
- ✅ Windows WSL
- ✅ Python 3.12+

## Next Steps

1. Create `tests/` directory with `__init__.py`
2. Create `test_*.py` files
3. Write test functions with `@test` decorator
4. Run `pyforge` to execute tests

Enjoy automated testing with PyForge!
