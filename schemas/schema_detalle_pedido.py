from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from uuid import UUID

class DetallePedidoBase(BaseModel):
    cantidad : int
    precio :Decimal=Field(...,decimal_places=2, le=Decimal("99999.99"))
    productos_id:UUID
    pedidos_id:UUID

class DetallePedidoActualizar(BaseModel):
    cantidad : Optional[int]
    precio : Optional[Decimal]=Field(None,decimal_places=2, le=Decimal("99999.99"))
    productos_id: Optional[UUID] = None
    pedidos_id: Optional[UUID] = None

class DetallePedidoResponder(DetallePedidoBase):
    id : UUID

    class Config:
        from_attributes=True

"""
    id = Column(SMALLINT(unsigned=True),nullable=False,autoincrement=True,primary_key=True)
    cantidad = Column(TINYINT(unsigned=True),nullable=False)
    precio = Column(Numeric(7,2),nullable=False)
    productos_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("productos.id",onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    pedidos_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("pedidos.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )
"""