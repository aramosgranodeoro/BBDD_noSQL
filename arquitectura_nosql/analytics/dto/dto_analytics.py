from pydantic import BaseModel
import requests, time

class DTOAnalytics(BaseModel):
    evento: dict
    operacion: str


