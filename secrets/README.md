# Secrets

This directory contains the tracked manifest for local Docker Compose secrets.
Generated secret values stay local and are ignored by Git.

## Important

- Do not commit real secret values to the repository.
- Commit only documentation, examples, and `secret.manifest.toml`.
- The generated `chat_database_password` file must remain local.
- The `logos_key` file must contain your real `lg-...` Logos key and must
  remain local.

The local Compose stack expects these secret files:

- `app_database_password`
- `chat_database_password`
- `logos_key` when `LLM_PROVIDER=openai` is used

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

Create the Logos key manually when you want to use Logos:

```bash
printf '%s\n' 'lg-...' > secrets/logos_key
```

For details about the helper scripts, see `../scripts/README.md`.
