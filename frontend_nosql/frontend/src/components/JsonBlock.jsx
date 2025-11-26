import React from "react";
import { useState } from "react";

export default function JsonBlock({ title, data }) {
  return (
    <div className="bloque">
        <h4>{title}</h4>
        <pre className="json">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
