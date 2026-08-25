# ============================================================
# Este NO es un archivo que se ejecuta solo.
# Copia cada bloque a las secciones correspondientes de
# backend/core/settings.py (el que crea django-admin startproject).
# ============================================================

# 1) Agregar a INSTALLED_APPS (ya trae varias por defecto, solo añade estas 3):
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',       # <-- nuevo
    'corsheaders',          # <-- nuevo
    'experiments',          # <-- nuevo (tu app)
]

# 2) Agregar CorsMiddleware AL PRINCIPIO de MIDDLEWARE (antes de CommonMiddleware):
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # <-- nuevo, debe ir primero
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 3) Agregar al final del archivo settings.py:
#    Reemplaza esta URL por la que te dé Codespaces para el puerto 5173
#    (la ves en la pestaña "Ports" una vez que corras el frontend).
CORS_ALLOWED_ORIGINS = [
    "https://TU-CODESPACE-5173.app.github.dev",
    "http://localhost:5173",   # por si alguna vez lo corres fuera de Codespaces
]

# 4) También agrega esto para que Codespaces no bloquee las peticiones por el host:
ALLOWED_HOSTS = ['*']   # en producción real conviene restringir esto, pero para
                        # desarrollo en Codespaces (dominio dinámico) es lo más simple
