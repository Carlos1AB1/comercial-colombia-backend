# api/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción")
    imagen_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="URL de Imagen")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
        # db_table = 'Categorias' # Descomentar si necesitas que el nombre sea EXACTO al SQL

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.RESTRICT, # No borrar categoría si tiene productos
        related_name='productos', # Permite acceder desde Categoria: cat.productos.all()
        verbose_name="Categoría"
    )
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción")
    referencia_muestra = models.CharField(
        max_length=50, null=True, blank=True, unique=True, verbose_name="Referencia Muestra"
    )
    video_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="URL de Video")
    fecha_agregado = models.DateTimeField(default=timezone.now, verbose_name="Fecha Agregado")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_agregado', 'nombre']
        # db_table = 'Productos'

    def __str__(self):
        return self.nombre

class ImagenProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE, # Borrar imágenes si se borra el producto
        related_name='imagenes', # Permite acceder desde Producto: prod.imagenes.all()
        verbose_name="Producto"
    )
    imagen_url = models.URLField(max_length=255, verbose_name="URL de Imagen")
    alt_text = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Texto Alternativo"
    )
    es_principal = models.BooleanField(default=False, verbose_name="Es Principal")
    orden = models.IntegerField(default=0, verbose_name="Orden")
    fecha_subida = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Subida")

    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Producto"
        ordering = ['producto', 'orden', '-es_principal']
        # db_table = 'ImagenesProducto'

    def __str__(self):
        return f"Imagen de {self.producto.nombre} ({self.id})"

class Resena(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE, # Borrar reseñas si se borra el producto
        related_name='resenas', # Permite acceder desde Producto: prod.resenas.all()
        verbose_name="Producto"
    )
    comentario = models.TextField(verbose_name="Comentario")
    calificacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Calificación (1-5)"
    )
    ciudad_resenador = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ciudad")
    ip_resenador = models.GenericIPAddressField(verbose_name="IP Reseñador")
    fecha_hora_resena = models.DateTimeField(default=timezone.now, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-fecha_hora_resena']
        # db_table = 'Resenas'
        # Añadir constraints si es necesario (ej: check en versiones > Django 3.2)
        # constraints = [
        #     models.CheckConstraint(check=models.Q(calificacion__gte=1) & models.Q(calificacion__lte=5), name='chk_calificacion_range')
        # ]

    def __str__(self):
        return f"Reseña de {self.producto.nombre} ({self.calificacion} estrellas)"

class Reaccion(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    TIPO_REACCION_CHOICES = [
        (LIKE, 'Me gusta'),
        (DISLIKE, 'No me gusta'),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE, # Borrar reacciones si se borra el producto
        related_name='reacciones', # Permite acceder desde Producto: prod.reacciones.all()
        verbose_name="Producto"
    )
    ip_usuario = models.GenericIPAddressField(verbose_name="IP Usuario")
    tipo_reaccion = models.CharField(
        max_length=10,
        choices=TIPO_REACCION_CHOICES,
        verbose_name="Tipo de Reacción"
    )
    fecha_hora_reaccion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Reacción"
        verbose_name_plural = "Reacciones"
        ordering = ['-fecha_hora_reaccion']
        # Restricción única para que una IP solo pueda reaccionar una vez por producto
        unique_together = ('producto', 'ip_usuario')
        # db_table = 'Reacciones'

    def __str__(self):
        return f"{self.get_tipo_reaccion_display()} de {self.ip_usuario} en {self.producto.nombre}"