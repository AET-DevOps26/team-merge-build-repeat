#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import platform
from pathlib import Path
import shutil
import subprocess
import sys
from textwrap import dedent


SECRETCTL_PACKAGE = "secretctl"
SECRETCTL_SPEC = "git+https://github.com/DarkbreakerDE/secretctl.git@v0.1.2"
PIPX_MODULE_CMD = [sys.executable, "-m", "pipx"]


def user_data_dir() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local"
        return Path(base) / "secretctl-installer"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "secretctl-installer"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "secretctl-installer"


PIPX_BOOTSTRAP_VENV = user_data_dir() / "pipx-venv"
PIPX_BOOTSTRAP_PYTHON = (
    PIPX_BOOTSTRAP_VENV / "Scripts" / "python.exe"
    if sys.platform == "win32"
    else PIPX_BOOTSTRAP_VENV / "bin" / "python"
)
PIPX_BOOTSTRAP_MODULE_CMD = [str(PIPX_BOOTSTRAP_PYTHON), "-m", "pipx"]


def run(
    command: list[str], *, capture: bool = False, check: bool = True
) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(command), flush=True)
    return subprocess.run(
        command,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def can_run(command: list[str]) -> bool:
    return (
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def version_or_missing(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except OSError as error:
        return f"missing ({error})"

    output = (result.stdout or "").strip().splitlines()
    suffix = output[0] if output else f"exit code {result.returncode}"
    return suffix if result.returncode == 0 else f"failed: {suffix}"


def print_diagnostics() -> None:
    pipx_command_for_version = pipx_command_or_none()
    pipx_version = (
        version_or_missing(pipx_command_for_version + ["--version"])
        if pipx_command_for_version
        else "missing"
    )

    print("Diagnostics:")
    print(f"  platform: {platform.platform()}")
    print(f"  python:   {sys.executable}")
    print(f"  version:  {sys.version.split()[0]}")
    print(f"  pip:      {version_or_missing([sys.executable, '-m', 'pip', '--version'])}")
    print(f"  pipx:     {pipx_version}")
    print(f"  git:      {version_or_missing(['git', '--version'])}")
    print(f"  PATH:     {os.environ.get('PATH', '')}")
    print()
    sys.stdout.flush()


def print_pipx_install_help() -> None:
    print(
        dedent(
            """
            Could not bootstrap pipx automatically.

            Install pipx manually, or make sure Python can create virtual environments,
            then run this script again:
              Windows:      py -m pip install --user pipx
              macOS:        brew install pipx
              Arch:         sudo pacman -S python-pipx
              Debian/Ubuntu sudo apt install pipx python3-venv

            Then ensure pipx is on PATH:
              python -m pipx ensurepath
            """
        ).strip()
    )


def ensure_pipx() -> None:
    if pipx_command_or_none() is not None:
        print("pipx is already installed.")
        return

    print(f"pipx not found. Bootstrapping pipx in {PIPX_BOOTSTRAP_VENV}...")
    try:
        run([sys.executable, "-m", "venv", str(PIPX_BOOTSTRAP_VENV)])
        run([str(PIPX_BOOTSTRAP_PYTHON), "-m", "pip", "install", "--upgrade", "pipx"])
    except subprocess.CalledProcessError:
        print_pipx_install_help()
        raise

    run(PIPX_BOOTSTRAP_MODULE_CMD + ["ensurepath"], check=False)


def ensure_git() -> None:
    if command_exists("git"):
        return

    print(
        dedent(
            """
            git is required because secretctl is installed from GitHub.

            Install git and run this script again:
              Windows:      winget install --id Git.Git -e
              macOS:        xcode-select --install
              Debian/Ubuntu sudo apt install git
            """
        ).strip()
    )
    raise SystemExit(1)


def pipx_command_or_none() -> list[str] | None:
    if can_run(PIPX_MODULE_CMD + ["--version"]):
        return PIPX_MODULE_CMD
    if command_exists("pipx"):
        return ["pipx"]
    if PIPX_BOOTSTRAP_PYTHON.exists() and can_run(PIPX_BOOTSTRAP_MODULE_CMD + ["--version"]):
        return PIPX_BOOTSTRAP_MODULE_CMD
    return None


def pipx_command() -> list[str]:
    command = pipx_command_or_none()
    if command is not None:
        return command
    raise RuntimeError("pipx is not available")


def is_secretctl_installed() -> bool:
    try:
        result = run(pipx_command() + ["list", "--json"], capture=True)
    except subprocess.CalledProcessError:
        return False

    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return False

    return SECRETCTL_PACKAGE in data.get("venvs", {})


def install_secretctl(*, force: bool = False) -> None:
    command = pipx_command()

    if is_secretctl_installed():
        if not force:
            print(f"{SECRETCTL_PACKAGE} is already installed.")
            return
        print(f"{SECRETCTL_PACKAGE} is already installed. Reinstalling pinned version...")
        run(command + ["uninstall", SECRETCTL_PACKAGE], check=False)

    print(f"Installing {SECRETCTL_PACKAGE}...")
    result = run(command + ["install", SECRETCTL_SPEC], check=False)
    if result.returncode == 0:
        return

    print()
    print("Initial install failed. Removing any existing pipx venv and retrying once...")
    run(command + ["uninstall", SECRETCTL_PACKAGE], check=False)
    run(command + ["install", SECRETCTL_SPEC])


def ensure_pipx_path() -> None:
    run(pipx_command() + ["ensurepath"], check=False)


def main() -> int:
    force = "--force" in sys.argv[1:]
    print_diagnostics()
    ensure_pipx()
    ensure_git()
    install_secretctl(force=force)
    ensure_pipx_path()

    print()
    print("Setup complete.")
    print("Test with:")
    print("  secretctl --help")
    print()
    print("If 'secretctl' is not found, restart your terminal or run:")
    print("  python -m pipx ensurepath")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
