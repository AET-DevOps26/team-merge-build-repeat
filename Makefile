# Pick a Python 3.10+ command automatically, while still allowing overrides like:
#   make secrets PYTHON=python
PYTHON ?= $(shell python3 scripts/find-python.py 2>/dev/null || python scripts/find-python.py 2>/dev/null || py -3 scripts/find-python.py 2>NUL || py scripts/find-python.py 2>NUL)

# Fail early with a readable error if no supported Python interpreter is available.
ifeq ($(strip $(PYTHON)),)
$(error No Python 3.10+ interpreter found. Install Python 3 or run `make secrets PYTHON=<command>`)
endif

.PHONY: secrets secretctl-install secretctl-apply

# Install secretctl if needed, then create or update local secret files.
secrets: secretctl-install secretctl-apply

# Installs secretctl through the cross-platform Python installer script.
secretctl-install:
	$(PYTHON) scripts/install-secretctl.py

# Runs `secretctl apply`; the wrapper also works before pipx's bin dir is on PATH.
secretctl-apply:
	$(PYTHON) scripts/run-secretctl.py apply
