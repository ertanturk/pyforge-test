"""PyForge Testing Framework - User Guide.

This guide shows how to use PyForge in your projects without manually
configuring sys.path.
"""

# ============================================================================

# How to Use PyForge in Your Projects

# ============================================================================

"""

## Installation

Install the pyforge-test package:

    pip install git+https://github.com/ertanturk/pyforge-test.git

## Creating Test Files

Create test files in your project's `tests/` directory with the pattern
`test_*.py` or `*_test.py`.

### Example 1: Simple Test File

Create `tests/test_my_features.py`:

```python
from pyforge_test import collecter


@collecter
def test_addition() -> None:
    assert 2 + 2 == 4


@collecter
def test_subtraction() -> None:
    assert 5 - 3 == 2


@collecter
def test_string_concat() -> None:
    assert "Hello" + " World" == "Hello World"
```

That's it! No sys.path manipulation needed!

### Key Points About Test Functions

✓ Function name must start with `test_`
✓ Function must have no parameters (except for fixtures in future versions)
✓ Use `@collecter` decorator to register the test
✓ Use standard `assert` statements for test assertions
✓ Add type hints (especially return type `-> None`)

## Running Tests

### Option 1: Using the CLI

After installing pyforge-test, run from your project directory:

    pyforge

### Option 2: Running from Python

From your project root:

    python3 -m src.main

## Test Discovery

PyForge automatically discovers and loads:

- All files matching `test_*.py` in the `tests/` directory
- Tests are executed in alphabetical order of filenames
- All `@collecter` decorated functions within each file are collected

## Test Results

PyForge reports each test as:

- **Passed** - Test assertion succeeded
- **Failed** - Test assertion failed (AssertionError)
- **Error: <message>** - Test raised an unexpected exception

## Example Project Structure

```
my-project/
├── pyproject.toml
├── src/
│   ├── main.py
│   ├── utils/
│   └── ...
└── tests/
    ├── test_features.py      # Automatically discovered
    ├── test_utils.py         # Automatically discovered
    └── test_integration.py   # Automatically discovered
```

## Auto Path Setup

The `tests/__init__.py` file automatically configures the Python path,
so your test modules can simply import from `core`:

```python
# tests/test_example.py
from core.collector import collecter  # No need for sys.path.insert()

@collecter
def test_example() -> None:
    pass
```

## Next Steps

1. Create a `tests/` directory in your project root
2. Create `test_*.py` files in that directory
3. Define test functions with `@collecter` decorator
4. Run `pyforge` to execute all tests

## Troubleshooting

If tests aren't being discovered:

- Ensure filenames match `test_*.py` pattern
- Verify functions start with `test_` prefix
- Check that `tests/__init__.py` exists in your tests directory
- Make sure test functions have no parameters

If imports fail:

- Verify your project has a `src/` directory with your code
- Ensure the `tests/__init__.py` file exists
- Check that core modules are in `src/core/`
  """
