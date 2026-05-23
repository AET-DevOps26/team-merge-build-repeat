#!/usr/bin/env python3

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys


def candidate_paths() -> list[Path]:
    candidates: list[Path] = []

    pipx_bin_dir = os.environ.get("PIPX_BIN_DIR")
    if pipx_bin_dir:
        candidates.append(Path(pipx_bin_dir) / executable_name())

    candidates.append(Path.home() / ".local" / "bin" / executable_name())
    return candidates


def executable_name() -> str:
    return "secretctl.exe" if sys.platform == "win32" else "secretctl"


def secretctl_command() -> list[str]:
    from_path = shutil.which("secretctl")
    if from_path:
        return [from_path]

    for candidate in candidate_paths():
        if candidate.exists():
            return [str(candidate)]

    print(
        "secretctl was installed, but the executable was not found. "
        "Open a new terminal or run the installer again.",
        file=sys.stderr,
    )
    raise SystemExit(1)


def main() -> int:
    command = secretctl_command() + sys.argv[1:]
    print("+", " ".join(command), flush=True)
    return subprocess.run(command).returncode


if __name__ == "__main__":
    raise SystemExit(main())
