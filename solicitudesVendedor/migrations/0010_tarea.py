# Generated by Django 5.1.3 on 2024-12-01 04:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudesVendedor', '0009_pedido_vendedor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_proceso', 'En Proceso'), ('completada', 'Completada')], default='pendiente', max_length=20)),
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tarea', to='solicitudesVendedor.pedido')),
                ('repartidor', models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'repartidores'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tareas_repartidor', to=settings.AUTH_USER_MODEL)),
                ('vendedor', models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'vendedores'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tareas_vendedor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
