import uuid
from sqlalchemy import Column, SmallInteger, Numeric, Boolean, CheckConstraint, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base

class DetalleCarrito(Base):
    __tablename__ = "detalles_carrito"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    cantidad = Column(SmallInteger, nullable=False, default=1)
    precio = Column(Numeric(7,2), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    productos_id = Column(
        UUID(as_uuid=True),
        ForeignKey("productos.id"),
        nullable=False,
        index=True
    )
    usuarios_id = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True
    )

    __table_args__ = (
        Index("idx_detalles_carrito_productos_id", "productos_id"),
        Index("idx_detalles_carrito_usuarios_id", "usuarios_id"),
        CheckConstraint("cantidad > 0", name="check_cantidad_positiva"),
        CheckConstraint("precio >= 0", name="check_precio_no_negativo"),
    )