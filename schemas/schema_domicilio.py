from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class DomicilioBase(BaseModel):
    calle:str=Field(...,max_length=45)
    numero:str=Field(...,max_length=10)
    colonia:str=Field(...,max_length=30)
    cp:str=Field(...,min_length=5,max_length=5)
    estado:str=Field(...,max_length=20)
    detalles: Optional[str] =Field()
    destinatario:str=Field(...,max_length=100)
    ciudad:str=Field(...,max_length=45)
    preferido:bool

class DomicilioActualizar(BaseModel):
    calle: Optional[str] = Field(None, max_length=45) 
    numero: Optional[str] = Field(None, max_length=10)
    colonia: Optional[str] = Field(None, max_length=30)
    cp: Optional[str] = Field(None, max_length=5)
    estado: Optional[str] = Field(None, max_length=20)
    ciudad: Optional[str] = Field(None, max_length=45)
    detalles:Optional[str] =Field(None, max_length=100)
    destinatario:Optional[str] =Field(None,max_length=60)
    preferido: Optional[bool] = None

class DomicilioResponder(DomicilioBase):
    id:UUID

    class Config():
        from_attributes=True
