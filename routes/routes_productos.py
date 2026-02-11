from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_usuarios import Usuario
from models.models_productos import Producto
from schemas.schema_producto import ProductoResponder,ProductoBase
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from services.service_producto import get_productos,get_producto_por_id,post_producto
from dependencies.dependencies_autenticacion import get_current_user

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

@router.get('/{id}',response_model=ProductoResponder)
def leer_producto_por_id(id:str,db: Session = Depends(get_db)):
    return get_producto_por_id(db,id)

@router.post('/', response_model=ProductoResponder)
async def crear_producto(
    nombre: str = Form(...),
    precio: float = Form(...),
    sku: str = Form(...),
    color: str = Form(...),
    marca: str = Form(...),
    descripcion: str = Form(""),
    peso: float = Form(...),
    alto: float = Form(...),
    ancho: float = Form(...),
    profundidad: float = Form(...),
    categorias_id: str = Form(...),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return post_producto(
        db,
        current_user.rol,
        nombre,
        precio,
        sku,
        color,
        marca,
        descripcion,
        peso,
        alto,
        ancho,
        profundidad,
        categorias_id,
        imagen
    )
