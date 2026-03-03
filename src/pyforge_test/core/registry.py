from collections.abc import Callable
from typing import Any, TypedDict


class TestCase(TypedDict, total=False):
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


TESTS: list[TestCase] = []
