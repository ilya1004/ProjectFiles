from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Boolean
from src.database import Base

metadata = MetaData()

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(100), nullable=False),
    Column('hashed_password', String(100), nullable=False),
    Column('nickname', String(100), nullable=False),
    Column('registration_time', TIMESTAMP, default=datetime.utcnow),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
    Column('number_matches_blitz', Integer, default=0, nullable=False),
    Column('number_matches_rapid', Integer, default=0, nullable=False),
    Column('number_matches_classical', Integer, default=0, nullable=False),
    Column('rate_blitz', Integer, default=1000, nullable=False),
    Column('rate_rapid', Integer, default=1000, nullable=False),
    Column('rate_classical', Integer, default=1000, nullable=False)
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(100), nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    nickname: str = Column(String(100), nullable=False)
    registration_time: TIMESTAMP = Column(TIMESTAMP, default=datetime.utcnow)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    number_matches_blitz: int = Column(Integer, default=0, nullable=False)
    number_matches_rapid: int = Column(Integer, default=0, nullable=False)
    number_matches_classical: int = Column(Integer, default=0, nullable=False)
    rate_blitz: int = Column(Integer, default=1000, nullable=False)
    rate_rapid: int = Column(Integer, default=1000, nullable=False)
    rate_classical: int = Column(Integer, default=1000, nullable=False)
