from django import forms
from .models import Order
from django.utils.translation import ugettext_lazy as _

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'home_delivery', 'address',
                  'postal_code']
        labels = {
            'first_name': _('Nombre(s)'),
            'last_name': _('Apellidos'),
            'email': _('Correo electrónico'),
            'home_delivery': _('Recoger en tienda'),
            'address': _('Dirección'),
            'postal_code': _('Código postal'),
        }
