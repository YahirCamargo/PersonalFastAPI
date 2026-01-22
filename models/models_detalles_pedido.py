import uuid
from sqlalchemy import Column, Numeric, ForeignKey, Index, CheckConstraint, Boolean, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base

class DetallePedido(Base):
    __tablename__ = "detalles_pedido"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cantidad = Column(SmallInteger, nullable=False)
    precio = Column(Numeric(7, 2), nullable=False)
    productos_id = Column(
        UUID(as_uuid=True),
        ForeignKey("productos.id", onupdate="CASCADE"),
        nullable=False
    )
    pedidos_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pedidos.id", ondelete="CASCADE"),
        nullable=False
    )
    activo = Column(Boolean, nullable=False, default=True)
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="chk_detalles_pedido_cantidad"),
        Index("idx_detalles_pedido_pedido_producto", "pedidos_id", "productos_id"),
    )
