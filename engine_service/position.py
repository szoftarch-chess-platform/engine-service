import chess


class InvalidPositionError(ValueError):
    pass


def parse_position(fen: str) -> chess.Board:
    try:
        board = chess.Board(fen)
    except ValueError as error:
        raise InvalidPositionError("The FEN string is invalid.") from error

    if not board.is_valid():
        raise InvalidPositionError("The FEN position is invalid.")

    return board
