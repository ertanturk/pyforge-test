# PyForge Testing Framework - Complete Documentation

A lightweight Python testing framework with decorator-based test collection and execution.

## Installation

```bash
pip install git+https://github.com/ertanturk/pyforge-test.git
```

## Quick Start

### 1. Setup

```bash
mkdir tests
```

### 2. Write Tests

Create `tests/test_example.py`:

```python
from pyforge_test import test

@test
def test_addition() -> None:
    assert 2 + 2 == 4
```

### 3. Run Tests

```bash
pyforge
```

## Core Features

### Basic Tests

```python
from pyforge_test import test

@test
def test_string_operations() -> None:
    """Test basic string manipulation."""
    result = "hello".upper()
    assert result == "HELLO"
    assert "world" in "hello world"
```

**Requirements:**

- Function name starts with `test_`
- No parameters
- Return type `-> None`
- Use `@test` decorator

### Test Markers

Organize tests by execution priority: **Unmarked (0)** → **Integration (1)** → **Slow (2)**

#### Unmarked Tests (Priority 0)

```python
@test
def test_fast_calculation() -> None:
    """Fast unit test - runs first."""
    assert 5 * 5 == 25
```

#### Integration Tests (Priority 1)

```python
from pyforge_test import test, test_marker

@test_marker("integration")
@test
def test_database_query() -> None:
    """Requires external database."""
    result = db.query("SELECT 1")
    assert result is not None
```

#### Slow Tests (Priority 2)

```python
import time
from pyforge_test import test, test_marker

@test_marker("slow")
@test
def test_performance() -> None:
    """Performance-intensive operation."""
    time.sleep(0.5)
    result = process_large_dataset()
    assert len(result) > 1000
```

**Built-in Markers:**

- `"integration"` - External resources (DB, API, filesystem)
- `"slow"` - Time-consuming operations (>100ms)

**Important:** Decorator order matters - `@test_marker` must come **before** `@test`

### Parameterized Tests

Run same test with multiple inputs:

```python
from pyforge_test import test_parameterized

@test_parameterized([
    (2, 3, 5),
    (10, 5, 15),
    (100, 200, 300),
])
def test_addition(a: int, b: int, expected: int) -> None:
    """Test addition with multiple cases."""
    assert a + b == expected
```

Generates: `test_addition_0`, `test_addition_1`, `test_addition_2`

### Skip Tests

#### Conditional Skip

```python
import sys
from pyforge_test import test, test_skipif

@test_skipif(
    sys.platform == "win32",
    reason="Not supported on Windows"
)
def test_unix_feature() -> None:
    """Only runs on Unix-like systems."""
    assert os.fork() >= 0
```

#### Unconditional Skip

```python
from pyforge_test import test, test_skip

@test_skip(reason="Feature not implemented yet")
def test_future_feature() -> None:
    """This test is always skipped."""
    assert future_api_call() == "success"
```

### Combined Features

```python
import os
from pyforge_test import test, test_marker, test_skipif

@test_marker("integration")
@test_skipif(
    not os.getenv("DATABASE_URL"),
    reason="Database not configured"
)
def test_real_database() -> None:
    """Integration test with skip condition."""
    conn = connect_database()
    assert conn.is_connected()
```

## Complete Example

```python
"""Complete test suite example."""

import time
import os
from pyforge_test import (
    test,
    test_marker,
    test_parameterized,
    test_skip,
    test_skipif,
)


# Unmarked test (Priority 0)
@test
def test_basic_arithmetic() -> None:
    """Fast unit test."""
    assert 10 / 2 == 5
    assert 3 ** 2 == 9


# Parameterized test
@test_parameterized([
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("PyForge", "PYFORGE"),
])
def test_uppercase(input_str: str, expected: str) -> None:
    """Test string uppercase conversion."""
    assert input_str.upper() == expected


# Integration test (Priority 1)
@test_marker("integration")
@test
def test_api_endpoint() -> None:
    """Test external API."""
    response = api_client.get("/health")
    assert response.status_code == 200


# Slow test (Priority 2)
@test_marker("slow")
@test
def test_large_computation() -> None:
    """Performance-intensive test."""
    time.sleep(0.2)
    result = sum(i ** 2 for i in range(10000))
    assert result > 0


# Conditional skip
@test_skipif(
    os.getenv("CI") == "true",
    reason="Skip in CI environment"
)
def test_local_only() -> None:
    """Only runs locally."""
    assert local_resource_available()


# Unconditional skip
@test_skip(reason="Temporarily disabled")
def test_broken_feature() -> None:
    """Skipped until bug is fixed."""
    assert broken_function() == "works"


# Combined: marker + skip
@test_marker("slow")
@test_skip(reason="Takes 10+ minutes")
def test_extensive_benchmark() -> None:
    """Long-running benchmark test."""
    time.sleep(600)
```

## Project Structure

```
my-project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   ├── __init__.py              # Required (empty file)
│   ├── test_main.py             # Auto-discovered
│   ├── test_utils.py            # Auto-discovered
│   └── test_integration.py      # Auto-discovered
└── pyproject.toml
```

## Running Tests

### Command Line

```bash
# Run all tests in tests/ directory
pyforge

# Run specific test file (alternative)
python -m pyforge_test tests/test_example.py
```

### Auto-Discovery

PyForge automatically:

1. Finds `tests/` directory in current/parent directory
2. Loads all `test*.py` files
3. Collects functions decorated with `@test`
4. Sorts by marker priority
5. Executes and reports results

### Output Format

