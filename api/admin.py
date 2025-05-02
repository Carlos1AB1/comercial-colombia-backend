# api/admin.py
from django.contrib import admin
from .models import Categoria, Producto, ImagenProducto, Resena, Reaccion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre',)

class ImagenProductoInline(admin.TabularInline): # Mostrar imágenes dentro del producto
    model = ImagenProducto
    extra = 1 # Cuántos formularios vacíos mostrar
    readonly_fields = ('fecha_subida',)

class ResenaInline(admin.StackedInline): # Mostrar reseñas dentro del producto
    model = Resena
    extra = 0 # No mostrar formularios vacíos por defecto
    readonly_fields = ('ip_resenador', 'fecha_hora_resena')
    fields = ('comentario', 'calificacion', 'ciudad_resenador', 'ip_resenador', 'fecha_hora_resena')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'referencia_muestra', 'fecha_agregado')
    list_filter = ('categoria', 'fecha_agregado')
    search_fields = ('nombre', 'referencia_muestra', 'descripcion')
    inlines = [ImagenProductoInline, ResenaInline] # Añadir inlines

@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'imagen_url', 'alt_text', 'es_principal', 'orden', 'fecha_subida')
    list_filter = ('producto', 'es_principal')
    search_fields = ('alt_text', 'producto__nombre')

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'calificacion', 'ciudad_resenador', 'ip_resenador', 'fecha_hora_resena')
    list_filter = ('calificacion', 'fecha_hora_resena', 'producto__categoria')
    search_fields = ('comentario', 'ciudad_resenador', 'ip_resenador', 'producto__nombre')
    readonly_fields = ('ip_resenador', 'fecha_hora_resena') # No editables

@admin.register(Reaccion)
class ReaccionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'ip_usuario', 'tipo_reaccion', 'fecha_hora_reaccion')
    list_filter = ('tipo_reaccion', 'fecha_hora_reaccion', 'producto__categoria')
    search_fields = ('ip_usuario', 'producto__nombre')
    readonly_fields = ('fecha_hora_reaccion',) # No editable