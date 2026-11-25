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
The engine wait is bounded so the complete request stays below the 10-second contract limit.

## Move request

```http
POST /moves
Content-Type: application/json
```

```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "variant": "standard"
}
```

`variant` is optional and defaults to `standard`. Unknown fields are ignored.

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
| `400 Bad Request` | The request or FEN is malformed or invalid |
| `422 Unprocessable Content` | The variant is unsupported or the position has no legal move |
| `500 Internal Server Error` | Stockfish fails or is unavailable |

Errors use `application/problem+json` and the RFC 9457 Problem Details fields
`title`, `status` and `detail`.

## Configuration

| Environment variable | Required | Description |
|---|---|---|
| `PORT` | yes | HTTP listening port |
| `HOST` | yes | HTTP listening address, `127.0.0.1` on the host and `0.0.0.0` in a container |
| `STOCKFISH_PATH` | yes | executable path |
| `STOCKFISH_DEPTH` | no | Stockfish search depth, default `10` |

The container sets `STOCKFISH_PATH=/usr/games/stockfish`.

## Caller behavior

The game service should apply the following rules:

1. Generate FEN from the authoritative game state.
2. Send `POST /moves` with `fen` and, optionally, `variant: "standard"`.
3. Apply a request timeout.
4. Repeat a request once when it fails with 500 or gets no answer in time.
5. Treat a 400 response as an invalid local request or game state.
6. Treat 422 as an unsupported variant or terminal position.
7. Treat 500 as an unavailable engine and use the service's normal game error handling.
8. Validate the returned UCI move against the position before applying it.

The OpenAPI description in the `infra` repository is the cross-repository contract. ADR-6 remains the authority for the communication decision.

## Automated validation

The GitHub Actions workflow installs Stockfish, runs unit and real-engine tests,
builds the Docker image and starts the container for an HTTP smoke test.
The smoke test verifies `/health` and a real `POST /moves` response for the
starting position.
