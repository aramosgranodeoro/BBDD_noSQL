import React, { useState } from "react";
import OperationBlock from "./OperationBlock";

export default function CreateProduct({ nuevo, setNuevo, crearProducto }) {
  // Guardamos el JSON crudo en texto editable
  const [rawJson, setRawJson] = useState(JSON.stringify(nuevo, null, 2));

  function handleCreate() {
    try {
      const parsed = JSON.parse(rawJson);
      setNuevo(parsed);
      crearProducto();
    } catch (err) {
      alert("El contenido no es JSON válido.");
    }
  }

  return (
    <div className="card">
        <h3>Crear producto</h3>

        <textarea
        className="input"
        value={rawJson}
        onChange={(e) => setRawJson(e.target.value)}
        />

        <div class="row">
            <OperationBlock operacion={"operacion de create"} />

            <button className="btn" onClick={handleCreate}>
                CREAR
            </button>
        </div>
    </div>
  );
}
