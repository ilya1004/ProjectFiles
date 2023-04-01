from datetime import datetime
from sqlalchemy import Table, MetaData, Column, Integer, String, TIMESTAMP, ForeignKey

from src.database import Base

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
    Column('player_1_id', Integer, nullable=False),
    Column('player_2_id', Integer, nullable=False),
    Column('rate_change_1', Integer, nullable=False),
    Column('rate_change_2', Integer, nullable=False),
)


class Mode(Base):
    __tablename__ = 'mode'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    mode_length_sec = Column(Integer, nullable=False)


class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)
    mode_id = Column(Integer, ForeignKey(mode.c.id), nullable=False)
    played_at = Column(TIMESTAMP, default=datetime.utcnow)
    game_length_sec = Column(Integer, nullable=False)
    player_1_id = Column(Integer, nullable=False)
    player_2_id = Column(Integer, nullable=False)
    rate_change_1 = Column(Integer, nullable=False)
    rate_change_2 = Column(Integer, nullable=False)
