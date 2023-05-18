from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, MetaData
from src.api.authentication.models import user
# from src.database import metadata

metadata = MetaData()

mode = Table(
    'mode',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('mode_length_sec', Integer, nullable=False)
)

match = Table(
    'match',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('mode_id', Integer, ForeignKey(mode.c.id), nullable=False),
    Column('played_at', TIMESTAMP, default=datetime.utcnow),
    Column('game_length_sec', Integer, nullable=False),
    Column('player_1_id', Integer, ForeignKey(user.c.id), nullable=False),
    Column('player_2_id', Integer, ForeignKey(user.c.id), nullable=False),
    Column('player_1_nickname', String(50), nullable=False),
    Column('player_2_nickname', String(50), nullable=False),
    Column('rate_change_player_1', Integer, nullable=False),
    Column('rate_change_player_2', Integer, nullable=False),
)
