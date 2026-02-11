from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models_usuarios import Usuario
from services.service_autenticacion import post_refresh_token,post_registrar,post_login,get_obtener_mi_perfil,patch_completar_perfil,post_registrar_admin
from schemas.schema_usuario import UsuarioCrear, UsuarioResponder,UsuarioCompletarPerfil
from fastapi.security import OAuth2PasswordRequestForm
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
    return post_refresh_token(data,db)

@router.post('/register', response_model=UsuarioResponder,status_code=status.HTTP_201_CREATED)
def registrar(user: UsuarioCrear, db:Session=Depends(get_db)):
    return post_registrar(user,db)

@router.post('/register-admin', response_model=UsuarioResponder,status_code=status.HTTP_201_CREATED)
def registrar(user: UsuarioCrear, db:Session=Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return post_registrar_admin(user,current_user,db)

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return post_login(form_data,db)

@router.get('/perfil', response_model=UsuarioResponder)
def obtener_mi_perfil(current_user: Usuario = Depends(get_current_user)):
    return get_obtener_mi_perfil(current_user)

@router.patch('/perfil', response_model=UsuarioResponder)
def completar_perfil(data: UsuarioCompletarPerfil,db: Session = Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    return patch_completar_perfil(data, current_user, db)
