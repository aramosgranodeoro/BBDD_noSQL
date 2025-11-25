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


# ============================================================================
#   GET Producto → Unificar los 3 DTO
# ============================================================================
@app.get("/productos/{id}", response_model=DTOFinal)
async def get_producto(id: str):

    async with httpx.AsyncClient() as c:

        # 1) Obtener producto (DTOCatalogo)
        catalog_res = await c.get(f"{catalog_url}/productos/{id}")
        if catalog_res.status_code == 404:
            raise HTTPException(404, "Producto no encontrado")
        dto_catalog = catalog_res.json()

        # 2) Registrar visita (DTORecommendation)
        rec_res = await c.post(f"{rec_url}/visita/{id}")
        dto_rec = rec_res.json()

        # 3) Enviar evento a analytics (DTOAnalytics)
        analytics_res = await c.post(
            f"{analytics_url}/evento",
            json={"evento": "producto_visto", "producto": id}
        )
        dto_analytics = analytics_res.json()

        # 4) Unificar en DTOFinal
        return DTOFinal(
            producto=dto_catalog["producto"],
            catalog=dto_catalog,
            recommendation=dto_rec,
            analytics=dto_analytics
        )

@app.get("/productos", response_model=DTOFinal)
async def get_todos_productos():
    async with httpx.AsyncClient() as c:

        # 1) Obtener todos los productos (DTOCatalogo)
        catalog_res = await c.get(f"{catalog_url}/productos")
        
        # Verificar si la respuesta fue exitosa
        if catalog_res.status_code != 200:
            raise HTTPException(status_code=catalog_res.status_code, detail="Error al obtener productos de catalog")

        dto_catalog = catalog_res.json()

        # 2) recommendation no interviene aquí (puedes dejar un valor predeterminado)
        dto_rec = {
            "resultado": "sin cambios",
            "operacion": "N/A"
        }

        # 3) Evento analytics
        analytics_res = await c.post(
            f"{analytics_url}/evento",
            json={"evento": "listado_productos"}
        )

        if analytics_res.status_code != 200:
            raise HTTPException(status_code=analytics_res.status_code, detail="Error al registrar evento en analytics")

        dto_analytics = analytics_res.json()

        # 4) Devolver la respuesta unificada en DTOFinal
        return DTOFinal(
            producto=dto_catalog["producto"],  # Asegúrate de que 'producto' es la lista de productos
            catalog=dto_catalog,
            recommendation=dto_rec,
            analytics=dto_analytics
        )

# ============================================================================
#   DELETE producto → también unifica DTOs
# ============================================================================
@app.delete("/productos/{id}", response_model=DTOFinal)
async def delete_producto(id: str):

    async with httpx.AsyncClient() as c:

        # 1) Borrar producto catalog
        catalog_res = await c.delete(f"{catalog_url}/productos/{id}")
        dto_catalog = catalog_res.json()

        # 2) NO usamos recommendation en delete (opcional)
        dto_rec = {
            "resultado": "sin cambios",
            "operacion": "N/A"
        }

        # 3) Registrar evento en analytics
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


# ============================================================================
#   DELETE ALL productos
# ============================================================================
@app.delete("/productos", response_model=DTOFinal)
async def delete_todos_productos():

    async with httpx.AsyncClient() as c:

        # 1) Borrar todos
        catalog_res = await c.delete(f"{catalog_url}/productos")
        dto_catalog = catalog_res.json()

        # 2) recommendation tampoco interviene
        dto_rec = {
            "resultado": "sin cambios",
            "operacion": "N/A"
        }

        # 3) Evento analytics
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
    

