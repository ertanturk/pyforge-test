"""Basic test scenarios for PyForge."""

from core.collector import collecter


@collecter
def test_addition() -> None:
    """Test basic addition."""
    assert 2 + 2 == 4


@collecter
def test_subtraction() -> None:
    """Test basic subtraction."""
    assert 5 - 3 == 2


@collecter
def test_string_concat() -> None:
    """Test string concatenation."""
    assert "Hello" + " " + "World" == "Hello World"
