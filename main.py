import sys
from pathlib import Path

# Ensure project root is on the path so all src.* imports resolve correctly
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.ui.app import main

if __name__ == "__main__":
    main()
