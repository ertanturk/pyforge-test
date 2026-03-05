"""PyForge testing framework.

A lightweight unit testing framework with simple decorator-based tests.
"""

from importlib.metadata import PackageNotFoundError, version

from .core.collector import (
    BUILTIN_MARKERS,
    test,
    test_marker,
    test_parameterized,
    test_skip,
    test_skipif,
)

try:
    __version__: str = version("pyforge-test")
except PackageNotFoundError:
    # Fallback for editable installs or running from source without metadata
    try:
        from ._version import version as __version__  # type: ignore[no-redef]
    except ImportError:
        __version__ = "0.0.0+unknown"

__all__ = [
    "BUILTIN_MARKERS",
    "test",
    "test_marker",
    "test_parameterized",
    "test_skip",
    "test_skipif",
]
