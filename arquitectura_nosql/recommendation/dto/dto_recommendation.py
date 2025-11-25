from pydantic import BaseModel

class ProductoScore(BaseModel):
    producto: str
    vistas: float | None
    operacion: str
