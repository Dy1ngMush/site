from contextlib import asynccontextmanager

import uvicorn
from fastapi.responses import ORJSONResponse
from fastapi import FastAPI
from core.config import settings
from api import router as api_router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(
    title='Магазин "ТО ЧТО НАДО"',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
templates = Jinja2Templates(directory='pages')
main_app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
