from collections.abc import Callable

from .registry import TESTS


# The collecter function is a decorator that collects test functions
# and adds them to the TESTS list.
def collecter(function: Callable[..., None]) -> Callable[..., None]:
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
        # Add the function to TESTS list
        TESTS.append(function)
        return function
    except Exception as e:
        raise RuntimeError(
            f"An error occurred while collecting test function '{function.__name__}': {e}"
        ) from e
