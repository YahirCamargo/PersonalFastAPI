from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import date
from uuid import UUID

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCrear(UsuarioBase):
    contrasena:str=Field(...,min_length=8)
    telefono:str=Field(...,max_length=10)
    sexo:Literal["H","M"]
    fecha_nacimiento:date


class UsuarioLogin(BaseModel):
    email:EmailStr
    contrasena:str

class UsuarioResponder(UsuarioBase):
    id:UUID
    rol:str

    class Config:
        from_attributes = True