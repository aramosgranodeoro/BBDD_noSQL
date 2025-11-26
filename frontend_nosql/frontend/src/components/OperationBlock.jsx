import React from "react";
import { useState } from "react";

export default function OperationBlock({ operacion }) {
  return (
    <div className="operacion">
      <span>{operacion}</span>

      <button className="copiar" onClick={() => navigator.clipboard.writeText(operacion)} > 🗐 </button>
    </div>
  );
}
