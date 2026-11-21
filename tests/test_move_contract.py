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
        "/move",
        json={"fen": STARTING_POSITION, "variant": "standard"},
    )

    assert response.status_code == 200
    assert response.json() == {"move": "e2e4"}


def test_malformed_fen_is_rejected() -> None:
    response = client.post("/move", json={"fen": "not a fen"})

    assert response.status_code == 400
    assert response.json() == {"detail": "The FEN string is invalid."}


def test_variant_defaults_to_standard() -> None:
    app.state.engine = FakeEngine()

    response = client.post("/move", json={"fen": STARTING_POSITION})

    assert response.status_code == 200


def test_unsupported_variant_is_rejected() -> None:
    response = client.post(
        "/move",
        json={"fen": STARTING_POSITION, "variant": "chess960"},
    )

    assert response.status_code == 422


def test_terminal_position_is_rejected() -> None:
    app.state.engine = FakeEngine()

    response = client.post(
        "/move",
        json={"fen": "7k/6Q1/6K1/8/8/8/8/8 b - - 0 1"},
    )

    assert response.status_code == 409


def test_engine_error_is_reported() -> None:
    class FailingEngine:
        def recommend(self, board) -> str:
            raise chess.engine.EngineError("Stockfish failed.")

    app.state.engine = FailingEngine()

    response = client.post(
        "/move",
        json={"fen": STARTING_POSITION},
    )

    assert response.status_code == 503
