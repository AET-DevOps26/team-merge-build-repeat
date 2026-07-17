# Docker Compose

Docker Compose is split into a shared base file and environment-specific
overrides:

| File | Purpose |
| --- | --- |
| `docker-compose.yaml` | Shared service definitions, images, secrets, volumes, and health checks |
| `docker-compose.dev.yaml` | Local builds and localhost port mappings |
| `docker-compose.prod.yaml` | Production settings, restart policies, public Caddy ports, and `DOMAIN` |

## Just Wrapper

`Justfile` shortens repeated Docker Compose commands. It forwards all arguments
to Docker Compose with the right file set:

```bash
just dev up -d --build
just dev ps
just dev logs -f
just dev down

just prod up -d
just prod ps
```

Equivalent explicit local command:

```bash
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d --build
```

## Profiles

Profiles enable optional services:

| Profile | Service | Use when |
| --- | --- | --- |
| `local-llm` | `ollama` | GenAI should use a local Ollama model |
| `proxy` | `caddy` | The stack should be reached through the Caddy reverse proxy |
| `dev` | `frontend-dev` | Vite dev server should run instead of only the built frontend |

Examples:

```bash
COMPOSE_PROFILES=local-llm just dev up -d --build
COMPOSE_PROFILES=proxy just dev up -d --build
COMPOSE_PROFILES=dev just dev up -d --build

docker compose --profile local-llm -f docker-compose.yaml -f docker-compose.dev.yaml up -d --build
docker compose --profile proxy -f docker-compose.yaml -f docker-compose.dev.yaml up -d --build
docker compose --profile dev -f docker-compose.yaml -f docker-compose.dev.yaml up -d --build
```

## LLM Selection

Local Ollama:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3:4b
```

Start with the `local-llm` profile so the `ollama` service exists.

OpenAI/Logos:

```env
LLM_PROVIDER=openai
OPENAI_BASE_URL=https://logos.aet.cit.tum.de:8080/v1
OPENAI_MODEL=openai/gpt-oss-120b
```

Also create `secrets/logos_key`; see [secrets/README.md](../secrets/README.md).
