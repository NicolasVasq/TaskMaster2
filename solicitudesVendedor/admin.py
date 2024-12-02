from django.contrib import admin
from .models import Cliente, Producto, Pedido, Repartidor, Tarea

# Registra tus modelos
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Repartidor)
admin.site.register(Tarea)