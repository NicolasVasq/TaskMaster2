from django.db import models
from django.contrib.auth.models import User  # Para asociar un vendedor a la solicitud




class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el vendedor (User)
    fecha_pedido = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total(self):
        # Calcula el total del pedido sumando los subtotales de cada detalle
        total = sum(detalle.subtotal for detalle in self.detallepedido_set.all())
        self.total = total
        self.save()


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calcula el subtotal antes de guardar el detalle
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)



class Repartidor(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    ESTADO_TAREA = (
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
    )

    pedido = models.OneToOneField('Pedido', on_delete=models.CASCADE, related_name='tarea')
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'vendedores'}, related_name='tareas_vendedor')
    repartidor = models.ForeignKey(Repartidor, on_delete=models.SET_NULL, null=True, blank=True)  # Asignación del repartidor
    estado = models.CharField(max_length=20, choices=ESTADO_TAREA, default='pendiente')

    def __str__(self):
        return f"Tarea {self.pedido.id} - {self.estado}"