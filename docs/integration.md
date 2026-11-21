# Engine service integration

## Purpose

The engine service recommends a move for a chess position. It is an internal synchronous service used only by the game service, as decided in ADR-6.

The engine service does not own the game state. The game service supplies the current position, validates that the returned move belongs to the position, and applies the move to the game.

## Network

In Docker Compose, the game service calls:

```text
http://engine-service:8000
```

The `engine` network is internal. The engine service has no route from the API gateway.

## Move request

```http
POST /move
Content-Type: application/json
```

```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "variant": "standard"
}
```

`variant` is optional and defaults to `standard`. Unsupported variants are rejected by request validation.

## Move response

```http
200 OK
Content-Type: application/json
```

```json
{
  "move": "e2e4"
}
```

The move is in UCI notation. A legal move in a starting position might be `e2e4`, but Stockfish can return another valid move.

## Health request

```http
GET /health
```

The successful response is plain text:

```text
healthy
```

## Error responses

| Status | Meaning |
|---|---|
| `400 Bad Request` | The FEN is malformed or the chess position is invalid |
| `409 Conflict` | The position is terminal and has no move |
| `422 Unprocessable Content` | The request fields fail validation |
| `503 Service Unavailable` | Stockfish is unavailable or cannot calculate a move |

## Configuration

| Environment variable | Required | Description |
|---|---|---|
| `PORT` | yes | HTTP listening port |
| `STOCKFISH_PATH` | yes | executable path |
| `STOCKFISH_DEPTH` | no | Stockfish search depth, default `10` |

The container sets `STOCKFISH_PATH=/usr/games/stockfish`.

## Caller behavior

The game service should apply the following rules:

1. Generate FEN from the authoritative game state.
2. Send `POST /move` with `variant: "standard"`.
3. Apply a request timeout.
4. Repeat a failed request once.
5. Treat a 400 or 422 response as an invalid local game state.
6. Treat 409 as a terminal game.
7. Treat 503 as an unavailable engine and use the service's normal game error handling.
8. Validate the returned UCI move against the position before applying it.

The OpenAPI description in the `infra` repository is the cross-repository contract. ADR-6 remains the authority for the communication decision.

## Automated validation

The GitHub Actions workflow installs Stockfish, runs unit and real-engine tests,
builds the Docker image and starts the container for an HTTP smoke test.
The smoke test verifies `/health` and a real `POST /move` response for the
starting position.
