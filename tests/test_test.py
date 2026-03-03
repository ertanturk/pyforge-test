"""Complete test suite example."""

import os
import time

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
    assert 3**2 == 9


# Parameterized test
@test_parameterized(
    [
        ("hello", "HELLO"),
        ("world", "WORLD"),
        ("PyForge", "PYFORGE"),
    ]
)
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
    result = sum(i**2 for i in range(10000))
    assert result > 0


# Conditional skip
@test_skipif(os.getenv("CI") == "true", reason="Skip in CI environment")
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
