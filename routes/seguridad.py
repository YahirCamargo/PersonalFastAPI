from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext
from pydantic_settings import BaseSettings
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta
from models.models_refresh_tokens import RefreshToken

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudieron validar las credenciales",
    headers={"WWW-Authenticate": "Bearer"},
)

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    refresh_token_expire_days:int
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
contraseña_contexto = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hashear_contraseña(password: str) -> str:
    return contraseña_contexto.hash(password)

def verificar_contraseña(plain_password: str, hashed_password: str):
    return contraseña_contexto.verify(plain_password, hashed_password)

def crear_refresh_token(db: Session, user_id: int) -> str:
    token_str = str(uuid.uuid4())
    expira = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    
    nuevo_refresh_token = RefreshToken(
        token=token_str,
        usuarios_id=user_id,
        expira_en=expira,
        usado=False
    )
    
    db.add(nuevo_refresh_token)
    db.flush() 
    
    return token_str

def crear_token_acceso(data: dict, expires_delta: timedelta | None = None):
    if "sub" not in data:
        raise ValueError("El token debe incluir el campo sub")
    to_encode = data.copy()
    expira = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def verificar_token(token:str,credenciales_excepcion:HTTPException = CREDENTIALS_EXCEPTION) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_exp": True} 
        )
        username:str=payload.get("sub")
        if username is None:
            raise credenciales_excepcion
        
        return payload 
    except JWTError as e:
        print(f"Error de JWT: {e}")
        raise credenciales_excepcion