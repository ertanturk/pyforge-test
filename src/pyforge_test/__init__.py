"""PyForge testing framework.

A lightweight unit testing framework with simple decorator-based tests.
"""

from .core.collector import (
    BUILTIN_MARKERS,
    test,
    test_marker,
    test_parameterized,
    test_skip,
    test_skipif,
)

__version__ = "0.1.0"
__all__ = [
    "BUILTIN_MARKERS",
    "test",
    "test_marker",
    "test_parameterized",
    "test_skip",
    "test_skipif",
]
