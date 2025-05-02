# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers # Para rutas anidadas

from .views import (
    CategoriaViewSet, ProductoViewSet, ImagenProductoViewSet,
    ResenaViewSet, ReaccionViewSet
)

# Router principal
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'imagenes', ImagenProductoViewSet, basename='imagenproducto') # Ruta base para imágenes
router.register(r'resenas', ResenaViewSet, basename='resena') # Ruta base para reseñas
router.register(r'reacciones', ReaccionViewSet, basename='reaccion') # Ruta base para reacciones

# Router anidado para Reseñas dentro de Productos
# Esto creará URLs como /api/v1/productos/{producto_pk}/resenas/
productos_router = routers.NestedSimpleRouter(router, r'productos', lookup='producto')
productos_router.register(r'resenas', ResenaViewSet, basename='producto-resenas')

# Puedes añadir más rutas anidadas si lo necesitas, por ejemplo, para imágenes o reacciones por producto
# productos_router.register(r'imagenes', ImagenProductoViewSet, basename='producto-imagenes')
# productos_router.register(r'reacciones', ReaccionViewSet, basename='producto-reacciones')

urlpatterns = [
    # Incluye las URLs generadas por el router principal
    path('', include(router.urls)),
    # Incluye las URLs generadas por el router anidado
    path('', include(productos_router.urls)),
]

# Las URLs generadas serán algo como:
# /api/v1/categorias/
# /api/v1/categorias/{id}/
# /api/v1/productos/
# /api/v1/productos/{id}/
# /api/v1/productos/{producto_pk}/resenas/       <-- Anidada
# /api/v1/productos/{producto_pk}/resenas/{id}/  <-- Anidada
# /api/v1/imagenes/
# /api/v1/resenas/
# /api/v1/reacciones/
# /api/v1/reacciones/{id}/