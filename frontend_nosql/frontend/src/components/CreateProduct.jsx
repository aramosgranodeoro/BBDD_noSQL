import React, { useState, useEffect } from "react";
import OperationBlock from "./OperationBlock";

export default function CreateProduct({ nuevo, setNuevo, crearProducto }) {
  const [rawJson, setRawJson] = useState(JSON.stringify(nuevo, null, 2));
  const [operacion, setOperacion] = useState("db.productos.insertOne({})");

  useEffect(() => {
    try {
      const obj = JSON.parse(rawJson);
      setOperacion(`db.productos.insertOne(${JSON.stringify(obj)})`);
    } catch {
      setOperacion("JSON inválido");
    }
  }, [rawJson]);

  function handleCreate() {
    try {
      const parsed = JSON.parse(rawJson);
      setNuevo(parsed);
      crearProducto();
    } catch {
      alert("El contenido no es JSON válido.");
    }
  }

  return (
    <div className="card">
      <h3>Crear producto</h3>

      <textarea className="input" value={rawJson} onChange={(e) => setRawJson(e.target.value)} />
      <div className="row">
        <OperationBlock operacion={operacion} />
        <button className="btn" onClick={handleCreate}> CREAR </button>
      </div>
    </div>
  );
}
