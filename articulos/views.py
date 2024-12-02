from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from .models import Producto, Marca, Boleta,DetalleBoleta
from .forms import  ProductoForm
from django.contrib.auth.decorators import login_required
from .carrito import Carrito
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

def admin_required(login_url=None):
    return user_passes_test(lambda u: u.is_active and u.is_staff, login_url=login_url)

def crear(request):
    return render(request,'crud/crear.html')

def producto_detalle(request, id):
    producto = get_object_or_404(Producto, productoId=id)
    context = {
        'productos': [producto]
    }
    return render(request, 'crud/detalle.html', context)

# CRUD para producto 

@admin_required()
def producto_lista(request):
    productos_list = Producto.objects.all()
    paginator = Paginator(productos_list, 10)
    page = request.GET.get('page')
    
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    
    context = {
        'productos': productos
    }
    return render(request, 'crud/Lista_productos.html', context)


def producto_nuevo(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'crud/crear.html', {'form': form})
    
def producto_editar(request, id):
    producto = get_object_or_404(Producto, productoId=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  
    else:
        form = ProductoForm(instance=producto)

    context = {
        'form': form
    }
    return render(request, 'crud/modificar.html', context)



def producto_borrar(request, pk):
    producto = get_object_or_404(Producto, productoId=pk)
    producto.delete()
    return redirect('Inicio') 

def tienda(request):
    productos_list = Producto.objects.all().order_by('nombre')
    paginator = Paginator(productos_list, 12)
    page = request.GET.get('page')
    
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    
    return render(request, 'vista_usuario/tienda.html', {'productos': productos})


@login_required
def agregar_producto(request, id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, pk=id)
    carrito.agregar(producto=producto)
    page = request.GET.get('page', 1)
    
    return redirect(f'/articulos/tienda/?page={page}')

def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, productoId=producto_id)
    carrito = Carrito(request)
    carrito.eliminar(producto)
    page = request.GET.get('page', 1)
    
    return redirect(f'/articulos/tienda/?page={page}')

def restar_del_carrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(productoId=id)
    carrito.restar(producto = producto)
    page = request.GET.get('page', 1)
    
    return redirect(f'/articulos/tienda/?page={page}')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    page = request.GET.get('page', 1)
    
    return redirect(f'/articulos/tienda/?page={page}')

def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, 'vista_usuario/tienda.html', {'productos': Producto.objects.all()})  


@login_required
def generarBoleta(request):
    carrito = request.session.get('carrito', None)
    if not carrito:
        return render(request, 'carrito/detallecarrito.html', {'error': 'El carrito está vacío.'})

    precio_total = 0
    detalles_boleta = []

    for key, value in carrito.items():
        precio_total += int(value['precio']) * int(value['cantidad'])

    
    boleta = Boleta(total=precio_total, usuario=request.user) 
    boleta.save()

    
    for key, value in carrito.items():
        producto = Producto.objects.get(productoId=value['productoId'])
        cant = value['cantidad']
        subtotal = cant * int(value['precio'])
        detalle = DetalleBoleta(id_boleta=boleta, id_producto=producto, cantidad=cant, subtotal=subtotal)
        detalle.save()
        detalles_boleta.append(detalle)

    datos = {
        'productos': detalles_boleta,
        'fecha': boleta.fecha,
        'total': boleta.total,
        'id_boleta': boleta.id_boleta,
    }

    request.session['boleta'] = boleta.id_boleta

    carrito = Carrito(request)
    carrito.vaciar()

    return render(request, 'carrito/detallecarrito.html', datos)



@login_required
def compras_cliente(request):
    usuario = request.user
    boletas = Boleta.objects.filter(usuario=usuario).distinct()

    compras = []
    for boleta in boletas:
        detalles = DetalleBoleta.objects.filter(id_boleta=boleta)
        compras.append({
            'boleta': boleta,
            'detalles': detalles
        })

    return render(request, 'vista_usuario/compras_cliente.html', {'compras': compras})


@staff_member_required
def ver_compras_todos_clientes(request):
    boletas = Boleta.objects.all().distinct()

    compras = []
    for boleta in boletas:
        detalles = DetalleBoleta.objects.filter(id_boleta=boleta)
        compras.append({
            'boleta': boleta,
            'detalles': detalles,
            'usuario': boleta.usuario
        })

    return render(request, 'vista_admin/compras_todos_clientes.html', {'compras': compras})