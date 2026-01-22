import uuid
from sqlalchemy import Column, Numeric, ForeignKey, SmallInteger, Boolean
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