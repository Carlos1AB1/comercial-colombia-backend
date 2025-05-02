# Comercial Colombia Backend

Backend API REST para el catálogo virtual de muestras comerciales. Desarrollado con Django y Django REST Framework.

## 📋 Descripción

Este proyecto proporciona una API para gestionar un catálogo de muestras de productos comerciales, permitiendo:

- Gestión de categorías de productos
- Manejo de productos con imágenes múltiples
- Sistema de reseñas de productos
- Sistema de reacciones (likes/dislikes) para productos
- Endpoints optimizados para frontend

## 🛠️ Tecnologías

- **Django 5.2**: Framework web de alto nivel
- **Django REST Framework**: Toolkit para crear APIs REST
- **MySQL**: Base de datos relacional
- **python-dotenv**: Gestión de variables de entorno

## 📦 Modelos

El sistema está compuesto por los siguientes modelos principales:

- **Categoria**: Clasificación de productos
- **Producto**: Muestras comerciales con referencias únicas
- **ImagenProducto**: Imágenes asociadas a cada producto
- **Resena**: Sistema de reseñas y calificaciones (1-5)
- **Reaccion**: Sistema de likes/dislikes para productos

## 🚀 Instalación

### Prerrequisitos

- Python 3.10+
- MySQL
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/comercial_colombia_backend.git
   cd comercial_colombia_backend
   ```

2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crear archivo `.env` en la raíz (usar `.env.example` como referencia):
   ```
   DJANGO_SECRET_KEY='tu_super_clave_secreta_aqui_generada_aleatoriamente'
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   
   DB_NAME=comercial_colombia_muestras
   DB_USER=tu_usuario_mysql
   DB_PASSWORD=tu_password_mysql
   DB_HOST=127.0.0.1
   DB_PORT=3306
   
   CORS_ALLOWED_ORIGINS='http://localhost:3000,http://127.0.0.1:3000'
   ```

5. Crear base de datos MySQL:
   ```sql
   CREATE DATABASE comercial_colombia_muestras CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. Aplicar migraciones:
   ```bash
   python manage.py migrate
   ```

7. Crear superusuario para acceder al panel de administración:
   ```bash
   python manage.py createsuperuser
   ```

8. Iniciar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## 🔍 Endpoints de la API

### Categorías

- `GET /api/v1/categorias/`: Lista todas las categorías
- `GET /api/v1/categorias/{id}/`: Detalle de una categoría

### Productos

- `GET /api/v1/productos/`: Lista todos los productos
- `GET /api/v1/productos/?categoria={id}`: Filtra productos por categoría
- `GET /api/v1/productos/{id}/`: Detalle de un producto

### Reseñas

- `GET /api/v1/resenas/`: Lista todas las reseñas
- `GET /api/v1/resenas/?producto={id}`: Filtra reseñas por producto
- `GET /api/v1/productos/{producto_id}/resenas/`: Reseñas de un producto específico
- `POST /api/v1/productos/{producto_id}/resenas/`: Crea una reseña para un producto

### Reacciones

- `POST /api/v1/reacciones/`: Crea una reacción (like/dislike)
- `DELETE /api/v1/reacciones/{id}/`: Elimina una reacción

## 🔧 Configuración

### Panel de Administración

El sistema incluye un panel de administración completo en `/admin/` donde puedes:

- Gestionar categorías
- Añadir/editar productos con sus imágenes
- Moderar reseñas
- Ver estadísticas de reacciones

### Variables de Entorno

Todas las configuraciones sensibles se manejan a través de variables de entorno:

- `DJANGO_SECRET_KEY`: Clave secreta para Django
- `DJANGO_DEBUG`: Modo depuración (True/False)
- `DJANGO_ALLOWED_HOSTS`: Hosts permitidos
- `DB_*`: Configuración de la base de datos
- `CORS_ALLOWED_ORIGINS`: Orígenes permitidos para CORS

## 👨‍💻 Desarrollo

### Estructura del Proyecto

```
comercial_colombia_backend/
├── api/                    # Aplicación principal
│   ├── migrations/         # Migraciones de la base de datos
│   ├── admin.py            # Configuración del panel de administración
│   ├── models.py           # Modelos de datos
│   ├── serializers.py      # Serializadores para la API
│   ├── urls.py             # Rutas de la API
│   ├── utils.py            # Funciones de utilidad
│   └── views.py            # Vistas y lógica de negocio
├── comercial_colombia_project/  # Configuración del proyecto
│   ├── settings.py         # Configuración general
│   ├── urls.py             # Rutas principales
│   └── wsgi.py             # Configuración WSGI
└── manage.py               # Script de gestión de Django
```
