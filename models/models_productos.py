import uuid
from sqlalchemy import Column, Numeric,ForeignKey,String, Boolean
from sqlalchemy.dialects.postgresql import UUID,TEXT
from db.database import Base

class Producto(Base):
    __tablename__ = "productos"
    id = Column(UUID(as_uuid=True),nullable=False,primary_key=True,default=uuid.uuid4)
    nombre = Column(String(60),nullable=False)
    precio = Column(Numeric(7,2), nullable=False,index=True)
    sku = Column(String(15), nullable=False,unique=True)
    color = Column(String(15),nullable=False)
    marca = Column(String(20),nullable=False,index=True)
    descripcion = Column(TEXT,nullable=True)
    peso = Column(Numeric(5,1),nullable=False)
    alto = Column(Numeric(5,1),nullable=False,default=0.0)
    ancho = Column(Numeric(5,1),nullable=False,default=0.0)
    profundidad = Column(Numeric(5,1),nullable=False,default=0.0)
    activo = Column(Boolean, nullable=False, default=True)
    categorias_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categorias.id"),
        index=True,
        nullable=False
    )
    url_producto = Column(String(255),nullable=False)

