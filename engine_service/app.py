from contextlib import asynccontextmanager

import chess
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse

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


def problem_response(status_code: int, title: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        media_type="application/problem+json",
        content={
            "title": title,
            "status": status_code,
            "detail": detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    error: RequestValidationError,
) -> JSONResponse:
    if any(
        "variant" in [str(part) for part in item.get("loc", ())]
        and item.get("type") == "literal_error"
        for item in error.errors()
    ):
        return problem_response(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Unsupported variant",
            "The requested game variant is unsupported.",
        )

    return problem_response(
        status.HTTP_400_BAD_REQUEST,
        "Invalid position",
        "The request or FEN is invalid.",
    )


@app.get("/health", response_class=PlainTextResponse)
def health() -> str:
    return "healthy"


@app.post("/moves")
def get_move(request: MoveRequest) -> MoveResponse:
    try:
        board = parse_position(request.fen)
    except InvalidPositionError as error:
        return problem_response(
            status.HTTP_400_BAD_REQUEST,
            "Invalid position",
            str(error),
        )

    if board.is_game_over():
        return problem_response(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Invalid position",
            "The side to move has no legal move.",
        )

    engine = getattr(app.state, "engine", None)
    if engine is None:
        return problem_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Engine failure",
            "The chess engine is unavailable.",
        )

    try:
        move = engine.recommend(board)
    except chess.engine.EngineError as error:
        return problem_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Engine failure",
            "The chess engine could not calculate a move.",
        )

    return MoveResponse(move=move)
