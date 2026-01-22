from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.exceptions_categorias import CategoriaNoExistenteException,CategoriaYaExisteException
from exceptions.exceptions_detalles_carrito import DetalleCarritoVacioException,DetalleCarritoNoExistenteException
from exceptions.exceptions_detalles_pedido import DetallePedidoNoExistenteException
from exceptions.exceptions_domicilios import DomicilioNoExistenteException, NoDomicilioPreferidoException
from exceptions.exceptions_envios import EnvioExistenteException,EnvioNoExistenteException
from exceptions.exceptions_metodos_pago import MetodoPagoExistenteException,MetodoPagoNoExistenteException
from exceptions.exceptions_productos import ProductoNoExistenteException

def register_exception_handlers(app):

    @app.exception_handler(CategoriaNoExistenteException)
    async def categoria_no_existente_handler(
        equest: Request,
        exc: CategoriaNoExistenteException  
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "Categoria no encontrada"}
        )
    @app.exception_handler(CategoriaYaExisteException)
    async def categoria_ya_existente_handler(
        equest: Request,
        exc: CategoriaYaExisteException  
    ):
        return JSONResponse(
            status_code=400,
            content={"detail":"Categoria ya existente"}
        )


    @app.exception_handler(DetalleCarritoVacioException)
    async def carrito_vacio_handler(
        request: Request,
        exc: DetalleCarritoVacioException
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": "El carrito está vacío"}
        )
    
    @app.exception_handler(DetalleCarritoNoExistenteException)
    async def detalle_pedido_no_existente_handler(
        request: Request,
        exc: DetalleCarritoNoExistenteException
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "Carrito no encontrado"}
        )
    
    @app.exception_handler(DetallePedidoNoExistenteException)
    async def detalle_pedido_no_existente_handler(
        request: Request,
        exc: DetallePedidoNoExistenteException
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "Detalle pedido no encontrado"}
        )
    
    @app.exception_handler(DomicilioNoExistenteException)
    async def domicilio_no_existente_handler(
        request: Request,
        exc: DomicilioNoExistenteException
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "Domicilio no encontrado"}
        )

    @app.exception_handler(NoDomicilioPreferidoException)
    async def no_domicilio_preferido_handler(
        request: Request,
        exc: NoDomicilioPreferidoException
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "No hay domicilio preferido"}
        )
    
    @app.exception_handler(EnvioExistenteException)
    async def envio_existente_handler(
        request: Request,
        exc: EnvioExistenteException
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": "Numero de seguimiento existente"}
        )
    
    @app.exception_handler(EnvioNoExistenteException)
    async def envio_no_existente_handler(
        request: Request,
        exc: EnvioNoExistenteException
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "Envio no encontrado"}
        )
    
    @app.exception_handler(MetodoPagoExistenteException)
    async def metodo_pago_existente_handler(
        request: Request,
        exc: MetodoPagoExistenteException
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": "Metodo de pago existente"}
        )
    
    @app.exception_handler(MetodoPagoNoExistenteException)
    async def metodo_pago_no_existente_handler(
        request: Request,
        exc: MetodoPagoNoExistenteException
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "Metodo de pago no encontrado"}
        )

    
    @app.exception_handler(ProductoNoExistenteException)
    async def producto_no_existente_handler(
        request: Request,
        exc: ProductoNoExistenteException
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "Producto no encontrado"}
        )

