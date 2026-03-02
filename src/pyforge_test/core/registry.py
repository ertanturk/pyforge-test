from collections.abc import Callable
from typing import Any

TESTS: list[tuple[Callable[..., None], str, int, dict[str, Any] | None, str | None]] = []
