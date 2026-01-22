from sqlalchemy.orm import Session
from models.models_categorias import Categoria
from schemas.schema_categoria import CategoriaBase
from exceptions.exceptions_categorias import CategoriaNoExistenteException,CategoriaYaExisteException
from uuid import UUID

def get_categoria(db:Session):
    return db.query(Categoria).filter(Categoria.activo == True).all()

# Poner exepcion para si la categoria existe pero esta desactivada
def post_categoria(db:Session,categoria:CategoriaBase):
    resultado = db.query(Categoria).filter(
        Categoria.nombre == categoria.nombre
        ).first()
    if not resultado:
        nueva_categoria = Categoria(
            nombre = categoria.nombre
        )
        db.add(nueva_categoria)
        db.commit()
        db.refresh(nueva_categoria)
        return nueva_categoria
    
    if resultado:
        raise CategoriaYaExisteException()
    
    

def put_categoria(db:Session,categoria_id:UUID,categoria_actualizada:CategoriaBase):
    categoria_a_actualizar = db.query(Categoria).filter(Categoria.id == categoria_id,Categoria.activo == True).first()
    if not categoria_a_actualizar:
        raise CategoriaNoExistenteException()
    
    categoria_a_actualizar.nombre = categoria_actualizada.nombre
    db.commit()
    db.refresh(categoria_a_actualizar)
    return categoria_a_actualizar

def delete_categoria(db:Session,categoria_id:UUID):
    categoria_a_borrar = db.query(Categoria).filter(Categoria.id == categoria_id,Categoria.activo == True).first()
    if not categoria_a_borrar:
        raise CategoriaNoExistenteException()
    categoria_a_borrar.activo = False
    db.commit()
    db.refresh(categoria_a_borrar)
    return categoria_a_borrar