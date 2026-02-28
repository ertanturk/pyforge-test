"""Basic test scenarios for PyForge."""

from core.collector import test, test_parameterized


@test_parameterized([(2, 2, 4), (3, 5, 8), (10, -5, 5)])
def test_addition_parameterized(a: int, b: int, expected: int) -> None:
    """Test addition with multiple cases."""
    assert a + b == expected


@test_parameterized(
    [
        (int, "123", 123),
        (float, "3.14", 3.14),
        (str, 42, "42"),
        (list, "abc", ["a", "b", "c"]),
    ]
)
def test_type_conversion(func: type, value: object, expected: object) -> None:
    """Test type conversion functions with various inputs."""
    assert func(value) == expected


@test_parameterized(
    [
        (ValueError, int, "not_a_number"),
        (ZeroDivisionError, lambda: 1 / 0, None),
        (KeyError, lambda: {}["missing"], None),  # type: ignore[return-value]
    ]
)
def test_exception_handling(
    expected_error: type[Exception],
    func: object,
    arg: object,
) -> None:
    """Test that specific exceptions are raised."""
    try:
        if arg is not None:
            func(arg)  # type: ignore[operator]
        else:
            func()  # type: ignore[operator]
        raise AssertionError(f"Expected {expected_error.__name__} was not raised")
    except expected_error:
        pass  # Expected exception was raised


@test_parameterized(
    [
        ("hello world", str.upper, "HELLO WORLD"),
        ("  stripped  ", str.strip, "stripped"),
        ("abc", str.replace, "Abc", "a", "A"),
    ]
)
def test_string_methods(
    input_str: str,
    method: object,
    expected: str,
    *args: str,
) -> None:
    """Test string methods with various inputs."""
    result = method(input_str, *args)  # type: ignore[operator]
    assert result == expected


@test
def test_addition() -> None:
    """Test basic addition."""
    assert 2 + 2 == 4


@test
def test_subtraction() -> None:
    """Test basic subtraction."""
    assert 5 - 3 == 2


@test
def test_string_concat() -> None:
    """Test string concatenation."""
    assert "Hello" + " " + "World" == "Hello World"
