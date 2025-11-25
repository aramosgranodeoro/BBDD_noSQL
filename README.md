# 🚀 Arquitectura NoSQL — Microservicios + Frontend

Este proyecto implementa una arquitectura distribuida basada en microservicios, utilizando tres bases de datos NoSQL distintas:

- **MongoDB** → Servicio de usuarios  
- **Redis** → Servicio de productos  
- **Riak KV (HTTP API)** → Servicio de analítica de eventos  
- **Frontend (React)** → Interfaz unificada

La arquitectura está diseñada para ser modular, fácilmente desplegable y extensible.

---

# 🧱 Estructura del Proyecto

```
/arquitectura_completa_nosql
│
├── catalog/                # Microservicio Usuarios (MongoDB)
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── recommedation/             # Microservicio Productos (Redis)
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── analytics/            # Microservicio Analítica (Riak KV HTTP)
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── gateway/            # API Gateway
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/             # React Frontend
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── .dockerignore
│
└── README.md             # Este archivo
```

---

# ⚙️ Microservicios

## 1️⃣ Servicio de Usuarios  
**Stack:** FastAPI + MongoDB  
**Puerto:** `8001`

📌 Funcionalidades:  
- Crear usuarios  
- Listar usuarios  
- Consultar usuario por ID  

📌 Base de datos:  
- Repositorio `users` en MongoDB  
- Colección `users`

---

## 2️⃣ Servicio de Productos  
**Stack:** FastAPI + Redis  
**Puerto:** `8002`

📌 Funcionalidades:
- Crear producto  
- Obtener producto  
- Listar productos (solo keys)  

📌 Base de datos:
- Redis almacenado como hashes

---

## 3️⃣ Servicio de Analítica  
**Stack:** FastAPI + Riak KV HTTP API  
**Puerto:** `8003`

📌 Funcionalidades:
- Registrar eventos en Riak  
- Consultar eventos de un bucket  

📌 Base de datos:
- Riak KV a través del puerto `8098`
- Bucket: `eventos`

---

# 🖥️ Frontend (React)

**Stack:** React + Axios  
**Puerto dev:** `5173`

📌 Funcionalidades:  
- Formulario para crear usuarios  
- Formulario para crear productos  
- Envío de eventos al microservicio analytics  
- Consumo de los 3 microservicios  

---

# 🐳 Docker

Cada microservicio + frontend incluye su propio `Dockerfile` y su `.dockerignore`.

### Ejemplo para arrancar el microservicio Users:

```bash
cd users
docker build -t users_service .
docker run -p 8001:8001 users_service
```

### Ejemplo para Riak KV:

```bash
docker run -d --name riak_db   -p 8098:8098 -p 8087:8087 basho/riak-kv
```

---

# ▶️ Arranque Local (sin Docker)

## 1. Microservicios

En cada carpeta:

```
pip install -r requirements.txt
uvicorn app:app --reload --port XXXX
```

Puertos:  
- Users → **8001**  
- Products → **8002**  
- Analytics → **8003**

## 2. Frontend

```
cd frontend
npm install
npm run dev
```

---

# 🧪 Test rápido desde CMD / PowerShell

### Crear usuario:

```bash
curl -X POST http://localhost:8001/usuarios   -H "Content-Type: application/json"   -d "{\"nombre\": \"Juan\"}"
```

### Crear producto:

```bash
curl -X POST http://localhost:8002/productos   -H "Content-Type: application/json"   -d "{\"id\":\"1\",\"nombre\":\"Laptop\"}"
```

### Crear evento:

```bash
curl -X POST http://localhost:8003/evento   -H "Content-Type: application/json"   -d "{\"evento\": \"login\"}"
```

---

# 📌 Notas Importantes

- Cada microservicio MUST tener un `.dockerignore` en la misma carpeta que su Dockerfile.
- Riak KV solo funciona correctamente por **HTTP**, no por drivers Python modernos.
- Puedes añadir **NGINX** para unificar los microservicios en un mismo dominio.

---

# 📄 Licencia
Proyecto educativo y libre para uso académico.
