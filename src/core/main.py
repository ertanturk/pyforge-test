"""PyForge test runner entry point.

Executes collected tests and displays results.
Discovers and loads all test files from the tests directory.
"""

import contextlib
import importlib.util
import sys
import traceback
from pathlib import Path

# Set up path for tests package import
_pyforge_root: Path = Path(__file__).parent.parent  # src/
sys.path.insert(0, str(_pyforge_root))
with contextlib.suppress(ImportError):
    import tests  # noqa: F401

from .reporter import report
from .runner import execute


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
    pyforge_root: Path = Path(__file__).parent.parent
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

            print(f"✓ Loaded: {test_file.name}")
            loaded_count += 1

        except Exception as e:
            print(f"✗ Error loading {test_file.name}: {type(e).__name__}: {e}")

    return loaded_count


def main() -> int:
    """Main entry point for PyForge test runner.

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    try:
        # Find project root (where tests/ directory is located)
        project_root: Path = _find_project_root()

        # Setup src/ directory in sys.path if it exists
        _setup_src_path(project_root)

        # Add src directory to path for core module imports
        sys.path.insert(0, str(Path(__file__).parent))

        # Discover and load test modules
        modules_loaded: int = discover_and_load_tests(project_root)
        print(f"\nLoaded {modules_loaded} test module(s).\n")

        # Execute collected tests
        results: list[tuple[str, str]] = execute()

        # Generate and display report
        output: str = report(results)
        print(output)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
