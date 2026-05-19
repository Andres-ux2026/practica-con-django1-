# Tutorial Django CRUD paso a paso

> Django 5.2 + SQLite3 — Guía tutorizada para aprender desde cero.

---

## 📋 Índice

1. [Fase 0 — Preparación del entorno](#fase-0--preparación-del-entorno)
2. [Fase 1 — Crear la app y el modelo](#fase-1--crear-la-app-y-el-modelo)
3. [Fase 2 — Admin y migraciones](#fase-2--admin-y-migraciones)
4. [Fase 3 — Views (CBV vs FBV)](#fase-3--views-cbv-vs-fbv)
5. [Fase 4 — URLs y namespacing](#fase-4--urls-y-namespacing)
6. [Fase 5 — Templates y formularios](#fase-5--templates-y-formularios)
7. [Fase 6 — CRUD completo](#fase-6--crud-completo)
8. [Referencias rápidas](#referencias-rápidas)

---

## Fase 0 — Preparación del entorno

### 0.1 Crear y activar entorno virtual

Aísla las dependencias del proyecto para no contaminar el sistema.

**Linux / macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

Verás `(venv)` al inicio del prompt. Para desactivarlo luego: `deactivate`.

| Recurso | Link |
|---------|------|
| `venv` (built-in) | https://docs.python.org/3/library/venv.html |
| Por qué entornos virtuales | https://realpython.com/python-virtual-environments-a-primer/ |

> **Importante:** Cada vez que abras una nueva terminal, reactiva el entorno con `source venv/bin/activate`.

### 0.2 Instalar Django

Con el entorno activo:

```bash
pip install django
```

| Recurso | Link |
|---------|------|
| Instalación Django | https://docs.djangoproject.com/en/5.2/topics/install/ |
| `pip install` | https://pip.pypa.io/en/stable/cli/pip_install/ |

### 0.3 (Opcional) Congelar dependencias

```bash
pip freeze > requirements.txt
```

Esto guarda las versiones. Para reinstalar después: `pip install -r requirements.txt`.

### 0.4 Crear el proyecto

```bash
django-admin startproject config .
```

El `.` final hace que `config/` (settings, urls, wsgi) se cree en la raíz actual, sin subcarpeta extra. Así la estructura queda:

```
manage.py          ← gestión del proyecto
config/
├── __init__.py
├── asgi.py
├── settings.py    ← configuración
├── urls.py        ← urls raíz
└── wsgi.py
```

| Recurso | Link |
|---------|------|
| `startproject` | https://docs.djangoproject.com/en/5.2/ref/django-admin/#startproject |
| Archivos del proyecto | https://docs.djangoproject.com/en/5.2/intro/tutorial01/ |

### 0.5 Ajustar `ALLOWED_HOSTS` (necesario para servir)

En `guia/settings.py` (o `config/settings.py` según el nombre que hayas usado):

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
```

| Recurso | Link |
|---------|------|
| `ALLOWED_HOSTS` | https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts |

### 0.6 Ajustar `CSRF_TRUSTED_ORIGINS` (necesario si usas HTTPS)

Si accedes por `https://` (Codespaces, Gitpod, etc.), agrega en `settings.py`:

```python
CSRF_TRUSTED_ORIGINS = ['https://localhost:8000', 'https://*.github.dev']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

| Recurso | Link |
|---------|------|
| `CSRF_TRUSTED_ORIGINS` | https://docs.djangoproject.com/en/5.2/ref/settings/#csrf-trusted-origins |
| `SECURE_PROXY_SSL_HEADER` | https://docs.djangoproject.com/en/5.2/ref/settings/#secure-proxy-ssl-header |

### 0.7 Verificar funcionamiento

```bash
python manage.py runserver
```

Corta con `Ctrl+C`.

---

## Fase 1 — Crear la app y el modelo

### 1.1 Crear la aplicación

Django separa funcionalidad en **apps**. Para nuestro CRUD creamos una:

```bash
python manage.py startapp articulos
```

Esto crea `articulos/` con:

```
articulos/
├── __init__.py
├── admin.py       ← registro de modelos en admin
├── apps.py        ← configuración de la app
├── migrations/    ← migraciones de base de datos
├── models.py      ← modelos (tablas)
├── tests.py       ← tests
└── views.py       ← vistas (lógica)
```

**Pendiente:** Registrar la app en `config/settings.py` → `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'articulos',
]
```

| Recurso | Link |
|---------|------|
| `startapp` | https://docs.djangoproject.com/en/5.2/ref/django-admin/#startapp |
| Estructura de apps | https://docs.djangoproject.com/en/5.2/intro/tutorial01/#creating-the-polls-app |
| `INSTALLED_APPS` | https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-INSTALLED_APPS |

### 1.2 Escribir el modelo

En `articulos/models.py` creamos una clase por cada tabla. Ejemplo:

```python
from django.db import models

class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    publicado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
```

| Campo | Tipo SQL | Uso |
|-------|----------|-----|
| `CharField` | `VARCHAR` | Texto corto (requiere `max_length`) |
| `TextField` | `TEXT` | Texto largo sin límite |
| `DateTimeField` | `DATETIME` | Fecha y hora |
| `auto_now_add` | — | Pone la fecha actual al crear |
| `__str__` | — | Representación legible en admin/shell |

| Recurso | Link |
|---------|------|
| Modelos | https://docs.djangoproject.com/en/5.2/topics/db/models/ |
| Field types | https://docs.djangoproject.com/en/5.2/ref/models/fields/#field-types |
| `__str__` | https://docs.djangoproject.com/en/5.2/ref/models/instances/#django.db.models.Model.__str__ |

---

## Fase 2 — Admin y migraciones

### 2.1 Crear migraciones

```bash
python manage.py makemigrations articulos
```

Esto genera `articulos/migrations/0001_initial.py`.

### 2.2 Aplicar migraciones

```bash
python manage.py migrate
```

SQLite3 se crea automáticamente como `db.sqlite3`.

| Recurso | Link |
|---------|------|
| Migraciones | https://docs.djangoproject.com/en/5.2/topics/migrations/ |
| `makemigrations` | https://docs.djangoproject.com/en/5.2/ref/django-admin/#makemigrations |
| `migrate` | https://docs.djangoproject.com/en/5.2/ref/django-admin/#migrate |

### 2.3 Registrar en admin

En `articulos/admin.py`:

```python
from django.contrib import admin
from .models import Articulo

admin.site.register(Articulo)
```

Crea un superusuario:

```bash
python manage.py createsuperuser
```

Accede a `http://127.0.0.1:8000/admin/`.

| Recurso | Link |
|---------|------|
| Admin site | https://docs.djangoproject.com/en/5.2/ref/contrib/admin/ |
| `createsuperuser` | https://docs.djangoproject.com/en/5.2/ref/django-admin/#createsuperuser |

---

## Fase 3 — Views (CBV vs FBV)

Django tiene dos estilos de vistas:

| Estilo | Ventaja |
|--------|---------|
| **FBV** — Function Based View | Explícita, fácil de entender |
| **CBV** — Class Based View | Reutilizable, menos código |

Empezamos con **FBV** (más didáctico) y después migramos a **CBV**.

### FBV básica

```python
from django.shortcuts import render
from .models import Articulo

def lista(request):
    articulos = Articulo.objects.all()
    return render(request, 'articulos/lista.html', {'articulos': articulos})
```

### CBV equivalente usando `ListView`

```python
from django.views.generic import ListView
from .models import Articulo

class ArticuloListView(ListView):
    model = Articulo
    template_name = 'articulos/lista.html'
    context_object_name = 'articulos'
```

| Recurso | Link |
|---------|------|
| FBV | https://docs.djangoproject.com/en/5.2/topics/http/views/ |
| CBV (ListView) | https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-display/#listview |
| CBV index | https://docs.djangoproject.com/en/5.2/ref/class-based-views/ |
| `render()` | https://docs.djangoproject.com/en/5.2/topics/http/shortcuts/#render |
| `QuerySet` (`objects.all()`) | https://docs.djangoproject.com/en/5.2/topics/db/queries/ |

---

## Fase 4 — URLs y namespacing

### 4.1 Crear `articulos/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
]
```

### 4.2 Incluir en urls raíz (`guia/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articulos/', include('articulos.urls')),
]
```

> ⚠️ **Importante:** Debe haber **una sola** definición de `urlpatterns`. Borra cualquier bloque anterior que también defina `urlpatterns` en el mismo archivo.

| Recurso | Link |
|---------|------|
| `path()` | https://docs.djangoproject.com/en/5.2/ref/urls/#path |
| `include()` | https://docs.djangoproject.com/en/5.2/ref/urls/#include |
| `name` en URLs | https://docs.djangoproject.com/en/5.2/topics/http/urls/#naming-url-patterns |
| URL dispatcher | https://docs.djangoproject.com/en/5.2/topics/http/urls/ |

---

## Fase 5 — Templates y formularios

### 5.1 Crear la carpeta de templates

```bash
mkdir -p articulos/templates/articulos
```

La estructura queda: `articulos/templates/articulos/`. Django busca templates dentro de `templates/` automáticamente.

### 5.2 Template para listar

Crear `articulos/templates/articulos/lista.html`:

```html
<!DOCTYPE html>
<html>
<head><title>Artículos</title></head>
<body>
  <h1>Artículos</h1>
  <ul>
    {% for articulo in articulos %}
      <li>{{ articulo.titulo }}</li>
    {% endfor %}
  </ul>
</body>
</html>
```

### 5.3 Probar en el navegador

```bash
python manage.py runserver
```

Entra a `http://127.0.0.1:8000/articulos/`. Deberías ver la lista de artículos que creaste desde el admin.

### 5.4 Formulario con `django.forms`

Crear `articulos/forms.py`:

```python
from django import forms
from .models import Articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido']
```

| Recurso | Link |
|---------|------|
| Template language | https://docs.djangoproject.com/en/5.2/ref/templates/language/ |
| `ModelForm` | https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/ |
| Forms | https://docs.djangoproject.com/en/5.2/topics/forms/ |
| Template loading | https://docs.djangoproject.com/en/5.2/topics/templates/ |

---

## Fase 6 — CRUD completo

Vistas necesarias para CRUD:

| Acción | Vista sugiere | URL name |
|--------|---------------|----------|
| Listar | `ListView` (o FBV) | `lista` |
| Crear | `CreateView` (o FBV) | `crear` |
| Detalle | `DetailView` (o FBV) | `detalle` |
| Editar | `UpdateView` (o FBV) | `editar` |
| Eliminar | `DeleteView` (o FBV) | `eliminar` |

### CBV genéricas recomendadas

| Clase | Link |
|-------|------|
| `CreateView` | https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-editing/#createview |
| `DetailView` | https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-display/#detailview |
| `UpdateView` | https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-editing/#updateview |
| `DeleteView` | https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-editing/#deleteview |

### Path parameters en URLs

```python
path('<int:pk>/', views.detalle, name='detalle'),
path('nuevo/', views.crear, name='crear'),
path('<int:pk>/editar/', views.editar, name='editar'),
path('<int:pk>/eliminar/', views.eliminar, name='eliminar'),
```

`<int:pk>` captura un entero y lo pasa como `pk` a la vista.

Documentación: https://docs.djangoproject.com/en/5.2/topics/http/urls/#path-converters

### Redirección después de crear/editar

```python
from django.urls import reverse_lazy

success_url = reverse_lazy('lista')
```

| Recurso | Link |
|---------|------|
| `reverse_lazy` | https://docs.djangoproject.com/en/5.2/ref/urlresolvers/#reverse-lazy |

---

## Referencias rápidas

### Comandos útiles

```bash
python manage.py runserver              # Iniciar servidor
python manage.py makemigrations         # Crear migraciones
python manage.py migrate                # Aplicar migraciones
python manage.py createsuperuser        # Crear admin
python manage.py shell                  # Shell interactiva con Django
python manage.py showmigrations         # Ver estado migraciones
python manage.py sqlmigrate articulos 0001  # Ver SQL generado
```

### Documentación oficial por librería

| Librería | Docs |
|----------|------|
| Django 5.2 | https://docs.djangoproject.com/en/5.2/ |
| Python 3 | https://docs.python.org/3/ |
| SQLite | https://www.sqlite.org/docs.html |
| pip | https://pip.pypa.io/en/stable/ |

### Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `No module named 'django'` | Django no instalado | `pip install django` |
| `Table not found` | No hiciste migrate | `python manage.py migrate` |
| `TemplateDoesNotExist` | Ruta de template incorrecta | Revisa `DIRS` en settings o crea el archivo |
| `Reverse for 'x' not found` | URL name mal escrito | Revisa `name=` en urls.py |
| `OperationalError: no such column` | Modelo cambió sin migrar | `makemigrations` + `migrate` |

---

> **Siguiente paso:** Cuando termines la Fase 0, avísame y seguimos con la Fase 1. Voy a guiarte línea por línea para que escribas cada archivo tú mismo.
