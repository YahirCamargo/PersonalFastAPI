from sqlalchemy.orm import Session
from typing import List
from exceptions.exceptions_autenticacion import NoAccesoAlRecursoException
from exceptions.exceptions_productos import ProductoNoExistenteException
from models.models_productos import Producto
from schemas.schema_producto import ProductoBase
from core.cloudinary import upload_image
from fastapi import UploadFile, File, Form

def get_productos(db:Session) -> List[Producto]:
    return db.query(Producto).filter(Producto.activo==True).all()

def get_producto_por_id(db:Session,producto_id:str):
    producto = db.query(Producto).filter(Producto.id == producto_id,Producto.activo==True).first()
    if not producto:
        raise ProductoNoExistenteException()
    return producto



def post_producto(
    db: Session,
    user_role: str,
    nombre: str,
    precio: float,
    sku: str,
    color: str,
    marca: str,
    descripcion: str,
    peso: float,
    alto: float,
    ancho: float,
    profundidad: float,
    categorias_id: str,
    imagen: UploadFile):
    
    if user_role != 'admin':
        raise NoAccesoAlRecursoException()

    url_producto = upload_image(imagen)

    nuevo_producto = Producto(
        nombre=nombre,
        precio=precio,
        sku=sku,
        color=color,
        marca=marca,
        descripcion=descripcion,
        peso=peso,
        alto=alto,
        ancho=ancho,
        profundidad=profundidad,
        activo=True,
        categorias_id=categorias_id,
        url_producto=url_producto
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto
