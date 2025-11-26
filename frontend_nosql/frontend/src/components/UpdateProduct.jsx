import React, { useState } from "react";
import OperationBlock from "./OperationBlock";

export default function UpdateProduct({ id, setId, editar, setEditar, actualizarProducto }) {
  const [rawJson, setRawJson] = useState(JSON.stringify(editar, null, 2));

  function handleUpdate() {
    try {
      const parsed = JSON.parse(rawJson);
      setEditar(parsed);
      actualizarProducto();
    } catch (err) {
      alert("El contenido no es JSON válido.");
    }
  }

  return (
    <div className="card">
        <h3>Actualizar producto</h3>

        <input
        className="input"
        placeholder="ID a actualizar"
        value={id}
        onChange={(e) => setId(e.target.value)}
        />

        <textarea
        className="input"
        value={rawJson}
        onChange={(e) => setRawJson(e.target.value)}
        />

        <div class="row">
            <OperationBlock operacion={"operacion de update"} />

            <button className="btn" onClick={handleUpdate}>
            ACTUALIZAR
            </button>
        </div>
    </div>
  );
}
