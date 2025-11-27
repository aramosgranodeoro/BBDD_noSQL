from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
from dto.dto_final import DTOFinal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

catalog_url = "http://catalog:8001"
rec_url = "http://recommendation:8002"
analytics_url = "http://analytics:8003"


# ====================================================================
#   GET /productos/{id}  → UNIFICA catalog + recommendation + analytics
# ====================================================================
@app.get("/productos/{id}", response_model=DTOFinal)
async def get_producto(id: str):

    async with httpx.AsyncClient() as c:

        # 1) Obtener producto del catálogo
        catalog_res = await c.get(f"{catalog_url}/productos/{id}")
        if catalog_res.status_code == 404:
            raise HTTPException(404, "Producto no encontrado")

        dto_catalog = catalog_res.json()

        # 2) Registrar visita en recommendation
        rec_res = await c.post(f"{rec_url}/visita/{id}")
        dto_rec = rec_res.json()

        # 3) Evento a analytics
        analytics_res = await c.post(
            f"{analytics_url}/evento",
            json={"evento": "producto_visto", "producto": id}
        )
        dto_analytics = analytics_res.json()

        # 4) Unificar
        return DTOFinal(
            producto=dto_catalog["producto"],
            catalog=dto_catalog,
            recommendation=dto_rec,
            analytics=dto_analytics
        )


# ====================================================================
#   GET /productos → lista completa unificada
# ====================================================================
@app.get("/productos", response_model=DTOFinal)
async def get_todos_productos():

    async with httpx.AsyncClient() as c:

        # 1) Llamar al catálogo
        catalog_res = await c.get(f"{catalog_url}/productos")
        if catalog_res.status_code != 200:
            raise HTTPException(500, "Error en catálogo")

        dto_catalog = catalog_res.json()

        # 2) recommendation no aplica en este caso
        dto_rec = {
            "resultado": "sin cambios",
            "operacion": "N/A"
        }

        # 3) Analytics
        analytics_res = await c.post(
            f"{analytics_url}/evento",
            json={"evento": "listado_productos"}
        )
        dto_analytics = analytics_res.json()

        return DTOFinal(
            producto=dto_catalog["producto"],
            catalog=dto_catalog,
            recommendation=dto_rec,
            analytics=dto_analytics
        )


# ====================================================================
#   DELETE /productos/{id} → unifica delete
# ====================================================================
@app.delete("/productos/{id}", response_model=DTOFinal)
async def delete_producto(id: str):

    async with httpx.AsyncClient() as c:

        # 1) Borrar del catálogo
        catalog_res = await c.delete(f"{catalog_url}/productos/{id}")
        dto_catalog = catalog_res.json()

        # 2) Eliminar recomensacion de un producto
        rec_res = await c.delete(f"{rec_url}/producto/{id}")
        dto_rec = rec_res.json()

        # 3) Analytics
        analytics_res = await c.post(
            f"{analytics_url}/evento",
            json={"evento": "producto_borrado", "producto": id}
        )
        dto_analytics = analytics_res.json()

        return DTOFinal(
            producto=None,
            catalog=dto_catalog,
            recommendation=dto_rec,
            analytics=dto_analytics
        )


# ====================================================================
#   DELETE /productos → borrar todos
# ====================================================================
@app.delete("/productos", response_model=DTOFinal)
async def delete_todos_productos():

    async with httpx.AsyncClient() as c:

        # 1) Limpiar catálogo
        catalog_res = await c.delete(f"{catalog_url}/productos")
        dto_catalog = catalog_res.json()

        # 2) Limpiar recomendacioens
        rec_res = await c.delete(f"{rec_url}/reset")
        dto_rec = rec_res.json()

        # 3) Analytics
        analytics_res = await c.post(
            f"{analytics_url}/evento",
            json={"evento": "todos_productos_borrados"}
        )
        dto_analytics = analytics_res.json()

        return DTOFinal(
            producto=None,
            catalog=dto_catalog,
            recommendation=dto_rec,
            analytics=dto_analytics
        )
        
# ====================================================================
#   POST /productos → Crear producto (unificado)
# ====================================================================
@app.post("/productos", response_model=DTOFinal)
async def crear_producto(producto: dict):
    async with httpx.AsyncClient() as c:

        # 1) Crear en catalog
        catalog_res = await c.post(f"{catalog_url}/productos", json=producto)
        if catalog_res.status_code != 200:
            raise HTTPException(500, "Error creando producto en catálogo")

        dto_catalog = catalog_res.json()

        # 2) Agregar recomendaciones del producto
        rec_res = await c.post(f"{rec_url}/producto/{dto_catalog['producto']['id']}")
        dto_rec = rec_res.json()

        # 3) Registrar evento analytics
        analytics_res = await c.post(
            f"{analytics_url}/evento",
            json={"evento": "producto_creado", "producto": producto.get("_id")}
        )
        dto_analytics = analytics_res.json()

        return DTOFinal(
            producto=dto_catalog["producto"],
            catalog=dto_catalog,
            recommendation=dto_rec,
            analytics=dto_analytics
        )


# ====================================================================
#   PUT /productos/{id} → Actualizar producto (unificado)
# ====================================================================
@app.put("/productos/{id}", response_model=DTOFinal)
async def actualizar_producto(id: str, datos: dict):
    async with httpx.AsyncClient() as c:

        # 1) Actualizar en catalog
        catalog_res = await c.put(f"{catalog_url}/productos/{id}", json=datos)
        if catalog_res.status_code != 200:
            raise HTTPException(500, "Error actualizando producto en catálogo")

        dto_catalog = catalog_res.json()

        # 2) recommendation no interviene
        dto_rec = {
            "resultado": "sin cambios",
            "operacion": "N/A"
        }

        # 3) analytics registra evento
        analytics_res = await c.post(
            f"{analytics_url}/evento",
            json={"evento": "producto_actualizado", "producto": id}
        )
        dto_analytics = analytics_res.json()

        return DTOFinal(
            producto=dto_catalog["producto"],
            catalog=dto_catalog,
            recommendation=dto_rec,
            analytics=dto_analytics
        )
