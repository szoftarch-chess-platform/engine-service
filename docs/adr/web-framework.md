# ES-ADR-3: FastAPI as the web framework

**Related:** ADR-6, ADR-7, ADR-8, [ES-ADR-1](container-image.md), [ES-ADR-2](chess-engine.md)

## Context

The walking skeleton served the health check with the HTTP server of the Python standard library. The move request of ADR-6 needs a JSON body that is validated, errors in the ProblemDetails form of ADR-8, and a Stockfish process that starts and stops with the service (ES-ADR-2).

## Decision

- The service is a FastAPI application, and Uvicorn serves it on the address of `HOST` and the port of `PORT`.
- Pydantic models describe the request and the response. The request ignores the fields that it does not know, as ADR-7 decides for readers.
- Exception handlers turn every error into ProblemDetails in `application/problem+json`, the validation errors of FastAPI included.
- The lifespan of the application starts Stockfish and stops it.
- The tests call the application in memory with the `TestClient` of FastAPI.

## Rationale

- FastAPI validates the request against its Pydantic model, so the service has no parsing code of its own.
- One exception handler returns every error in the same form, which ADR-8 requires.
- The lifespan ties the Stockfish process to the life of the application.
- The `TestClient` tests the HTTP behavior without a server or a port.
- FastAPI and Pydantic are under the MIT license, and Starlette and Uvicorn under the BSD license, so they can be used in the GPL code of ES-ADR-2.

## Rejected alternatives

- **The HTTP server of the standard library:** it needs no dependency, but the service would parse and validate the JSON and route the requests by hand, and it has no lifespan for Stockfish.
- **Flask:** it is widespread, but it validates no request body by itself and needs an extension for that.

## Consequences

- FastAPI answers a validation error with 422 and its own body by default, so the exception handler maps it to the statuses of the contract.
- FastAPI generates an OpenAPI document of the service. It is not the contract, which is `engine-service.openapi.yaml` in the infra repo (ADR-7).

## Sources

- FastAPI: https://fastapi.tiangolo.com/
- FastAPI, handling errors: https://fastapi.tiangolo.com/tutorial/handling-errors/
- FastAPI, lifespan events: https://fastapi.tiangolo.com/advanced/events/
- Uvicorn: https://www.uvicorn.org/
