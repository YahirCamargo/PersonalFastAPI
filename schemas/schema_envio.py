from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class EnvioBase(BaseModel):
    fecha_entrega : Optional[datetime] = None
    estado: str #dejar pendiente
    numero_seguimiento : str=Field(...,max_length=20)
    pedidos_id : UUID

class EnvioActualizar(BaseModel):
    fecha_entrega : Optional[datetime]
    estado: Optional[str] #dejar pendiente
    numero_seguimiento : Optional[str]=Field(None,max_length=20)

class EnviosResponder(EnvioBase):
    id : UUID
    fecha : datetime
    
    class Config:
        from_attributes = True
