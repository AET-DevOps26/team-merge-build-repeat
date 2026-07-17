# Kubernetes Deployment

The standard Kubernetes deployment mirrors the production Docker Compose stack
used by Ansible:

- GHCR images for `frontend`, `application`, `chat`, `genai`, and `game-engine`
- PostgreSQL `StatefulSet`s for the application and chat databases
- PostgreSQL exporters, Prometheus, and Grafana with persistent data volumes
- Init containers that wait for PostgreSQL before starting the dependent
  Spring services
- Kubernetes `Secret` data for database passwords and the Logos/OpenAI key
- Kubernetes `ConfigMap` data for the non-secret runtime configuration
- NGINX Ingress routing for `/`, `/game-engine`, `/genai`, `/application`,
  `/chat`, and `/grafana`
- Hostless HTTP Ingress rules so the stack is reachable through the ingress
  controller IP before a domain exists

The manifests target the `merge-build-repeat` namespace. The deployment
workflow attempts to apply `k8s/base/namespace.yaml`, but the main rendered
Kustomize output does not include the namespace object so namespace-scoped
deployment credentials can be used when the namespace already exists.

Kubernetes production uses Logos/OpenAI. Ollama is available only in the local
Docker Compose development configuration.

For release flow details, see [../RELEASE.md](../RELEASE.md). For API and health
URLs exposed through the ingress, see
[../doc/API_DOCS.md](../doc/API_DOCS.md) and
[../doc/HEALTH_AND_INFO.md](../doc/HEALTH_AND_INFO.md).

## Startup Dependencies

Kubernetes does not provide Docker Compose style `depends_on` ordering. The
manifests handle the database startup dependency explicitly:

- `application` waits for `application-database` with `pg_isready`
- `chat` waits for `chat-database` with `pg_isready`

All workloads still define readiness probes so Services and Ingress route only
to ready Pods after startup.

## GitHub Actions Deployment

Pushing a SemVer tag such as `v1.2.3` to a commit reachable from `main` runs
`.github/workflows/build-images-on-tag.yaml`. After all service images are built
and pushed, the same workflow deploys the Kubernetes manifests with the plain
image tag, for example `1.2.3`.

Required production environment variables:

| Variable | Default |
| --- | --- |
| `APP_DATABASE_NAME` | `game_database` |
| `APP_DATABASE_USER` | `app_user` |
| `CHAT_DATABASE_NAME` | `chat_database` |
| `CHAT_DATABASE_USER` | `chat_user` |
| `CHAT_DATABASE_SPRING_PROFILE` | `docker` |
| `APPLICATION_CONTEXT_PATH` | `/application` |
| `CHAT_CONTEXT_PATH` | `/chat` |
| `GENAI_ROOT_PATH` | `/genai` |
| `GAME_ENGINE_ROOT_PATH` | `/game-engine` |
| `OPENAI_BASE_URL` | `https://logos.aet.cit.tum.de:8080/v1` |
| `OPENAI_MODEL` | `openai/gpt-oss-120b` |
| `PUBLIC_IP_ADDR` | Detected automatically from the frontend Ingress |
| `SUPABASE_AUTH_ISSUER` | `https://pwjnldzqwwagnxjycfaq.supabase.co/auth/v1` |
| `SUPABASE_AUTH_JWKS_URI` | `https://pwjnldzqwwagnxjycfaq.supabase.co/auth/v1/.well-known/jwks.json` |
| `VITE_SUPABASE_URL` | `https://pwjnldzqwwagnxjycfaq.supabase.co` |
| `VITE_SUPABASE_PUBLISHABLE_KEY` | `sb_publishable_ILaMZuzBfV5NOnKfCQdJJQ_ESpvjbBt` |

Required production secrets:

| Secret | Description |
| --- | --- |
| `KUBE_CONFIG` | Kubeconfig content for the target cluster |
| `APP_DATABASE_PASSWORD` | Application PostgreSQL password |
| `CHAT_DATABASE_PASSWORD` | Chat PostgreSQL password |
| `LOGOS_KEY` | Logos/OpenAI API key |

The GenAI workload uses Logos/OpenAI in Kubernetes production.

Render the standard manifests locally with:

```sh
kubectl kustomize k8s
```

The local root kustomization renders application images with `latest`. The
production GitHub Actions workflow renders `k8s/overlays/release` and replaces
`RELEASE_TAG` with the SemVer tag before applying manifests, so production never
deploys `latest`.
