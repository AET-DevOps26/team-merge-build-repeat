# Scripts

Small helper scripts for local project setup.

- `find-python.py`: finds a Python 3.10+ command for the Makefile.
- `install-secretctl.py`: installs `secretctl` with `pipx`; if `pipx` is missing, it bootstraps an isolated pipx venv in the user's data directory.
- `run-secretctl.py`: runs `secretctl`, including immediately after installation when the pipx bin directory is not yet on `PATH`.

Common usage from the repository root:

```bash
make secrets
```

This installs `secretctl` if needed and runs `secretctl apply`.
