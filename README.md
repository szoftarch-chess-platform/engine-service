# engine-service

Minimal chess engine microservice bootstrap.

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
