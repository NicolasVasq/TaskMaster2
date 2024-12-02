from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Pedido, DetallePedido, Cliente, Producto, Tarea
from .forms import PedidoForm, DetallePedidoFormSet, AsignarRepartidorForm
from django.contrib.auth.decorators import login_required

@login_required  # Asegúrate de que solo los usuarios autenticados puedan crear pedidos
def crear_pedido(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    productos = Producto.objects.all()

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        detalle_formset = DetallePedidoFormSet(request.POST)

        if form.is_valid() and detalle_formset.is_valid():
            # Guardar el pedido
            pedido = form.save(commit=False)
            pedido.cliente = cliente
            pedido.vendedor = request.user  # Asignar el vendedor (usuario actual)
            pedido.save()

            # Guardar los detalles del pedido
            for detalle_form in detalle_formset:
                detalle = detalle_form.save(commit=False)
                detalle.pedido = pedido
                detalle.save()

            # Calcular el total del pedido
            pedido.calcular_total()
            pedido.save()

            messages.success(request, 'Pedido creado con éxito.')
            return redirect('solicitudes_lista')  # Asegúrate de que esta URL sea la correcta

        else:
            # Si el formulario no es válido, imprime los errores en la consola
            print(form.errors)
            print(detalle_formset.errors)
            messages.error(request, 'Hubo un error al crear el pedido. Verifica los campos.')
    
    else:
        form = PedidoForm()
        detalle_formset = DetallePedidoFormSet()

    return render(request, 'solicitudes/crear_solicitud.html', {
        'form': form,
        'detalle_formset': detalle_formset,
        'cliente': cliente,
        'productos': productos,
    })


# Vista para listar las solicitudes
def obtener_pedidos(request):
    # Obtener todos los pedidos
    pedidos = Pedido.objects.all()

    # Verificar que realmente estamos obteniendo los pedidos
    print("Pedidos obtenidos:", pedidos)
    
    # Asegúrate de que hay pedidos
    if pedidos:
        for pedido in pedidos:
            print(f"Pedido ID: {pedido.id}, Cliente: {pedido.cliente.nombre}, Total: {pedido.total}")
    else:
        print("No hay pedidos disponibles.")
    
    # Pasar los pedidos al contexto para renderizarlos en la plantilla
    return render(request, 'solicitudes/solicitudes_lista.html', {'pedidos': pedidos})

def obtener_precio_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({
            'precio': producto.precio,
        })
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

def obtener_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        return JsonResponse({
            'nombre': cliente.nombre,
            'rut': cliente.rut,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono
        })
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

def lista_clientes(request):
    clientes = Cliente.objects.all()  # Obtener todos los clientes
    return render(request, 'solicitudes/lista_clientes.html', {'clientes': clientes})  # Pasar 'clientes' al contexto

def generar_informe(request, pedido_id):
    # Obtener el pedido
    pedido = Pedido.objects.get(id=pedido_id)
    
    # Crear la respuesta HTTP para descargar el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_pedido_{pedido.id}.pdf"'
    
    # Crear el objeto canvas para generar el PDF
    c = canvas.Canvas(response, pagesize=letter)
    
    # Título del informe
    c.setFont('Helvetica-Bold', 16)
    c.drawString(100, 750, f'Factura - Pedido ID: {pedido.id}')
    
    # Información del cliente, vendedor y fecha
    c.setFont('Helvetica', 12)
    c.drawString(100, 720, f'Cliente: {pedido.cliente.nombre}')
    c.drawString(100, 700, f'Vendedor: {pedido.vendedor.username}')
    c.drawString(100, 680, f'Fecha del Pedido: {pedido.fecha_pedido}')
    c.drawString(100, 660, f'Total del Pedido: ${pedido.total}')
    
    # Detalles de los productos en el pedido
    c.setFont('Helvetica', 10)
    c.drawString(100, 640, f'Productos solicitados:')
    
    y_position = 620
    for detalle in pedido.detallepedido_set.all():
        c.drawString(100, y_position, f'{detalle.producto.nombre} - Cantidad: {detalle.cantidad} - Subtotal: ${detalle.subtotal}')
        y_position -= 20  # Mover la posición hacia abajo para la siguiente línea
    
    # Si el pedido no tiene productos, mostrar un mensaje
    if y_position <= 640:
        c.drawString(100, y_position, "No se encontraron productos en este pedido.")
    
    # Finalizar el PDF
    c.showPage()
    c.save()
    
    return response

def generar_reporte_general(request):
    # Obtener todos los pedidos
    pedidos = Pedido.objects.all()

    # Crear la respuesta HTTP para descargar el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_general_solicitudes.pdf"'
    
    # Crear el objeto canvas para generar el PDF
    c = canvas.Canvas(response, pagesize=letter)
    
    # Título del reporte
    c.setFont('Helvetica-Bold', 16)
    c.drawString(100, 750, 'Reporte General de Solicitudes')
    c.setFont('Helvetica', 12)
    c.drawString(100, 730, f'Total de Pedidos: {len(pedidos)}')
    
    # Generar los encabezados
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, 710, 'ID Pedido')
    c.drawString(180, 710, 'Cliente')
    c.drawString(300, 710, 'Vendedor')
    c.drawString(420, 710, 'Fecha')
    c.drawString(500, 710, 'Total')

    y_position = 690
    c.setFont('Helvetica', 10)
    
    # Recorrer todos los pedidos y agregar la información al PDF
    for pedido in pedidos:
        c.drawString(100, y_position, str(pedido.id))
        c.drawString(180, y_position, pedido.cliente.nombre if pedido.cliente else 'Sin cliente')
        c.drawString(300, y_position, pedido.vendedor.username if pedido.vendedor else 'Sin vendedor')
        c.drawString(420, y_position, str(pedido.fecha_pedido))
        c.drawString(500, y_position, f'${pedido.total}')
        y_position -= 20

        # Si la posición en Y se acerca al límite inferior de la página, crear una nueva página
        if y_position < 100:
            c.showPage()  # Crear una nueva página
            c.setFont('Helvetica-Bold', 12)
            c.drawString(100, 750, 'Reporte General de Solicitudes')
            c.setFont('Helvetica', 12)
            c.drawString(100, 730, f'Total de Pedidos: {len(pedidos)}')
            c.setFont('Helvetica-Bold', 12)
            c.drawString(100, 710, 'ID Pedido')
            c.drawString(180, 710, 'Cliente')
            c.drawString(300, 710, 'Vendedor')
            c.drawString(420, 710, 'Fecha')
            c.drawString(500, 710, 'Total')
            y_position = 690  # Resetear la posición para los detalles

    # Finalizar el PDF
    c.showPage()
    c.save()

    return response

def ver_pedidos_asignar_repartidor(request):
    # Obtener los pedidos sin tareas asignadas
    pedidos = Pedido.objects.filter(tarea__isnull=True)

    return render(request, 'solicitudes/ver_pedidos_asignar.html', {'pedidos': pedidos})


# Vista para asignar repartidor
def asignar_repartidor(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    tarea, created = Tarea.objects.get_or_create(pedido=pedido)

    if request.method == 'POST':
        form = AsignarRepartidorForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('ver_pedidos_asignar')
    else:
        form = AsignarRepartidorForm(instance=tarea)

    return render(request, 'solicitudes/asignar_tarea.html', {'form': form, 'pedido': pedido})

def obtener_tareas(request):
    tareas = Tarea.objects.all()

    # Imprimir el estado de cada tarea
    for tarea in tareas:
        print(f"Tarea {tarea.id} - Estado: {tarea.get_estado_display()}")

    return render(request, 'solicitudes/obtener_tareas.html', {'tareas': tareas})
