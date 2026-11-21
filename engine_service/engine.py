from threading import Lock

import chess
import chess.engine


class StockfishEngine:
    def __init__(self, path: str, depth: int) -> None:
        self._engine = chess.engine.SimpleEngine.popen_uci(path)
        self._depth = depth
        self._lock = Lock()

    def recommend(self, board: chess.Board) -> str:
        with self._lock:
            result = self._engine.play(
                board,
                chess.engine.Limit(depth=self._depth),
            )

        if result.move is None:
            raise chess.engine.EngineError("Stockfish did not return a move.")

        return result.move.uci()

    def close(self) -> None:
        self._engine.quit()
