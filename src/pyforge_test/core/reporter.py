"""Reporter module for PyForge.

Provides functionality to format and display test results.
"""

import os
import re
import sys

from .registry import ResultDict

# Verbosity levels
VERBOSITY_QUIET = 0
VERBOSITY_NORMAL = 1
VERBOSITY_VERBOSE = 2

# ANSI color codes
COLORS = {
    "green": "\033[1;92m",  # Bold bright green for PASSED
    "blue": "\033[1;94m",  # Bold bright blue for SKIPPED
    "red": "\033[1;91m",  # Bold bright red for FAILED
    "orange": "\033[1;33m",  # Bold yellow/orange for ERROR
    "white": "\033[1;97m",  # Bold bright white
    "gray": "\033[90m",  # Dim gray for separators
    "cyan": "\033[1;96m",  # Bold bright cyan for highlighted code lines
    "reset": "\033[0m",  # Reset to default
}

# Compiled regex for parsing traceback "  File ..." lines
_FILE_LINE_RE: re.Pattern[str] = re.compile(r'  File "([^"]+)", line (\d+), in (.+)')


def _format_duration(duration_str: str) -> str:
    """Format duration string to human-readable format.

    Args:
        duration_str (str): Duration as timedelta string (e.g., "0:00:02.345678").

    Returns:
        str: Human-readable duration (e.g., "2.35 seconds").
    """
    try:
        # Parse timedelta string format
        duration_parts = 3
        seconds_per_minute = 60
        seconds_per_hour = 3600
        milliseconds_per_second = 1000

        parts = duration_str.split(":")
        if len(parts) == duration_parts:
            hours, minutes, seconds = parts
            total_seconds = (
                int(hours) * seconds_per_hour + int(minutes) * seconds_per_minute + float(seconds)
            )
            if total_seconds < 1:
                return f"{total_seconds * milliseconds_per_second:.0f} ms"
            elif total_seconds < seconds_per_minute:
                return f"{total_seconds:.2f} seconds"
            else:
                mins = int(total_seconds // seconds_per_minute)
                secs = total_seconds % seconds_per_minute
                return f"{mins}m {secs:.2f}s"
        return duration_str
    except Exception:
        return duration_str


def report(results: list[ResultDict], summary: dict[str, int | str], verbosity: int = 1) -> str:
    """Prints the test results in a readable format with summary counts.

    Args:
        results (list[ResultDict]): A list of dictionaries containing test results
            with keys: name, result, filename, line_number, skip_info, marker,
            traceback.
        summary (dict[str, int | str]): Dictionary with test counts for passed,
            failed, skipped, errors, and duration as a timedelta string.
        verbosity (int): Verbosity level (0=quiet, 1=normal, 2=verbose).
            Defaults to 1.

    Returns:
        str: Formatted test results with summary as a string.
    """
    try:
        if not results:
            sys.exit(0)  # Exit with code 0 if there are no tests to report

        # Extract summary data with type casting
        passed: int = int(summary.get("passed", 0))
        failed: int = int(summary.get("failed", 0))
        skipped: int = int(summary.get("skipped", 0))
        errors: int = int(summary.get("errors", 0))
        duration_raw = summary.get("duration", "N/A")
        duration = _format_duration(str(duration_raw))
        total = passed + failed + skipped + errors

        # Filter results based on verbosity
        if verbosity == VERBOSITY_QUIET:  # Quiet mode
            display_results = [r for r in results if r["result"] != "Passed"]
        else:
            display_results = results

        # Categorize results by file
        categorized_results: dict[str, list[ResultDict]] = {}
        for result in display_results:
            file = result["filename"]
            if file not in categorized_results:
                categorized_results[file] = []
            categorized_results[file].append(result)

        # Determine overall status
        has_failures = failed > 0 or errors > 0
        status_color = COLORS["red"] if has_failures else COLORS["green"]

        # Build output
        formatted_results: list[str] = []
        separator = f"{COLORS['gray']}{'-' * 72}{COLORS['reset']}"

        # Header (skip in quiet mode if no failures)
        if verbosity > VERBOSITY_QUIET or (
            verbosity == VERBOSITY_QUIET and (failed > 0 or errors > 0)
        ):
            formatted_results.append("")
            header_line = f"{status_color}PyForge Test Results{COLORS['reset']}"
            formatted_results.append(header_line)
            formatted_results.append(separator)

        # Test results by file
        if verbosity > VERBOSITY_QUIET or (verbosity == VERBOSITY_QUIET and display_results):
            for file, tests in categorized_results.items():
                file_name = file.split("/")[-1]
                formatted_results.append(f"\n{file_name}")
                for result in tests:
                    formatted_results.append(_format_test_result(result, verbosity=verbosity))

        # Summary section
        formatted_results.append("")
        formatted_results.append(separator)

        # Summary stats in grid format
        passed_count = (
            f"{COLORS['green']}PASSED:{COLORS['reset']} "
            f"{COLORS['white']}{passed}/{total}{COLORS['reset']}"
        )
        failed_count = (
            f"{COLORS['red']}FAILED:{COLORS['reset']} "
            f"{COLORS['white']}{failed}/{total}{COLORS['reset']}"
        )
        skipped_count = (
            f"{COLORS['blue']}SKIPPED:{COLORS['reset']} "
            f"{COLORS['white']}{skipped}/{total}{COLORS['reset']}"
        )
        errors_count = (
            f"{COLORS['orange']}ERRORS:{COLORS['reset']} "
            f"{COLORS['white']}{errors}/{total}{COLORS['reset']}"
        )
        summary_line = f"Summary: {passed_count}  {failed_count}  {skipped_count}  {errors_count}"
        formatted_results.append(summary_line)
        formatted_results.append(
            f"Took {COLORS['white']}{duration}{COLORS['reset']} to execute all tests"
        )
        formatted_results.append(separator)
        formatted_results.append("")

        return "\n".join(formatted_results)
    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the report: {e}") from e


def _shorten_path(filepath: str) -> str:
    """Shorten a file path to be relative to CWD when possible.

    Args:
        filepath (str): Absolute or relative file path.

    Returns:
        str: Relative path from CWD, or a shortened version using the last
            two path components as a fallback.
    """
    try:
        rel = os.path.relpath(filepath)
        # Only keep relative if it doesn't go more than one level above CWD
        if not rel.startswith(f"..{os.sep}..{os.sep}"):
            return rel
    except ValueError:
        pass  # Windows drive-letter mismatch edge case
    # Fallback: last 2 path components
    parts = [p for p in filepath.replace("\\", "/").split("/") if p]
    return "/".join(parts[-2:]) if len(parts) > 2 else filepath


def _parse_traceback(
    tb_str: str,
) -> tuple[list[tuple[str, int, str, str | None]], str]:
    """Parse a traceback string into structured frames and exception text.

    Args:
        tb_str (str): Raw traceback string from the traceback module.

    Returns:
        tuple[list[tuple[str, int, str, str | None]], str]: A tuple of
            (frames, exception_string). Each frame is a
            (filename, lineno, funcname, code_snippet) tuple, where
            code_snippet may be None if absent.
    """
    frames: list[tuple[str, int, str, str | None]] = []
    exception_str = ""
    if not tb_str:
        return frames, exception_str

    lines = tb_str.strip().splitlines()
    i = 0
    # Skip "Traceback (most recent call last):" header
    if lines and lines[0].startswith("Traceback"):
        i = 1

    while i < len(lines):
        line = lines[i]
        match = _FILE_LINE_RE.match(line)
        if match:
            filename = match.group(1)
            lineno = int(match.group(2))
            funcname = match.group(3)
            # The following line may be an inline code snippet
            code: str | None = None
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.startswith("    ") and not _FILE_LINE_RE.match(next_line):
                    code = next_line.strip()
                    i += 1
            frames.append((filename, lineno, funcname, code))
        elif line and not line.startswith((" ", "\t")):
            # Non-indented line after frames → exception type / message
            exception_str = "\n".join(lines[i:])
            break
        i += 1

    return frames, exception_str


def _format_traceback_location(tb_str: str) -> str:
    """Extract the last frame and return a compact location string.

    Used in normal verbosity mode to show exactly where a test failed
    without printing the full traceback.

    Args:
        tb_str (str): Raw traceback string.

    Returns:
        str: Compact location line (e.g., '    → tests/file.py:10  in func'),
            or an empty string if parsing fails.
    """
    frames, _ = _parse_traceback(tb_str)
    if not frames:
        return ""
    filepath, lineno, funcname, _ = frames[-1]
    short = _shorten_path(filepath)
    return (
        f"    {COLORS['gray']}→ "
        f"{COLORS['white']}{short}"
        f"{COLORS['gray']}:{lineno}"
        f"  in {funcname}{COLORS['reset']}"
    )


def _format_traceback_block(tb_str: str) -> str:
    """Format a complete traceback with ANSI colors for verbose mode.

    The last (failing) frame and its code snippet are highlighted in
    distinct colors; earlier frames are dimmed. The exception type is
    rendered in red and the message in gray.

    Args:
        tb_str (str): Raw traceback string.

    Returns:
        str: Fully formatted and colorized traceback block, or an empty
            string if the input cannot be parsed.
    """
    frames, exception_str = _parse_traceback(tb_str)
    if not frames and not exception_str:
        return ""

    indent = "    "
    lines: list[str] = []

    # Traceback header
    lines.append(f"{indent}{COLORS['gray']}Traceback (most recent call last):{COLORS['reset']}")

    total = len(frames)
    for idx, (filepath, lineno, funcname, code) in enumerate(frames):
        is_last = idx == total - 1
        short = _shorten_path(filepath)
        # Highlight the failing frame; dim earlier frames
        frame_color = COLORS["white"] if is_last else COLORS["gray"]
        lines.append(
            f'{indent}  {frame_color}File "{short}", line {lineno}, in {funcname}{COLORS["reset"]}'
        )
        if code:
            code_color = COLORS["cyan"] if is_last else COLORS["gray"]
            lines.append(f"{indent}      {code_color}{code}{COLORS['reset']}")

    # Exception type and message
    if exception_str:
        # Split "ExcType: message" on the first colon only
        colon_idx = exception_str.find(":")
        if colon_idx != -1 and "\n" not in exception_str[:colon_idx]:
            exc_type = exception_str[:colon_idx]
            exc_rest = exception_str[colon_idx:]
        else:
            exc_type = exception_str.splitlines()[0]
            exc_rest = ""

        exc_rest_lines = exc_rest.splitlines()
        first_rest = exc_rest_lines[0] if exc_rest_lines else ""
        lines.append(
            f"{indent}{COLORS['red']}{exc_type}{COLORS['reset']}"
            f"{COLORS['gray']}{first_rest}{COLORS['reset']}"
        )
        for extra in exc_rest_lines[1:]:
            if extra:
                lines.append(f"{indent}  {COLORS['gray']}{extra}{COLORS['reset']}")

    return "\n".join(lines)


def _format_test_result(result: ResultDict, verbosity: int = 1) -> str:
    """Format a single test result with proper symbols and colors.

    Args:
        result (ResultDict): A test result dictionary.
        verbosity (int): Verbosity level (0=quiet, 1=normal, 2=verbose).
            Defaults to 1.

    Returns:
        str: Formatted test result line.
    """
    test_name = result["name"]
    result_status = result["result"]
    line = result["line_number"]
    skip_info = result["skip_info"]
    traceback_str = result.get("traceback")

    result_line = ""

    if skip_info and skip_info.get("skip", False):
        skip_reason = skip_info["reason"]
        colored_status = f"{COLORS['blue']}SKIPPED{COLORS['reset']}"
        result_line = f"  {colored_status} {test_name} (Line {line}): {skip_reason}"
    elif result_status == "Passed":
        colored_status = f"{COLORS['green']}PASSED{COLORS['reset']}"
        result_line = f"  {colored_status} {test_name} (Line {line})"
    elif result_status.startswith("Failed"):
        colored_status = f"{COLORS['red']}FAILED{COLORS['reset']}"
        error_msg = result_status.replace("Failed: ", "")
        result_line = f"  {colored_status} {test_name} (Line {line}): {error_msg}"
    else:
        colored_status = f"{COLORS['orange']}ERROR{COLORS['reset']}"
        error_msg = result_status.replace("Error: ", "")
        result_line = f"  {colored_status} {test_name} (Line {line}): {error_msg}"

    # Add location (normal) or full colorized traceback (verbose) for failures/errors
    if traceback_str:
        if verbosity == VERBOSITY_NORMAL:
            location = _format_traceback_location(traceback_str)
            if location:
                result_line += f"\n{location}"
        elif verbosity == VERBOSITY_VERBOSE:
            tb_block = _format_traceback_block(traceback_str)
            if tb_block:
                result_line += f"\n{tb_block}"

    return result_line
