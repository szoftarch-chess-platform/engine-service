# engine-service

Engine service of the online chess platform. Its responsibilities are decided in ADR-1.

## Current status
- Health check endpoint implemented.

## Run
```bash
python engine-service/engine_service.py
```

## Health check
- **GET** `http://localhost/health`
- Response: `healthy`

## Notes
- Service listens on port `80` by default.
- You can override it with environment variable `PORT`.

## File structure
```
engine-service/
├── docs/                         # decisions and open questions
├── engine-service/
│   ├── engine_service.py         # HTTP server with the health check
│   └── engine-service.pyproj     # Visual Studio project
└── requirements.txt              # Python dependencies
```

## Documentation
- The decisions and open questions of the engine-service are in [docs/](docs/README.md).
