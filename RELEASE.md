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
the tag format, builds all service images, and pushes them to GHCR.

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
