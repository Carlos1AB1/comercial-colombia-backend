# api/views.py
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # O IsAuthenticatedOrReadOnly si necesitas login
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import IntegrityError

from .models import Categoria, Producto, ImagenProducto, Resena, Reaccion
from .serializers import (
    CategoriaSerializer, ProductoSerializer, ImagenProductoSerializer,
    ResenaSerializer, ReaccionSerializer
)
from .utils import get_client_ip # Importamos la utilidad

# --- ViewSets para CRUD básico ---

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para ver Categorías. Solo lectura.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny] # Cualquiera puede ver categorías

class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para ver Productos. Solo lectura.
    Incluye imágenes, reseñas y conteo de likes/dislikes.
    Permite filtrar por categoría usando ?categoria=<id>
    """
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Opcionalmente filtra los productos por categoría si se pasa
        el parámetro 'categoria' en la URL.
        """
        queryset = Producto.objects.prefetch_related(
            'imagenes', # Optimiza la carga de imágenes relacionadas
            'resenas',  # Optimiza la carga de reseñas relacionadas
            'reacciones' # Necesario para calcular likes/dislikes eficientemente
        ).select_related('categoria').all() # Optimiza carga de categoría

        categoria_id = self.request.query_params.get('categoria')
        if categoria_id is not None:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset

class ImagenProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para ver Imágenes de Productos. Solo lectura.
    (Generalmente se accederá a través del producto anidado)
    """
    queryset = ImagenProducto.objects.all()
    serializer_class = ImagenProductoSerializer
    permission_classes = [AllowAny]

# --- ViewSets con lógica personalizada para creación ---

class ResenaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y crear Reseñas.
    La visualización es pública, la creación requiere datos válidos.
    """
    serializer_class = ResenaSerializer
    permission_classes = [AllowAny] # Cualquiera puede ver y crear reseñas

    def get_queryset(self):
        """
        Filtra las reseñas por producto si se accede a través de una URL anidada
        o si se pasa el parámetro 'producto' en la URL.
        Ejemplo URL: /api/v1/productos/5/resenas/
        Ejemplo URL: /api/v1/resenas/?producto=5
        """
        queryset = Resena.objects.select_related('producto').all()
        producto_id = self.kwargs.get('producto_pk') or self.request.query_params.get('producto')

        if producto_id:
            # Nos aseguramos que el producto exista antes de filtrar
            get_object_or_404(Producto, pk=producto_id)
            queryset = queryset.filter(producto_id=producto_id)
        return queryset

    def perform_create(self, serializer):
        """
        Asigna automáticamente el producto (si viene en la URL) y la IP
        al crear una nueva reseña.
        """
        producto_id = self.kwargs.get('producto_pk') or self.request.data.get('producto')
        if not producto_id:
             raise serializers.ValidationError({"producto": "El ID del producto es requerido."})

        producto = get_object_or_404(Producto, pk=producto_id)
        client_ip = get_client_ip(self.request)
        # Guarda la reseña asociándola al producto y guardando la IP y fecha
        serializer.save(
            producto=producto,
            ip_resenador=client_ip,
            fecha_hora_resena=timezone.now()
        )

class ReaccionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para crear (y potencialmente ver/eliminar) Reacciones (Likes/Dislikes).
    """
    serializer_class = ReaccionSerializer
    permission_classes = [AllowAny] # Cualquiera puede reaccionar
    queryset = Reaccion.objects.all() # Queryset base

    # Solo permitimos crear (POST), ver uno (GET) y quizás eliminar (DELETE).
    # No tiene sentido listar todas las reacciones o actualizar.
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        """
        Opcionalmente filtra por producto si se pasa ?producto=<id>
        """
        queryset = super().get_queryset()
        producto_id = self.request.query_params.get('producto')
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        return queryset


    def perform_create(self, serializer):
        """
        Asigna automáticamente la IP del usuario al crear la reacción.
        Maneja el caso de que el usuario ya haya reaccionado (IntegrityError).
        """
        client_ip = get_client_ip(self.request)
        producto_id = self.request.data.get('producto')
        tipo_reaccion = self.request.data.get('tipo_reaccion')

        if not producto_id:
             raise serializers.ValidationError({"producto": "El ID del producto es requerido."})
        if tipo_reaccion not in [Reaccion.LIKE, Reaccion.DISLIKE]:
             raise serializers.ValidationError({"tipo_reaccion": "El tipo de reacción debe ser 'like' o 'dislike'."})

        producto = get_object_or_404(Producto, pk=producto_id)

        try:
            serializer.save(
                producto=producto,
                ip_usuario=client_ip
            )
        except IntegrityError:
            # Si la restricción unique_together falla, significa que ya existe
            # Podríamos actualizar la reacción existente o simplemente informar
            existing_reaction = Reaccion.objects.filter(producto=producto, ip_usuario=client_ip).first()
            if existing_reaction:
                # Opción 1: Actualizar la reacción existente
                if existing_reaction.tipo_reaccion != tipo_reaccion:
                    existing_reaction.tipo_reaccion = tipo_reaccion
                    existing_reaction.fecha_hora_reaccion = timezone.now() # Actualizar timestamp
                    existing_reaction.save()
                    # Re-serializar la instancia actualizada para la respuesta
                    serializer = self.get_serializer(existing_reaction)
                    # Devolver la instancia actualizada con status 200 OK en lugar de 201 Created
                    # Necesitamos sobreescribir la respuesta que daría perform_create
                    self.saved_instance = serializer.instance # Guardar para la respuesta
                else:
                    # Opción 2: Informar que ya existe y no hacer nada más
                    raise serializers.ValidationError({
                         "detail": "Ya has registrado esta misma reacción para este producto."
                    })
            else:
                 # Si IntegrityError ocurrió por otra razón (poco probable aquí)
                 raise # Relanza la excepción

    # Sobreescribimos create para manejar la respuesta en caso de actualización
    def create(self, request, *args, **kwargs):
        self.saved_instance = None # Resetear instancia guardada
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # Si perform_create actualizó una instancia existente
            if hasattr(self, 'saved_instance') and self.saved_instance:
                 return Response(self.get_serializer(self.saved_instance).data, status=status.HTTP_200_OK, headers=headers)
            # Si se creó una nueva instancia
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
             # Captura explícita de ValidationError para devolver 409 si es por duplicado
             if "detail" in e.detail and "reaccionado" in str(e.detail["detail"]):
                 return Response(e.detail, status=status.HTTP_409_CONFLICT)
             elif "detail" in e.detail and "misma reacción" in str(e.detail["detail"]):
                 # Si intentó poner la misma reacción que ya tenía
                 return Response(e.detail, status=status.HTTP_200_OK) # O 304 Not Modified? 200 es más simple
             # Otros errores de validación
             return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            # Catchall por si algo más falló en la BD a pesar de las validaciones
            return Response({"detail": "Error al procesar la reacción."}, status=status.HTTP_400_BAD_REQUEST)