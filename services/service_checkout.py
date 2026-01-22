from sqlalchemy.orm import Session
from sqlalchemy import func,text
from core.utils import generar_numero_seguimiento
from models.models_pedidos import Pedido
from models.models_envios import Envio, EstadoEnvioEnum
from models.models_detalles_pedido import DetallePedido
from models.models_detalles_carrito import DetalleCarrito
from exceptions.exceptions_domicilios import NoDomicilioPreferidoException
from exceptions.exceptions_detalles_carrito import DetalleCarritoVacioException
from typing import List
import uuid


from schemas.schema_pedido import PedidoBase,PedidoActualizar
from schemas.schema_envio import EnvioBase,EnvioActualizar
from schemas.schema_checkout import CheckoutBase

from services.service_domicilio import get_domicilio_preferido


def crear_pedido(db:Session,checkout:CheckoutBase,user_id:str):
    importe_productos = db.query(
        func.sum(DetalleCarrito.precio * DetalleCarrito.cantidad)
    ).filter(DetalleCarrito.usuarios_id == user_id,DetalleCarrito.activo == True).scalar()
    
    if not importe_productos:
        raise DetalleCarritoVacioException()

    if importe_productos>=300:
        importe_envio=0
    else:
        importe_envio=90 
    
    domicilio_preferido = get_domicilio_preferido(db,user_id)
    if not domicilio_preferido:
        raise NoDomicilioPreferidoException()

    try:
        nuevo_pedido = Pedido(
            numero=str(uuid.uuid4()),
            importe_productos=importe_productos,
            importe_envio=importe_envio,
            usuarios_id=user_id,
            metodos_pago_id=checkout.metodo_de_pago_id,
        )

        db.add(nuevo_pedido)
        db.flush()
        pedido_id = nuevo_pedido.id
        
        db.execute(text("""
            INSERT INTO detalles_pedido (pedidos_id, productos_id, cantidad, precio)
            SELECT 
                :p_id,                 
                productos_id,
                cantidad,
                precio
            FROM detalles_carrito
            WHERE usuarios_id = :u_id
            AND activo = true; 
        """), {"p_id": pedido_id, "u_id": user_id})

        nuevo_envio = Envio(
            pedidos_id=pedido_id,
            domicilios_id=domicilio_preferido.id,
            estado=EstadoEnvioEnum.PENDIENTE,
            numero_seguimiento = generar_numero_seguimiento()
        )

        db.add(nuevo_envio)
        
        db.query(DetalleCarrito).filter(
            DetalleCarrito.usuarios_id == user_id,
            DetalleCarrito.activo == True
        ).update(
            {DetalleCarrito.activo: False},
            synchronize_session=False
        )
        
        db.commit()
        db.refresh(nuevo_pedido)
        return nuevo_pedido
        
    except Exception as e:
        db.rollback() 
        raise e