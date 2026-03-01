from .registry import TESTS


# The execute function runs all the collected test functions and returns their results.
def execute() -> list[tuple[str, str, str, int, dict[str, str]]]:
    """Executes the collected test functions and returns their results.

    Returns:
        list[tuple[str, str, str, int, dict[str, str]]]: A list of tuples
            containing the test function
            name, result ("Passed", "Failed", or "Error: <error message>"),
            file name, line number, and skip info.
    """
    try:
        results: list[tuple[str, str, str, int, dict[str, str]]] = []
        # Print how many tests are being executed
        if not TESTS:
            print("No tests to execute. Exiting.")
            return results
        print(f"Executing {len(TESTS)} test(s).\n")
        for test, file, line, skip_info in TESTS:
            skip_info_dict: dict[str, str] = skip_info or {}
            try:
                if skip_info_dict and skip_info_dict.get("skip", False):
                    results.append(
                        (
                            test.__name__,
                            f"Skipped: {skip_info_dict['reason']}",
                            file,
                            line,
                            skip_info_dict,
                        )
                    )
                    continue
                test()
                results.append((test.__name__, "Passed", file, line, skip_info_dict))
            except AssertionError:
                results.append((test.__name__, "Failed", file, line, skip_info_dict))
            except Exception as e:
                results.append((test.__name__, f"Error: {e}", file, line, skip_info_dict))
        # After executing all tests, clear the TESTS list to avoid re-execution in future runs
        TESTS.clear()
        return results
    except Exception as e:
        raise RuntimeError(f"An error occurred while executing tests: {e}") from e
