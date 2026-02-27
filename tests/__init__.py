"""PyForge test module initialization.

Automatically configures the Python path to enable test modules
to import from the core package without manual sys.path manipulation.
"""

import sys
from pathlib import Path

# Try to add src directory from the project being tested (CWD first, then relative)
_cwd: Path = Path.cwd()
_src_dir: Path | None = None

# Check if src exists in CWD
if (_cwd / "src").exists():
    _src_dir = _cwd / "src"
# Check if src exists relative to tests directory
elif (Path(__file__).parent.parent / "src").exists():
    _src_dir = Path(__file__).parent.parent / "src"

if _src_dir and str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))
