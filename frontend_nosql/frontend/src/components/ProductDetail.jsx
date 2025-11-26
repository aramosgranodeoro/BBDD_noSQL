import JsonBlock from "./JsonBlock";
import OperationBlock from "./OperationBlock";
import React from "react";
import { useState } from "react";

export default function ProductDetail({ product, deleteProduct }) {
  return (
    <div className="resultado">
      <h2>Resultado</h2>
      <ul className="lista-secciones">

        {product.catalog && (
          <li className="seccion">
            <JsonBlock title="Catalogo (MondoDB)" data={product.catalog.producto} />
            <OperationBlock operacion={product.catalog.operacion} />
          </li>
        )}

        {product.recommendation && (
          <li className="seccion">
            <JsonBlock title="Recomendacion (Redis)" data={product.recommendation.detalle} />
            <OperationBlock operacion={product.recommendation.operacion} />
          </li>
        )}

        {product.analytics && (
          <li className="seccion">
            <JsonBlock title="Analiticas (Riak KV)" data={product.analytics.evento} />
            <OperationBlock operacion={product.analytics.operacion} />
          </li>
        )}

        {product.producto && (
          <li className="seccion">
            <JsonBlock title="Producto" data={product.producto} />
          </li>
        )}
      </ul>

      <button className="btn delete" onClick={deleteProduct}>ELIMINAR</button>
    </div>
  );
}

