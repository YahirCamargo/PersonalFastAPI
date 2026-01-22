import uuid
from sqlalchemy import Column, String, Text, Date, TIMESTAMP, func,Boolean
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
import enum


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(45), nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    telefono = Column(String(10))
    sexo = Column(String(1), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    contrasena = Column(Text, nullable=False)
    fecha_registro = Column(TIMESTAMP,nullable=False,server_default=func.now(),index=True)
    rol = Column(String(20),default="cliente",nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
