from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_productos import Producto
from schemas.schema_producto import ProductoResponder
from services.service_producto import get_productos,get_producto_por_id

router = APIRouter(prefix="/products",tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[ProductoResponder])
def leer_productos(db: Session = Depends(get_db)):
    return get_productos(db)

@router.get('/{producto_id}',response_model=ProductoResponder)
def leer_producto_por_id(producto_id:str,db: Session = Depends(get_db)):
    return get_producto_por_id(db,producto_id)