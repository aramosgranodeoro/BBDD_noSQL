import ProductItem from "./ProductItem";
import React from "react";
import { useState } from "react";

export default function ProductList({ products }) {
  return (
    <div className="resultado">
        <h2>Lista de productos</h2>

        <ul className="lista-secciones">
            {products.producto.map((p, index) => (
                <ProductItem key={index} p={p} index={index} />
            ))}
        </ul>

        <ul className="lista-secciones">
            {product.recommendation && (
                <li className="seccion">
                <JsonBlock title="Recomendacion (Redis)" data={products.recommendation.resultado} />
                <OperationBlock operacion={products.recommendation.operacion} />
                </li>
            )}

            {product.analytics && (
                <li className="seccion">
                <JsonBlock title="Analiticas (Riak KV)" data={products.analytics.evento} />
                <OperationBlock operacion={products.analytics.operacion} />
                </li>
            )}
        </ul>
    </div>
  );
}
