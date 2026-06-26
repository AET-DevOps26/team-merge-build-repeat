# Ansible Deployment

The Ansible deployment is the Docker host production path for Team Merge Build
Repeat. It installs the production Docker Compose stack on a remote host and is
intended to run after Terraform has provisioned the VM.

The playbook deploys:

- GHCR images for `caddy`, `frontend`, `application`, `chat`, `genai`,
  `ollama`, and `game-engine`
- PostgreSQL containers for the application and chat databases
- The shared `docker-compose.yaml` file plus the production override
  `docker-compose.prod.yaml`
- A rendered `.env` file with non-secret runtime configuration
- Docker Compose secret files for database passwords and the Logos/OpenAI key
- The stack under `/opt/team-merge-build-repeat`

For release flow details, see [../RELEASE.md](../RELEASE.md). Production Docker
Compose behavior is documented in [../doc/DOCKER.md](../doc/DOCKER.md). For API
and health URLs, see [../doc/API_DOCS.md](../doc/API_DOCS.md) and
[../doc/HEALTH_AND_INFO.md](../doc/HEALTH_AND_INFO.md).

## Deployment Flow

`ansible/playbook.yml` targets the `docker_hosts` inventory group. The playbook:

- Waits for SSH to become available
- Validates required deployment variables and secrets
- Creates `/opt/team-merge-build-repeat` and its `secrets/` directory
- Copies the Docker Compose files to the target host
- Renders `templates/prod.env.j2` to `/opt/team-merge-build-repeat/.env`
- Writes production secret files below `/opt/team-merge-build-repeat/secrets`
- Pulls the requested production images
- Starts the stack with `docker compose up -d --remove-orphans --force-recreate`
- Prints `docker compose ps`

The target host must already have Docker and Docker Compose available. Terraform
is responsible for provisioning that host in the standard production workflow.

## GitHub Actions Deployment

The manual workflow `.github/workflows/deploy-prod-ansible.yaml` deploys the
Docker host stack from `main`.

Run `Terraform` first to create or update the Azure VM and remote state backed
infrastructure. Then run `Deploy Production` with an image tag such as:

```text
v1.2.3
1.2.3
v1.2.3-rc.1
1.2.3-rc.1
```

The workflow normalizes a leading `v` away before passing `IMAGE_TAG` to
Ansible, so `v1.2.3` deploys images tagged `1.2.3`. It reads the VM public IP
and admin username from Terraform output, builds a temporary inventory, installs
`ansible-core`, configures the SSH key, and runs:

```sh
ansible-playbook -i inventory.ini ansible/playbook.yml
```

## Configuration

Defaults are defined in `group_vars/docker_hosts.yml` and are read from
environment variables. Required values without defaults are validated by the
playbook.

Required production environment variables:

| Variable | Default |
| --- | --- |
| `DOMAIN` | Required |
| `IMAGE_TAG` | Required |
| `APP_DATABASE_NAME` | `game_database` |
| `APP_DATABASE_USER` | `app_user` |
| `CHAT_DATABASE_NAME` | `chat_database` |
| `CHAT_DATABASE_USER` | `chat_user` |
| `CHAT_DATABASE_SPRING_PROFILE` | `docker` |
| `APPLICATION_CONTEXT_PATH` | `/application` |
| `CHAT_CONTEXT_PATH` | `/chat` |
| `LLM_PROVIDER` | `openai` |
| `GENAI_ROOT_PATH` | `/genai` |
| `GAME_ENGINE_ROOT_PATH` | `/game-engine` |

Required production secrets:

| Secret | Description |
| --- | --- |
| `ANSIBLE_SSH_PRIVATE_KEY` | SSH private key used by the workflow to connect to the VM |
| `APP_DATABASE_PASSWORD` | Application PostgreSQL password |
| `CHAT_DATABASE_PASSWORD` | Chat PostgreSQL password |
| `LOGOS_KEY` | Logos/OpenAI API key |

The GitHub Actions workflow also needs the Terraform and Azure variables
documented in [../terraform/README.md](../terraform/README.md), because it reads
the target host connection data from Terraform state.

Set `LLM_PROVIDER=openai` for the default production path. Use
`LLM_PROVIDER=ollama` only when the Docker host should run the Ollama container
and the GenAI service should call it.

## Manual Run

For a local manual deployment, create an inventory with a `docker_hosts` group:

```ini
[docker_hosts]
docker-host ansible_host=<public-ip> ansible_user=<admin-user> ansible_ssh_private_key_file=~/.ssh/ansible_deploy_key ansible_python_interpreter=/usr/bin/python3
```

Export the required variables and run:

```sh
export DOMAIN=example.com
export IMAGE_TAG=1.2.3
export APP_DATABASE_PASSWORD='...'
export CHAT_DATABASE_PASSWORD='...'
export LOGOS_KEY='...'

ansible-playbook -i inventory.ini ansible/playbook.yml
```

After deployment, inspect the remote stack with:

```sh
ssh <admin-user>@<public-ip>
cd /opt/team-merge-build-repeat
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml ps
```
