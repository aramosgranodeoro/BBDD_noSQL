from pydantic import BaseModel
from typing import Union, List, Dict, Any

class DTOFinal(BaseModel):
    recommendation: dict
    analytics: dict
    # Aceptamos dict (un producto), list (varios) o None (borrado)
    producto: Union[Dict[str, Any], List[Any], None]