```
Executing 8 test(s).

File: /path/to/tests/test_example.py
  Line 10: test_basic_arithmetic - ✅ Passed
  Line 15: test_uppercase_0 - ✅ Passed
  Line 15: test_uppercase_1 - ✅ Passed
  Line 15: test_uppercase_2 - ✅ Passed
  Line 25: test_api_endpoint - ✅ Passed
  Line 33: test_large_computation - ✅ Passed
  Line 42: test_local_only - ⏭️  Skipped: Skip in CI environment
  Line 50: test_broken_feature - ⏭️  Skipped: Temporarily disabled
```

## Test Results

- **✅ Passed** - Assertion succeeded
- **❌ Failed: <message>** - AssertionError
- **⚠️ Error: <message>** - Unexpected exception
- **⏭️ Skipped: <reason>** - Test skipped

## API Reference

### Decorators

| Decorator                    | Purpose                  | Example                        |
| ---------------------------- | ------------------------ | ------------------------------ |
| `@test`                      | Mark function as test    | `@test`                        |
| `@test_marker(marker)`       | Apply priority marker    | `@test_marker("slow")`         |
| `@test_parameterized(cases)` | Run with multiple inputs | `@test_parameterized([(1,2)])` |
| `@test_skip(reason)`         | Always skip              | `@test_skip("Not ready")`      |
| `@test_skipif(cond, reason)` | Conditionally skip       | `@test_skipif(True, "Skip")`   |

### Built-in Markers

| Marker          | Priority | Use Case              |
| --------------- | -------- | --------------------- |
| None (unmarked) | 0        | Fast unit tests       |
| `"integration"` | 1        | External dependencies |
| `"slow"`        | 2        | Performance-intensive |

### Import Paths

```python
# Recommended: Import from main package
from pyforge_test import (
    test,
    test_marker,
    test_parameterized,
    test_skip,
    test_skipif,
    BUILTIN_MARKERS,
)

# Alternative: Import from core module
from pyforge_test.core.collector import test
```

## Best Practices

### 1. Test Naming

```python
# ✅ Good: Descriptive, starts with test_
@test
def test_user_authentication_with_valid_credentials() -> None:
    pass

# ❌ Bad: Vague, doesn't start with test_
def check_auth() -> None:
    pass
```

### 2. Marker Usage

```python
# ✅ Good: Unmarked for fast unit tests
@test
def test_string_length() -> None:
    assert len("hello") == 5

# ✅ Good: Integration marker for external resources
@test_marker("integration")
@test
def test_database_connection() -> None:
    db.connect()

# ✅ Good: Slow marker for performance tests
@test_marker("slow")
@test
def test_million_records() -> None:
    process_records(1_000_000)
```

### 3. Parameterization

```python
# ✅ Good: Multiple related test cases
@test_parameterized([
    (0, True),
    (1, False),
    (-1, False),
    (10, True),
])
def test_is_even(num: int, expected: bool) -> None:
    assert (num % 2 == 0) == expected

# ❌ Bad: Separate tests for each case
@test
def test_zero_is_even() -> None:
    assert 0 % 2 == 0

@test
def test_one_is_odd() -> None:
    assert 1 % 2 != 0
```

### 4. Skip Conditions

```python
# ✅ Good: Conditional skip with clear reason
@test_skipif(
    sys.version_info < (3, 12),
    reason="Requires Python 3.12+"
)
def test_new_syntax() -> None:
    pass

# ✅ Good: Skip unfinished tests
@test_skip(reason="Implementation pending")
def test_new_feature() -> None:
    pass
```

## Troubleshooting

### Tests Not Found

**Problem:** `No tests to execute. Exiting.`

**Solution:**

- Ensure `tests/` directory exists
- Create `tests/__init__.py` (can be empty)
- Test files must match `test*.py` pattern
- Functions must start with `test_`
- Functions must use `@test` decorator

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'pyforge_test'`

**Solution:**

```bash
pip install git+https://github.com/ertanturk/pyforge-test.git
```

### Marker Errors

**Problem:** `ValueError: Marker 'custom' is not a built-in marker.`

**Solution:**

- Only use `"integration"` or `"slow"` markers
- Check spelling: `@test_marker("integration")` not `"Integration"`

### Decorator Order

**Problem:** `ValueError: Test function must be collected before applying marker.`

**Solution:**

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

## Advanced Usage

### Custom Assertions

```python
@test
def test_with_custom_assertion() -> None:
    """Use custom assertion helpers."""
    result = compute_value()

    # Multiple assertions in one test
    assert result > 0, "Result should be positive"
    assert result < 100, "Result should be less than 100"
    assert isinstance(result, int), "Result should be integer"
```

### Environment-Based Testing

```python
import os

@test_skipif(
    os.getenv("ENVIRONMENT") == "production",
    reason="Don't run in production"
)
def test_destructive_operation() -> None:
    """Only runs in dev/test environments."""
    delete_all_data()
    assert True
```

### Multiple Markers with Skip

```python
@test_marker("integration")
@test_skipif(
    not os.path.exists("/var/run/docker.sock"),
    reason="Docker not available"
)
def test_docker_container() -> None:
    """Integration test requiring Docker."""
    container = docker_client.run("alpine")
    assert container.status == "running"
```

## Platform Support

- ✅ Linux
- ✅ macOS
- ✅ Windows (WSL)
- ✅ Python 3.12+

## Summary

PyForge provides:

1. **Simple test collection** with `@test` decorator
2. **Test prioritization** with markers (`integration`, `slow`)
3. **Parameterized tests** for multiple test cases
4. **Skip conditions** for conditional execution
5. **Auto-discovery** of test files
6. **Clear output** with pass/fail/skip status

Write tests, run `pyforge`, see results. That's it!
