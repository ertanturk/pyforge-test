# PyForge Testing Framework - Complete Documentation

A lightweight Python testing framework designed for **personal projects and learning**. Zero configuration, decorator-based test collection, automatic discovery.

> **Note**: PyForge is designed for personal projects, learning, and small-scale testing. It is **not** a substitute or competitor to production frameworks like pytest or unittest.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Features](#core-features)
4. [CLI Reference](#cli-reference)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [Platform Support](#platform-support)

---

## Installation

### From PyPI

```bash
pip install pyforge-test
```

### From GitHub

```bash
pip install git+https://github.com/ertanturk/pyforge-test.git
```

### For Development

```bash
git clone https://github.com/ertanturk/pyforge-test.git
cd pyforge-test
pip install -e .
```

---

## Quick Start

### 1. Create Test Directory

```bash
mkdir -p tests
touch tests/__init__.py
```

### 2. Write a Test

Create `tests/test_example.py`:

```python
from pyforge_test import test


@test
def test_addition() -> None:
    """Test basic arithmetic."""
    assert 2 + 2 == 4
```

### 3. Run Tests

```bash
# Run all tests
pyforge

# Run with verbose output
pyforge -v

# Run specific tests
pyforge -k addition

# Show only failures
pyforge -q
```

---

## Core Features

### Basic Tests

A test function must:

- Start with `test_` prefix
- Have no parameters
- Return `-> None`
- Use `@test` decorator

```python
from pyforge_test import test


@test
def test_string_operations() -> None:
    """Test string manipulation."""
    result = "hello".upper()
    assert result == "HELLO"
```

### Test Markers

Organize tests by execution priority:

| Priority | Marker          | Use Case                  |
| -------- | --------------- | ------------------------- |
| 0        | None (unmarked) | Fast unit tests           |
| 1        | `"integration"` | External dependencies     |
| 2        | `"slow"`        | Time-consuming operations |

**Important**: `@test_marker` must come **before** `@test`.

```python
from pyforge_test import test, test_marker


@test_marker("integration")
@test
def test_database_query() -> None:
    """Requires external database."""
    result = db.connect()
    assert result is not None


@test_marker("slow")
@test
def test_performance() -> None:
    """Performance-intensive operation."""
    time.sleep(0.5)
    assert compute_result() > 0
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
    """Test arithmetic with multiple cases."""
    assert a + b == expected
```

Generates: `test_addition_0`, `test_addition_1`, `test_addition_2`

### Skip Tests

#### Conditional Skip

```python
import sys
from pyforge_test import test_skipif


@test_skipif(
    sys.platform == "win32",
    reason="Not supported on Windows"
)
def test_unix_feature() -> None:
    """Only runs on Unix-like systems."""
    pass
```

#### Unconditional Skip

```python
from pyforge_test import test_skip


@test_skip(reason="Implementation pending")
def test_future_feature() -> None:
    """This test is always skipped."""
    pass
```

### Complete Example

```python
"""Complete test suite example with all features."""

import os
import sys
import time

from pyforge_test import (
    test,
    test_marker,
    test_parameterized,
    test_skip,
    test_skipif,
)


# ===== Unmarked Tests (Priority 0) =====

@test
def test_basic_arithmetic() -> None:
    """Fast unit test."""
    assert 10 / 2 == 5
    assert 3 ** 2 == 9


@test_parameterized([
    ("hello", "HELLO"),
    ("world", "WORLD"),
])
def test_uppercase(input_str: str, expected: str) -> None:
    """Test string case conversion."""
    assert input_str.upper() == expected


# ===== Integration Tests (Priority 1) =====

@test_marker("integration")
@test
def test_file_operations() -> None:
    """Test reading files."""
    with open("README.md", "r") as f:
        content = f.read()
    assert len(content) > 0


# ===== Slow Tests (Priority 2) =====

@test_marker("slow")
@test
def test_large_computation() -> None:
    """Performance-intensive test."""
    time.sleep(0.2)
    result = sum(i ** 2 for i in range(10000))
    assert result > 0


# ===== Skip Tests =====

@test_skipif(
    os.getenv("CI") == "true",
    reason="Skip in CI environment"
)
def test_local_only() -> None:
    """Only runs locally."""
    pass


@test_skip(reason="Temporarily disabled")
def test_broken_feature() -> None:
    """Skipped test."""
    pass
```

---

## CLI Reference

### Syntax

```bash
pyforge [OPTIONS] [FILES...]
```

### Options

| Option        | Short | Description              |
| ------------- | ----- | ------------------------ |
| `--help`      | `-h`  | Show help message        |
| `--quiet`     | `-q`  | Show only failures       |
| `--verbose`   | `-v`  | Show detailed tracebacks |
| `--fail-fast` |       | Stop at first failure    |
| `-k PATTERN`  |       | Filter by name substring |

### Examples

```bash
# Run all tests
pyforge

# Quiet mode (failures only)
pyforge -q

# Verbose mode (full tracebacks)
pyforge -v

# Stop on first failure
pyforge --fail-fast

# Filter by test name
pyforge -k basic
pyforge -k test_api

# Run from specific file(s)
pyforge test_example.py
pyforge test_utils.py test_models.py

# Combine options
pyforge -k api -v test_integration.py --fail-fast
```

### Output Format

#### Normal Mode

```
PyForge Test Results
------------------------------------------------------------------------

test_example.py
  PASSED test_basic_arithmetic (Line 10)
  PASSED test_uppercase_0 (Line 15)
  FAILED test_check_value (Line 22): expected 42
    → tests/test_example.py:25  in test_check_value
  ERROR test_api (Line 30): name 'api_client' is not defined
  SKIPPED test_local (Line 40): Skip in CI environment

------------------------------------------------------------------------
Summary: PASSED: 2/5  FAILED: 1/5  SKIPPED: 1/5  ERRORS: 1/5
Took 156 ms to execute all tests
------------------------------------------------------------------------
```

#### Verbose Mode

Shows full colorized traceback for failures/errors:

```
  FAILED test_check_value (Line 22): expected 42
    Traceback (most recent call last):
      File "tests/test_example.py", line 25, in test_check_value
          assert result == 42
    AssertionError: expected 42
```

#### Quiet Mode

Shows only failures and summary.

---

## Auto-Discovery

PyForge automatically:

1. Finds `tests/` directory (current or parent)
2. Loads all `test*.py` files
3. Collects functions with `@test` decorator
4. Filters by criteria (if provided)
5. Sorts by marker priority (0→1→2)
6. Executes and reports results

---

## Best Practices

### 1. Descriptive Test Names

```python
# ✅ Good
@test
def test_user_authentication_with_valid_credentials() -> None:
    pass

# ❌ Bad
def check_auth() -> None:
    pass
```

### 2. Use Markers Properly

```python
# ✅ Fast unit tests (unmarked, Priority 0)
@test
def test_string_length() -> None:
    assert len("hello") == 5

# ✅ Tests with external resources (Priority 1)
@test_marker("integration")
@test
def test_database() -> None:
    db.connect()

# ✅ Performance tests (Priority 2)
@test_marker("slow")
@test
def test_large_dataset() -> None:
    process_records(1_000_000)
```

### 3. Parameterize Related Cases

```python
# ✅ Good: Multiple cases in one test
@test_parameterized([
    (0, True),
    (1, False),
    (10, True),
])
def test_is_even(num: int, expected: bool) -> None:
    assert (num % 2 == 0) == expected

# ❌ Bad: One test per case
@test
def test_zero_is_even() -> None:
    assert 0 % 2 == 0
```

### 4. Use Skip for Intentional Skips

```python
# ✅ Skip tests that require external setup
@test_skipif(
    not os.getenv("DATABASE_URL"),
    reason="Database not configured"
)
def test_database() -> None:
    pass
```

### 5. Multiple Assertions

```python
@test
def test_value_validation() -> None:
    """Check multiple assertions."""
    result = compute_value()
    assert result > 0, "Result should be positive"
    assert result < 100, "Result should be less than 100"
    assert isinstance(result, int), "Result should be integer"
```

---

## Project Structure

Recommended layout:

```
my-project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   ├── __init__.py              # Required (can be empty)
│   ├── test_main.py             # Auto-discovered
│   ├── test_utils.py            # Auto-discovered
│   └── test_integration.py      # Auto-discovered
├── README.md
└── pyproject.toml
```

---

## Troubleshooting

### Tests Not Found

**Problem**: `No tests to execute. Exiting.`

**Solution**:

- Ensure `tests/` directory exists
- Create `tests/__init__.py`
- Test files must match `test*.py` pattern
- Functions must start with `test_` and use `@test` decorator

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'pyforge_test'`

**Solution**:

```bash
pip install pyforge-test
```

### Decorator Order

**Problem**: `ValueError: Test function must be collected before applying marker.`

**Solution**:

```python
# ✅ Correct order
@test_marker("slow")
@test
def test_something() -> None:
    pass

# ❌ Wrong order
@test
@test_marker("slow")
def test_something() -> None:
    pass
```

### Invalid Marker

**Problem**: `ValueError: Marker 'custom' is not a built-in marker.`

**Solution**: Only use `"integration"` or `"slow"` markers.

---

## API Reference

### Decorators

```python
from pyforge_test import (
    test,
    test_marker,
    test_parameterized,
    test_skip,
    test_skipif,
    BUILTIN_MARKERS,
)

# Mark function as test
@test
def test_example() -> None:
    pass

# Apply priority marker (before @test)
@test_marker("slow")

# Run with multiple inputs
@test_parameterized([(1, 2), (3, 4)])

# Always skip
@test_skip(reason="Not ready")

# Skip conditionally
@test_skipif(condition, reason="Reason")
```

### Built-in Markers

```python
from pyforge_test import BUILTIN_MARKERS

# Returns dict:
# {
#     "slow": "Mark test as slow-running",
#     "integration": "Mark test as an integration test...",
# }
```

---

## Platform Support

- ✅ Linux
- ✅ macOS
- ✅ Windows (WSL)
- ✅ Python 3.12+

---

## Type Hints & Quality

PyForge is **fully type-hinted** (PEP 484) and passes:

- **Ruff**: All linting checks
- **Pylint**: 9.89/10 code quality
- **Pyright**: Strict type checking in strict mode

---

## Summary

PyForge provides:

1. **Simple decorator-based tests** with `@test`
2. **Automatic test discovery** from `tests/` directory
3. **Test prioritization** with markers
4. **Parameterized tests** for multiple cases
5. **Skip conditions** for conditional execution
6. **Clean output** with pass/fail/skip status

**Design Philosophy**: Zero configuration, zero dependencies, perfect for personal projects and learning.

---

## License

MIT License — See [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Open issues or PRs on [GitHub](https://github.com/ertanturk/pyforge-test).
