from .registry import TESTS


# The execute function runs all the collected test functions and returns their results.
def execute() -> list[tuple[str, str, str, int]]:
    """Executes the collected test functions and returns their results.

    Returns:
        list[tuple[str, str, str, int]]: A list of tuples containing the test function
            name, result ("Passed", "Failed", or "Error: <error message>"),
            file name, and line number.
    """
    try:
        results: list[tuple[str, str, str, int]] = []
        # Print how many tests are being executed
        if not TESTS:
            print("No tests to execute. Exiting.")
            return results
        print(f"Executing {len(TESTS)} test(s).\n")
        for test, file, line in TESTS:
            try:
                test()
                results.append((test.__name__, "Passed", file, line))
            except AssertionError:
                results.append((test.__name__, "Failed", file, line))
            except Exception as e:
                results.append((test.__name__, f"Error: {e}", file, line))
        # After executing all tests, clear the TESTS list to avoid re-execution in future runs
        TESTS.clear()
        return results
    except Exception as e:
        raise RuntimeError(f"An error occurred while executing tests: {e}") from e
