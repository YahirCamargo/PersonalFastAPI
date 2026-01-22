import uuid
from sqlalchemy import Column, String, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(40), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        Index("idx_categorias_nombre", "nombre"),
    )
