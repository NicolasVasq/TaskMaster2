from django.shortcuts import render
from articulos.models import Producto


def vistaIndex(request):
    productos = Producto.objects.all()
    return render(request,'inicio/index.html',{'productos':productos})
