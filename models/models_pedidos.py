import uuid
from sqlalchemy import Column, DateTime, Numeric, func,ForeignKey,String,Boolean
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4, primary_key=True)
    fecha = Column(DateTime, nullable=False, server_default=func.now())
    numero = Column(String(36),nullable=False,unique=True)
    importe_productos = Column(Numeric(10,2),nullable=False)
    importe_envio = Column(Numeric(6,2),nullable=False)
    fecha_hora_pago = Column(DateTime,nullable=True)
    activo = Column(Boolean, nullable=False, default=True)
    usuarios_id = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    metodos_pago_id = Column(
        UUID(as_uuid=True),
        ForeignKey("metodos_pago.id"),
        default='1',
        nullable=False,
        index=True,
    )
    