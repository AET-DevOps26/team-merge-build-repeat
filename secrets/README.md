# Secrets

This directory contains the tracked manifest for local Docker Compose secrets.
Generated secret values stay local and are ignored by Git.

## Important

- Do not commit real secret values to the repository.
- Commit only documentation, examples, and `secret.manifest.toml`.
- The generated `chat_database_password` file must remain local.

The local Compose stack expects these generated files:

- `app_database_password`
- `chat_database_password`

## Creating Secrets

From the repository root, run:

```bash
make secrets
```

This installs `secretctl` if needed and then runs:

```bash
secretctl apply
```

The Makefile auto-detects `python3`, `python`, or the Windows `py` launcher.
You can override it if needed:

```bash
make secrets PYTHON=python
```

For details about the helper scripts, see `../scripts/README.md`.
