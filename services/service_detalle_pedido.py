from sqlalchemy.orm import Session
from models.models_pedidos import Pedido
from models.models_detalles_pedido import DetallePedido
from schemas.schema_detalle_pedido import DetallePedidoBase,DetallePedidoActualizar
from exceptions.exceptions_detalles_pedido import DetallePedidoNoExistenteException
from typing import List

def get_detalles_pedido(db:Session,user_id:str) -> List[DetallePedido]:
    envio = db.query(DetallePedido).join(
        Pedido,
        DetallePedido.pedidos_id == Pedido.id,
    ).filter(
        Pedido.usuarios_id == user_id,
        DetallePedido.activo == True
    ).all()
    return envio

def get_detalles_pedido_por_id(db:Session,detalle_pedido_id:str,user_id:str):
    envio = db.query(DetallePedido).join(
        Pedido,
        DetallePedido.pedidos_id == Pedido.id,
    ).filter(
        Pedido.usuarios_id == user_id,
        DetallePedido.id == detalle_pedido_id,
        DetallePedido.activo == True
    ).first()
    if not envio:
        raise DetallePedidoNoExistenteException()
    return envio
    

# No sirve, luego quitar
def post_detalles_pedido(db:Session,detalle_pedido:DetallePedidoBase,user_id:str):
    detalle_pedido_a_crear = DetallePedido(
        cantidad=detalle_pedido.cantidad,
        precio=detalle_pedido.precio,
        productos_id = detalle_pedido.productos_id,
        pedidos_id = detalle_pedido.pedidos_id
    )
    db.add(detalle_pedido_a_crear)
    db.commit()
    db.refresh(detalle_pedido_a_crear)
    return detalle_pedido_a_crear

def patch_detalles_pedido(db:Session,detalle_pedido_id:str,detalle_pedido:DetallePedidoActualizar):
    detalle_pedido_a_actualizar = db.query(DetallePedido).filter(DetallePedido.id == detalle_pedido_id,DetallePedido.activo == True).first()
    if not detalle_pedido_a_actualizar:
        raise DetallePedidoNoExistenteException()
    update_data = detalle_pedido.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(detalle_pedido_a_actualizar, key, value)
    db.commit()
    db.refresh(detalle_pedido_a_actualizar)
    return detalle_pedido_a_actualizar

def delete_detalles_pedido(db:Session,detalle_pedido_id:str):
    detalle_pedido_a_borrar = db.query(DetallePedido).filter(DetallePedido.id == detalle_pedido_id,DetallePedido.activo == True).first()
    if not detalle_pedido_a_borrar:
        raise DetallePedidoNoExistenteException()
    detalle_pedido_a_borrar.activo = False
    db.commit()
    db.refresh(detalle_pedido_a_borrar)
    return detalle_pedido_a_borrar