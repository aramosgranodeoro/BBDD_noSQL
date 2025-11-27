from fastapi import FastAPI
import redis
from dto.dto_recommendation import ProductoScore
from dto.dto_recommedation_list import ProductosScore

app = FastAPI()
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
ZSET = "productos:vistas"

# ---------------------------------------------------------
# Incrementar vistas de un producto
# ---------------------------------------------------------
@app.post("/visita/{id}", response_model=ProductoScore)
def incr(id: str):
    score = r.zincrby(ZSET, 1, id)
    return ProductoScore(
        detalle={
            "producto": id,
            "vistas": score
        },
        operacion=f"ZINCRBY {ZSET} 1 {id}"
    )


# ---------------------------------------------------------
# Disminuir vistas
# ---------------------------------------------------------
@app.post("/visita/{id}/decr", response_model=ProductoScore)
def decr(id: str):
    score = r.zincrby(ZSET, -1, id)
    return ProductoScore(
        detalle={
            "producto": id,
            "vistas": score
        },
        operacion=f"ZINCRBY {ZSET} -1 {id}"
    )


# ---------------------------------------------------------
# Añadir recomedacion 0 inicial
# ---------------------------------------------------------
@app.post("/producto/{id}", response_model=ProductoScore)
def init_score(id: str):
    r.zadd(ZSET, {id: 0}, nx=True)
    return ProductoScore(
        detalle={
            "producto": id,
            "vistas": 0
        },
        operacion=f"ZADD {ZSET} {{ {id}: 0 }} NX"
    )

# ---------------------------------------------------------
# Obtener score de un producto
# ---------------------------------------------------------
@app.get("/producto/{id}", response_model=ProductoScore)
def get_score(id: str):
    score = r.zscore(ZSET, id)
    return ProductoScore(
        detalle={
            "producto": id,
            "vistas": score
        },
        operacion=f"ZSCORE {ZSET} {id}"
    )


# ---------------------------------------------------------
# Eliminar un producto del ranking
# ---------------------------------------------------------
@app.delete("/producto/{id}", response_model=ProductoScore)
def delete(id: str):
    r.zrem(ZSET, id)
    return ProductoScore(
        detalle={
            "producto": id,
            "vistas": None
        },
        operacion=f"ZREM {ZSET} {id}"
    )


# ---------------------------------------------------------
# Resetear todo el ZSET
# ---------------------------------------------------------
@app.delete("/reset", response_model=ProductoScore)
def reset():
    r.delete(ZSET)
    return ProductoScore(
        detalle={
            "resultado": "ranking reseteado",
        },
        operacion=f"DEL {ZSET}"
    )


# ---------------------------------------------------------
# Insertar múltiples productos de golpe
# ---------------------------------------------------------
@app.post("/bulk", response_model=ProductosScore)
def bulk_insert(productos: dict):
    operaciones = []

    with r.pipeline() as pipe:
        for p, score in productos.items():
            pipe.zadd(ZSET, {p: score})
            operaciones.append(f"ZADD {ZSET} {{ {p}: {score} }}")
        pipe.execute()

    return ProductosScore(
        detalle={
            "producto": productos,
            "resultado": "bulk inserción ok"
        },
        operacion=operaciones
    )

#=====================================================
# CONSULTAS AGREGADAS
#=====================================================

# ---------------------------------------------------------
# Obtener el TOP N de productos
# ---------------------------------------------------------
@app.get("/top/{n}", response_model=ProductoScore)
def top(n: int):
    resultado = r.zrevrange(ZSET, 0, n - 1, withscores=True)
    return ProductoScore(
        detalle={
            "resultado": resultado,
        },
        operacion=f"ZREVRANGE {ZSET} 0 {n - 1} WITHSCORES"
    )
    
# ---------------------------------------------------------
# Obtener un rango (paginación)
# ---------------------------------------------------------
@app.get("/rango", response_model=ProductoScore)
def rango(start: int = 0, stop: int = 9):
    resultado = r.zrevrange(ZSET, start, stop, withscores=True)
    return ProductoScore(
        detalle={
            "resultado": resultado
        },
        operacion=f"ZREVRANGE {ZSET} {start} {stop} WITHSCORES"
    )


# ---------------------------------------------------------
# Obtener todos los productos
# ---------------------------------------------------------
@app.get("/all", response_model=ProductoScore)
def get_all():
    resultado = r.zrevrange(ZSET, 0, -1, withscores=True)
    return ProductoScore(
        detalle={
            "resultado": resultado
        },
        operacion=f"ZREVRANGE {ZSET} 0 -1 WITHSCORES"
    )


# ---------------------------------------------------------
# Filtrar por score mínimo y máximo
# ---------------------------------------------------------
@app.get("/filtrar", response_model=ProductoScore)
def filtrar(min: float = float("-inf"), max: float = float("inf")):
    resultado = r.zrangebyscore(ZSET, min, max, withscores=True)
    return ProductoScore(
        detalle={
            "resultado": resultado
        },
        operacion=f"ZRANGEBYSCORE {ZSET} {min} {max} WITHSCORES"
    )
