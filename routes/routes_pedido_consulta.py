from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_usuarios import Usuario
from services.service_pedido_consulta import get_pedido_completo,get_pedidos_no_entregados
from starlette import status
from dependencies.dependencies_autenticacion import get_current_user

router = APIRouter(prefix="/orders-check",tags=["Orders Check"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List)
def obtener_pedidos(db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return get_pedidos_no_entregados(db,current_user.id)


@router.get('/{pedido_id}')
def obtener_pedidos_por_id(pedido_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    pedido = get_pedido_completo(db,pedido_id,current_user.id)
    if not pedido:
        raise HTTPException(status_code=404,detail="Pedido no encontrado")
    return pedido
