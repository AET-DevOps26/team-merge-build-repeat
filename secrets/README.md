# Local Secrets

This directory contains the tracked manifest for local Docker Compose secrets.
Generated secret values stay local and are ignored by Git.

## Required Files

The local Compose stack reads these files from `secrets/` by default:

| File | Required when | Purpose |
| --- | --- | --- |
| `app_database_password` | Always | PostgreSQL password for the application database |
| `chat_database_password` | Always | PostgreSQL password for the chat database |
| `logos_key` | `LLM_PROVIDER=openai` | Logos/OpenAI-compatible API key |

The file paths can be overridden in `.env` with
`APP_DATABASE_PASSWORD_FILE`, `CHAT_DATABASE_PASSWORD_FILE`, and
`LOGOS_KEY_FILE`.

## Create Local Secrets

From the repository root:

```bash
make secrets
```

This installs `secretctl` if needed and applies `secrets/secret.manifest.toml`.
For details about the helper scripts, see [scripts/README.md](../scripts/README.md).

When using OpenAI/Logos locally, create the API key file manually:

```bash
printf '%s\n' 'lg-...' > secrets/logos_key
```

Do not commit generated secret files or real secret values.
