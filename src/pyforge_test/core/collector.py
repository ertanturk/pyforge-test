from collections.abc import Callable
from typing import Any

from .registry import TESTS


# The test function is a decorator that collects test functions
# and adds them to the TESTS list.
def test(function: Callable[..., None]) -> Callable[..., None]:
    """Collects the test functions and adds them to the TESTS list.

    Args:
        function (Callable[..., None]): The test function to be collected.

    Returns:
        Callable[..., None]: The original test function, unmodified.
    """
    try:
        # check if the function is already in the TESTS list to avoid duplicates
        if any(test_dict["function"] == function for test_dict in TESTS):
            raise ValueError(f"Test function '{function.__name__}' is already collected.")
        # check if the function name starts with "test_"
        if not function.__name__.startswith("test_"):
            raise ValueError(f"Test function '{function.__name__}' must start with 'test_'.")
        # check if the function is valid or not (should be callable and should not have parameters)
        if not callable(function):
            raise ValueError(f"Test function '{function.__name__}' must be callable.")
        elif function.__code__.co_argcount > 0:
            raise ValueError(f"Test function '{function.__name__}' must not have parameters.")
        # Add the function to TESTS list with the file name and line number for better debugging
        TESTS.append(
            {
                "function": function,
                "filename": function.__code__.co_filename,
                "line_number": function.__code__.co_firstlineno,
                "skip_info": None,
                "marker": None,
            }
        )
        return function
    except Exception as e:
        raise RuntimeError(
            f"An error occurred while collecting test function '{function.__name__}': {e}"
        ) from e


# test_cases will be a list of tuples, where each tuple contains expression and expected result.
def test_parameterized(
    test_cases: list[tuple[Any, ...]],
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """A decorator to parameterize test functions with multiple test cases.

    Args:
        test_cases (list[tuple[Any, ...]]): A list of tuples, where each tuple
            contains the parameters to be passed to the test function.

    Returns:
        Callable[[Callable[..., None]], Callable[..., None]]:
            A decorator that can be applied to a test function.
    """

    def decorator(function: Callable[..., None]) -> Callable[..., None]:
        """The actual decorator that wraps the test function.

        Args:
            function (Callable[..., None]): The test function to be decorated.

        Returns:
            Callable[..., None]: The wrapped test function that will run with all test cases.
        """
        try:
            # Check if the function is already in the TESTS list to avoid duplicates
            if any(test_dict["function"] == function for test_dict in TESTS):
                raise ValueError(f"Test function '{function.__name__}' is already collected.")
            # Check if the function name starts with "test_"
            if not function.__name__.startswith("test_"):
                raise ValueError(f"Test function '{function.__name__}' must start with 'test_'.")
            # Check if the function is valid or not (should be callable)
            if not callable(function):
                raise ValueError(f"Test function '{function.__name__}' must be callable.")
            # Add the parameterized test cases to TESTS list with the file name
            # and line number for better debugging
            for case_index, case in enumerate(test_cases):

                def make_test(c: tuple[Any, ...] = case) -> None:
                    function(*c)

                make_test.__name__ = f"{function.__name__}_{case_index}"

                TESTS.append(
                    {
                        "function": make_test,
                        "filename": function.__code__.co_filename,
                        "line_number": function.__code__.co_firstlineno,
                        "skip_info": None,
                        "marker": None,
                    }
                )
            return function
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while collecting parameterized test function "
                f"'{function.__name__}': {e}"
            ) from e

    return decorator


# The test_skipif function is a decorator that allows skipping a test function based on a condition.
def test_skipif(
    condition: bool, reason: str
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """A decorator to skip a test function if a certain condition is met.

    Args:
        condition (bool): The condition that determines whether the test should be skipped.
        reason (str): The reason for skipping the test, which will be displayed in the report.

    Returns:
        Callable[[Callable[..., None]], Callable[..., None]]:
            A decorator that can be applied to a test function.
    """

    def decorator(function: Callable[..., None]) -> Callable[..., None]:
        """The actual decorator that wraps the test function.

        Args:
            function (Callable[..., None]): The test function to be decorated.

        Returns:
            Callable[..., None]: The wrapped test function that will
            be skipped if the condition is met.
        """
        try:
            # Check if the function is already in the TESTS list to avoid duplicates
            if any(test_dict["function"] == function for test_dict in TESTS):
                raise ValueError(f"Test function '{function.__name__}' is already collected.")
            # Check if the function name starts with "test_"
            if not function.__name__.startswith("test_"):
                raise ValueError(f"Test function '{function.__name__}' must start with 'test_'.")
            # Check if the function is valid or not (should be callable)
            if not callable(function):
                raise ValueError(f"Test function '{function.__name__}' must be callable.")
            # Add the skip information to TESTS list with the file name
            # and line number for better debugging
            TESTS.append(
                {
                    "function": function,
                    "filename": function.__code__.co_filename,
                    "line_number": function.__code__.co_firstlineno,
                    "skip_info": {"skip": condition, "reason": reason},
                    "marker": None,
                }
            )
            return function
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while collecting skipif test function "
                f"'{function.__name__}': {e}"
            ) from e

    return decorator


# The test_skip function is a decorator that allows skipping a test function unconditionally.
def test_skip(reason: str) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """A decorator to skip a test function unconditionally.

    Args:
        reason (str): The reason for skipping the test, which will be displayed in the report.

    Returns:
        Callable[[Callable[..., None]], Callable[..., None]]:
            A decorator that can be applied to a test function.
    """

    def decorator(function: Callable[..., None]) -> Callable[..., None]:
        """The actual decorator that wraps the test function.

        Args:
            function (Callable[..., None]): The test function to be decorated.

        Returns:
            Callable[..., None]: The wrapped test function that will be skipped unconditionally.
        """
        return test_skipif(True, reason)(function)

    return decorator


# Built-in markers
BUILTIN_MARKERS = {
    "slow": "Mark test as slow-running",
    "integration": "Mark test as an integration test (requires external resources)",
}


# The test_marker function is a decorator that allows marking a test function with a custom marker.
def test_marker(marker: str) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """A decorator to apply a built-in marker to a test function.

    Usage:
        @test_marker("integration")
        @test
        def test_database_connection() -> None:
            pass

    Args:
        marker (str): The marker to be applied to the test function.

    Returns:
        Callable[[Callable[..., None]], Callable[..., None]]:
            A decorator that can be applied to a test function.

    Raises:
        ValueError: If the marker is not a built-in marker.
    """

    def decorator(function: Callable[..., None]) -> Callable[..., None]:
        """The actual decorator that applies the marker to the test function.

        Args:
            function (Callable[..., None]): The test function to be marked.

        Returns:
            Callable[..., None]: The test function with the applied marker.

        Raises:
            ValueError: If the test function is not collected before applying the marker.
            RuntimeError: If an error occurs while applying the marker.
        """
        try:
            # Check if the marker is a built-in marker
            if marker not in BUILTIN_MARKERS:
                raise ValueError(f"Marker '{marker}' is not a built-in marker.")
            # Check if the marker is applied to collected test function
            if not any(test_dict["function"] == function for test_dict in TESTS):
                raise ValueError(
                    f"Test function '{function.__name__}' must be collected before applying marker."
                )
            # Update the marker information in TESTS list
            for test_dict in TESTS:
                if test_dict["function"] == function:
                    test_dict["marker"] = marker
                    break
            return function
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while applying marker '{marker}' to test function "
                f"'{function.__name__}': {e}"
            ) from e

    return decorator
