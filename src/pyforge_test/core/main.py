"""PyForge test runner entry point.

Executes collected tests and displays results.
Discovers and loads all test files from the tests directory.
"""

import argparse
import contextlib
import importlib.util
import sys
import traceback
from pathlib import Path

from .reporter import VERBOSITY_NORMAL, VERBOSITY_QUIET, VERBOSITY_VERBOSE, report
from .runner import execute

# Set up path for tests package import
_pyforge_root: Path = Path(__file__).parent.parent.parent.parent  # project root
sys.path.insert(0, str(_pyforge_root))
with contextlib.suppress(ImportError):
    import tests  # pyright: ignore[reportUnusedImport] # noqa: F401


def _find_project_root() -> Path:
    """Find the project root directory.

    First checks current working directory, then the directory where
    pyforge is installed.

    Returns:
        Path: The project root directory containing tests/ subdirectory.

    Raises:
        FileNotFoundError: If no project structure is found.
    """
    # Check current working directory first (for user projects)
    cwd: Path = Path.cwd()
    if (cwd / "tests").exists() and (cwd / "tests").is_dir():
        return cwd

    # Check one level up from CWD
    parent: Path = cwd.parent
    if (parent / "tests").exists() and (parent / "tests").is_dir():
        return parent

    # Fall back to pyforge installation directory
    pyforge_root: Path = Path(__file__).parent.parent.parent.parent
    if (pyforge_root / "tests").exists() and (pyforge_root / "tests").is_dir():
        return pyforge_root

    raise FileNotFoundError(
        "No project structure found. Expected 'tests/' directory in "
        f"current directory ({cwd}), parent directory ({parent}), "
        f"or pyforge installation ({pyforge_root})"
    )


def _setup_src_path(project_root: Path) -> None:
    """Add src directory to sys.path if it exists.

    Args:
        project_root: The root directory of the project.
    """
    src_dir: Path = project_root / "src"
    if src_dir.exists() and src_dir.is_dir():
        src_path: str = str(src_dir)
        if src_path not in sys.path:
            sys.path.insert(0, src_path)


def discover_and_load_tests(project_root: Path) -> int:
    """Discover and load all test modules from the tests directory.

    Args:
        project_root: The root directory containing the tests/ folder.

    Returns:
        int: Number of test modules successfully loaded.

    Raises:
        FileNotFoundError: If the tests directory does not exist.
    """
    tests_dir: Path = project_root / "tests"

    if not tests_dir.exists() or not tests_dir.is_dir():
        raise FileNotFoundError(f"Tests directory '{tests_dir}' does not exist.")

    # Find all test files (anything matching test*.py pattern)
    test_files: list[Path] = sorted(tests_dir.glob("test*.py"))

    if not test_files:
        print(f"No test modules found in '{tests_dir}'")
        return 0

    loaded_count: int = 0
    print(f"Discovering test modules in '{tests_dir}'...")

    for test_file in test_files:
        try:
            # Load the module using importlib
            spec = importlib.util.spec_from_file_location(test_file.stem, test_file)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not create module spec for {test_file.name}")

            module = importlib.util.module_from_spec(spec)
            sys.modules[test_file.stem] = module
            spec.loader.exec_module(module)

            # Verify that the module has a __name__ attribute (it should)
            if not hasattr(module, "__name__"):
                raise ImportError(f"Module {test_file.name} does not have a __name__ attribute")

            print(f"Loaded: {test_file.name}")
            loaded_count += 1

        except Exception as e:
            print(f"✗ Error loading {test_file.name}: {type(e).__name__}: {e}")

    return loaded_count


def main() -> int:
    """Main entry point for PyForge test runner.

    Supports verbosity levels, fail-fast option, and selective running:
    - Default: Normal output
    - -q/--quiet: Only show summary and failures
    - -v/--verbose: Show detailed info with tracebacks
    - --fail-fast: Stop on first failure
    - -k: Substring filtering on test names
    - FILES: File paths to run tests from (positional arguments)

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    # Parse CLI arguments
    parser = argparse.ArgumentParser(
        description="PyForge - Lightweight Python testing framework",
        epilog="Examples:\n"
        "  pyforge                    # Run all tests\n"
        "  pyforge -k test_basic      # Run tests with 'test_basic' in name\n"
        "  pyforge test_name.py       # Run tests from specific file(s)\n"
        "  pyforge -k basic -v        # Verbose output for matching tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Quiet mode: only show summary and failures",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose mode: show detailed info with tracebacks",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop execution at first failure",
    )
    parser.add_argument(
        "-k",
        dest="name_pattern",
        default=None,
        help="Substring filter: run tests with this string in their name",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="File paths to run tests from (supports partial paths and filenames)",
    )
    args = parser.parse_args()

    # Determine verbosity level
    if args.quiet:
        verbosity = VERBOSITY_QUIET
    elif args.verbose:
        verbosity = VERBOSITY_VERBOSE
    else:
        verbosity = VERBOSITY_NORMAL

    try:
        # Find project root (where tests/ directory is located)
        project_root: Path = _find_project_root()

        # Setup src/ directory in sys.path if it exists
        _setup_src_path(project_root)

        # Add src directory to path for core module imports
        sys.path.insert(0, str(Path(__file__).parent))

        # Discover and load test modules
        modules_loaded: int = discover_and_load_tests(project_root)
        if modules_loaded == 0:
            return 0

        if verbosity >= VERBOSITY_NORMAL:
            print(f"\nLoaded {modules_loaded} test module(s).\n")

        # Execute collected tests with filters
        results, summary = execute(
            fail_fast=args.fail_fast,
            name_pattern=args.name_pattern,
            file_patterns=args.files if args.files else None,
        )

        # Generate and display report
        output: str = report(results, summary, verbosity=verbosity)
        print(output)

        # Return 1 if any tests failed or errors occurred
        has_failures: bool = int(summary.get("failed", 0)) > 0 or int(summary.get("errors", 0)) > 0
        return 1 if has_failures else 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
