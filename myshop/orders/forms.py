from django import forms
from .models import Order, Postal_Code
from django.utils.translation import ugettext_lazy as _

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address',
                  'postal_code',]
        exclude = ['user',]
        labels = {
            'first_name': _('Nombre(s)'),
            'last_name': _('Apellidos'),
            'email': _('Correo electrónico'),
            'phone': _('Teléfono'),
            'address': _('Dirección'),
            'postal_code': _('Código postal'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['postal_code'].queryset = Postal_Code.objects.filter(postal_code__gte=10000)
