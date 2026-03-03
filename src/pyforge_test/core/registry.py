from collections.abc import Callable
from typing import Any, TypedDict


class TestCase(TypedDict):
    """TypedDict for test case structure.

    Attributes:
        function: The test function to execute.
        filename: The source file where the test is defined.
        line_number: The line number where the test is defined.
        skip_info: Dictionary containing skip information and reason.
        marker: The test marker (e.g., 'slow', 'integration', 'wip').
    """

    function: Callable[..., None]
    filename: str
    line_number: int
    skip_info: dict[str, Any] | None
    marker: str | None


class ResultDict(TypedDict):
    """TypedDict for test result structure.

    Attributes:
        name: The test function name.
        result: The test result status (Passed, Failed, Error, or Skipped).
        filename: The source file where the test is defined.
        line_number: The line number where the test is defined.
        skip_info: Dictionary containing skip information and reason.
        marker: The test marker (e.g., 'slow', 'integration', 'wip').
        traceback: The traceback string for failed/error tests, None otherwise.
    """

    name: str
    result: str
    filename: str
    line_number: int
    skip_info: dict[str, Any] | None
    marker: str | None
    traceback: str | None


TESTS: list[TestCase] = []
