from contextlib import asynccontextmanager

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import ORJSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from uuid import UUID

from api.api_v1.order.crud import get_order_with_products_assoc
from api.api_v1.profile.dependencies import profile_by_user_id
from api.api_v1.users.dependencies import user_by_id
from auth.utils import decode_jwt

from api.api_v1.products.views import get_all_products
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

dynamictemplates = Jinja2Templates(directory='templates')
main_app.mount('/static/', StaticFiles(directory='pages/static'), name='pages/static')
main_app.mount('/js/', StaticFiles(directory='pages/js'), name='pages/js')
main_app.mount('/CSS/', StaticFiles(directory='pages/css'), name='pages/css')


@main_app.get('/')
async def get(req: Request):
    if req.cookies.get('access_token'):
        access_token = decode_jwt(req.cookies['access_token'])
        return dynamictemplates.TemplateResponse('index.html', {"request": req, "access_token": access_token})
    else:
        return dynamictemplates.TemplateResponse('index.html', {"request": req, "access_token": ''})


@main_app.get('/products')
async def get(req: Request, products=Depends(get_all_products)):
    if req.cookies.get('access_token'):
        access_token = decode_jwt(req.cookies['access_token'])
        return dynamictemplates.TemplateResponse('products.html', {"request": req, "products": products, "access_token": access_token})
    else:
        return dynamictemplates.TemplateResponse('products.html', {"request": req, "products": products, "access_token": ''})


@main_app.get('/product/{product_name}')
async def get(req: Request, products=Depends(get_all_products)):
    if req.cookies.get('access_token'):
        access_token = decode_jwt(req.cookies['access_token'])
        return dynamictemplates.TemplateResponse('product.html', {"request": req,
                                                                  "products": products,
                                                                  'zxc': ['200w', '140w'],
                                                                  "access_token": access_token,
                                                                  })
    else:
        return dynamictemplates.TemplateResponse(
            'product.html', {
                "request": req,
                "products": products,
                'zxc': ['200w', '140w'],
                "access_token": ''
                 }
        )


@main_app.get('/create_profile/{user_id}')
async def create_profile(req: Request):
    return dynamictemplates.TemplateResponse('create_profile.html', {"request": req})


@main_app.get('/profile/{user_id}')
async def get_profile(req: Request, session=Depends(db_helper.session_getter)):
    profile = await profile_by_user_id(UUID(str(req.url)[30:]), session=session)
    user = await user_by_id(UUID(str(req.url)[30:]), session=session)
    print(user.username)
    if req.cookies.get('access_token'):
        access_token = decode_jwt(req.cookies['access_token'])
        return dynamictemplates.TemplateResponse('profile.html', {"request": req, "profile": profile, "user": user, "access_token": access_token})
    else:
        return dynamictemplates.TemplateResponse('profile.html', {"request": req, "profile": profile, "user": user, "access_token": ''})


@main_app.get('/cart')
async def get_cart(req: Request, session=Depends(db_helper.session_getter)):
    if req.cookies.get('access_token'):
        access_token = decode_jwt(req.cookies['access_token'])
        cart = await get_order_with_products_assoc(session, access_token['sub'])
        sum = 0
        for product in cart.products_details:
            sum += product.quantity*product.product.price
        return dynamictemplates.TemplateResponse('cart.html', {"request": req, "access_token": access_token, "cart": cart, "sum": sum})
    else:
        return dynamictemplates.TemplateResponse('nocart.html', {"request": req, "access_token": ''})


@main_app.get('/orders/{user_id}')
async def get_orders(req: Request, session=Depends(db_helper.session_getter)):
    if req.cookies.get('access_token'):
        access_token = decode_jwt(req.cookies['access_token'])
        orders = await get_order_by_user_id(access_token['sub'], session)
        return dynamictemplates.TemplateResponse('orders.html', {"request": req, "access_token": access_token, "orders": orders})
    else:
        return dynamictemplates.TemplateResponse('noorders.html', {"request": req, "access_token": ''})


main_app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
