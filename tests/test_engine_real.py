import os
import shutil
from pathlib import Path

import chess
import pytest

from engine_service.engine import StockfishEngine


def find_stockfish() -> str | None:
    configured_path = os.getenv("STOCKFISH_PATH")
    if configured_path and Path(configured_path).is_file():
        return configured_path

    executable = shutil.which("stockfish")
    if executable:
        return executable

    debian_path = Path("/usr/games/stockfish")
    if debian_path.is_file():
        return str(debian_path)

    return None


STOCKFISH_PATH = find_stockfish()


@pytest.mark.skipif(
    STOCKFISH_PATH is None,
    reason="Set STOCKFISH_PATH to run the real Stockfish integration test.",
)
def test_stockfish_recommends_a_legal_starting_move() -> None:
    engine = StockfishEngine(path=STOCKFISH_PATH, depth=10)
    board = chess.Board()

    try:
        recommended = engine.recommend(board)
        move = chess.Move.from_uci(recommended)

        assert move in board.legal_moves
    finally:
        engine.close()
