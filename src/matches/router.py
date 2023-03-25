from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, Row
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from src.database import get_async_session
from src.matches.models import match, mode
from src.matches.schemas import MatchCreate

router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)


@router.get("/get_matches")
async def get_matches(user_id: int, session: AsyncSession = Depends(get_async_session)):
    # query = select(match).where(match.c.player_1_id == user_id)
    query = select(mode)
    result = await session.execute(query)
    return result.all()


def row2dict(row: Row) -> dict:
    """Преобразует объект типа Row в словарь"""
    return {col: getattr(row, col) for col in row.__table__.columns.keys()}

@router.get('/get_all_matches')
async def get_all_matches(session: AsyncSession = Depends(get_async_session)):
    query = select(match)
    result = await session.execute(query)
    return jsonable_encoder([row2dict(row) for row in result.all()])


@router.post('/')
async def add_match(new_match: MatchCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(match).values(**new_match.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
