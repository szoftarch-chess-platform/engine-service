from typing import Literal

from pydantic import BaseModel, Field


# Unknown fields are ignored, because a reader tolerates what it does not know (ADR-7).
class MoveRequest(BaseModel):
    fen: str
    variant: Literal["standard"] = "standard"


class MoveResponse(BaseModel):
    move: str = Field(pattern=r"^[a-h][1-8][a-h][1-8][qrbn]?$")
