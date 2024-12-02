from django import forms
from .models import Pedido, DetallePedido, Tarea, Repartidor
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['fecha_pedido']

# Formset para Detalles del Pedido
DetallePedidoFormSet = inlineformset_factory(
    Pedido, DetallePedido, fields=['producto', 'cantidad'], extra=1
)

class AsignarRepartidorForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['repartidor']

    repartidor = forms.ModelChoiceField(queryset=Repartidor.objects.all(), required=True)
