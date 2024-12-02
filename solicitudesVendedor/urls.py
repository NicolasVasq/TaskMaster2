from django.urls import path
from .views import crear_pedido , obtener_precio_producto, obtener_cliente, obtener_pedidos, lista_clientes, generar_informe, generar_reporte_general,ver_pedidos_asignar_repartidor, asignar_repartidor, obtener_tareas

urlpatterns = [
    path('crear/<int:cliente_id>/', crear_pedido, name='crear_solicitud'),
    path('pedidos/', obtener_pedidos, name='solicitudes_lista'),
    path('lista_clientes/',lista_clientes, name='lista_clientes'),
    path('generar_informe/<int:pedido_id>/', generar_informe, name='generar_informe'),
    path('generar_reporte_general/', generar_reporte_general, name='generar_reporte_general'),
    path('ver_pedidos_asignar', ver_pedidos_asignar_repartidor, name='ver_pedidos_asignar'),
    path('pedidos/assignar_repartidor/<int:pedido_id>/', asignar_repartidor, name='asignar_tarea'),
    path('obtener_tareas', obtener_tareas, name='obtener_tareas'),
]
