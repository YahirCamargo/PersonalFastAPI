import uuid
from sqlalchemy import Column, Numeric, ForeignKey, SmallInteger, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base

class DetalleCarrito(Base):
    __tablename__ = "detalles_carrito"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    cantidad = Column(SmallInteger, nullable=False, default=1, check="cantidad > 0")
    precio = Column(Numeric(7,2), nullable=False, check="precio >= 0")
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
    )