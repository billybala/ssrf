# SSRF Proof of Concept con FastAPI

Este proyecto demuestra una vulnerabilidad del tipo **Server-Side Request Forgery (SSRF)** y su mitigación utilizando **FastAPI**.  
Incluye un backend vulnerable y corregido, un servicio interno simulado y un frontend básico para probar visualmente el ataque.

---

## 📌 Arquitectura del proyecto

- **Backend (FastAPI)**  
  Expone dos endpoints:
  - `/fetch-vuln` → vulnerable a SSRF
  - `/fetch-safe` → versión mitigada

- **Servicio interno (Flask)**  
  Simula un recurso interno no expuesto públicamente.

- **Frontend (HTML + CSS + JavaScript)**  
  Permite probar visualmente la vulnerabilidad y la mitigación.

---

## 📂 Estructura de carpetas
```
ssrf/
│
├── backend/
│ └── app/
│ ├── main.py
│ ├── ssrf.py
│ └── requirements.txt
│
├── internal_service/
│ ├── app.py
│ └── requirements.txt
│
├── frontend/
│ ├── index.html
│ ├── styles.css
│ └── script.js
│
├── docker-compose.yml
└── README.md
```
---

## ⚙️ Requisitos

- Python
- Docker y Docker Compose
- Navegador web moderno

---

## 🚀 Puesta en marcha

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/billybala/ssrf.git
cd ssrf
```

### 2️⃣ Levantar el servicio interno (Docker)

Este servicio simula un recurso interno accesible solo desde el servidor.

```bash
docker compose up --build internal_service
```

El servicio quedará accesible en `http://127.0.0.1:5001`.

### 3️⃣ Backend FastAPI (entorno virtual)

```bash
python -m venv .venv
source .venv\Scripts\activate # SO Windows
pip install -r backend/app/requirements.txt
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend disponible en `http://127.0.0.1:8000`.

### 4️⃣ Frontend (servidor estático)

```bash
cd frontend
python -m http.server 8080
```

Abrir en el navegador `http://127.0.0.1:8080`.

## 🧪 Pruebas de la vulnerabilidad SSRF

### 🔴 Endpoint vulnerable

```bash
GET /fetch-vuln?url=<URL>
```

Ejemplo desde consola:

```bash
curl "http://127.0.0.1:8000/fetch-vuln?url=http://127.0.0.1:5001/admin/secret"
```

Resultado esperado:

- El backend accede al servicio interno

- Se devuelve información sensible

### 🟢 Endpoint mitigado

```bash
GET /fetch-safe?url=<URL>
```

Ejemplo desde consola:

```bash
curl "http://127.0.0.1:8000/fetch-safe?url=http://127.0.0.1:5001/admin/secret"
```

Resultado esperado:

- Petición bloqueada

- Error 400 indicando acceso a IP interna

### ✔️ Ejemplo permitido

```bash
curl "http://127.0.0.1:8000/fetch-safe?url=https://example.com"
```
