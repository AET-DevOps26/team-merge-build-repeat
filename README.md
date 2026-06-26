# Team Merge, Build, Repeat

## Problem Statement

Sudoku learners often know whether a move is right or wrong, but not why.
Many Sudoku applications provide hints or mark mistakes, but they rarely explain the reasoning behind a move or teach the techniques needed to improve over time.

This project addresses that gap by building a Sudoku learning platform with integrated AI support.
The goal is to help users solve puzzles while learning the underlying logic through contextual hints, mistake explanations, and strategy guidance.

## Configuration

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Create the required database password secret with one of these options.

Option 1: create the secret file manually by editing the file.

Option 2: install `secretctl` and generate the secret:

```bash
make secrets
```

The following secret files are expected:

- `secrets/app_database_password`
- `secrets/chat_database_password`
- `secrets/logos_key` when `LLM_PROVIDER=openai` is used

## Run The Project

Docker Compose is split into a shared base file and environment-specific
overrides:

- `docker-compose.yaml` contains the shared service definitions.
- `docker-compose.dev.yaml` is used for local development, exposes services on
  localhost, and can build local images.
- `docker-compose.prod.yaml` is used for production, enables restart policies,
  uses production Caddy ports, and expects production configuration such as
  `DOMAIN`.

Start the local development stack:

```bash
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d --build
```

Start the production stack:

```bash
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d
```

Check the running services:

```bash
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml ps
```

Show logs:

```bash
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml logs -f
```

The `Justfile` can be used as a shorter wrapper around Docker Compose commands:

```bash
just dev up -d --build
just dev ps
just dev logs -f
just dev down
just prod up -d
just prod ps
```

## Stop The Project

Stop the containers while keeping the database volume:

```bash
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml down
```

Stop the containers and delete the local database volume:

```bash
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml down -v
```

Use `down -v` only when you intentionally want to reset the local PostgreSQL data.

## Production Deployment

Infrastructure and application deployment are separated:

- `.github/workflows/terraform.yaml` creates or updates the Azure Docker host.
- `.github/workflows/deploy-prod-ansible.yaml` deploys the Docker Compose stack with Ansible.
- `.github/workflows/build-images-on-tag.yaml` builds release images and deploys
  the Kubernetes stack when a valid release tag is pushed to a commit on `main`.

The production deploy workflow is manual. Run `Deploy Production` from GitHub
Actions on `main` and provide the image tag, for example `v1.2.3`. The workflow
normalizes the tag to `1.2.3`, reads the VM public IP from Terraform output, and
deploys the Compose stack to `/opt/team-merge-build-repeat`.

For Kubernetes deployment, create and push a release tag on `main`. The tag
workflow verifies that the tagged commit is reachable from `main`, builds all
service images, creates/updates `app-secrets` and `app-config` in the
`merge-build-repeat` namespace, applies `k8s/kustomization.yaml`, sets the
workload images to the release tag, and waits for the rollout.

Configure these GitHub repository or `production` environment variables:

| Variable                       | Value                                      |
| ------------------------------ | ------------------------------------------ |
| `DOMAIN`                       | Production domain used by Caddy            |
| `APP_DATABASE_NAME`            | Application database name                  |
| `APP_DATABASE_USER`            | Application database user                  |
| `CHAT_DATABASE_NAME`           | Chat database name                         |
| `CHAT_DATABASE_USER`           | Chat database user                         |
| `CHAT_DATABASE_SPRING_PROFILE` | Spring profile for the chat service        |
| `AZURE_CLIENT_ID`              | Azure app registration client ID           |
| `AZURE_TENANT_ID`              | Azure tenant ID                            |
| `AZURE_SUBSCRIPTION_ID`        | Azure subscription ID                      |
| `TF_STATE_RESOURCE_GROUP`      | Resource group containing Terraform state  |
| `TF_STATE_STORAGE_ACCOUNT`     | Storage account containing Terraform state |
| `TF_STATE_CONTAINER`           | Blob container containing Terraform state  |
| `TF_VAR_ssh_public_key`        | Public SSH key allowed on the VM           |
| `TF_VAR_ssh_source_address_prefix` | SSH source prefix for the VM NSG       |

Configure these GitHub secrets:

| Secret                   | Value                                      |
| ------------------------ | ------------------------------------------ |
| `ANSIBLE_SSH_PRIVATE_KEY` | Private key matching `TF_VAR_ssh_public_key` |
| `KUBE_CONFIG`            | Kubeconfig content for Kubernetes deployment |
| `APP_DATABASE_PASSWORD`  | Application PostgreSQL password            |
| `CHAT_DATABASE_PASSWORD` | Chat PostgreSQL password                   |
| `LOGOS_KEY`              | Logos/OpenAI API key                       |

## Health Checks

Check the application health endpoints:

```bash
curl http://127.0.0.1:8083/actuator/health
```

The default local endpoints are:

- Chat database service: `http://127.0.0.1:8083`
- Application service: `http://127.0.0.1:8081`
- PostgreSQL chat database: `http://127.0.0.1:5431`
- PostgreSQL application: `http://127.0.0.1:5432`
- Frontend service: `http://127.0.0.1:8090`
