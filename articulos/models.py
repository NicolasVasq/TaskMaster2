from django.db import models
from django.core.files.storage import default_storage
from django.contrib.auth.models import User


class Marca(models.Model):
    idMarca = models.AutoField(primary_key=True, verbose_name="Id de Marca")
    nombreMarca=models.CharField(max_length=50, blank=True, verbose_name="Nombre Marca")

    def __str__(self):
        return self.nombreMarca


class Producto(models.Model):
    productoId = models.AutoField(primary_key=True, verbose_name="Id Producto")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    imagen = models.ImageField(upload_to="imagenes", null=True, blank=True, verbose_name="Imagen")
    precio = models.IntegerField(blank=True, null=True, verbose_name="Precio")
    nombreMarca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name="Marca")
    stock = models.PositiveIntegerField(verbose_name="Stock",default=0)

    def __str__(self):
        return self.nombre
    
    
class Boleta(models.Model):
    id_boleta = models.AutoField(primary_key=True, verbose_name="Id Boleta")
    fecha = models.DateTimeField(auto_now_add=True , verbose_name="Fecha")
    total = models.BigIntegerField(verbose_name="Total")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return str(self.id_boleta)

class DetalleBoleta(models.Model):
    id_boleta = models.ForeignKey(Boleta,blank= True, on_delete=models.CASCADE)
    id_detalle_boleta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.BigIntegerField()

    def __str__(self):
        return str(self.id_detalle_boleta)