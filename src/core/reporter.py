"""Reporter module for PyForge.

Provides functionality to format and display test results.
"""


def report(results: list[tuple[str, str]]) -> str:
    """Prints the test results in a readable format.

    Args:
        results (list[tuple[str, str]]): A list of tuples
            containing the test function name and its result.

    Returns:
        str: Formatted test results as a string.
    """
    try:
        if not results:
            return "No tests were executed."

        report_lines = ["Test Results:"]
        for test_name, result in results:
            report_lines.append(f"{test_name}: {result}")
        return "\n".join(report_lines)
    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the report: {e}") from e
