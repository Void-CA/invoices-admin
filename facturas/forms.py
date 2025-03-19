from django import forms
from django.core.exceptions import ValidationError

from django import forms
from django.forms import inlineformset_factory, formset_factory
from .models import Invoice, Service, Client

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'emitted_date', 'expire_date', 'state', 
                  'invoice_type', 'print_number', 'description']
        widgets = {
    'client': forms.Select(attrs={
        'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400',
    }),
    'service': forms.SelectMultiple(attrs={
        'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400',
    }),
    'emitted_date': forms.DateInput(attrs={
        'type': 'date',
        'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400',
    }),
    'expire_date': forms.DateInput(attrs={
        'type': 'date',
        'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400',
    }),
    'state': forms.Select(attrs={
        'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400',
    }),
    'invoice_type': forms.Select(attrs={
        'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400',
    }),
    'print_number': forms.TextInput(attrs={
        'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400',
        'placeholder': 'Ejemplo: 123456789',
    }),
    'description': forms.Textarea(attrs={
        'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400 resize-none',
        'rows': 4,
        'placeholder': 'Agrega detalles adicionales aquí...',
    }),
}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expire_date'].required = False  

    def clean_expire_date(self):
        emitted_date = self.cleaned_data.get('emitted_date')
        expire_date = self.cleaned_data.get('expire_date')

        if expire_date and emitted_date and expire_date < emitted_date:
            raise forms.ValidationError("La fecha de expiración no puede ser anterior a la fecha de emisión.")
        
        return expire_date
    
ServiceFormSet = inlineformset_factory(Invoice, Service, 
                                       fields=['specification', 'price'], 
                                       extra=1,  # Número de formularios vacíos adicionales
                                       can_delete=True)  # Permite eliminar servicios
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['invoice', 'specification', 'price']
        widgets = {
            'specification': forms.Textarea(attrs={
            'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400 resize-none',
            'rows': 2,
            'placeholder': 'Agrega especificaciones del servicio aquí...',
        }),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'ruc', 'address', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
