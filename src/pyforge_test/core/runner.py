"""Test runner module for PyForge.

Executes collected tests and handles test result management.
"""

import os
import time
import traceback
from datetime import timedelta

from .registry import TESTS, ResultDict, TestCase

# Path segment identifying pyforge internal core modules (filtered from user-facing tracebacks)
_PYFORGE_CORE: str = os.path.join("pyforge_test", "core")


def _clean_traceback(exc: BaseException) -> str:
    """Format a clean traceback, filtering out pyforge internal frames.

    Removes framework-internal frames so users only see code relevant
    to their test failures.

    Args:
        exc (BaseException): The exception whose traceback to format.

    Returns:
        str: Formatted traceback string with internal pyforge frames removed.
    """
    te = traceback.TracebackException.from_exception(exc)
    filtered = [frame for frame in te.stack if _PYFORGE_CORE not in frame.filename]
    # Preserve at least the last frame if all frames were internal
    if not filtered and te.stack:
        filtered = list(te.stack[-1:])
    te.stack = traceback.StackSummary.from_list(filtered)
    return "".join(te.format())


def _filter_tests(
    tests: list[TestCase],
    name_pattern: str | None = None,
    file_patterns: list[str] | None = None,
) -> list[TestCase]:
    """Filter tests by name and file patterns.

    Args:
        tests: The list of tests to filter.
        name_pattern: Substring pattern to match test names. Defaults to None (all).
        file_patterns: List of file patterns to match. Defaults to None (all).

    Returns:
        list[TestCase]: Filtered tests matching the criteria.
    """
    filtered = tests

    # Filter by name substring
    if name_pattern:
        filtered = [t for t in filtered if name_pattern in t["function"].__name__]

    # Filter by file patterns
    if file_patterns:
        filtered = [
            t for t in filtered if any(pattern in t["filename"] for pattern in file_patterns)
        ]

    return filtered


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


def execute(
    fail_fast: bool = False,
    name_pattern: str | None = None,
    file_patterns: list[str] | None = None,
) -> tuple[list[ResultDict], dict[str, int | str]]:
    """Execute collected test functions and return their results.

    Tests are filtered by name and file patterns, then sorted by marker
    priority before execution. Skip conditions are evaluated at runtime.
    Results include test name, status, file, line number, skip info, marker,
    and traceback for failures.

    Args:
        fail_fast: Stop execution at first failure or error. Defaults to False.
        name_pattern: Substring pattern to match test names. Defaults to None.
        file_patterns: List of file patterns to match. Defaults to None.

    Returns:
        tuple[list[ResultDict], dict[str, int | str]]: A tuple containing a list of
            dictionaries with test results and a summary dictionary with counts
            and duration.
    Raises:
        RuntimeError: If an error occurs during test execution.
    """
    try:
        start_time = time.monotonic()
        results: list[ResultDict] = []
        # Counters for summary
        pass_count = 0
        fail_count = 0
        skip_count = 0
        error_count = 0

        if not TESTS:
            print("No tests to execute. Exiting.")
            return results, {"passed": 0, "failed": 0, "skipped": 0, "errors": 0}

        # Filter tests based on criteria
        filtered_tests = _filter_tests(TESTS, name_pattern, file_patterns)

        if not filtered_tests:
            print(
                "No tests match the specified filters. "
                f"(name pattern: {name_pattern}, files: {file_patterns})"
            )
            TESTS.clear()
            return results, {"passed": 0, "failed": 0, "skipped": 0, "errors": 0}

        print(f"Executing {len(filtered_tests)} test(s).\n")

        # Sort tests by marker priority
        sorted_tests = _sort_tests_by_marker(filtered_tests)

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
                            "traceback": None,
                        }
                    )
                    skip_count += 1
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
                        "traceback": None,
                    }
                )
                pass_count += 1

            except AssertionError as e:
                tb_str = _clean_traceback(e)
                results.append(
                    {
                        "name": test_func.__name__,
                        "result": f"Failed: {e}",
                        "filename": file,
                        "line_number": line,
                        "skip_info": skip_info_dict,
                        "marker": marker,
                        "traceback": tb_str,
                    }
                )
                fail_count += 1
                if fail_fast:
                    break
            except Exception as e:
                tb_str = _clean_traceback(e)
                results.append(
                    {
                        "name": test_func.__name__,
                        "result": f"Error: {e}",
                        "filename": file,
                        "line_number": line,
                        "skip_info": skip_info_dict,
                        "marker": marker,
                        "traceback": tb_str,
                    }
                )
                error_count += 1
                if fail_fast:
                    break
        end_time = time.monotonic()
        duration = timedelta(seconds=end_time - start_time)
        # Clear TESTS to avoid re-execution in future runs
        TESTS.clear()
        summary: dict[str, int | str] = {
            "passed": pass_count,
            "failed": fail_count,
            "skipped": skip_count,
            "errors": error_count,
            "duration": str(duration),
        }
        return (results, summary)
    except Exception as e:
        raise RuntimeError(f"An error occurred while executing tests: {e}") from e
