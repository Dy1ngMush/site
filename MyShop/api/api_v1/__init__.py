from fastapi import APIRouter

from core.config import settings

from .users.views import router as users_router
from .products.views import router as products_router
from .profile.views import router as profiles_router
from .tokens.views import router as tokens_router
from .order.views import router as order_router
from .trueorder.views import router as true_order_router
# from .pages.views import router as pages_router

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

router.include_router(
    order_router,
    prefix=settings.api.v1.orders,
)

router.include_router(
    true_order_router,
    prefix=settings.api.v1.true_orders,
)

# router.include_router(
#     demo_jwt_auth_router,
#     prefix=settings.api.v1.demo_jwt_auth,
# )
