from fastapi.testclient import TestClient
import chess
import chess.engine

from engine_service.app import app


client = TestClient(app)

STARTING_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class FakeEngine:
    def recommend(self, board) -> str:
        return "e2e4"


def test_valid_fen_returns_recommended_move() -> None:
    app.state.engine = FakeEngine()

    response = client.post(
        "/moves",
        json={"fen": STARTING_POSITION},
    )

    assert response.status_code == 200
    assert response.json() == {"move": "e2e4"}


def test_malformed_fen_is_rejected() -> None:
    response = client.post("/moves", json={"fen": "not a fen"})

    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["status"] == 400


def test_fen_must_have_six_fields() -> None:
    response = client.post(
        "/moves",
        json={"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The FEN must contain exactly 6 fields."


def test_unknown_field_is_rejected() -> None:
    response = client.post(
        "/moves",
        json={"fen": STARTING_POSITION, "variant": "standard"},
    )

    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")


def test_terminal_position_is_rejected() -> None:
    app.state.engine = FakeEngine()

    response = client.post(
        "/moves",
        json={"fen": "7k/6Q1/6K1/8/8/8/8/8 b - - 0 1"},
    )

    assert response.status_code == 400
    assert response.json()["title"] == "Invalid position"


def test_engine_error_is_reported() -> None:
    class FailingEngine:
        def recommend(self, board) -> str:
            raise chess.engine.EngineError("Stockfish failed.")

    app.state.engine = FailingEngine()

    response = client.post(
        "/moves",
        json={"fen": STARTING_POSITION},
    )

    assert response.status_code == 500
    assert response.headers["content-type"].startswith("application/problem+json")
