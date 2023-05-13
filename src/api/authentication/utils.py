from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.authentication.models import User
from src.database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


# Custom errors:

class ExceptionUnauthorized(Exception):
    def __init__(self, message: str):
        self.message = message


class ExceptionNoUser(Exception):
    def __init__(self, message: str):
        self.message = message
