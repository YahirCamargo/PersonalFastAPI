from core.config import settings
from datetime import datetime
from sqlalchemy.orm import Session
from models.models_usuarios import Usuario
from schemas.schema_usuario import UsuarioCrear,UsuarioCompletarPerfil
from fastapi.security import OAuth2PasswordRequestForm
from models.models_refresh_tokens import RefreshToken
from schemas.schema_autenticacion import TokenRefreshRequest
from exceptions.exceptions_autenticacion import NoAutorizadoException,CorreoYaRegistadoException,SesionExpiradaException,TokenNoValidoException,TokenYaUsadoException,UsuarioNoExistenteException, NoAccesoAlRecursoException
from core.seguridad import hashear_contraseña, verificar_contraseña, crear_token_acceso,crear_refresh_token


def post_refresh_token(data: TokenRefreshRequest,db: Session):
    token_antiguo = db.query(RefreshToken).filter(RefreshToken.token == data.refresh_token).first()

    if not token_antiguo:
        raise TokenNoValidoException()

    if token_antiguo.usado:
        raise TokenYaUsadoException()

    if token_antiguo.expira_en < datetime.utcnow():
        db.delete(token_antiguo)
        db.commit()
        raise SesionExpiradaException()

    user_id = token_antiguo.usuarios_id
    user_actual = db.query(Usuario).filter(Usuario.id == user_id).first()

    token_antiguo.usado = True
    db.add(token_antiguo)

    nuevo_access_token = crear_token_acceso({
        "sub": user_actual.email,
        "rol": user_actual.rol,
        "user_id": str(user_actual.id)
    })
    nuevo_refresh_token_str = crear_refresh_token(db, user_id)
    
    db.commit()

    return {
        "access_token": nuevo_access_token,
        "token_type": "bearer",
        "refresh_token": nuevo_refresh_token_str,
        "expires_in": settings.access_token_expire_minutes * 60
    }

def post_registrar(user: UsuarioCrear, db:Session):
    existing_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existing_user:
        raise CorreoYaRegistadoException()
    contraseña_hasheada = hashear_contraseña(user.contrasena)
    nuevo_usuario = Usuario(
        nombre=user.nombre, 
        email=user.email, 
        contrasena=contraseña_hasheada,
        activo=True,
        rol='cliente'
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def post_registrar_admin(user:UsuarioCrear,current_user: Usuario, db:Session):
    existing_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existing_user:
        raise CorreoYaRegistadoException()
    if current_user.rol != 'admin':
        raise NoAccesoAlRecursoException()
    contraseña_hasheada = hashear_contraseña(user.contrasena)
    nuevo_usuario = Usuario(
        nombre=user.nombre, 
        email=user.email, 
        contrasena=contraseña_hasheada,
        activo=True,
        rol='admin'
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def post_login(form_data: OAuth2PasswordRequestForm , db:Session):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not user or not verificar_contraseña(form_data.password, user.contrasena):
        raise NoAutorizadoException()
    
    access_token = crear_token_acceso({"sub": user.email,"user_id": str(user.id),"rol": user.rol})
    refresh_token = crear_refresh_token(db,user.id)
    db.commit()
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "expires_in": settings.access_token_expire_minutes * 60
    }

def get_obtener_mi_perfil(current_user: Usuario):
    return current_user

def patch_completar_perfil(data: UsuarioCompletarPerfil,current_user: Usuario,db: Session):
    user_db = db.query(Usuario).filter(Usuario.id == current_user.id).first()

    if not user_db:
        raise UsuarioNoExistenteException()

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return user_db

