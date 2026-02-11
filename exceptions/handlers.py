from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.exceptions_autenticacion import CorreoYaRegistadoException,NoAutorizadoException,SesionExpiradaException,TokenNoValidoException,TokenYaUsadoException,UsuarioNoExistenteException,NoAccesoAlRecursoException
from exceptions.exceptions_categorias import CategoriaNoExistenteException,CategoriaYaExisteException
from exceptions.exceptions_detalles_carrito import DetalleCarritoVacioException,DetalleCarritoNoExistenteException
from exceptions.exceptions_detalles_pedido import DetallePedidoNoExistenteException
from exceptions.exceptions_domicilios import DomicilioNoExistenteException, NoDomicilioPreferidoException
from exceptions.exceptions_envios import EnvioExistenteException,EnvioNoExistenteException
from exceptions.exceptions_metodos_pago import MetodoPagoExistenteException,MetodoPagoNoExistenteException
from exceptions.exceptions_productos import ProductoNoExistenteException

def register_exception_handlers(app):

    @app.exception_handler(TokenNoValidoException)
    async def token_no_valido_handler(
        equest: Request,
        exc: TokenNoValidoException  
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": "Refresh token inválido o no existe"}
        )
    
    @app.exception_handler(TokenYaUsadoException)
    async def token_ya_usado_handler(
        equest: Request,
        exc: TokenYaUsadoException  
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": "Token ya utilizado. Acceso denegado por seguridad"}
        )
    
    @app.exception_handler(SesionExpiradaException)
    async def sesion_expirada_handler(
        equest: Request,
        exc: SesionExpiradaException  
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": "Sesión expirada. Por favor, inicie sesión nuevamente"}
        )
    
    @app.exception_handler(CorreoYaRegistadoException)
    async def correo_ya_registrado_handler(
        equest: Request,
        exc: CorreoYaRegistadoException  
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": "El correo ya está registrado"}
        )
    
    @app.exception_handler(NoAutorizadoException)
    async def no_autorizado_handler(
        equest: Request,
        exc: NoAutorizadoException  
    ):
        return JSONResponse(
            status_code=403,
            content={"detail": "Credenciales inválidas"},
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    @app.exception_handler(UsuarioNoExistenteException)
    async def usuario_no_existente_handler(
        equest: Request,
        exc: UsuarioNoExistenteException  
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "Usuario no encontrada"}
        )
    
    @app.exception_handler(NoAccesoAlRecursoException)
    async def no_acceso_al_recurso_handler(
        equest: Request,
        exc: NoAccesoAlRecursoException  
    ):
        return JSONResponse(
            status_code=403,
            content={"detail": "No tienes acceso a este recurso"}
        )


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

