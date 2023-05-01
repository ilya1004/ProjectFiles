from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from src.api.authentication.base_config import current_user
from src.api.authentication.models import User, user
from src.database import get_async_session
from src.api.authentication.utils import ExceptionUnauthorized
from src.api.authentication.utils import ExceptionNoUser

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post('/is_user_in_database_by_id')
async def is_user_in_database_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if not type(user_id) is int:
            raise TypeError("Error")
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        if len(result.all()) == 1:
            is_user_res = 1
        else:
            is_user_res = 0
        return {
            "status": "success",
            "data": is_user_res,
            "details": None
        }
    except TypeError:
        return {
            "status": "error",
            "data": "TypeError",
            "details": f"Type of (user_id) in not int"
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }



@router.post('/get_current_user')
def get_current_user(curr_user: User = Depends(current_user)):
    try:
        if type(curr_user) is int and curr_user == 401:
            raise ExceptionUnauthorized("Error")
        return {
            "status": "success",
            "data": f"Hello, {curr_user.nickname}",
            "details": None
        }

    except ExceptionUnauthorized:
        return {
            "status": "error",
            "data": "ExceptionUnauthorized",
            "details": "User is unauthorized"
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }


@router.post('/get_info_of_current_user')
def get_info_of_current_user(curr_user: User = Depends(current_user)):
    try:
        if type(curr_user) is int and curr_user == 401:
            raise ExceptionUnauthorized("Error")

        lst = ["id", "nickname", "registration_time", "number_matches_blitz", "number_matches_rapid",
               "number_matches_classical", "rate_blitz", "rate_rapid", "rate_classical"]
        dict_res = dict()
        dict_res[lst[0]] = curr_user.id_
        dict_res[lst[1]] = curr_user.nickname
        dict_res[lst[2]] = curr_user.registration_time
        dict_res[lst[3]] = curr_user.number_matches_blitz
        dict_res[lst[4]] = curr_user.number_matches_rapid
        dict_res[lst[5]] = curr_user.number_matches_classical
        dict_res[lst[6]] = curr_user.rate_blitz
        dict_res[lst[7]] = curr_user.rate_rapid
        dict_res[lst[8]] = curr_user.rate_classical
        return {
            "status": "success",
            "data": dict_res,
            "details": None
        }

    except ExceptionUnauthorized:
        return {
            "status": "error",
            "data": "ExceptionUnauthorized",
            "details": "User is unauthorized"
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }


@router.post("/get_info_by_user_id")
async def get_info_by_user_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if not type(user_id) is int:
            raise TypeError("Error")
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        if len(result.all()) == 0:
            raise ExceptionNoUser("Error")
        lst = ["id", "email", "hashed_password", "nickname", "registration_time", "is_active", "is_superuser", "is_verified",
               "number_matches_blitz", "number_matches_rapid", "number_matches_classical",
               "rate_blitz", "rate_rapid", "rate_classical"]
        list_res = list()
        for tup in result:
            list_res.append(dict(zip(lst, tup)))
        return {
            "status": "success",
            "data": list_res[0],
            "details": None
        }
    except ExceptionNoUser:
        return {
            "status": "error",
            "data": "ExceptionNoUser",
            "details": f"No user in database with given id"
        }
    except TypeError:
        return {
            "status": "error",
            "data": "TypeError",
            "details": f"Type of (user_id) in not int"
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }
