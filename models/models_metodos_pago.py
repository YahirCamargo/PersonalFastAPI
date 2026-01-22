import uuid
from sqlalchemy import Column, String, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base

class MetodoPago(Base):
    __tablename__ = "metodos_pago"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4, nullable=False)
    nombre = Column(String(25), nullable=False, index=True)
    comision = Column(Numeric(4,2),nullable=False, default=1.5)
    activo = Column(Boolean, nullable=False, default=True)
