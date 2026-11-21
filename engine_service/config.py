import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    stockfish_path: str
    stockfish_depth: int


def get_settings() -> Settings:
    # The address to listen on, 0.0.0.0 in a container and 127.0.0.1 on the host.
    host = os.getenv("HOST")
    if not host:
        raise SystemExit("The HOST environment variable is required.")

    port = os.getenv("PORT")
    if not port:
        raise SystemExit("The PORT environment variable is required.")

    stockfish_path = os.getenv("STOCKFISH_PATH")
    if not stockfish_path:
        raise SystemExit("The STOCKFISH_PATH environment variable is required.")

    try:
        parsed_port = int(port)
    except ValueError:
        raise SystemExit("The PORT environment variable must be an integer.")

    try:
        stockfish_depth = int(os.getenv("STOCKFISH_DEPTH", "10"))
    except ValueError:
        raise SystemExit("The STOCKFISH_DEPTH environment variable must be an integer.")

    if stockfish_depth < 1:
        raise SystemExit("The STOCKFISH_DEPTH environment variable must be positive.")

    return Settings(
        host=host,
        port=parsed_port,
        stockfish_path=stockfish_path,
        stockfish_depth=stockfish_depth,
    )
