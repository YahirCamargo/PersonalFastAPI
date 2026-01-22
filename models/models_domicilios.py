import uuid
from sqlalchemy import Column, String, ForeignKey, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base

class Domicilios(Base):
    __tablename__ = "domicilios"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True,default=uuid.uuid4)
    calle = Column(String(45), nullable=False)
    numero = Column(String(10), nullable=False) #Ej 123A, S/N, 456-B
    colonia = Column(String(30), nullable=False)
    cp = Column(String(5), nullable=False)
    estado = Column(String(20), nullable=False)
    ciudad = Column(String(45),nullable=False)
    preferido = Column(Boolean, nullable=False, default=False)
    activo = Column(Boolean, nullable=False, default=True)
    usuarios_id = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id",onupdate="CASCADE",ondelete="CASCADE"),
        index=True,
    )
    __table_args__ = (
        Index('idx_estado_ciudad', 'estado', 'ciudad'),
    )

