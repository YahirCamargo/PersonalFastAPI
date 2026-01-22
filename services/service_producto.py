from sqlalchemy.orm import Session
from typing import List
from exceptions.exceptions_productos import ProductoNoExistenteException
from models.models_productos import Producto

def get_productos(db:Session) -> List[Producto]:
    return db.query(Producto).filter(Producto.activo==True).all()

def get_producto_por_id(db:Session,producto_id:str):
    producto = db.query(Producto).filter(Producto.id == producto_id,Producto.activo==True).first()
    if not producto:
        raise ProductoNoExistenteException()
    return producto