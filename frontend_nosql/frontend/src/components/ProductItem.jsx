import JsonBlock from "./JsonBlock";
import OperationBlock from "./OperationBlock";
import React from "react";
import { useState } from "react";

export default function ProductItem({ p, index }) {
  return (
    <li className="seccion">
        <h3> Producto {index + 1}</h3>
        <JsonBlock data={p} />
    </li>
  );
}
