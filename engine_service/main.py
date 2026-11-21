import uvicorn

from engine_service.app import app
from engine_service.config import get_settings


def main() -> None:
    settings = get_settings()
    app.state.settings = settings
    uvicorn.run(app, host="0.0.0.0", port=settings.port)


if __name__ == "__main__":
    main()
