import React, { useState, useEffect } from "react";
import OperationBlock from "./OperationBlock";

export default function CreateProduct({ nuevo, setNuevo, crearProducto }) {
  const [rawJson, setRawJson] = useState(JSON.stringify(nuevo, null, 2));
  const [mongoOp, setMongoOp] = useState("db.productos.insertOne({})");
  const [redisOp, setRedisOp] = useState("");
  const [riakOp, setRiakOp] = useState("");

  useEffect(() => {
    try {
      const obj = JSON.parse(rawJson);
      setMongoOp(`db.productos.insertOne(${JSON.stringify(obj)})`);

      const id = obj.id ?? obj._id ?? "ID_NO_ENCONTRADO";
      setRedisOp(`ZADD productos:vistas 0 ${id}`);

      const key = Date.now().toString();
      const riakUrl = `http://localhost:8098/types/default/buckets/eventos/keys/${key}`;
      const evento = {
        evento: "producto_creado",
        producto: id
      };
      const eventoString = JSON.stringify(evento).replace(/'/g, "\\'");
      setRiakOp(  `curl -X PUT "${riakUrl}" -H "Content-Type: application/json" -d "{\"evento\":\"producto_creado\",\"producto\":\"${id}\"}"` );

    } catch {
      setMongoOp("JSON inválido");
      setRedisOp("");
      setRiakOp("");
    }
  }, [rawJson]);

  function handleCreate() {
    try {
      const parsed = JSON.parse(rawJson);
      setNuevo(parsed); 
      crearProducto(parsed); 
    } catch {
      alert("El contenido no es JSON válido.");
    }
  }

  return (
    <div className="card">
      <h3>Crear producto</h3>

      <textarea className="input" value={rawJson} onChange={(e) => setRawJson(e.target.value)} />
      <div className="row">
        <OperationBlock operacion={mongoOp} />
        <button className="btn" onClick={handleCreate}> CREAR </button>
      </div>

      <div className="row">
        <OperationBlock operacion={redisOp} />
      </div>

      <div className="row">
        <OperationBlock operacion={riakOp} />
      </div>
    </div>
  );
}
