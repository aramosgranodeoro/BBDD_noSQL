import React, { useState } from "react";
import "./App.css";

import ProductList from "./components/ProductList";
import ProductDetail from "./components/ProductDetail";
import CreateProduct from "./components/CreateProduct";
import UpdateProduct from "./components/UpdateProduct";

export default function App() {
  const [id, setId] = useState("");
  const [product, setProduct] = useState(null);
  const [products, setProducts] = useState({});
  const [estado, setEstado] = useState(null);
  const [menu, setMenu] = useState(1);

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
      setProducts({});
      setProduct(null);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div id="containerPrincipal">
      <h1>NoSQL Microservices Frontend</h1>

      {/* ---- MENÚ PRINCIPAL ---- */}
      <div className="menu">
        <button className={`btn ${menu === 1 ? "activo" : ""}`} onClick={() => setMenu(1)}>Lista de Productos</button>
        <button className={`btn ${menu === 2 ? "activo" : ""}`} onClick={() => setMenu(2)}>Buscar por ID</button>
        <button className={`btn ${menu === 3 ? "activo" : ""}`} onClick={() => setMenu(3)}>Crear Producto</button>
        <button className={`btn ${menu === 4 ? "activo" : ""}`} onClick={() => setMenu(4)}>Actualizar Producto</button>
      </div>

      <div className="divider"></div>

      {/* ---- OPCIÓN 1: LISTA ---- */}
      {menu == 1 && (
        <>
          <h2>Lista completa</h2>
          <div className="row">
            <button className="btn" onClick={fetchProducts}>Cargar lista</button>
            <button className="btn delete" onClick={deleteProducts}>Eliminar Todo</button>
          </div>

          {Object.keys(products).length > 0 && (
            <ProductList products={products} />
          )}
        </>
      )}

      {/* ---- OPCIÓN 2: BUSCAR POR ID ---- */}
      {menu == 2 && (
        <>
          <h2>Buscar producto por ID</h2>

          <div className="row">
            <input className="input" placeholder="ID producto" value={id} onChange={(e) => setId(e.target.value)} />
            <button className="btn" onClick={fetchProduct}>Buscar</button>
          </div>

          {product && (
            <ProductDetail product={product} deleteProduct={deleteProduct} />
          )}
        </>
      )}

      {/* ---- OPCIÓN 3: CREAR PRODUCTO ---- */}
      {menu == 3 && (
        <>
          <h2>Crear nuevo producto</h2>
          <CreateProduct nuevo={nuevo} setNuevo={setNuevo} crearProducto={crearProducto} />
        </>
      )}

      {/* ---- OPCIÓN 4: ACTUALIZAR PRODUCTO ---- */}
      {menu == 4 && (
        <>
          <h2>Actualizar producto</h2>
          <UpdateProduct id={id} setId={setId} editar={editar} setEditar={setEditar} actualizarProducto={actualizarProducto} />
        </>
      )}

    </div>
  );

}
