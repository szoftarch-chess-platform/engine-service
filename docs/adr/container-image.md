# ES-ADR-1: Container image on Alpine

**Related:** NF-9, ADR-2, ADR-6

## Context

The service runs as a container image, which the CI and the compose of the infra repo build.

## Decision

- The `Dockerfile` starts from `python:3.14-alpine` and installs the packages of `requirements.txt` in a separate layer.
- The service runs as the non-root user `nobody`.
- The image sets no port. The service listens on the port of the required `PORT` environment variable.
- The image has no `HEALTHCHECK`. The compose of the infra repo checks `GET /health`.

## Rationale

- Alpine gives the smallest image, and most other images of the system are built on Alpine too.
- Python 3.14 has had a year of fixes. 3.15 is the newest release, and the first release of a new version is too fresh to build on.
- The tag follows the patch releases of 3.14, so fixes arrive without a change.

## Rejected alternatives

- **`python:3.14-slim`:** the Debian-based image is larger. It becomes the better choice if the service needs a native package that has no wheel for Alpine, and switching to it is a change of one line.

## Consequences

- Python does not handle SIGTERM when it runs as process 1, so the container needs an init process to stop at once. The compose of the infra repo sets `init: true`, and `docker run` needs `--init`.
- Python buffers its output when it does not write to a terminal, so the image sets `PYTHONUNBUFFERED`.

## Sources

- Official python image: https://hub.docker.com/_/python
- `docker run --init`: https://docs.docker.com/reference/cli/docker/container/run/
