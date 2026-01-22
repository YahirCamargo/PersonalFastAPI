from sqlalchemy.orm import Session
from typing import List
from models.models_productos import Producto
from models.models_detalles_carrito import DetalleCarrito
from schemas.schema_detalle_carrito import DetalleCarritoBase,DetalleCarritoActualizar,DetalleCarritoCrear
from exceptions.exceptions_productos import ProductoNoExistenteException
from exceptions.exceptions_detalles_carrito import DetalleCarritoNoExistenteException


def _get_detalle_activo(db: Session, detalle_id: str, user_id: str) -> DetalleCarrito | None:
    return db.query(DetalleCarrito).filter(
        DetalleCarrito.id == detalle_id,
        DetalleCarrito.usuarios_id == user_id,
        DetalleCarrito.activo == True
    ).first()


def get_detalle_carrito(db:Session,user_id:str) -> List[DetalleCarrito]:
    return db.query(DetalleCarrito).filter(DetalleCarrito.usuarios_id == user_id,DetalleCarrito.activo==True).all()

def get_detalle_carrito_por_id(db:Session,detalle_carrito_id:str,user_id:str):
    detalle_carrito = _get_detalle_activo(db,detalle_carrito_id,user_id)
    if not detalle_carrito:
        raise DetalleCarritoNoExistenteException()
    return detalle_carrito

def post_detalle_carrito(db: Session, detalle_carrito: DetalleCarritoCrear, user_id: str):
    try:
        detalle_existente = db.query(DetalleCarrito).filter(
            DetalleCarrito.productos_id == detalle_carrito.productos_id,
            DetalleCarrito.usuarios_id == user_id,
            DetalleCarrito.activo == True
        ).first()

        if detalle_existente:
            detalle_existente.cantidad += detalle_carrito.cantidad
            db.commit()
            db.refresh(detalle_existente)
            return detalle_existente

        producto = db.query(Producto).filter(
            Producto.id == detalle_carrito.productos_id,
            Producto.activo == True
        ).first()

        if not producto:
            raise ProductoNoExistenteException()

        nuevo_detalle = DetalleCarrito(
            cantidad=detalle_carrito.cantidad,
            precio=producto.precio,
            productos_id=detalle_carrito.productos_id,
            usuarios_id=user_id
        )

        db.add(nuevo_detalle)
        db.commit()
        db.refresh(nuevo_detalle)
        return nuevo_detalle

    except Exception:
        db.rollback()
        raise


def patch_detalle_carrito(db:Session,detalle_carrito_id:str,detalle_carrito_actualizado:DetalleCarritoActualizar,user_id:str):
    detalle_carrito_a_actualizar = _get_detalle_activo(db,detalle_carrito_id,user_id)

    if not detalle_carrito_a_actualizar:
        raise DetalleCarritoNoExistenteException()
    
    update_data = detalle_carrito_actualizado.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(detalle_carrito_a_actualizar, key, value)

    db.commit()
    db.refresh(detalle_carrito_a_actualizar)
    return detalle_carrito_a_actualizar

def delete_detalle_carrito(db:Session,detalle_carrito_id:str,user_id:str):
    detalle_carrito_a_borrar = _get_detalle_activo(db,detalle_carrito_id,user_id)

    if not detalle_carrito_a_borrar:
        raise DetalleCarritoNoExistenteException()
    detalle_carrito_a_borrar.activo = False
    db.commit()
    db.refresh(detalle_carrito_a_borrar)
    return detalle_carrito_a_borrar
