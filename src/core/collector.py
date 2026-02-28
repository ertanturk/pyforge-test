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
        if function in TESTS:
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
        TESTS.append((function, function.__code__.co_filename, function.__code__.co_firstlineno))
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
            if function in TESTS:
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
                    (
                        make_test,
                        function.__code__.co_filename,
                        function.__code__.co_firstlineno,
                    )
                )
            return function
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while collecting parameterized test function "
                f"'{function.__name__}': {e}"
            ) from e

    return decorator
