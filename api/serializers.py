# api/serializers.py
from rest_framework import serializers
from .models import Categoria, Producto, ImagenProducto, Resena, Reaccion
from django.db.models import Count, Q # Para contar likes/dislikes

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'imagen_url', 'fecha_creacion']

class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        # Excluimos 'producto' porque se anidará o vendrá del contexto
        fields = ['id', 'imagen_url', 'alt_text', 'es_principal', 'orden', 'fecha_subida']

class ResenaSerializer(serializers.ModelSerializer):
    # Hacemos que producto sea de solo lectura al serializar,
    # se asignará en la vista al crear.
    producto = serializers.PrimaryKeyRelatedField(read_only=True)
    # Hacemos la IP de solo lectura, se asignará en la vista.
    ip_resenador = serializers.IPAddressField(read_only=True)
    # La fecha se asigna automáticamente
    fecha_hora_resena = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Resena
        fields = [
            'id', 'producto', 'comentario', 'calificacion',
            'ciudad_resenador', 'ip_resenador', 'fecha_hora_resena'
        ]
        read_only_fields = ['ip_resenador', 'fecha_hora_resena'] # Campos que no deben venir del cliente

    def validate_calificacion(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5.")
        return value

class ProductoSerializer(serializers.ModelSerializer):
    # Mostrar el nombre de la categoría en lugar del ID (solo lectura)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    # Anidar las imágenes del producto (solo lectura)
    imagenes = ImagenProductoSerializer(many=True, read_only=True)
    # Anidar las reseñas del producto (solo lectura)
    resenas = ResenaSerializer(many=True, read_only=True)
    # Campos calculados para likes y dislikes
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id', 'categoria', 'categoria_nombre', 'nombre', 'descripcion',
            'referencia_muestra', 'video_url', 'fecha_agregado',
            'imagenes', # Lista de imágenes anidadas
            'resenas',  # Lista de reseñas anidadas
            'likes_count',
            'dislikes_count',
        ]
        # 'categoria' es escribible (para asignar al crear/actualizar),
        # 'categoria_nombre' es solo para lectura.
        extra_kwargs = {
            'categoria': {'write_only': True, 'required': True}
        }

    def get_likes_count(self, obj):
        # Contar reacciones de tipo 'like' para este producto (obj)
        return Reaccion.objects.filter(producto=obj, tipo_reaccion=Reaccion.LIKE).count()

    def get_dislikes_count(self, obj):
        # Contar reacciones de tipo 'dislike' para este producto (obj)
        return Reaccion.objects.filter(producto=obj, tipo_reaccion=Reaccion.DISLIKE).count()

class ReaccionSerializer(serializers.ModelSerializer):
    # Hacemos producto escribible para asociar la reacción
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    # Hacemos IP de solo lectura
    ip_usuario = serializers.IPAddressField(read_only=True)
    # La fecha se asigna automáticamente
    fecha_hora_reaccion = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Reaccion
        fields = [
            'id', 'producto', 'ip_usuario', 'tipo_reaccion', 'fecha_hora_reaccion'
        ]
        read_only_fields = ['ip_usuario', 'fecha_hora_reaccion']

    # Validación adicional para asegurar que una IP no reaccione dos veces al mismo producto
    # Esto complementa el `unique_together` de la base de datos
    def validate(self, data):
        # En creación (no hay `self.instance`) o si el producto/IP cambian en actualización
        request = self.context.get('request')
        ip_usuario = self.get_client_ip(request) if request else None
        producto = data.get('producto')

        if ip_usuario and producto:
            # Comprobar si ya existe una reacción para esta IP y producto
            query = Reaccion.objects.filter(producto=producto, ip_usuario=ip_usuario)
            # Si estamos actualizando, excluimos la instancia actual de la comprobación
            if self.instance:
                query = query.exclude(pk=self.instance.pk)

            if query.exists():
                raise serializers.ValidationError({
                    "detail": "Ya has reaccionado a este producto."
                })
        return data

    # Función helper para obtener IP (podría ir en utils.py)
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip