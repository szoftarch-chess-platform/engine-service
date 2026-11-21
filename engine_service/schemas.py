from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MoveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fen: str
    variant: Literal["standard"] = "standard"


class MoveResponse(BaseModel):
    move: str = Field(pattern=r"^[a-h][1-8][a-h][1-8][qrbn]?$")
