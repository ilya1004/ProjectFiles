from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from src.api.authentication.base_config import current_user
from src.api.authentication.models import User, user
from src.database import get_async_session
from src.custom_errors import ExceptionUnauthorized, ExceptionNoUser


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get('/is_user_in_database_by_id')
async def is_user_in_database_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(user_id, int):
            raise TypeError("Error")
        query = select(user.c.id).where(user.c.id == user_id)
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
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "data": "Exception",
            "details": str(e)
        }


@router.get('/get_info_of_current_user')
def get_info_of_current_user(curr_user: User = Depends(current_user)):
    try:
        if isinstance(curr_user, int) and curr_user == 401:
            raise ExceptionUnauthorized("Error")

        lst = ["id", "nickname", "registration_time", "number_matches_blitz", "number_matches_rapid",
               "number_matches_classical", "rate_blitz", "rate_rapid", "rate_classical",
               "winrate_blitz", "winrate_rapid", "winrate_classical"]
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
        dict_res[lst[9]] = curr_user.winrate_blitz
        dict_res[lst[10]] = curr_user.winrate_rapid
        dict_res[lst[11]] = curr_user.winrate_classical
        return {
            "status": "success",
            "data": dict_res,
            "details": None
        }
    except ExceptionUnauthorized:
        return {
            "status": "error",
            "data": "ExceptionUnauthorized",
            "details": "User is not authorized"
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "data": "Exception",
            "details": str(e)
        }


@router.post("/change_curr_user_nickname")
async def change_curr_user_nickname(new_nickname: str, curr_user: User = Depends(current_user),
                                    session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(new_nickname, str):
            raise TypeError("Nickname should be str")
        update_query = user.update().where(user.c.id == curr_user.id).values(nickname=new_nickname)
        await session.execute(update_query)
        await session.commit()
        return {
            "status": "success",
            "data": new_nickname,
            "detail": None
        }
    except TypeError as e:
        return {
            "status": "error",
            "data": "TypeError",
            "details": str(e)
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }


@router.get("/get_info_by_user_id")
async def get_info_by_user_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(user_id, int):
            raise TypeError("Error")
        query = select(user.c.id, user.c.nickname, user.c.registration_time,
                       user.c.number_matches_blitz, user.c.number_matches_rapid, user.c.number_matches_classical,
                       user.c.rate_blitz, user.c.rate_rapid, user.c.rate_classical).where(user.c.id == user_id)
        result = await session.execute(query)
        lst = ["id", "nickname", "registration_time",
               "number_matches_blitz", "number_matches_rapid", "number_matches_classical",
               "rate_blitz", "rate_rapid", "rate_classical",
               "winrate_blitz", "winrate_rapid", "winrate_classical"]
        list_res = [dict(zip(lst, row)) for row in result.all()]
        if len(list_res) == 0:
            raise ExceptionNoUser("Error")
        return {
            "status": "success",
            "data": list_res[0],
            "details": None
        }
    except ExceptionNoUser:
        return {
            "status": "error",
            "data": "ExceptionNoUser",
            "details": "No user in database with given id"
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except OperationalError as e:
        return {
            "status": "error",
            "data": "OperationalError",
            "details": f"Database error: {str(e)}"
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


@router.get("/get_info_of_all_users")
async def get_info_of_all_users(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user.c.id, user.c.nickname,
                       user.c.number_matches_blitz, user.c.number_matches_rapid, user.c.number_matches_classical,
                       user.c.rate_blitz, user.c.rate_rapid, user.c.rate_classical)
        result = await session.execute(query)
        lst = ["id", "nickname",
               "number_matches_blitz", "number_matches_rapid", "number_matches_classical",
               "rate_blitz", "rate_rapid", "rate_classical",
               "winrate_blitz", "winrate_rapid", "winrate_classical"]
        list_res = [dict(zip(lst, row)) for row in result.all()]
        if len(list_res) == 0:
            raise ExceptionNoUser("error")
        return {
            "status": "success",
            "data": list_res,
            "details": None
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except ExceptionNoUser:
        return {
            "status": "error",
            "data": "ExceptionNoUser",
            "details": "No users in database"
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }


@router.post("/delete_user_by_id")
async def delete_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if not isinstance(user_id, int):
            TypeError("error")
        is_user_in_db = await is_user_in_database_by_id(user_id, session)
        if is_user_in_db["data"] == 0:
            raise ExceptionNoUser("error")
        stmt = delete(user).where(user.c.id == user_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": user_id,
            "details": None
        }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except ExceptionNoUser:
        return {
            "status": "error",
            "data": "ExceptionNoUser",
            "details": "No user in database with given id"
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
