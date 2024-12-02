# forms.py
from django import forms
from django.forms import widgets
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'imagen', 'precio', 'nombreMarca','stock']
        labels = {
            'nombre': 'Nombre Producto',
            'imagen': 'Imagen del producto',
            'precio': 'Precio del producto',
            'nombreMarca': 'Marca del producto',
            'stock': 'Stock del producto'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto',
                'id': 'nombre'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el precio del producto',
                'id': 'precio'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'imagen'
            }),
            'nombreMarca': forms.Select(attrs={
                'class': 'form-control',
                'id': 'nombreMarca'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el stock del producto',
                'id': 'stock'
            })
        }