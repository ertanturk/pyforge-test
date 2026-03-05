"""PyForge testing framework.

A lightweight unit testing framework with simple decorator-based tests.
"""

from ._version import __version__
from .core.collector import (
    BUILTIN_MARKERS,
    test,
    test_marker,
    test_parameterized,
    test_skip,
    test_skipif,
)

__all__ = [
    "BUILTIN_MARKERS",
    "__version__",
    "test",
    "test_marker",
    "test_parameterized",
    "test_skip",
    "test_skipif",
]
