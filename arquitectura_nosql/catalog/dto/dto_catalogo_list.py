from pydantic import BaseModel

class DTOCatalogos(BaseModel):
    producto: dict | list 
    operacion: str | list
