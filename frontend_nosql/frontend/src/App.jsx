import React, { useState } from "react";
import "./App.css";

import ProductList from "./components/ProductList";
import ProductDetail from "./components/ProductDetail";
import CreateProduct from "./components/CreateProduct";
import UpdateProduct from "./components/UpdateProduct";

export default function App() {
  const [id, setId] = useState("");
  const [product, setProduct] = useState(null);
  const [products, setProducts] = useState([]);
  const [estado, setEstado] = useState(null);

  const [nuevo, setNuevo] = useState({});
  const [editar, setEditar] = useState({});

  // Obtener todos los productos
  const fetchProducts = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos`);
      const data = await res.json();
      setProducts(data);
      setEstado(null);
      
    } catch (error) {
      console.error(error);
    }
  };

  // Obtener un producto por ID
  const fetchProduct = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos/${id}`);
      const data = await res.json();

      if (!data) {
        setEstado("Producto no encontrado");
        setProduct(null);
      } else {
        setProduct(data);
        setEstado(null);
      }
    } catch (error) {
      console.error(error);
    }
  };

  // Crear producto
  const crearProducto = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(nuevo),
      });

      await res.json();
      setEstado("Producto creado");
      setNuevo({});
      fetchProducts();
    } catch (error) {
      console.error(error);
    }
  };

  // Actualizar producto
  const actualizarProducto = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editar),
      });

      await res.json();
      setEstado("Producto actualizado");
      setEditar({});
      fetchProduct();
    } catch (error) {
      console.error(error);
    }
  };

  // Borrar uno
  const deleteProduct = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos/${id}`, {
        method: "DELETE",
      });

      const data = await res.json();
      setEstado(data.msg);
      setProduct(null);
      fetchProducts();
    } catch (error) {
      console.error(error);
    }
  };

  // Borrar todos
  const deleteProducts = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos`, {
        method: "DELETE",
      });

      const data = await res.json();
      setEstado(data.msg);
      setProducts([]);
      setProduct(null);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div id="containerPrincipal">
      <h1>NoSQL Microservices Frontend</h1>

      {/* LISTAR Y BORRAR TODO */}
      <div className="row">
        <button className="btn" onClick={fetchProducts}>LISTA DE PRODUCTOS</button>
        <button className="btn delete" onClick={deleteProducts}>ELIMINAR TODO</button>
      </div>

      {/* LISTA DE PRODUCTOS */}
      {products.length > 0 && <ProductList products={products} />}

      <div className="divider"></div>

      {/* BUSCAR POR ID */}
      <div className="row">
        <input className="input" placeholder="ID producto" value={id} onChange={(e) => setId(e.target.value)} />
        <button className="btn" onClick={fetchProduct}>Buscar</button>
      </div>

      {/* RESULTADO INDIVIDUAL */}
      {product && ( <ProductDetail product={product} deleteProduct={deleteProduct} /> )}

      <div className="divider"></div>

      {/* CREAR */}
      <CreateProduct nuevo={nuevo} setNuevo={setNuevo} crearProducto={crearProducto} />

      <div className="divider"></div>

      {/* EDITAR */}
      <UpdateProduct id={id} setId={setId} editar={editar} setEditar={setEditar} actualizarProducto={actualizarProducto}/>

      {estado && <p className="estado">{estado}</p>}
    </div>
  );
}
