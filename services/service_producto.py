from sqlalchemy.orm import Session
from typing import List
from models.models_productos import Producto

def get_productos(db:Session) -> List[Producto]:
    return db.query(Producto).all()

def get_producto_por_id(db:Session,producto_id:str):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return None
    return producto