"""
Script to be run before a commit. Ensures that the code adheres to best
style  practices by running the black formatter, pylint linter, and the
isort import sorter.

To automatically run this file on `git commit`, remove the `.sample`
extension from the `.git/hooks/pre-commit.sample` file and replace the
content with:

```shell
#!/bin/sh
echo "[pre-commit] Running pre-commit hook..."
python check_style.py
if [ $? -ne 0 ]; then
    echo "[pre-commit] FAIL"
    exit 1
fi
echo "[pre-commit] OK"
exit 0
```
If you're on Windows, replace the shebang (line 1) with:
```
#!C:/Progra~1/Git/usr/bin/sh.exe
```
"""

# It's probably better practice to do this kind of thing in a .bat or
# .ps1 file, but since that imposes Windows on other contributers, I
# think it's the safest to just use a Python wrapper.

import os
import shlex
import subprocess

# ==================== Commands to automate ==================== #

FORMATTER_COMMAND = "black ."
LINTER_COMMAND = "pylint MotionControl.py"
SORTER_COMMAND = "isort ."

# ============================================================== #

filename = os.path.basename(__file__)


def log(message: str) -> None:
    """Simple logger-like wrapper for `print`."""
    print(f"[{filename}] {message}", flush=True)


def run(command: str) -> None:
    """Wrapper for `subprocess.run`. Run the command and stream output.

    Args:
        command (str): Command to run as it if were at the command
        line.
    """
    args = shlex.split(command, posix=os.name == "posix")
    process = subprocess.Popen(args, stderr=subprocess.STDOUT)
    process.communicate()


log("Running formatter...")
run(FORMATTER_COMMAND)

log("Running linter...")
run(LINTER_COMMAND)

log("Running import sorter...")
run(SORTER_COMMAND)

log(f"Finished executing {filename}, no errors raised.")
