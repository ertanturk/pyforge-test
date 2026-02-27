---
name: pyforge-python-conventions
description: "Use when: developing pyforge testing framework in Python. Enforce PEP 484 type hints, Google-style docstrings, consistent error handling, and pyforge-specific test patterns."
applyTo: "**/*.py"
---

# PyForge Python Development Conventions

This guide ensures consistent code quality and maintainability across the pyforge testing framework.

## Type Hints (PEP 484)

**Always include type hints** on function signatures and module-level variables. Use modern Python 3.12+ syntax.

### Requirements

- Function parameters must have type annotations
- Return types must be annotated (including `-> None` for functions without return)
- Module-level variables should have type hints
- Use `|` for union types instead of `Union[]`
- Use `list[X]`, `dict[K, V]` instead of `List[]`, `Dict[]` (Python 3.9+)
- Use `collections.abc.Callable` for function types

### Examples

```python
from collections.abc import Callable

# ✓ Correct
def execute() -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    return results

def report(results: list[tuple[str, str]]) -> str:
    pass

# ✗ Wrong
def execute():  # Missing return type
    results = []  # Missing variable type hint
    return results
```

## Docstring Style (Google Format)

Use **Google-style docstrings** for all public functions and classes. Include sections as needed:

### Structure

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief one-line description.

    Longer description if needed. Explain purpose and behavior.

    Args:
        param1 (str): Description of param1.
        param2 (int): Description of param2.

    Returns:
        bool: Description of return value.

    Raises:
        ValueError: When invalid input is provided.
        RuntimeError: When execution fails.
    """
```

### Requirements

- Use triple quotes `"""`
- First line is a summary (under 80 chars)
- Add blank line before sections (Args, Returns, Raises, Note, etc.)
- List exceptions in `Raises:` section
- Match parameter names and types to function signature

### Examples

```python
# ✓ Correct
def collecter(function: Callable[..., None]) -> Callable[..., None]:
    """Collects the test functions and adds them to the TESTS list.

    Args:
        function (Callable[..., None]): The test function to be collected.

    Returns:
        Callable[..., None]: The original test function, unmodified.

    Raises:
        ValueError: If function is already collected or doesn't start with 'test_'.
        RuntimeError: If an error occurs during collection.
    """
```

## Error Handling Patterns

Establish clear, consistent error handling that aids debugging.

### Requirements

- Use specific exception types (not bare `Exception`)
- Catch specific exceptions first, then general ones
- Provide descriptive error messages
- Use `raise ... from e` to preserve exception chain
- Wrap external operations with try-except
- Validate inputs at entry points

### Pattern

```python
def operation() -> ResultType:
    """..."""
    try:
        # Main logic
        return result
    except SpecificError as e:
        raise RuntimeError(f"Specific failure context: {e}") from e
    except Exception as e:
        raise RuntimeError(f"General failure context: {e}") from e
```

### Examples

```python
# ✓ Correct
def execute() -> list[tuple[str, str]]:
    try:
        results: list[tuple[str, str]] = []
        for test in TESTS:
            try:
                test()
                results.append((test.__name__, "Passed"))
            except AssertionError:
                results.append((test.__name__, "Failed"))
            except Exception as e:
                results.append((test.__name__, f"Error: {e}"))
        TESTS.clear()
        return results
    except Exception as e:
        raise RuntimeError(f"An error occurred while executing tests: {e}") from e

# ✗ Wrong
def execute():
    results = []
    for test in TESTS:
        test()  # No error handling
        results.append((test.__name__, "Passed"))
    return results
```

## Code Organization

Organize modules and functions logically for clarity and maintainability.

### Module Structure

- **`core/` package**: Core functionality (collector, registry, runner, reporter)
- **`utils/` package**: Shared utilities
- **`tests/` directory**: Test modules for the framework itself
- **`main.py`**: Entry point or public API

### Naming Conventions

- Module names: lowercase with underscores (`collector.py`, `test_runner.py`)
- Function names: lowercase with underscores (`execute_tests()`, `collect_test()`)
- Class names: PascalCase (`TestRunner`, `TestCollector`)
- Constants: UPPERCASE with underscores (`TESTS`, `MAX_RETRIES`)
- Private: prefix with underscore (`_internal_helper()`)

### File Organization

1. Imports (stdlib, then third-party, then local)
2. Module docstring (if needed)
3. Constants
4. Functions/Classes
5. Leave blank lines between top-level definitions

### Example

```python
# ✓ Correct structure
from collections.abc import Callable

from .registry import TESTS

# Module comment on purpose (optional)
def collecter(function: Callable[..., None]) -> Callable[..., None]:
    """..."""


def other_function() -> None:
    """..."""
```

## Testing Patterns (PyForge-Specific)

Tests for the framework must follow pyforge's own conventions.

### Requirements

- Test functions must start with `test_` prefix
- Test functions must have **no parameters** (except those injected by the framework)
- Test functions should use `assert` statements
- Each test should verify one behavior
- Use descriptive test names: `test_function_behavior_when_condition()`

### Example

```python
# ✓ Correct
@collecter
def test_valid_function_is_collected() -> None:
    """Verify a valid test function is added to TESTS."""
    assert len(TESTS) > 0


def test_collector_rejects_non_test_functions() -> None:
    """Verify functions not starting with 'test_' are rejected."""
    with pytest.raises(ValueError):
        collecter(lambda: None)

# ✗ Wrong
def test_invalid_name():  # Missing return type, wrong prefix
    pass

def test_with_params(arg1, arg2):  # Test functions cannot have parameters
    assert arg1 == arg2
```

## Code Comments

- Add brief comments before functions explaining their purpose
- Use comments to clarify complex logic, not obvious code
- Avoid redundant comments
- Update comments when code changes

## Import Organization

```python
# 1. Standard library (sorted alphabetically)
from collections.abc import Callable
from typing import Any

# 2. Third-party libraries (sorted alphabetically)
# (Currently: none for pyforge core)

# 3. Local imports (relative imports for same package)
from .registry import TESTS
from ..utils import helper_function
```

## Summary Checklist

Before committing code:

- [ ] All functions have type hints (parameters + return)
- [ ] All parameters match docstring Args section
- [ ] Google-style docstrings on public functions
- [ ] Error handling uses specific exceptions with clear messages
- [ ] Errors use `raise ... from e` for context
- [ ] Test functions start with `test_`, have no parameters
- [ ] Variable names follow conventions (snake_case)
- [ ] Imports organized and sorted
- [ ] No bare `except:` clauses
