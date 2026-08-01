from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional
from uuid import UUID

class PedidoBase(BaseModel):
    numero:str=Field(max_length=36)
    importe_productos:Decimal=Field(...,decimal_places=2,le=Decimal("99999999.99"))
    importe_envio:Decimal=Field(...,decimal_places=2,le=Decimal("9999.99"))
    metodos_pago_id:UUID
    fecha_hora_pago:datetime | None

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        }

class PedidoActualizar(BaseModel):
    numero:Optional[str]=Field(max_length=36)
    importe_productos:Optional[Decimal]
    importe_envio:Optional[Decimal]
    fecha_hora_pago:Optional[datetime] | Optional[None]
    metodos_pago_id: Optional[int] = None
    fecha_hora_pago: Optional[datetime] = None
    

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        }

class PedidoCheckout(BaseModel):
    metodos_pago_id: UUID
    domicilios_id: UUID

class PedidoResponder(PedidoBase):
    id:UUID
    
    class Config:
        from_attributes=True
