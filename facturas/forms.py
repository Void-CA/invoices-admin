from django import forms
from django.core.exceptions import ValidationError

from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, Service, InvoiceService, Client

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'emitted_date', 'expire_date', 'state', 
                  'invoice_type', 'print_number', 'description']
        widgets = {
            'client': forms.Select(attrs={'class': 'w-full p-2 border rounded-md'}),
            'services': forms.SelectMultiple(attrs={'class': 'w-full p-2 border rounded-md'}),
            'emitted_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-md'}),
            'expire_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-md'}),
            'state': forms.Select(attrs={'class': 'w-full p-2 border rounded-md'}),
            'invoice_type': forms.Select(attrs={'class': 'w-full p-2 border rounded-md'}),
            'print_number': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-md'}),
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
    
# Formset para manejar servicios dentro de la factura
InvoiceServiceFormSet = inlineformset_factory(
        Invoice, InvoiceService, fields=['service'], extra=1, can_delete=True
    )

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['specification', 'price']

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
