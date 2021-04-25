"""genshinhelper entry point.

Using `python <project_package>` or `python -m <project_package>` command.
"""

if not __package__:
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from genshinhelper import main

if __name__ == "__main__":
    main()
