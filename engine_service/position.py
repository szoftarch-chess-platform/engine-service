import chess


class InvalidPositionError(ValueError):
    pass


def parse_position(fen: str) -> chess.Board:
    if len(fen.split()) != 6:
        raise InvalidPositionError("The FEN must contain exactly 6 fields.")

    try:
        board = chess.Board(fen)
    except ValueError as error:
        raise InvalidPositionError("The FEN string is invalid.") from error

    if not board.is_valid():
        raise InvalidPositionError("The FEN position is invalid.")

    return board
