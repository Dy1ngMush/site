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

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory='pages')
main_app.mount('/static/', StaticFiles(directory='pages/static'), name='pages/static')
main_app.mount('/js/', StaticFiles(directory='pages/js'), name='pages/js')
main_app.mount('/CSS/', StaticFiles(directory='pages/css'), name='pages/css')


@main_app.get('/')
async def get(req: Request):
    return templates.TemplateResponse('index.html', {"request": req})


@main_app.get('/products')
async def get(req: Request):
    return templates.TemplateResponse('goods.html', {"request": req})


@main_app.get('/product/140w')
async def get(req: Request):
    return templates.TemplateResponse('140w.html', {"request": req})


@main_app.get('/product/r600')
async def get(req: Request):
    return templates.TemplateResponse('r600.html', {"request": req})


@main_app.get('/product/r1500')
async def get(req: Request):
    return templates.TemplateResponse('r1500.html', {"request": req})


@main_app.get('/product/s200')
async def get(req: Request):
    return templates.TemplateResponse('s200.html', {"request": req})


@main_app.get('/product/s300')
async def get(req: Request):
    return templates.TemplateResponse('s300.html', {"request": req})


@main_app.get('/product/s2000-pro')
async def get(req: Request):
    return templates.TemplateResponse('s2000pro.html', {"request": req})


@main_app.get('/product/s700')
async def get(req: Request):
    return templates.TemplateResponse('s700.html', {"request": req})


@main_app.get('/product/200w')
async def get(req: Request):
    return templates.TemplateResponse('200w.html', {"request": req})


main_app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
