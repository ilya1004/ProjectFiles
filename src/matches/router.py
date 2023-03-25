from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.matches.models import match, mode
from src.matches.schemas import MatchCreate, ModeCreate

router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)


@router.get("/get_matches_by_user_id")
async def get_matches_by_user_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(match).where((match.c.player_1_id == user_id) | (match.c.player_2_id == user_id))
    result = await session.execute(query)
    lst = ["id", "mode_id", "played_at", "game_length_sec",
           "player_1_id", "player_2_id", "rate_change_1", "rate_change_2"]
    list_res = list()
    for tup in result:
        list_res.append(dict(zip(lst, tup)))
    return list_res


@router.get('/get_all_matches')
async def get_all_matches(session: AsyncSession = Depends(get_async_session)):
    query = select(match)
    result = await session.execute(query)
    lst = ["id", "mode_id", "played_at", "game_length_sec",
           "player_1_id", "player_2_id", "rate_change_1", "rate_change_2"]
    list_res = list()
    for tup in result:
        list_res.append(dict(zip(lst, tup)))
    return list_res


@router.get('/get_all_modes')
async def get_all_modes(session: AsyncSession = Depends(get_async_session)):
    query = select(mode)
    result = await session.execute(query)
    lst = ["id", "name", "mode_length_sec"]
    list_res = list()
    for tup in result:
        list_res.append(dict(zip(lst, tup)))
    return list_res


@router.post('/add_match')
async def add_match(new_match: MatchCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(match).values(**new_match.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
