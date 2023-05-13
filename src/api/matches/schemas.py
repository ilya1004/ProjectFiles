from pydantic import BaseModel


class ModeCreate(BaseModel):
    id: int
    name: str
    mode_length_sec: int
