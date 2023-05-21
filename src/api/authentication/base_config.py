from fastapi_users import FastAPIUsers, schemas, models
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from src.api.authentication.models import User
from src.api.authentication.user_manager import get_user_manager
from src.config import SECRET_AUTH


cookie_transport = CookieTransport(cookie_name="cookie", cookie_max_age=7200,
                                   cookie_samesite="none", cookie_httponly=False)

SECRET = SECRET_AUTH


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=7200)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
