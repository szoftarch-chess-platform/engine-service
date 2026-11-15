# engine-service

Engine service of the online chess platform. Its responsibilities are decided in ADR-1.

## Current status
- Health check endpoint implemented.

## Configuration

| Environment variable | Required | Description |
|---|---|---|
| `PORT` | yes | port that the service listens on |

## Run
```bash
PORT=8000 python engine-service/engine_service.py
```

In PowerShell:
```powershell
$env:PORT = 8000; python engine-service/engine_service.py
```

## Health check
- **GET** `http://localhost:8000/health`
- Response: `healthy`

## Docker
```bash
docker build -t engine-service .
docker run --rm --init -e PORT=8000 -p 8000:8000 engine-service
```

[ES-ADR-1](docs/adr/container-image.md) describes the image.

## File structure
```
engine-service/
├── docs/                         # decisions, open questions and next steps
├── engine-service/
│   ├── engine_service.py         # HTTP server with the health check
│   └── engine-service.pyproj     # Visual Studio project
├── Dockerfile                    # container image
├── .dockerignore                 # files left out of the image build
└── requirements.txt              # Python dependencies
```

## Documentation
- The decisions, open questions and next steps of the engine-service are in [docs/](docs/README.md).
