from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from src.api.authentication.base_config import current_user
from src.api.authentication.models import User, user
from src.database import get_async_session

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post('/get_current_user', tags=["Auth"])
def get_current_user(curr_user: User = Depends(current_user)):
    return f"Hello, {curr_user.nickname}"


@router.post('/get_info_of_current_user', tags=["Auth"])
def get_info_of_current_user(curr_user: User = Depends(current_user)):
    lst = ["id", "nickname", "registration_time", "number_matches_blitz", "number_matches_rapid",
           "number_matches_classical", "rate_blitz", "rate_rapid", "rate_classical"]
    dict_res = dict()
    dict_res[lst[0]] = curr_user.id
    dict_res[lst[1]] = curr_user.nickname
    dict_res[lst[2]] = curr_user.registration_time
    dict_res[lst[3]] = curr_user.number_matches_blitz
    dict_res[lst[4]] = curr_user.number_matches_rapid
    dict_res[lst[5]] = curr_user.number_matches_classical
    dict_res[lst[6]] = curr_user.rate_blitz
    dict_res[lst[7]] = curr_user.rate_rapid
    dict_res[lst[8]] = curr_user.rate_classical
    return dict_res


@router.post("/get_info_by_user_id")
async def get_info_by_user_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.id == user_id)
    result = await session.execute(query)
    # print(result)
    lst = ["id", "email", "hashed_password", "nickname", "registration_time", "is_active", "is_superuser", "is_verified",
           "number_matches_blitz", "number_matches_rapid", "number_matches_classical",
           "rate_blitz", "rate_rapid", "rate_classical"]
    list_res = list()
    for tup in result:
        list_res.append(dict(zip(lst, tup)))
    return list_res[0]
