# engine-service

Engine service of the online chess platform. Its responsibilities are decided in ADR-1.

## Current status
- Health check endpoint implemented.
- FEN validation and Stockfish move recommendations implemented.
- Real-engine tests and container smoke testing implemented in CI.

## Configuration

| Environment variable | Required | Description |
|---|---|---|
| `PORT` | yes | port that the service listens on |
| `HOST` | yes | address that the service listens on, `127.0.0.1` on the host and `0.0.0.0` in a container |
| `STOCKFISH_PATH` | yes | path to the Stockfish executable |
| `STOCKFISH_DEPTH` | no | search depth, default `10` |

## Run
```bash
PORT=8000 HOST=127.0.0.1 STOCKFISH_PATH=/path/to/stockfish python -m engine_service.main
```

In PowerShell:
```powershell
$env:PORT = 8000
$env:HOST = '127.0.0.1'
$env:STOCKFISH_PATH = "C:\path\to\stockfish.exe"
$env:STOCKFISH_DEPTH = 10
python -m engine_service.main
```

The development compose of the infra repo publishes its engine-service on the same port. If it runs, stop that container first in the infra folder with `docker compose stop engine-service`.

## Health check
- **GET** `http://localhost:8000/health`
- Response: `healthy`

## Move recommendation
- **POST** `http://localhost:8000/moves`
- Request: `{"fen":"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1","variant":"standard"}`
- Response: `{"move":"e2e4"}`

## Docker
```bash
docker build -t engine-service .
docker run --rm --init -e PORT=8000 -e HOST=0.0.0.0 -e STOCKFISH_DEPTH=10 -p 127.0.0.1:8000:8000 engine-service
```

The container supplies `STOCKFISH_PATH=/usr/games/stockfish`. The image contains Stockfish from the package of Debian, which is under GPL-3.0. Its source is at https://tracker.debian.org/pkg/stockfish.

## Tests
```bash
python -m pytest tests -q
```

A real Stockfish test runs when `STOCKFISH_PATH` points to an executable.
It verifies that the recommended move is legal in the starting position.

CI installs Stockfish, runs the complete test suite, builds the Docker image,
starts the container and calls both HTTP endpoints.

## Integration
The engine service receives FEN positions from the game service and returns one UCI move.
The request, response and HTTP errors are specified in [integration.md](docs/integration.md).
The shared OpenAPI contract is maintained in the `infra` repository by ADR-6.

[ES-ADR-1](docs/adr/container-image.md) describes the image.

## CI

The workflow in `.github/workflows/engine-service.yml` runs the tests, builds the Docker image and smoke tests it on every pull request and every push to `dev` and `main`. A tag such as `v1.0.0` also publishes the image for amd64 and arm64 as `ghcr.io/szoftarch-chess-platform/engine-service:1.0.0`, as ADR-2 decides.

```bash
git tag v1.0.0
git push origin v1.0.0
```

After its first publication the package can be private. Make it public once in the package settings on GitHub.

## File structure
```
engine-service/
├── docs/                         # decisions, open questions and next steps
│   ├── integration.md            # service integration contract
│   └── architecture.md           # component diagram
├── engine_service/
│   ├── app.py                    # FastAPI application
│   ├── config.py                 # environment configuration
│   ├── engine.py                 # Stockfish integration
│   ├── position.py               # FEN parsing and validation
│   ├── schemas.py                # API request and response models
│   └── main.py                   # application entry point
├── tests/
│   ├── test_health.py            # health endpoint tests
│   ├── test_move_contract.py     # move endpoint contract tests
│   ├── test_engine_real.py       # real Stockfish integration test
│   └── test_engine.py            # engine restart and limit tests
├── scripts/
│   └── smoke_test.py             # container HTTP smoke test
├── .github/
│   └── workflows/
│       └── engine-service.yml    # tests and container validation
├── LICENSE                       # GNU General Public License version 3
├── Dockerfile                    # container image
├── .dockerignore                 # files left out of the image build
└── requirements.txt              # Python dependencies
```

## License

The engine-service is free software under the GNU General Public License version 3 or any later version. The full text is in [LICENSE](LICENSE), and [ES-ADR-2](docs/adr/chess-engine.md) describes the license.

## Documentation
- The decisions, open questions and next steps of the engine-service are in [docs/](docs/README.md).
