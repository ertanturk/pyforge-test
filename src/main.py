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
sys.path.insert(0, str(Path(__file__).parent.parent))
with contextlib.suppress(ImportError):
    import tests  # noqa: F401

from core.reporter import report
from core.runner import execute


def discover_and_load_tests() -> int:
    """Discover and load all test modules from the tests directory.

    Returns:
        int: Number of test modules successfully loaded.

    Raises:
        FileNotFoundError: If the tests directory does not exist.
    """
    tests_dir: Path = Path(__file__).parent.parent / "tests"

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
        # Add src directory to path for core module imports
        sys.path.insert(0, str(Path(__file__).parent))

        # Discover and load test modules
        modules_loaded: int = discover_and_load_tests()
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
