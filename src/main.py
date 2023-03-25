from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends
from src.authentication.base_config import auth_backend, fastapi_users, current_user
from src.authentication.models import User
from src.authentication.schemas import UserRead, UserCreate
from src.database import get_async_session
from src.matches.router import router as router_matches

app = FastAPI(
    title="Сайт для секса"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.post('/auth', tags=["Auth"])
def get_current_user(user: User = Depends(current_user)):
    return f"Hello, {user.nickname}"


app.include_router(router_matches)
