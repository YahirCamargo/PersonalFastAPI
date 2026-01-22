from pydantic import BaseModel, Field
from decimal import Decimal
from uuid import UUID

class MetodoPagoBase(BaseModel):
    nombre:str
    comision:Decimal=Field(...,decimal_places=2,le=Decimal("99.99"))


class MetodoPagoResponder(MetodoPagoBase):
    id:UUID

    class Config:
        from_attributes = True