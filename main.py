from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from exceptions.handlers import register_exception_handlers

from routes.routes_autenticacion import router as autenticacion_router
from routes.routes_metodos_pago import router as metodos_pago_router
# from routes.routes_categorias import router as cateogorias_router
from routes.routes_domicilio import router as domicilios_router
from routes.routes_pedido import router as pedidos_router
from routes.routes_detalle_carrito import router as detalles_carrito_router
# from routes.routes_detalle_pedido import router as detalles_pedido_router
from routes.routes_envio import router as envio_router
from routes.routes_productos import router as productos_router
from routes.routes_checkout import router as checkout_router


app = FastAPI()
register_exception_handlers(app)

origins = ['*']


app.include_router(autenticacion_router,prefix='/api',tags=["Auth"])
app.include_router(metodos_pago_router,prefix='/api',tags=["Payment Methods"])
# app.include_router(cateogorias_router,prefix='/api',tags=["Categories"])
app.include_router(domicilios_router,prefix='/api',tags=["Addresses"])
app.include_router(pedidos_router, prefix='/api', tags=["Orders"])
app.include_router(detalles_carrito_router, prefix='/api', tags=["Carts"])
# app.include_router(detalles_pedido_router,prefix='/api', tags=["Detalles Pedido"])
app.include_router(envio_router,prefix='/api', tags=["Shippings"])
app.include_router(productos_router,prefix='/api',tags=["Products"])
app.include_router(checkout_router,prefix='/api',tags=["Checkout"])


@app.get("/")
def read_root():
    return {"message": "Hi, FastAPI is working"}