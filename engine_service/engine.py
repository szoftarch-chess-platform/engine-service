from threading import Lock

import chess
import chess.engine


class StockfishEngine:
    def __init__(self, path: str, depth: int) -> None:
        self._path = path
        self._engine = chess.engine.SimpleEngine.popen_uci(path)
        self._depth = depth
        self._lock = Lock()

    def recommend(self, board: chess.Board) -> str:
        if not self._lock.acquire(timeout=1.0):
            raise chess.engine.EngineError("Timed out waiting for Stockfish.")

        try:
            try:
                result = self._engine.play(
                    board,
                    chess.engine.Limit(depth=self._depth, time=8.5),
                )
            except chess.engine.EngineTerminatedError:
                self._engine = chess.engine.SimpleEngine.popen_uci(self._path)
                result = self._engine.play(
                    board,
                    chess.engine.Limit(depth=self._depth, time=8.5),
                )
        finally:
            self._lock.release()

        if result.move is None:
            raise chess.engine.EngineError("Stockfish did not return a move.")

        return result.move.uci()

    def close(self) -> None:
        try:
            self._engine.quit()
        except chess.engine.EngineError:
            pass
