from contextlib import asynccontextmanager

import chess
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse

from engine_service.engine import StockfishEngine
from engine_service.position import InvalidPositionError, parse_position
from engine_service.schemas import MoveRequest, MoveResponse


@asynccontextmanager
async def lifespan(application: FastAPI):
    settings = getattr(application.state, "settings", None)
    if settings is not None:
        application.state.engine = StockfishEngine(
            path=settings.stockfish_path,
            depth=settings.stockfish_depth,
        )
        try:
            yield
        finally:
            application.state.engine.close()
    else:
        yield


app = FastAPI(title="Chess Engine Service", lifespan=lifespan)


@app.get("/health", response_class=PlainTextResponse)
def health() -> str:
    return "healthy"


@app.post("/move")
def get_move(request: MoveRequest) -> MoveResponse:
    try:
        board = parse_position(request.fen)
    except InvalidPositionError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    if board.is_game_over():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The position has no move to recommend.",
        )

    engine = getattr(app.state, "engine", None)
    if engine is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The chess engine is unavailable.",
        )

    try:
        move = engine.recommend(board)
    except chess.engine.EngineError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The chess engine could not calculate a move.",
        ) from error

    return MoveResponse(move=move)
