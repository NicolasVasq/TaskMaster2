from django.contrib import admin
from .models import Marca, Producto,Boleta,DetalleBoleta

@admin.register(Marca)
class marcaAdmin(admin.ModelAdmin):
    list_display=['idMarca','nombreMarca']
    

@admin.register(Producto)
class productoAdmin(admin.ModelAdmin):
    list_display=['productoId','nombre','imagen','precio','nombreMarca']

admin.site.register(Boleta)
admin.site.register(DetalleBoleta)

# Register your models here.
