from django.shortcuts import render
from .models import Articulo

def lista(request):
    articulos = Articulo.objects.all()
    return render(request, 'articulos/lista.html', {'articulos': articulos})
# Create your views here.
