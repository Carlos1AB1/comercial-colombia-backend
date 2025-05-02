# comercial_colombia_project/urls.py
from django.contrib import admin
from django.urls import path, include # Asegúrate de importar include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Prefijo para todas las URLs de nuestra API
    path('api/v1/', include('api.urls')), # Añade esta línea
]