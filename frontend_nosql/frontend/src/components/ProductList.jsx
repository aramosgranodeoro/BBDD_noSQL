import ProductItem from "./ProductItem";
import JsonBlock from "./JsonBlock";
import OperationBlock from "./OperationBlock";
import React from "react";
import { useState } from "react";

export default function ProductList({ products }) {
  return (
    <div className="resultado">
        <h2>Lista de productos</h2>

        <ul className="lista-secciones">
            {products.recommendation && (
                <li className="seccion">
                <JsonBlock title="Recomendacion (Redis)" data={products.recommendation.resultado} />
                <OperationBlock operacion={products.recommendation.operacion} />
                </li>
            )}

            {products.analytics && (
                <li className="seccion">
                    <JsonBlock title="Analiticas (Riak KV)" data={products.analytics.evento} />
                    <OperationBlock operacion={products.analytics.operacion} />
                </li>
            )}

            {products.producto.map((p, index) => (  <ProductItem key={index} p={p} index={index} /> ))}

            <li className="seccion">
                <OperationBlock operacion={products.catalog.operacion} />
            </li>
        </ul>
    </div>
  );
}
