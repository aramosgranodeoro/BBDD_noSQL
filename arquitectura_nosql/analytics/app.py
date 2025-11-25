from fastapi import FastAPI, HTTPException
import requests
import time
import os
import json
from dto.dto_analytics import DTOAnalytics as EventoDTO

app = FastAPI()

# Host y puerto de Riak (HTTP)
RIAK_HOST = os.getenv("RIAK_HOST", "riak")
RIAK_PORT = os.getenv("RIAK_PORT", "8098")

BUCKET_TYPE = "default"
BUCKET_NAME = "eventos"

BASE_URL = f"http://{RIAK_HOST}:{RIAK_PORT}/types/{BUCKET_TYPE}/buckets/{BUCKET_NAME}"


def riak_key_url(key: str) -> str:
    return f"{BASE_URL}/keys/{key}"


@app.post("/evento", response_model=EventoDTO)
def crear_evento(evento: dict):
    """
    Crea un evento en Riak y devuelve un DTO consistente.
    """

    key = str(int(time.time() * 1000))
    evento["timestamp"] = evento.get("timestamp", int(time.time()))

    url = riak_key_url(key)
    headers = {"Content-Type": "application/json"}

    resp = requests.put(url, headers=headers, data=json.dumps(evento))

    if resp.status_code not in (200, 204):
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar en Riak: {resp.text}"
        )

    return EventoDTO(
        evento=evento,
        operacion=f"riak.PUT('{url}')"
    )


@app.get("/evento/{key}", response_model=EventoDTO)
def obtener_evento(key: str):
    """
    Recupera un evento desde Riak y devuelve DTO.
    """

    url = riak_key_url(key)
    resp = requests.get(url)

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

    return EventoDTO(
        evento=data,
        operacion=f"riak.GET('{url}')"
    )


@app.delete("/evento/{key}", response_model=EventoDTO)
def borrar_evento(key: str):
    """
    Borra un evento por key y devuelve DTO.
    """

    url = riak_key_url(key)
    resp = requests.delete(url)

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    if resp.status_code not in (200, 204):
        raise HTTPException(
            status_code=500,
            detail=f"Error al borrar en Riak: {resp.text}"
        )

    return EventoDTO(
        evento={"key": key, "status": "borrado"},
        operacion=f"riak.DELETE('{url}')"
    )


@app.get("/eventos")
def listar_eventos():
    """
    Lista todas las keys del bucket.
    """

    url = f"{BASE_URL}/keys?keys=true"
    resp = requests.get(url)

    if resp.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Error listando keys en Riak: {resp.text}"
        )

    data = resp.json()
    keys = data.get("keys", [])

    return {"keys": keys}
