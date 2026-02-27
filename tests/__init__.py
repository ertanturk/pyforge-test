"""PyForge test module initialization.

Automatically configures the Python path to enable test modules
to import from the core package without manual sys.path manipulation.
"""

import sys
from pathlib import Path

# Add src directory to sys.path so tests can import core modules
_src_dir: Path = Path(__file__).parent.parent / "src"
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))
