from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('lista'), name='inicio'),
    path('admin/', admin.site.urls),
    path('articulos/', include('articulos.urls')),
]


