from typing import Literal

from pydantic import BaseModel


class MoveRequest(BaseModel):
    fen: str
    variant: Literal["standard"] = "standard"


class MoveResponse(BaseModel):
    move: str
