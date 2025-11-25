from fastapi import FastAPI
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Permite cualquier origen (frontend)
    allow_credentials=True,
    allow_methods=["*"],       # Permite GET/POST/PUT/DELETE
    allow_headers=["*"],
)

catalog_url="http://catalog:8001"
rec_url="http://recommendation:8002"
analytics_url="http://analytics:8003"

@app.get("/productos/{id}")
async def get_producto(id:str):
    async with httpx.AsyncClient() as c:
        prod = await c.get(f"{catalog_url}/productos/{id}")
        await c.post(f"{rec_url}/visita/{id}")
        await c.post(f"{analytics_url}/evento", json={"evento":"producto_visto","producto":id})
        return prod.json()
