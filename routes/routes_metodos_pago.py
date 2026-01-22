from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_metodos_pago import MetodoPago
from schemas.schema_metodo_pago import MetodoPagoBase,MetodoPagoResponder
from services.service_metodo_pago import obtener_metodo_pago,crear_metodo_pago,actualizar_metodo_pago,borrar_metodo_pago
from starlette import status

router = APIRouter(prefix="/payment-methods",tags=["Payment Methods"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/',response_model=List[MetodoPagoResponder])
def leer_metodos_pago(db: Session = Depends(get_db)):
    return obtener_metodo_pago(db)

@router.post('/',response_model=MetodoPagoResponder,status_code=status.HTTP_201_CREATED)
def crear_metodos_pagp(metodo: MetodoPagoBase, db:Session=Depends(get_db)):
    return crear_metodo_pago(db,metodo)

@router.put('/{metodo_id}',response_model=MetodoPagoResponder)
def actualizar_metodos_pago(metodo_id:str,metodo_actualizar:MetodoPagoBase,db:Session=Depends(get_db)):
    return actualizar_metodo_pago(metodo_id,metodo_actualizar,db)

@router.delete('/{metodo_id}',response_model=MetodoPagoResponder)
def eliminar_metodo_pago(metodo_id:str,db:Session=Depends(get_db)):
    return borrar_metodo_pago(db,metodo_id)
