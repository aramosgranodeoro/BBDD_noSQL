from fastapi import FastAPI, HTTPException
import requests
import time
import os
import json

from dto.dto_analytics import DTOAnalytics
from dto.dto_analytics_list import DTOListAnalytics

app = FastAPI()

# Host y puerto de Riak (HTTP)
RIAK_HOST = os.getenv("RIAK_HOST", "riak")
RIAK_PORT = os.getenv("RIAK_PORT", "8098")
RIAK_HOST_LOCAL = "localhost"

BUCKET_TYPE = "default"
BUCKET_NAME = "eventos"

BASE_URL = f"http://{RIAK_HOST}:{RIAK_PORT}/types/{BUCKET_TYPE}/buckets/{BUCKET_NAME}"
BASE_URL_LOCAL = f"http://{RIAK_HOST_LOCAL}:{RIAK_PORT}/types/{BUCKET_TYPE}/buckets/{BUCKET_NAME}"

def riak_key_url(key: str) -> str:
    return f"{BASE_URL}/keys/{key}"

def riak_key_url_local(key: str) -> str:
    return f"{BASE_URL_LOCAL}/keys/{key}"

# =====================================================================
# CREAR EVENTO
# =====================================================================
@app.post("/evento", response_model=DTOAnalytics)
def crear_evento(evento: dict):

    key = str(int(time.time() * 1000))
    evento["timestamp"] = evento.get("timestamp", int(time.time()))

    url = riak_key_url(key)
    headers = {"Content-Type": "application/json"}

    url_local = riak_key_url_local(key)

    resp = requests.put(url, headers=headers, data=json.dumps(evento))

    if resp.status_code not in (200, 204):
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar en Riak: {resp.text}"
        )
    
    evento_json = json.dumps(evento)
    evento_json_escaped = evento_json.replace('"', '\\"')

    return DTOAnalytics(
        evento=evento,
        operacion=f"curl -X PUT \"{url_local}\" -H \"Content-Type: application/json\" -d \"{evento_json_escaped}\""
    )


# =====================================================================
# OBTENER EVENTO POR ID
# =====================================================================
@app.get("/evento/{key}", response_model=DTOAnalytics)
def obtener_evento(key: str):

    url = riak_key_url(key)
    resp = requests.get(url)

    url_local = riak_key_url_local(key)

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    if resp.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Error al leer de Riak: {resp.text}"
        )

    try:
        data = resp.json()
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail="Datos corruptos en Riak (no JSON)"
        )

    return DTOAnalytics(
        evento=data,
        operacion=f"curl -X GET \"{url_local}\""
    )


# =====================================================================
# BORRAR EVENTO
# =====================================================================
@app.delete("/evento/{key}", response_model=DTOAnalytics)
def borrar_evento(key: str):

    url = riak_key_url(key)
    resp = requests.delete(url)

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    if resp.status_code not in (200, 204):
        raise HTTPException(
            status_code=500,
            detail=f"Error al borrar en Riak: {resp.text}"
        )

    return DTOAnalytics(
        evento={"key": key, "status": "borrado"},
        operacion=f"curl -X DELETE \"{url}\""
    )


# =====================================================================
# LISTAR TODAS LAS KEYS
# =====================================================================
@app.get("/eventos", response_model=DTOListAnalytics)
def listar_eventos():

    url = f"{BASE_URL}/keys?keys=true"
    resp = requests.get(url)

    if resp.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Error listando keys en Riak: {resp.text}"
        )

    data = resp.json()
    keys = data.get("keys", [])

    return DTOListAnalytics(
        evento=keys,
        operacion=f"curl -X GET \"{url}\""
    )
