# Generated by Django 5.1.3 on 2024-12-01 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('Administrador', 'Administrador'), ('Supervisor', 'Supervisor'), ('Vendedor', 'Vendedor')], max_length=20),
        ),
    ]
