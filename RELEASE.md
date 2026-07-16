# Release Process

Releases are driven by Git tags. A release tag must use SemVer with a leading
`v`, for example:

```text
v1.2.3
v1.2.3-rc.1
```

Build metadata tags such as `v1.2.3+build.1` are not supported because Docker
image tags cannot use `+`.

## Create a Release

1. Make sure the commit to release is on `main`.
2. Create and push a release tag:

```sh
git tag v1.2.3
git push origin v1.2.3
```

Pushing the tag starts the GitHub Actions workflow
`.github/workflows/build-images-on-tag.yaml`.

## What the Workflow Does

The workflow verifies that the tagged commit is reachable from `main`, validates
the tag format, builds all service images, pushes them to GHCR, creates or
updates runtime Kubernetes `Secret` and `ConfigMap` data, applies the release
Kustomize overlay, sets all workload images to the release tag, and waits for
the rollout.

For tag `v1.2.3`, the workflow sets:

```text
APP_VERSION=1.2.3
GIT_COMMIT=<tagged commit sha>
```

Images are tagged with both the original Git tag and the plain app version:

```text
ghcr.io/aet-devops26/team-merge-build-repeat-application:v1.2.3
ghcr.io/aet-devops26/team-merge-build-repeat-application:1.2.3
```

Stable releases also get `latest`. Pre-releases such as `v1.2.3-rc.1` do not.

The Kubernetes deployment uses the plain version tag, for example `1.2.3`, and
waits for the database `StatefulSet`s and application `Deployment`s to roll out.
See [k8s/README.md](k8s/README.md) for the required Kubernetes variables,
secrets, ingress paths, and optional Ollama deployment.

## Manual Docker Host Deployment

The Docker host path is split across two manual GitHub Actions workflows on
`main`:

1. Run `Terraform` to create or update the Azure VM and remote state backed
   infrastructure.
2. Run `Deploy Production` with the Git release tag, for example `v1.2.3`.

`Deploy Production` checks out that Git tag, reads the VM public IP and admin
user from Terraform output, builds a temporary Ansible inventory, and runs
`ansible/playbook.yml` to deploy the tagged production Docker Compose stack to
`/opt/team-merge-build-repeat`. The Docker images use the same release version
without the leading `v`.

Terraform setup and required Azure variables are documented in
[terraform/README.md](terraform/README.md). Production Docker Compose behavior is
documented in [doc/DOCKER.md](/doc/DOCKER.md).

## Runtime Version Info

Spring Boot services expose build information through:

```text
/actuator/info
```

The GenAI service exposes the same style of endpoint:

```text
/actuator/info
```

These endpoints include the release version and the Git commit used for the
build.

Concrete curl commands for local and remote checks are listed in
[doc/HEALTH_AND_INFO.md](doc/HEALTH_AND_INFO.md).
