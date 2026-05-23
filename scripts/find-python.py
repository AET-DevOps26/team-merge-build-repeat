#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import sys


def works(command: list[str]) -> bool:
    return (
        subprocess.run(
            command + ["-c", "import sys; raise SystemExit(sys.version_info < (3, 10))"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def main() -> int:
    candidates = [["python3"], ["python"], ["py", "-3"], ["py"]]

    for command in candidates:
        if shutil.which(command[0]) and works(command):
            print(" ".join(command))
            return 0

    print(
        "No Python 3.10+ interpreter found. Install Python 3 or run "
        "`make secrets PYTHON=<command>`.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
