import argparse
import json
import time
import urllib.error
import urllib.request

import chess


STARTING_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def get(base_url: str, path: str) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(base_url + path, timeout=5) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8")


def post(base_url: str, path: str, body: dict) -> tuple[int, dict]:
    request = urllib.request.Request(
        base_url + path,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


def wait_until_ready(base_url: str, timeout_seconds: int) -> None:
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        try:
            status, body = get(base_url, "/health")
            if status == 200 and body == "healthy":
                return
        except urllib.error.URLError:
            pass
        time.sleep(1)

    raise RuntimeError("The engine service did not become healthy.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    wait_until_ready(args.base_url, args.timeout)

    status, body = post(
        args.base_url,
        "/move",
        {"fen": STARTING_POSITION, "variant": "standard"},
    )
    if status != 200:
        raise RuntimeError(f"Move request failed with HTTP {status}: {body}")

    move = body.get("move")
    if not isinstance(move, str):
        raise RuntimeError(f"Invalid move response: {body}")

    board = chess.Board(STARTING_POSITION)
    try:
        parsed_move = chess.Move.from_uci(move)
    except ValueError as error:
        raise RuntimeError(f"Invalid UCI move response: {body}") from error

    if parsed_move not in board.legal_moves:
        raise RuntimeError(f"Illegal move response: {body}")

    print(json.dumps(body))


if __name__ == "__main__":
    main()
