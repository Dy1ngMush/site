from fastapi import APIRouter

from core.config import settings

from .users.views import router as users_router
from .products.views import router as products_router
from .profile.views import router as profiles_router
from .tokens.views import router as tokens_router

# from .demo_auth.views import router as demo_auth_router
# from .demo_auth.demo_jwt_auth import router as demo_jwt_auth_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)

router.include_router(
    profiles_router,
    prefix=settings.api.v1.profiles,
)

router.include_router(
    products_router,
    prefix=settings.api.v1.products,
)

router.include_router(
    tokens_router,
    prefix=settings.api.v1.tokens,
)
# router.include_router(
#     demo_auth_router,
#     prefix=settings.api.v1.demo_auth,
# )

# router.include_router(
#     demo_jwt_auth_router,
#     prefix=settings.api.v1.demo_jwt_auth,
# )
