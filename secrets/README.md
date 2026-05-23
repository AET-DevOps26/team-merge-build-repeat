# Secrets

This directory is used for local Docker Compose secrets.

## Important

- Do not commit real secret values to the repository.
- Keep generated secret files local.
- Commit only documentation, examples, or manifests that do not contain sensitive values.

The local Compose stack expects these generated files:

- `app_database_password`
- `chat_database_password`

## Creating Secrets

Secrets can be generated with `secretctl`:

```bash
secretctl
```

Project: https://github.com/DarkbreakerDE/secretctl
