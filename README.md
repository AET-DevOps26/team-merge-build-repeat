# Team Merge, Build, Repeat

## Problem Statement

Sudoku learners often know whether a move is right or wrong, but not why.
Many Sudoku applications provide hints or mark mistakes, but they rarely explain the reasoning behind a move or teach the techniques needed to improve over time.

This project addresses that gap by building a Sudoku learning platform with integrated AI support.
The goal is to help users solve puzzles while learning the underlying logic through contextual hints, mistake explanations, and strategy guidance.

## Documentation

### Local Deployment

For a local deployment, use the Docker Compose based setup described in
[doc/DOCKER.md](/doc/DOCKER.md). That guide explains the development compose
files, the `just` wrapper commands, service profiles, and local LLM selection.

### Ansible Deployment

The Ansible deployment runs the production Docker Compose stack on a dedicated
Docker host. Details about this deployment path are documented in
[ansible/README.md](ansible/README.md), and the current deployment is available
at `http://20.91.243.185/`.

### Kubernetes Deployment

The Kubernetes deployment runs the application stack in the
`merge-build-repeat` namespace using the manifests in `k8s/`. Details about the
Kubernetes deployment path are documented in [k8s/README.md](k8s/README.md), and
the current deployment is available at `http://131.159.88.14/`.

## Additional Documentation

- Local secrets: [secrets/README.md](secrets/README.md)
- Docker Compose, `just`, profiles, and LLM selection: [doc/DOCKER.md](/doc/DOCKER.md)
- Release and deployment paths: [RELEASE.md](RELEASE.md)
- Terraform Docker host details: [terraform/README.md](terraform/README.md)
- Health and info checks: [doc/HEALTH_AND_INFO.md](doc/HEALTH_AND_INFO.md)
- API docs and Swagger endpoints: [doc/API_DOCS.md](doc/API_DOCS.md)
