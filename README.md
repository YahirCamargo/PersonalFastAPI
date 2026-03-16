# SchoolarFastAPI

API REST desarrollada con **FastAPI** para un sistema de **tienda en línea**.

Incluye autenticación con **JWT**, gestión de usuarios, productos, carrito de compras, pedidos, direcciones y métodos de pago.

El proyecto implementa una arquitectura modular para separar la lógica de negocio, validación de datos y rutas de la API.

---

# Tecnologías utilizadas

- Python
- FastAPI
- JWT Authentication
- OAuth2 Password Flow
- Pydantic
- Uvicorn
- SQLAlchemy
- PostgreSQL

---

# Características

- Autenticación con **JWT**
- **Refresh Tokens**
- Control de acceso con **OAuth2PasswordBearer**
- CRUD completo de recursos
- Arquitectura modular
- Validaciones con **Pydantic**
- Documentación automática con **Swagger**

---

# Arquitectura del proyecto

El proyecto sigue una arquitectura modular para separar responsabilidades.

```
core/           # Configuración general (JWT, seguridad, settings)
db/             # Configuración de base de datos
dependencies/   # Dependencias reutilizables
exceptions/     # Manejo de errores personalizados
models/         # Modelos de base de datos
routes/         # Definición de endpoints
schemas/        # Validación de datos con Pydantic
services/       # Lógica de negocio
main.py         # Punto de entrada de la aplicación
```

Esta estructura permite:

- separación de responsabilidades  
- código más mantenible  
- mayor escalabilidad  

---

# Módulos principales de la API

## Autenticación

```
POST /api/auth/register
POST /api/auth/register-admin
POST /api/auth/login
POST /api/auth/refresh-token
GET /api/auth/perfil
PATCH /api/auth/perfil
```

Incluye autenticación mediante **JWT y Refresh Tokens**.

---

## Productos

```
GET /api/products
POST /api/products
GET /api/products/{id}
```

Permite registrar productos con:

- nombre
- precio
- SKU
- marca
- dimensiones
- imagen
- categoría

---

## Categorías

```
GET /api/categories
POST /api/categories
PUT /api/categories/{id}
DELETE /api/categories/{id}
```

---

## Métodos de pago

```
GET /api/payment-methods
POST /api/payment-methods
PUT /api/payment-methods/{id}
DELETE /api/payment-methods/{id}
```

---

## Direcciones

```
GET /api/addresses
POST /api/addresses
GET /api/addresses/{id}
PATCH /api/addresses/{id}
DELETE /api/addresses/{id}
```

Permite almacenar múltiples direcciones de envío por usuario.

---

## Carrito de compras

```
GET /api/cart
POST /api/cart
GET /api/cart/{id}
PATCH /api/cart/{id}
DELETE /api/cart/{id}
```

Permite gestionar los productos dentro del carrito del usuario.

---

## Pedidos

```
GET /api/orders
GET /api/orders/{id}
```

---

## Checkout

```
POST /api/checkout
```

Genera un pedido a partir del carrito del usuario.

---

## Envíos

```
GET /api/shippings
POST /api/shippings
GET /api/shippings/{id}
PATCH /api/shippings/{id}
DELETE /api/shippings/{id}
```

Permite registrar el estado y seguimiento de envíos.

---

# Instalación

Clonar repositorio

```
git clone https://github.com/YahirCamargo/spring-schoolar-backend-api.git
```

Entrar al proyecto

```
cd nombre-repo
```

Crear entorno virtual

```
python -m venv venv
```

Activar entorno virtual

```
venv\Scripts\activate
```

Instalar dependencias

```
pip install -r requirements.txt
```

---

# Ejecutar servidor

```
uvicorn main:app --reload
```

API disponible en:

```
http://127.0.0.1:8000
```

Documentación automática:

```
http://127.0.0.1:8000/docs
```

---

# Autor

**Yahir Camargo**

Estudiante de Ingeniería en Sistemas interesado en desarrollo backend y construcción de APIs escalables.