# Reemplaza el contenido de backend/core/urls.py por esto completo:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('experiments.urls')),
]
