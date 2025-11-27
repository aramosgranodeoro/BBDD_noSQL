import JsonBlock from "./JsonBlock";
import OperationBlock from "./OperationBlock";
import React from "react";
import { useState } from "react";

export default function ProductDetail({ product, deleteProduct }) {
const key = Date.now().toString(); 
  const riakUrl = `http://localhost:8098/types/default/buckets/eventos/keys/${key}`;
  const evento = {
    evento: "producto_visto",
    producto: product.producto.id
  };
  const eventoString = JSON.stringify(evento).replace(/'/g, "\\'");
  const riakOperacion = `curl -X PUT "${riakUrl}" -H "Content-Type: application/json" -d "{\"evento\":\"producto_visto\",\"producto\":\"${product.producto.id}\"}"`;

  return (
    <div className="resultado">
      <h2>Resultado</h2>
      <ul className="lista-secciones">

        {product.producto.id && (
          <li className="seccion">
            <JsonBlock title="Catalogo (MondoDB)" data={product.catalog.producto} />
            <OperationBlock operacion={product.catalog.operacion} />
          </li>
        )}

        {product.producto.id && (
          <li className="seccion">
            <JsonBlock title="Recomendacion (Redis)" data={product.recommendation.detalle} />
            <OperationBlock operacion={product.recommendation.operacion} />
          </li>
        )}

        {product.producto.id && (
          <li className="seccion">
            <JsonBlock title="Analiticas (Riak KV)" data={product.analytics.evento} />
            <OperationBlock operacion={product.analytics.operacion} />
          </li>
        )}

        {product.producto.id && (
          <li className="seccion">
            <JsonBlock title="Producto" data={product.producto} />
          </li>
        )}
      </ul>
      
      {product.producto.id && (
          <div className="card">
            <div className="row">
              <OperationBlock operacion={`db.productos.deleteOne({ _id: '${product.producto.id}' })`}  />
              <button className="btn delete" onClick={deleteProduct}>ELIMINAR</button>
            </div>

            <div className="row">
              <OperationBlock operacion={`ZINCRBY productos:vistas 1 '${product.producto.id}'`}  />
            </div>

            <div className="row">
              <OperationBlock operacion={riakOperacion} />
            </div>
          </div>
        )}
      
    </div>
  );
}

