
import React, { useState } from "react";

export default function App() {
  const [id, setId] = useState("");
  const [product, setProduct] = useState(null);

  const fetchProduct = async () => {
    const res = await fetch(`http://localhost:8000/productos/${id}`);
    const data = await res.json();
    setProduct(data);
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>NoSQL Microservices Frontend</h1>

      <input
        placeholder="ID producto"
        value={id}
        onChange={(e) => setId(e.target.value)}
      />
      <button onClick={fetchProduct}>Buscar</button>

      {product && (
        <pre>{JSON.stringify(product, null, 2)}</pre>
      )}
    </div>
  );
}
