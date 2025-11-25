from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from dto.dto_catalogo import DTOCatalogo

app = FastAPI()

# Conexión a MongoDB (docker)
db = MongoClient("mongodb://mongo:27017").catalogo

COL = db.productos


# ---------------------------------------------------------
# 1) Crear producto
# ---------------------------------------------------------
@app.post("/productos", response_model=DTOCatalogo)
def crear(p: dict):
    if "_id" not in p:
        raise HTTPException(400, "Falta _id en el producto")

    COL.insert_one(p)

    return DTOCatalogo(
        producto=p,
        operacion=f"db.productos.insertOne({p})"
    )


# ---------------------------------------------------------
# 2) Crear lote de productos
# ---------------------------------------------------------
@app.post("/productos/lote", response_model=DTOCatalogo)
def crear_lote(lista: list):

    for prod in lista:
        if "_id" not in prod:
            raise HTTPException(400, "Todos los productos necesitan _id")

    COL.insert_many(lista)

    return DTOCatalogo(
        producto={"insertados": len(lista)},
        operacion="db.productos.insertMany(<lista>)"
    )


# ---------------------------------------------------------
# 3) Listar todos
# ---------------------------------------------------------
@app.get("/productos", response_model=DTOCatalogo)
def listar():

    docs = list(COL.find({}, {"_id": 1, "nombre": 1, "precio": 1, "stock": 1}))

    for d in docs:
        d["id"] = d["_id"]
        del d["_id"]

    return DTOCatalogo(
        producto=docs,
        operacion="db.productos.find({})"
    )


# ---------------------------------------------------------
# 4) Obtener uno por ID
# ---------------------------------------------------------
@app.get("/productos/{id}", response_model=DTOCatalogo)
def obtener(id: str):

    prod = COL.find_one({"_id": id}, {"_id": 1, "nombre": 1, "precio": 1, "stock": 1})

    if not prod:
        raise HTTPException(404, "Producto no encontrado")

    # _id → id
    prod["id"] = prod["_id"]
    del prod["_id"]

    return DTOCatalogo(
        producto=prod,
        operacion=f"db.productos.findOne({{'_id': '{id}'}})"
    )


# ---------------------------------------------------------
# 5) Actualizar
# ---------------------------------------------------------
@app.put("/productos/{id}", response_model=DTOCatalogo)
def actualizar(id: str, p: dict):

    COL.update_one({"_id": id}, {"$set": p})

    return DTOCatalogo(
        producto={"id": id, "actualizado": p},
        operacion=f"db.productos.updateOne({{'_id': '{id}'}}, {{'$set': {p}}})"
    )


# ---------------------------------------------------------
# 6) Borrar uno
# ---------------------------------------------------------
@app.delete("/productos/{id}", response_model=DTOCatalogo)
def borrar(id: str):

    COL.delete_one({"_id": id})

    return DTOCatalogo(
        producto={"id": id},
        operacion=f"db.productos.deleteOne({{'_id': '{id}'}})"
    )


# ---------------------------------------------------------
# 7) Borrar todos
# ---------------------------------------------------------
@app.delete("/productos", response_model=DTOCatalogo)
def borrar_todos():

    resultado = COL.delete_many({})

    return DTOCatalogo(
        producto={"borrados": resultado.deleted_count},
        operacion="db.productos.deleteMany({})"
    )
