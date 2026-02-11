from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_categorias import Categoria
from schemas.schema_categoria import CategoriaBase,CategoriaResponder
from services.service_categoria import get_categoria,post_categoria,put_categoria,delete_categoria
from starlette import status

router = APIRouter(prefix="/categories",tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=List[CategoriaResponder])
def obtener_categoria(db:Session=Depends(get_db)):
    return get_categoria(db)

@router.post('/',response_model=CategoriaResponder,status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria:CategoriaBase,db:Session=Depends(get_db)):
    return post_categoria(db,categoria)

@router.put('/{id}',response_model=CategoriaResponder)
def actualizar_categoria(id:str,categoria_actualizada:CategoriaBase,db:Session=Depends(get_db)): 
    return put_categoria(db,id,categoria_actualizada)

@router.delete('/{id}',response_model=CategoriaResponder)
def borrar_categoria(id:str,db:Session=Depends(get_db)):
    return delete_categoria(db,id)