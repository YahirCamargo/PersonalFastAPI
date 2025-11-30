from pydantic import BaseModel, Field
from typing import Optional

class CategoriaBase(BaseModel):
    nombre:str=Field(max_length=40)

class CategoriaActualizar(BaseModel):
    nombre:Optional[str] | None

class CategoriaResponder(CategoriaBase):
    id:int

    class Config:
        from_attributes=True