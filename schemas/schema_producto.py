from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from uuid import UUID

class ProductoBase(BaseModel):
    nombre: str = Field(..., max_length=60)
    precio: Decimal = Field(..., decimal_places=2, le=Decimal("99999.99"))
    sku: str = Field(..., max_length=15, description="Código Único de Producto")
    color: str = Field(default="desconocido", max_length=15)
    marca: str = Field(..., max_length=20)
    descripcion: Optional[str] = Field(None, description="Descripción larga del producto")
    peso: Decimal = Field(..., decimal_places=1, le=Decimal("9999.9"), description="Peso en kg")
    alto: Decimal = Field(default=Decimal("0.0"), decimal_places=1, le=Decimal("9999.9"))
    ancho: Decimal = Field(default=Decimal("0.0"), decimal_places=1, le=Decimal("9999.9"))
    profundidad: Decimal = Field(default=Decimal("0.0"), decimal_places=1, le=Decimal("9999.9"))
    categorias_id: UUID = Field(..., description="ID de la Categoría asociada")
    url_producto: str = Field(..., max_length=255, description="URL de la imagen o ficha del producto")

    class Config:
        from_attributes = True 
        json_encoders = {Decimal: lambda v: str(v)}

class ProductoActualizar(BaseModel):
    nombre: Optional[str] = Field(None, max_length=60)
    precio: Optional[Decimal] = Field(None, decimal_places=2, le=Decimal("99999.99"))
    sku: Optional[str] = Field(None, max_length=15)
    color: Optional[str] = Field(None, max_length=15)
    marca: Optional[str] = Field(None, max_length=20)
    descripcion: Optional[str] = None
    peso: Optional[Decimal] = Field(None, decimal_places=1, le=Decimal("9999.9"))
    alto: Optional[Decimal] = Field(None, decimal_places=1, le=Decimal("9999.9"))
    ancho: Optional[Decimal] = Field(None, decimal_places=1, le=Decimal("9999.9"))
    profundidad: Optional[Decimal] = Field(None, decimal_places=1, le=Decimal("9999.9"))
    categorias_id: Optional[UUID] = None
    url_producto: Optional[str] = Field(None, max_length=255)

    class Config:
        from_attributes = True
        json_encoders = {Decimal: lambda v: str(v)}

class ProductoResponder(ProductoBase):
    id: UUID 
    
    class Config:
        from_attributes = True
        json_encoders = {Decimal: lambda v: str(v)}