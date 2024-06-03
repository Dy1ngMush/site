from fastapi import APIRouter

from core.config import settings

from .users.views import router as users_router
from .products.views import router as products_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)

router.include_router(
    products_router,
    prefix=settings.api.v1.products,
)
