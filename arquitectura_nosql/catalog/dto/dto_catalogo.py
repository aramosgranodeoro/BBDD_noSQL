from pydantic import BaseModel

class DTOCatalogo(BaseModel):
    producto: dict | list | None
    operacion: str
