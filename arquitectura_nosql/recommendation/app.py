from fastapi import FastAPI
import redis
from dto.dto_recommendation import ProductoScore

app = FastAPI()

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

ZSET = "productos:vistas"


# ---------------------------------------------------------
# 1) Incrementar vistas de un producto
# ---------------------------------------------------------
@app.post("/visita/{id}", response_model=ProductoScore)
def incr(id: str):
    score = r.zincrby(ZSET, 1, id)
    return ProductoScore(
        producto=id,
        vistas=score,
        operacion=f"redis.ZINCRBY('{ZSET}', 1, '{id}')"
    )


# ---------------------------------------------------------
# 2) Disminuir vistas
# ---------------------------------------------------------
@app.post("/visita/{id}/decr", response_model=ProductoScore)
def decr(id: str):
    score = r.zincrby(ZSET, -1, id)
    return ProductoScore(
        producto=id,
        vistas=score,
        operacion=f"redis.ZINCRBY('{ZSET}', -1, '{id}')"
    )


# ---------------------------------------------------------
# 3) Obtener el TOP N de productos
# ---------------------------------------------------------
@app.get("/top/{n}")
def top(n: int):
    return {
        "resultado": r.zrevrange(ZSET, 0, n - 1, withscores=True),
        "operacion": f"redis.ZREVRANGE('{ZSET}', 0, {n - 1}, WITHSCORES)"
    }


# ---------------------------------------------------------
# 4) Obtener score de un producto
# ---------------------------------------------------------
@app.get("/producto/{id}", response_model=ProductoScore)
def get_score(id: str):
    score = r.zscore(ZSET, id)
    return ProductoScore(
        producto=id,
        vistas=score,
        operacion=f"redis.ZSCORE('{ZSET}', '{id}')"
    )


# ---------------------------------------------------------
# 5) Eliminar un producto del ranking
# ---------------------------------------------------------
@app.delete("/producto/{id}", response_model=ProductoScore)
def delete(id: str):
    r.zrem(ZSET, id)
    return ProductoScore(
        producto=id,
        vistas=None,
        operacion=f"redis.ZREM('{ZSET}', '{id}')"
    )


# ---------------------------------------------------------
# 6) Resetear todo el ZSET
# ---------------------------------------------------------
@app.delete("/reset")
def reset():
    r.delete(ZSET)
    return {
        "msg": "ranking reseteado",
        "operacion": f"redis.DEL('{ZSET}')"
    }


# ---------------------------------------------------------
# 7) Insertar múltiples productos de golpe
# ---------------------------------------------------------
@app.post("/bulk")
def bulk_insert(productos: dict):

    with r.pipeline() as pipe:
        for p, score in productos.items():
            pipe.zadd(ZSET, {p: score})
        pipe.execute()

    return {
        "msg": "bulk insert ok",
        "productos": productos,
        "operacion": f"redis.ZADD('{ZSET}', <bulk>)"
    }


# ---------------------------------------------------------
# 8) Obtener un rango (paginación)
# ---------------------------------------------------------
@app.get("/rango")
def rango(start: int = 0, stop: int = 9):
    return {
        "resultado": r.zrevrange(ZSET, start, stop, withscores=True),
        "operacion": f"redis.ZREVRANGE('{ZSET}', {start}, {stop}, WITHSCORES)"
    }


# ---------------------------------------------------------
# 9) Obtener todos los productos
# ---------------------------------------------------------
@app.get("/all")
def get_all():
    return {
        "resultado": r.zrevrange(ZSET, 0, -1, withscores=True),
        "operacion": f"redis.ZREVRANGE('{ZSET}', 0, -1, WITHSCORES)"
    }


# ---------------------------------------------------------
# 10) Filtrar por score mínimo y máximo
# ---------------------------------------------------------
@app.get("/filtrar")
def filtrar(min: float = "-inf", max: float = "+inf"):
    return {
        "resultado": r.zrangebyscore(ZSET, min, max, withscores=True),
        "operacion": f"redis.ZRANGEBYSCORE('{ZSET}', {min}, {max}, WITHSCORES)"
    }
