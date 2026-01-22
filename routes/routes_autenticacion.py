from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from db.database import SessionLocal
from pydantic_settings import BaseSettings
from models.models_usuarios import Usuario
from schemas.schema_usuario import UsuarioCrear, UsuarioResponder,UsuarioLogin
from core.seguridad import hashear_contraseña, verificar_contraseña, crear_token_acceso,crear_refresh_token, CREDENTIALS_EXCEPTION
from fastapi.security import OAuth2PasswordRequestForm
from models.models_refresh_tokens import RefreshToken
from schemas.schema_autenticacion import TokenRefreshRequest, TokenPair
from starlette import status
from core.config import settings

from dependencies.dependencies_autenticacion import get_current_user


router = APIRouter(prefix="/auth",tags=["Auth"])




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/refresh-token', response_model=TokenPair)
def refresh_token(data: TokenRefreshRequest,db: Session = Depends(get_db)):
    token_antiguo = db.query(RefreshToken).filter(RefreshToken.token == data.refresh_token).first()

    if not token_antiguo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token de refresh inválido o no existe."
        )

    if token_antiguo.usado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token ya utilizado. Acceso denegado por seguridad."
        )

    if token_antiguo.expira_en < datetime.utcnow():
        db.delete(token_antiguo)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Sesión expirada. Por favor, inicie sesión nuevamente."
        )

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

@router.post('/register', response_model=UsuarioResponder,status_code=status.HTTP_201_CREATED)
def registrar(user: UsuarioCrear, db:Session=Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    contraseña_hasheada = hashear_contraseña(user.contrasena)
    nuevo_usuario = Usuario(
        nombre=user.nombre, 
        email=user.email, 
        contrasena=contraseña_hasheada,
        telefono=user.telefono,
        sexo=user.sexo,
        fecha_nacimiento=user.fecha_nacimiento,
        rol='cliente'
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not user or not verificar_contraseña(form_data.password, user.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = crear_token_acceso({"sub": user.email,"user_id": str(user.id),"rol": user.rol})
    refresh_token = crear_refresh_token(db,user.id)
    db.commit()
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "expires_in": settings.access_token_expire_minutes * 60
    }

@router.get('/perfil', response_model=UsuarioResponder)
def obtener_mi_perfil(current_user: Usuario = Depends(get_current_user)):
    return current_user