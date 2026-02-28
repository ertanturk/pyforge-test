"""PyForge testing framework.

A lightweight unit testing framework with simple decorator-based tests.
"""

from .core.collector import test, test_parameterized

__version__ = "0.0.1"
__all__ = ["test", "test_parameterized"]
