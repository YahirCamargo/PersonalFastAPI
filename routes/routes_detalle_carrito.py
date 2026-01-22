from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.models_usuarios import Usuario
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_detalles_carrito import DetalleCarrito
from schemas.schema_detalle_carrito import DetalleCarritoBase,DetalleCarritoActualizar,DetalleCarritoResponder,DetalleCarritoCrear
from services.service_detalle_carrito import get_detalle_carrito,get_detalle_carrito_por_id,post_detalle_carrito,patch_detalle_carrito,delete_detalle_carrito
from starlette import status
from dependencies.dependencies_autenticacion import get_current_user

router = APIRouter(prefix="/cart",tags=["Carts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[DetalleCarritoResponder])
def obtener_detalles_carrito(db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return get_detalle_carrito(db,current_user.id)

@router.get('/{detalle_carrito_id}',response_model=DetalleCarritoResponder)
def obtener_detalles_carrito_por_id(detalle_carrito_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return get_detalle_carrito_por_id(db,detalle_carrito_id,current_user.id)

@router.post('/',response_model=DetalleCarritoResponder,status_code=status.HTTP_201_CREATED)
def crear_detalles_carrito(detalle_carrito:DetalleCarritoCrear,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return post_detalle_carrito(db,detalle_carrito,current_user.id)

@router.patch('/{detalle_pedido_id}',response_model=DetalleCarritoResponder)
def actualizar_detalles_carrito(detalle_carrito_id:str,detalle_carrito:DetalleCarritoActualizar,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return patch_detalle_carrito(db,detalle_carrito_id,detalle_carrito,current_user.id)

@router.delete('/{detalle_pedido_id}',response_model=DetalleCarritoResponder)
def borrar_detalles_carrito(detalle_carrito_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return delete_detalle_carrito(db,detalle_carrito_id,current_user.id)