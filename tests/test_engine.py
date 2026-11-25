from types import SimpleNamespace

import chess
import chess.engine

from engine_service.engine import StockfishEngine


def test_restarts_stockfish_after_process_exit(monkeypatch) -> None:
    class FirstEngine:
        def play(self, board, limit):
            raise chess.engine.EngineTerminatedError("Stockfish exited.")

        def quit(self) -> None:
            pass

    class RestartedEngine:
        def play(self, board, limit):
            assert limit.time == 8.5
            return SimpleNamespace(move=chess.Move.from_uci("e2e4"))

        def quit(self) -> None:
            pass

    engines = iter((FirstEngine(), RestartedEngine()))
    monkeypatch.setattr(
        chess.engine.SimpleEngine,
        "popen_uci",
        lambda path: next(engines),
    )

    engine = StockfishEngine(path="stockfish", depth=10)
    move = engine.recommend(chess.Board())
    engine.close()

    assert move == "e2e4"
