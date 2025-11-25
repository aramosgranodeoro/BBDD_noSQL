from pydantic import BaseModel

class DTOFinal(BaseModel):
    catalog: dict
    recommendation: dict
    analytics: dict
    producto: dict | None
