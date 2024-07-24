from contextlib import asynccontextmanager

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import ORJSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from core.config import settings
from api import router as api_router
from core.models import db_helper

origins = [
    "http://127.0.0.1:5500",
    "http://localhost",
    "http://127.0.0.1"
]

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
main_app.mount('/static/', StaticFiles(directory='pages/static'), name='pages/static')
main_app.mount('/js/', StaticFiles(directory='pages/js'), name='pages/js')
main_app.mount('/CSS/', StaticFiles(directory='pages/css'), name='pages/css')
main_app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
