# from datetime import datetime

from pydantic import BaseModel
from pydantic.schema import datetime


class ModeCreate(BaseModel):
    id: int
    name: str
    mode_length_sec: int


class MatchCreate(BaseModel):
    id: int
    mode_id: int
    played_at: datetime
    game_length_sec: int
    player_1_id: int
    player_2_id: int
    rate_change_player_1: int
    rate_change_player_2: int
