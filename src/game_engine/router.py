from sqlalchemy.exc import SQLAlchemyError

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.authentication.models import user
from src.database import get_async_session

router = APIRouter(
    prefix="/matches",
    tags=["Game_engine"]
)


@router.post("/update_user_rate")
async def update_user_rate(user_id: int, mode_name: str, rate_diff: int,
                           session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        list_res = list()
        lst = ["id", "email", "hashed_password", "nickname", "registration_time", "is_active", "is_superuser", "is_verified",
               "number_matches_blitz", "number_matches_rapid", "number_matches_classical",
               "rate_blitz", "rate_rapid", "rate_classical"]
        for tup in result:
            list_res.append(dict(zip(lst, tup)))
        user_info = list_res[0]
        update_query = None
        if mode_name == "blitz":
            rate = user_info["rate_blitz"]
            new_rate = rate + rate_diff
            update_query = user.update().where(user.c.id == user_id).values(rate_blitz=new_rate)
        elif mode_name == "rapid":
            rate = user_info["rate_rapid"]
            new_rate = rate + rate_diff
            update_query = user.update().where(user.c.id == user_id).values(rate_rapid=new_rate)
        elif mode_name == "classical":
            rate = user_info["rate_classical"]
            new_rate = rate + rate_diff
            update_query = user.update().where(user.c.id == user_id).values(rate_classical=new_rate)

        await session.execute(update_query)
        await session.commit()

        return {"status": "success"}
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "data": "SQLAlchemyError",
            "details": f"Database error: {str(e)}"
        }
    except Exception:
        return {
            "status": "error",
            "data": "Exception",
            "details": "Unknown error"
        }