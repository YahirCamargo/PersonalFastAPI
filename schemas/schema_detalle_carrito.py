from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from uuid import UUID


class DetalleCarritoBase(BaseModel):
    cantidad:int
    precio:Decimal=Field(...,decimal_places=2, le=Decimal("99999.99"))
    productos_id:UUID

class DetalleCarritoCrear(BaseModel):
    cantidad:int
    productos_id:UUID
    
class DetalleCarritoActualizar(BaseModel):
    cantidad:Optional[int]

class DetalleCarritoResponder(DetalleCarritoBase):
    id:UUID

    class Config:
        from_attributes=True
    



"""
 id = Column(SMALLINT(unsigned=True), primary_key=True, nullable=False, autoincrement=True)
    cantidad = Column(TINYINT(unsigned=True), nullable=False, default=1)
    precio = Column(Numeric(7,2), nullable=False)
    productos_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("productos.id"),
        nullable=False,
        index=True
    )
    usuarios_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("usuarios.id"),
        nulleable=False,
        index=True
    )
"""