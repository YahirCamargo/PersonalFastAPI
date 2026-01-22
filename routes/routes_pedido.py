from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_usuarios import Usuario
from models.models_pedidos import Pedido
from schemas.schema_pedido import PedidoBase, PedidoActualizar, PedidoResponder, PedidoCheckout
from services.service_pedido import get_pedido,get_pedido_por_id, post_pedido, patch_pedido, delete_pedido
from starlette import status
from dependencies.dependencies_autenticacion import get_current_user

router = APIRouter(prefix="/orders",tags=["Orders"])
IMPORTE_ENVIO = 80.00

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[PedidoResponder])
def obtener_pedidos(db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return get_pedido(db,current_user.id)

@router.get('/{pedido_id}',response_model=PedidoResponder)
def obtener_pedidos_por_id(pedido_id:str,db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    pedido = get_pedido_por_id(db,pedido_id,current_user.id)
    if not pedido:
        raise HTTPException(status_code=404,detail="Pedido no encontrado")
    return pedido
