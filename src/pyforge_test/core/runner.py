from collections.abc import Callable

from .registry import TESTS


def _sort_tests_by_marker(
    tests: list[tuple[Callable[..., None], str, int, dict[str, str] | None, str | None]],
) -> list[tuple[Callable[..., None], str, int, dict[str, str] | None, str | None]]:
    """Sort tests by marker priority: unmarked first, wip tests last.

    Order: unmarked → fast → integration → slow → wip

    Args:
        tests (list[tuple[...]]): The list of tests to sort.

    Returns:
        list[tuple[...]]: Sorted tests by marker priority.
    """
    marker_priority: dict[str | None, int] = {
        None: 0,  # Unmarked tests run first
        "integration": 1,  # Then integration tests
        "slow": 2,  # Slow tests last
    }
    return sorted(tests, key=lambda t: marker_priority.get(t[4], 0))


def execute() -> list[tuple[str, str, str, int, dict[str, str], str | None]]:
    """Execute collected test functions and return their results.

    Tests are sorted by marker priority before execution. Skip conditions are
    evaluated at runtime. Results include test name, status, file, line number,
    skip info, and marker.

    Returns:
        list[tuple[str, str, str, int, dict[str, str], str | None]]: A list of
            tuples containing: (test_name, result, filename, line_number,
            skip_info, marker). Result values: "Passed", "Failed", "Error: <msg>",
            or "Skipped: <reason>".

    Raises:
        RuntimeError: If an error occurs during test execution.
    """
    try:
        results: list[tuple[str, str, str, int, dict[str, str], str | None]] = []

        if not TESTS:
            print("No tests to execute. Exiting.")
            return results

        print(f"Executing {len(TESTS)} test(s).\n")

        # Sort tests by marker priority
        sorted_tests = _sort_tests_by_marker(TESTS)

        for test, file, line, skip_info, marker in sorted_tests:
            skip_info_dict: dict[str, str] = skip_info or {}

            try:
                # Check if test should be skipped
                if skip_info_dict and skip_info_dict.get("skip", False):
                    results.append(
                        (
                            test.__name__,
                            f"Skipped: {skip_info_dict['reason']}",
                            file,
                            line,
                            skip_info_dict,
                            marker,
                        )
                    )
                    continue

                # Execute the test
                test()
                results.append((test.__name__, "Passed", file, line, skip_info_dict, marker))

            except AssertionError as e:
                results.append((test.__name__, f"Failed: {e}", file, line, skip_info_dict, marker))
            except Exception as e:
                results.append((test.__name__, f"Error: {e}", file, line, skip_info_dict, marker))

        # Clear TESTS to avoid re-execution in future runs
        TESTS.clear()
        return results

    except Exception as e:
        raise RuntimeError(f"An error occurred while executing tests: {e}") from e
