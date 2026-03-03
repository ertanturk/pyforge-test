from .registry import TESTS, ResultDict, TestCase


def _sort_tests_by_marker(
    tests: list[TestCase],
) -> list[TestCase]:
    """Sort tests by marker priority: unmarked first, wip tests last.

    Order: unmarked → fast → integration → slow → wip

    Args:
        tests (list[TestCase]): The list of tests to sort.

    Returns:
        list[TestCase]: Sorted tests by marker priority.
    """
    marker_priority: dict[str | None, int] = {
        None: 0,  # Unmarked tests run first
        "integration": 1,  # Then integration tests
        "slow": 2,  # Slow tests last
    }
    return sorted(tests, key=lambda t: marker_priority.get(t["marker"], 0))


def execute() -> list[ResultDict]:
    """Execute collected test functions and return their results.

    Tests are sorted by marker priority before execution. Skip conditions are
    evaluated at runtime. Results include test name, status, file, line number,
    skip info, and marker.

    Returns:
        list[ResultDict]: A list of dictionaries containing: name, result, filename,
            line_number, skip_info, and marker. Result values: "Passed", "Failed",
            "Error: <msg>", or "Skipped: <reason>".

    Raises:
        RuntimeError: If an error occurs during test execution.
    """
    try:
        results: list[ResultDict] = []

        if not TESTS:
            print("No tests to execute. Exiting.")
            return results

        print(f"Executing {len(TESTS)} test(s).\n")

        # Sort tests by marker priority
        sorted_tests = _sort_tests_by_marker(TESTS)

        for test in sorted_tests:
            test_func = test["function"]
            file = test["filename"]
            line = test["line_number"]
            skip_info = test["skip_info"]
            marker = test["marker"]
            skip_info_dict: dict[str, str] = skip_info or {}

            try:
                # Check if test should be skipped
                if skip_info_dict and skip_info_dict.get("skip", False):
                    results.append(
                        {
                            "name": test_func.__name__,
                            "result": f"Skipped: {skip_info_dict['reason']}",
                            "filename": file,
                            "line_number": line,
                            "skip_info": skip_info_dict,
                            "marker": marker,
                        }
                    )
                    continue

                # Execute the test
                test_func()
                results.append(
                    {
                        "name": test_func.__name__,
                        "result": "Passed",
                        "filename": file,
                        "line_number": line,
                        "skip_info": skip_info_dict,
                        "marker": marker,
                    }
                )

            except AssertionError as e:
                results.append(
                    {
                        "name": test_func.__name__,
                        "result": f"Failed: {e}",
                        "filename": file,
                        "line_number": line,
                        "skip_info": skip_info_dict,
                        "marker": marker,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "name": test_func.__name__,
                        "result": f"Error: {e}",
                        "filename": file,
                        "line_number": line,
                        "skip_info": skip_info_dict,
                        "marker": marker,
                    }
                )

        # Clear TESTS to avoid re-execution in future runs
        TESTS.clear()
        return results

    except Exception as e:
        raise RuntimeError(f"An error occurred while executing tests: {e}") from e
