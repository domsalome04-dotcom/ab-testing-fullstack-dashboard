# Backend starter — ab-testing-fullstack-dashboard

Estos archivos asumen que ya corriste, dentro de `backend/` en tu Codespace:

```bash
python -m venv venv
source venv/bin/activate
pip install django djangorestframework django-cors-headers gunicorn
django-admin startproject core .
python manage.py startapp experiments
```

## Dónde va cada archivo

```
backend/
├── core/
│   ├── settings.py     <- pega los 4 bloques de settings_snippet.py aquí
│   └── urls.py          <- REEMPLAZA por el contenido de core_urls.py
├── experiments/
│   ├── models.py         <- REEMPLAZA por experiments/models.py de este paquete
│   ├── serializers.py     <- CREAR (no existe por defecto), pega experiments/serializers.py
│   ├── views.py           <- REEMPLAZA por experiments/views.py
│   ├── urls.py             <- CREAR (no existe por defecto), pega experiments/urls.py
│   ├── admin.py            <- REEMPLAZA por experiments/admin.py
│   └── management/
│       ├── __init__.py                          <- CREAR, vacío
│       └── commands/
│           ├── __init__.py                       <- CREAR, vacío
│           └── load_experiment_data.py            <- CREAR, pega el archivo completo
├── data/                  <- CREAR esta carpeta
│   ├── experiment_summary.csv       <- copia de tu repo ux_ab_testing_analysis_complete/data/processed/
│   ├── statistical_results.csv      <- ídem
│   ├── experiment_decision.json     <- ídem
│   ├── exposure_analysis.csv        <- ídem
│   ├── conversion_by_day.csv        <- ídem
│   └── conversion_by_hour.csv       <- ídem
└── requirements.txt        <- REEMPLAZA por requirements.txt de este paquete
```

## Pasos para dejarlo corriendo

```bash
# 1. Copia los 6 archivos de datos desde tu otro repo a backend/data/
#    (clónalo aparte o descarga esos 6 archivos y súbelos a Codespaces)

# 2. Migraciones
python manage.py makemigrations experiments
python manage.py migrate

# 3. Crear un superusuario para poder entrar al admin de Django
python manage.py createsuperuser

# 4. Cargar los datos reales
python manage.py load_experiment_data --data-dir data

# Deberías ver algo como:
# Experimento creado: 'UX A/B Testing — Marketing Campaign (ad vs psa)'
#   - 5 bandas de exposición
#   - 7 días
#   - 24 horas

# 5. Levantar el servidor
python manage.py runserver 0.0.0.0:8000
```

## Verificar que funciona (antes de tocar React)

Con el servidor corriendo, en el navegador (usa la URL pública que te da la pestaña "Ports" de Codespaces para el puerto 8000, agregando la ruta):

- `/api/experiments/` → debe mostrar una lista con 1 experimento (versión resumida)
- `/api/experiments/1/` → debe mostrar el detalle completo, con `exposure_bands`, `day_conversions` y `hour_conversions` anidados
- `/admin/` → inicia sesión con tu superusuario y deberías poder ver y editar el experimento visualmente

Si estos tres funcionan, el backend está listo. Ahí es cuando pasamos a conectar React.

## Nota sobre PATCH

Para probar que el CRUD funciona de verdad (no solo GET), prueba esto desde la pestaña de administración de DRF (la interfaz navegable que aparece automáticamente en `/api/experiments/1/`, con un formulario abajo) o con `curl`:

```bash
curl -X PATCH http://localhost:8000/api/experiments/1/ \
  -H "Content-Type: application/json" \
  -d '{"decision": "Reject H0 — Revisado manualmente"}'
```

Eso actualiza solo el campo `decision`, sin tocar el resto — es la operación PATCH que puedes mencionar en tu CV con evidencia real detrás.
