# PyForge Test

A lightweight Python unit testing framework built from scratch, designed for simplicity and ease of use.

## Features

- **Simple Decorator-Based Tests** - Use the `@collecter` decorator to define tests
- **Automatic Discovery** - Finds and executes all test files in the `tests/` directory
- **Minimal Dependencies** - Zero external dependencies, pure Python implementation
- **Clear Reporting** - Human-readable test results and failure messages
- **Python 3.12+** - Modern Python support with full type hints

## Installation

```bash
pip install git+https://github.com/ertanturk/pyforge-test.git
```

## Quick Start

### 1. Create a test file

Create `tests/test_example.py`:

```python
from core.collector import collecter

@collecter
def test_addition():
    assert 2 + 2 == 4

@collecter
def test_string():
    assert "Hello" + " World" == "Hello World"
```

### 2. Run tests

```bash
pyforge
```

## Project Structure

```
pyforge-test/
├── src/
│   ├── main.py              # Entry point
│   └── core/
│       ├── collector.py     # Test decorator
│       ├── registry.py      # Test registry
│       ├── runner.py        # Test executor
│       └── reporter.py      # Results formatter
├── tests/                   # Your test files
└── pyproject.toml          # Project configuration
```

## License

MIT License - See [LICENSE](LICENSE) file for details
