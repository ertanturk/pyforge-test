"""Reporter module for PyForge.

Provides functionality to format and display test results.
"""

import sys

from .registry import ResultDict


def report(results: list[ResultDict]) -> str:
    """Prints the test results in a readable format.

    Args:
        results (list[ResultDict]): A list of dictionaries containing test results
            with keys: name, result, filename, line_number, skip_info, marker.

    Returns:
        str: Formatted test results as a string.
    """
    try:
        if not results:
            sys.exit(0)  # Exit with code 0 if there are no tests to report

        # First categorize results by file name and line number
        categorized_results: dict[str, list[ResultDict]] = {}
        for result in results:
            file = result["filename"]
            if file not in categorized_results:
                categorized_results[file] = []
            categorized_results[file].append(result)

        # Now format the results
        formatted_results: list[str] = []
        for file, tests in categorized_results.items():
            formatted_results.append(f"\nFile: {file}")
            for result in tests:
                test_name = result["name"]
                result_status = result["result"]
                line = result["line_number"]
                skip_info = result["skip_info"]

                if skip_info and skip_info.get("skip", False):
                    result_check = "⏭️ "
                    skip_reason = skip_info["reason"]
                    formatted_results_message = (
                        f"  Line {line}: {test_name} - {result_check} Skipped: {skip_reason}"
                    )
                else:
                    result_check = (
                        "✅"
                        if result_status == "Passed"
                        else "❌"
                        if result_status == "Failed"
                        else "⚠️ "
                    )
                    formatted_results_message = (
                        f"  Line {line}: {test_name} - {result_check} {result_status}"
                    )
                formatted_results.append(formatted_results_message)
        return "\n".join(formatted_results)
    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the report: {e}") from e
