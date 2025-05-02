# comercial_colombia_project/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv # Añadir para python-dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env (añadir esto)
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Carga desde variable de entorno o usa un valor por defecto (menos seguro para dev)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-un-valor-por-defecto-solo-para-dev')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True' # Lee DEBUG desde .env, por defecto True

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',        # Añadir corsheaders

    # Your apps
    'api',                # Añadir nuestra app 'api'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # ¡Añadir ANTES de CommonMiddleware!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'comercial_colombia_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'comercial_colombia_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# --- Configuración de Base de Datos MySQL ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'), # Nombre de tu BD
        'USER': os.getenv('DB_USER'),           # Usuario de BD
        'PASSWORD': os.getenv('DB_PASSWORD'), # Contraseña de BD
        'HOST': os.getenv('DB_HOST'),                  # O la IP/hostname de tu servidor MySQL
        'PORT': os.getenv('DB_PORT'),                      # Puerto estándar de MySQL
        'OPTIONS': {
            # Asegúrate de que la base de datos MySQL use UTF8MB4
            'charset': 'utf8mb4',
            # Opcional: modo estricto SQL
            # 'sql_mode': 'STRICT_TRANS_TABLES',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-co' # Español Colombia

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True # Habilitar soporte para zonas horarias


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles' # Descomentar para producción (collectstatic)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Configuración Django REST Framework ---
REST_FRAMEWORK = {
    # Permisos por defecto (puedes ajustarlos luego si necesitas autenticación)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Cualquiera puede acceder por ahora
    ],
    # Paginación por defecto (opcional)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10 # Número de items por página
}

# --- Configuración CORS ---
# Orígenes permitidos (¡IMPORTANTE para tu frontend!)
# En desarrollo, puedes permitir el origen de tu servidor de desarrollo de frontend
# Ejemplo: si tu frontend corre en http://localhost:3000
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000, http://localhost:5173, http://127.0.0.1:5173",' # Añade aquí el origen de tu frontend
).split(',')



# O, para desarrollo MUY temprano (menos seguro), permitir todos:
# CORS_ALLOW_ALL_ORIGINS = True # Cuidado con esto en producción

# Métodos HTTP permitidos
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Cabeceras permitidas
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]