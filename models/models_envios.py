import uuid
import enum
from sqlalchemy import (Column,String,ForeignKey,Boolean,Enum,Index,TIMESTAMP,func)
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base


class EstadoEnvioEnum(enum.Enum):
    PENDIENTE = "PENDIENTE"
    EN_TRANSITO = "EN_TRANSITO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"


class Envio(Base):
    __tablename__ = "envios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_entrega = Column(TIMESTAMP, nullable=True)
    fecha = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )
    estado = Column(
        Enum(EstadoEnvioEnum, name="estado_envio_enum"),
        nullable=False,
        default=EstadoEnvioEnum.PENDIENTE
    )
    numero_seguimiento = Column(String(50), nullable=False, unique=True)
    domicilios_id = Column(
        UUID(as_uuid=True),
        ForeignKey("domicilios.id", ondelete="RESTRICT"),
        nullable=False
    )
    pedidos_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pedidos.id", ondelete="CASCADE"),
        nullable=False
    )
    activo = Column(Boolean, nullable=False, default=True)
    __table_args__ = (
        Index("idx_envios_domicilios", "domicilios_id"),
        Index("idx_envios_pedidos", "pedidos_id"),
    )