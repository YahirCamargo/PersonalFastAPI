import uuid
from sqlalchemy import Column, DateTime, Numeric, func,ForeignKey,String,Boolean,Index
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
from models.envios import EstadoEnvioEnum
class EstadoEnvioEnum(enum.Enum):
    PENDIENTE = "PENDIENTE"
    EN_TRANSITO = "EN_TRANSITO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

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
    importe_iva = Column(Numeric(7,2),nullable=True)
    total = Column(Numeric(8,2),nullable=True)
    estado = Column(Enum(EstadoEnvioEnum),nullable=False,default=EstadoEnvioEnum.PENDIENTE)


    __table_args__ = (
        Index("idx_fecha", "fecha"),
        Index("idx_usuario_fecha", "usuarios_id", "fecha"),
    )