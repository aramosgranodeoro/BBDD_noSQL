import React, { useState, useEffect } from "react";
import OperationBlock from "./OperationBlock";

export default function UpdateProduct({ id, setId, editar, setEditar, actualizarProducto }) {
  const [rawJson, setRawJson] = useState(JSON.stringify(editar, null, 2));
  const [mongoOp, setMongoOp] = useState("db.productos.updateOne({}, {$set:{}})");
  const [riakOp, setRiakOp] = useState("");

  useEffect(() => {
    try {
      const obj = JSON.parse(rawJson);
      setMongoOp(
        `db.productos.updateOne({"_id": "${id}"}, {"$set": ${JSON.stringify(obj)}})`
      );
      
      const key = Date.now().toString();
      const riakUrl = `http://localhost:8098/types/default/buckets/eventos/keys/${key}`;
      const evento = {
        evento: "producto_actualizado",
        producto: id
      };
      const eventoString = JSON.stringify(evento).replace(/'/g, "\\'");
      setRiakOp(  `curl -X PUT "${riakUrl}" -H "Content-Type: application/json" -d "${eventoString}"` );
    } catch {
      setMongoOp("JSON inválido");
      setRiakOp("");
    }
  }, [rawJson, id]);

function handleUpdate() {
  try {
    const parsed = JSON.parse(rawJson);
    setEditar(parsed); 
    actualizarProducto(parsed); 
  } catch {
    alert("El contenido no es JSON válido.");
  }
}

  return (
    <div className="card">
      <h3>Actualizar producto</h3>

      <input className="input" placeholder="ID a actualizar" value={id} onChange={(e) => setId(e.target.value)} />
      <textarea className="input" value={rawJson} onChange={(e) => setRawJson(e.target.value)} />
      <div className="row">
        <OperationBlock operacion={mongoOp} />
        <button className="btn" onClick={handleUpdate}> ACTUALIZAR </button>
      </div>

      <div className="row">
        <OperationBlock operacion={riakOp} />
      </div>
    </div>
  );
}
