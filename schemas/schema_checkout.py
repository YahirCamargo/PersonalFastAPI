from pydantic import BaseModel
from uuid import UUID


class CheckoutBase(BaseModel):
    metodo_de_pago_id:UUID
