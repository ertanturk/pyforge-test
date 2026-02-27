from .registry import TESTS


# The execute function runs all the collected test functions and returns their results.
def execute() -> list[tuple[str, str]]:
    """Executes the collected test functions and returns their results.

    Returns:
        list[tuple[str, str]]: A list of tuples containing the test function
            name and its result ("Passed", "Failed", or "Error: <error message>").
    """
    try:
        results: list[tuple[str, str]] = []
        for test in TESTS:
            try:
                test()
                results.append((test.__name__, "Passed"))
            except AssertionError:
                results.append((test.__name__, "Failed"))
            except Exception as e:
                results.append((test.__name__, f"Error: {e}"))
        # After executing all tests, clear the TESTS list to avoid re-execution in future runs
        TESTS.clear()
        return results
    except Exception as e:
        raise RuntimeError(f"An error occurred while executing tests: {e}") from e
