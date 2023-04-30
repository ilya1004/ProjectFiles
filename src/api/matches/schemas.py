from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic.schema import datetime


class ModeCreate(BaseModel):
    id: int
    name: str
    mode_length_sec: int


class MatchCreate(BaseModel):
    def __init__(self,
                 id: int = 0,
                 mode_id: int = 0,
                 played_at: datetime = datetime.utcnow(),
                 game_length_sec: int = 0,
                 player_1_id: int = 0,
                 player_2_id: int = 0,
                 rate_change_player_1: int = 0,
                 rate_change_player_2: int = 0):
        super().__init__(
            id=id,
            mode_id=mode_id,
            played_at=played_at,
            game_length_sec=game_length_sec,
            player_1_id=player_1_id,
            player_2_id=player_2_id,
            rate_change_player_1=rate_change_player_1,
            rate_change_player_2=rate_change_player_2
        )
        self.id = id
        self.mode_id = mode_id
        self.played_at = played_at
        self.game_length_sec = game_length_sec
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
        self.rate_change_player_1 = rate_change_player_1
        self.rate_change_player_2 = rate_change_player_2

    id: int
    mode_id: int
    played_at: datetime
    game_length_sec: int
    player_1_id: int  # победитель
    player_2_id: int  # проигравший
    rate_change_player_1: int
    rate_change_player_2: int
