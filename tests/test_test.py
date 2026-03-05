"""Complete test suite example."""

import os
import time
from types import SimpleNamespace

from pyforge_test import (
    test,
    test_marker,
    test_parameterized,
    test_skip,
    test_skipif,
)

# ---------------------------------------------------------------------------
# Constants & stubs used by demo tests
# ---------------------------------------------------------------------------

EXPECTED_HALF_OF_TEN = 5
EXPECTED_THREE_SQUARED = 9
HTTP_OK = 200


def _mock_api_get(endpoint: str) -> SimpleNamespace:
    """Return a fake HTTP response for demonstration purposes."""
    return SimpleNamespace(status_code=HTTP_OK, body=f"OK from {endpoint}")


api_client: SimpleNamespace = SimpleNamespace(get=_mock_api_get)


def local_resource_available() -> bool:
    """Stub that checks whether a local-only resource is reachable."""
    return True


def broken_function() -> str:
    """Stub for a feature that is not yet implemented."""
    return "broken"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


# Unmarked test (Priority 0)
@test
def test_basic_arithmetic() -> None:
    """Fast unit test."""
    assert EXPECTED_HALF_OF_TEN == 10 / 2
    assert EXPECTED_THREE_SQUARED == 3**2


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
    assert response.status_code == HTTP_OK


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
