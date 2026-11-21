# ES-ADR-1: Container image on Debian slim

**Related:** NF-9, ADR-2, ADR-6

## Context

The service runs as a container image, which the CI and the compose of the infra repo build.

## Decision

- The `Dockerfile` starts from `python:3.14-slim` and installs Stockfish and the packages of `requirements.txt`.
- The image sets `STOCKFISH_PATH=/usr/games/stockfish`.
- The service runs as the non-root user `nobody`.
- The image sets no port. The service listens on the port of the required `PORT` environment variable.
- The image has no `HEALTHCHECK`. The compose of the infra repo checks `GET /health`.

## Rationale

- Debian slim supports the Stockfish package used by this service.
- Python 3.14 has had a year of fixes. 3.15 is the newest release, and the first release of a new version is too fresh to build on.
- The tag follows the patch releases of 3.14, so fixes arrive without a change.

## Rejected alternatives

- **`python:3.14-alpine`:** the smaller image was reconsidered because it does not provide Stockfish through its package repositories.

## Consequences

- Python does not handle SIGTERM when it runs as process 1, so the container needs an init process to stop at once. The compose of the infra repo sets `init: true`, and `docker run` needs `--init`.
- Python buffers its output when it does not write to a terminal, so the image sets `PYTHONUNBUFFERED`.

## Sources

- Official python image: https://hub.docker.com/_/python
- `docker run --init`: https://docs.docker.com/reference/cli/docker/container/run/
