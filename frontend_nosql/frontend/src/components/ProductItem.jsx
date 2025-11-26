import JsonBlock from "./JsonBlock";
import OperationBlock from "./OperationBlock";
import React from "react";
import { useState } from "react";

export default function ProductItem({ p, index }) {
  return (
    <li className="seccion">
        <h3> Producto {index + 1}</h3>

        {p.catalog && (
            <div>
                <JsonBlock title="Catalogo (MondoDB)" data={p.catalog.producto} />
                <OperationBlock operacion={p.catalog.operacion} />
            </div>
        )}

        {p.recommendation && (
            <div>
                <JsonBlock title="Recomendacion (Redis)" data={p.recommendation} />
                <OperationBlock operacion={p.recommendation.operacion} />
            </div>
        )}

        {p.analytics && (
            <div>
                <JsonBlock title="Analiticas (Riak KV)" data={p.analytics.evento} />
                <OperationBlock operacion={p.analytics.operacion} />
            </div>
        )}

        {p.producto && (
            <JsonBlock title=" Producto" data={p.producto} />
        )}
    </li>
  );
}
