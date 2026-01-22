from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.models_usuarios import Usuario
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas.schema_checkout import CheckoutBase
from services.service_checkout import crear_pedido
from starlette import status
from dependencies.dependencies_autenticacion import get_current_user

router = APIRouter(prefix="/checkout",tags=["Checkout"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/',status_code=status.HTTP_201_CREATED)
def crear_detalles_carrito(checkout:CheckoutBase,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return crear_pedido(db,checkout,current_user.id)