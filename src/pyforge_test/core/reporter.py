"""Reporter module for PyForge.

Provides functionality to format and display test results.
"""

import sys
from typing import Any


def report(results: list[tuple[str, str, str, int, dict[str, Any] | None]]) -> str:
    """Prints the test results in a readable format.

    Args:
        results (list[tuple[str, str, str, int]]): A list of tuples
            containing the test function name,
            result ("Passed", "Failed", or "Error: <error message>"),
            file name, and line number.

    Returns:
        str: Formatted test results as a string.
    """
    try:
        if not results:
            sys.exit(0)  # Exit with code 0 if there are no tests to report

        # First categorize results by file name and line number
        categorized_results: dict[str, list[tuple[str, str, int, dict[str, Any] | None]]] = {}
        for test_name, result, file, line, skip_info in results:
            if file not in categorized_results:
                categorized_results[file] = []
            categorized_results[file].append((test_name, result, line, skip_info))
        # Now format the results
        formatted_results: list[str] = []
        for file, tests in categorized_results.items():
            formatted_results.append(f"\nFile: {file}")
            for test_name, result, line, skip_info in tests:
                if skip_info and skip_info.get("skip", False):
                    result_check = "⏭️ "
                    skip_reason = skip_info["reason"]
                    formatted_results_message = (
                        f"  Line {line}: {test_name} - {result_check} Skipped: {skip_reason}"
                    )
                else:
                    result_check = (
                        "✅" if result == "Passed" else "❌" if result == "Failed" else "⚠️ "
                    )
                    formatted_results_message = (
                        f"  Line {line}: {test_name} - {result_check} {result}"
                    )
                formatted_results.append(formatted_results_message)
        return "\n".join(formatted_results)
    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the report: {e}") from e
