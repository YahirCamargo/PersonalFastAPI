from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import date
from uuid import UUID

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCrear(UsuarioBase):
    contrasena:str=Field(...,min_length=8)

class UsuarioCompletarPerfil(BaseModel):
    telefono: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None


class UsuarioLogin(BaseModel):
    email:EmailStr
    contrasena:str

class UsuarioResponder(UsuarioBase):
    id:UUID
    rol:str

    class Config:
        from_attributes = True