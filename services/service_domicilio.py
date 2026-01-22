from sqlalchemy.orm import Session
from models.models_domicilios import Domicilios
from schemas.schema_domicilio import DomicilioBase,DomicilioActualizar
from exceptions.exceptions_domicilios import DomicilioNoExistenteException, NoDomicilioPreferidoException
from typing import List

def get_domicilios(db:Session,user_id:str)-> List[Domicilios]:
    return db.query(Domicilios).filter(Domicilios.usuarios_id == user_id,Domicilios.activo == True).all()

def get_domicilios_por_id(db:Session,domicilio_id:str,user_id:str):
    domicilio = db.query(Domicilios).filter(Domicilios.usuarios_id == user_id, Domicilios.id == domicilio_id,Domicilios.activo == True).first()
    if not domicilio:
        raise DomicilioNoExistenteException()
    return domicilio

def get_domicilio_preferido(db:Session,user_id:str):
    domicilio_preferido = db.query(Domicilios).filter(
        Domicilios.usuarios_id == user_id,
        Domicilios.activo == True,
        Domicilios.preferido == True
    ).first()
    if not domicilio_preferido:
        raise NoDomicilioPreferidoException()
    return domicilio_preferido

# Checar bien para saber si evitar domicilios repetidos
# Cambiar la logica para que pueda enviar el usuarios_id de forma directa, de forma optional
def post_domicilios(db:Session,domicilio:DomicilioBase,user_id:str):
    try:
        domicilio_a_crear = Domicilios(
            calle = domicilio.calle,
            numero = domicilio.numero,
            colonia = domicilio.colonia,
            cp = domicilio.cp,
            estado = domicilio.estado,
            ciudad = domicilio.ciudad,
            usuarios_id = user_id,
            preferido = domicilio.preferido
        )
        db.add(domicilio_a_crear)
        db.flush()
        
        if domicilio.preferido:
            desmarcar_domicilios_preferidos(db,user_id,domicilio_a_crear.id)

        db.commit()
        db.refresh(domicilio_a_crear)
        return domicilio_a_crear
    except Exception:
        db.rollback()
        raise

def patch_domicilios(db: Session, domicilio_id: str, domicilio_actualizado: DomicilioActualizar, user_id:str):
    try:
        domicilio_query = db.query(Domicilios).filter(
            Domicilios.id == domicilio_id,
            Domicilios.usuarios_id == user_id,
            Domicilios.activo == True
        )
        domicilio_obj = domicilio_query.first()
        
        if not domicilio_obj:
            raise DomicilioNoExistenteException()
        
        update_data = domicilio_actualizado.model_dump(exclude_unset=True)

        if update_data.get("preferido") is True:
            desmarcar_domicilios_preferidos(db, user_id, excluir_id=domicilio_id)

        for key, value in update_data.items():
            setattr(domicilio_obj, key, value)

        db.commit()
        db.refresh(domicilio_obj)
        return domicilio_obj
    except Exception:
        db.rollback()
        raise

def delete_domicilios(db:Session,domicilio_id:str,user_id:str):
    domicilio_a_borrar = db.query(Domicilios).filter(Domicilios.id == domicilio_id,Domicilios.usuarios_id == user_id,Domicilios.activo==True).first()
    if not domicilio_a_borrar:
        raise DomicilioNoExistenteException()
    domicilio_a_borrar.activo = False
    db.commit()
    db.refresh(domicilio_a_borrar)
    return domicilio_a_borrar

def desmarcar_domicilios_preferidos(db: Session, user_id: str, excluir_id: str | None = None):
    query = db.query(Domicilios).filter(
        Domicilios.usuarios_id == user_id,
        Domicilios.activo == True
    )

    if excluir_id:
        query = query.filter(Domicilios.id != excluir_id)

    query.update(
        {"preferido": False},
        synchronize_session=False
    )
