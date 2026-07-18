# Team Merge, Build, Repeat

## Problem Statement

Sudoku learners often know whether a move is right or wrong, but not why.
Many Sudoku applications provide hints or mark mistakes, but they rarely explain the reasoning behind a move or teach the techniques needed to improve over time.

This project addresses that gap by building a Sudoku learning platform with integrated AI support.
The goal is to help users solve puzzles while learning the underlying logic through contextual hints, mistake explanations, and strategy guidance.

![Sudoku AI application](doc/pictures/Sudoku%20AI.png)

## Quick Start

Clone the repository:

```bash
git clone git@github.com:AET-DevOps26/team-merge-build-repeat.git
cd team-merge-build-repeat
```

### Kubernetes Deployment

The Kubernetes deployment is available at [http://131.159.88.14/](http://131.159.88.14/).

### Azure Deployment

The Azure deployment is available at [http://20.91.217.55/](http://20.91.217.55/).

> The Azure public IP address is not persistent. After `terraform destroy` and a subsequent Terraform deployment, Azure may assign a different IP address. Update this URL accordingly.

### Local Deployment

Start the local stack with OpenAI as the LLM provider:

```bash
LLM_PROVIDER=openai docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build
```

In a separate terminal, inspect the running services:

```bash
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml ps
```

Stop the stack when finished:

```bash
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml down
```

To use a local Ollama model instead, set `LLM_PROVIDER=ollama` and enable the `local-llm` profile:

```bash
LLM_PROVIDER=ollama docker compose --profile local-llm -f docker-compose.yaml -f docker-compose.dev.yaml up --build
```

## Using Sudoku AI

1. Create an account or sign in with your email address.
2. On the home page, start an easy, medium, or hard Sudoku, continue your most recent game, or start from a template. The template ID is shown while a game is in progress.
3. The game page is divided into three areas: the AI assistant chat on the left, the Sudoku board in the centre, and the input controls on the right. You can ask the AI assistant for advice at any time; it provides well-founded answers and guidance for the current puzzle.
4. To enter a number, select a cell and then select a number. Ensure that the pencil button at the top of the input controls is blue; this indicates normal number-entry mode.
5. Toggle the pencil button to enter pencil-mark mode. In this mode, selecting a number toggles that note in the selected cell. In normal number-entry mode, a number is set rather than toggled. Use the red remove button to clear a cell.
6. Use Undo and Redo to navigate recent changes. The game also provides a partial correctness check and a Reveal Solution option.
7. The Game History in the lower-left corner lists all started games and allows them to be resumed. Completed games are marked as **Finished**.

## Deployment

Deployments are managed through GitHub Actions.

### Kubernetes

Pushing a version tag on `main` triggers the Kubernetes deployment. Tags must match the `v*` pattern and use semantic versioning, for example:

```bash
git checkout main
git tag v1.2.3
git push origin v1.2.3
```

### Azure with Ansible

The Azure Docker Compose deployment is triggered manually from the **Deploy Production** GitHub Action. A Terraform-managed virtual machine must already be running before this workflow is started. Provide the release tag, for example `v1.2.3`, when dispatching the workflow.

The Terraform provision and destroy workflows can also be started manually from GitHub Actions. Use them to create or remove the Azure virtual machine as required.

## Operations and Monitoring

### Health, Version, and API Documentation

For Kubernetes and Azure, replace `<base-url>` with the current deployment URL. Services are addressed by the base URL followed by their service path.

| Service     | Health                                   | Release information                    | API documentation                              |
| ----------- | ---------------------------------------- | -------------------------------------- | ---------------------------------------------- |
| Application | `<base-url>/application/actuator/health` | `<base-url>/application/actuator/info` | `<base-url>/application/swagger-ui/index.html` |
| Chat        | `<base-url>/chat/actuator/health`        | `<base-url>/chat/actuator/info`        | `<base-url>/chat/swagger-ui/index.html`        |
| GenAI       | `<base-url>/genai/actuator/health`       | `<base-url>/genai/actuator/info`       | `<base-url>/genai/docs`                        |
| Game Engine | `<base-url>/game-engine/actuator/health` | `<base-url>/game-engine/actuator/info` | `<base-url>/game-engine/docs`                  |

Grafana is available at `<base-url>/grafana`. The default credentials are `admin` / `admin`.

### Alerting

An alert is raised when a service is down. To test this alert, deliberately stop the Chat service in a suitable non-production environment, for example by stopping its Docker Compose container or scaling its Kubernetes deployment down, and then verify the alert in Grafana.

## Further Documentation

- [Docker Compose and LLM configuration](doc/DOCKER.md)
- [Ansible deployment](ansible/README.md)
- [Kubernetes deployment](k8s/README.md)
- [Terraform Azure host](terraform/README.md)
- [Health and info checks](doc/HEALTH_AND_INFO.md)
- [API documentation](doc/API_DOCS.md)
- [Release process](RELEASE.md)
