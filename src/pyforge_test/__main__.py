"""Enable running pyforge_test as a module: python -m pyforge_test."""

import sys

from .core.main import main

if __name__ == "__main__":
    sys.exit(main())
