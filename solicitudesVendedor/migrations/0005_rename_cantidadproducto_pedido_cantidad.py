# Generated by Django 5.1.3 on 2024-11-30 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudesVendedor', '0004_detallepedido_direccioncliente_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='cantidadProducto',
            new_name='cantidad',
        ),
    ]
