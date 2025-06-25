from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, Service, Client
from django.db.models import Max

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'provider', 'emitted_date', 'expire_date', 'state', 
                  'invoice_type', 'print_number', 'description']
        widgets = {
            'client': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-500 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
            }),
            'service': forms.SelectMultiple(attrs={
                'class': 'w-full p-3 border border-gray-500 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
            }),
            'provider': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-500 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
                'placeholder': 'Nombre del proveedor',
            }),
            'emitted_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-3 border border-gray-500 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
            }),
            'expire_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-3 border border-gray-500 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
            }),
            'state': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-500 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
            }),
            'invoice_type': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-500 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
            }),
            'print_number': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-500 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
                'placeholder': 'Ejemplo: 123456789',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-500 rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200 resize-none',
                'rows': 3,
                'placeholder': 'Agrega detalles adicionales aquí...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expire_date'].required = False
        if not self.instance.pk:  # Esto SOLO funciona aquí
            ultimo = Invoice.objects.aggregate(Max('print_number'))['print_number__max'] or 0
            self.fields['print_number'].initial = ultimo + 1

    def clean_expire_date(self):
        emitted_date = self.cleaned_data.get('emitted_date')
        expire_date = self.cleaned_data.get('expire_date')
        
    

        if expire_date and emitted_date and expire_date < emitted_date:
            raise forms.ValidationError("La fecha de expiración no puede ser anterior a la fecha de emisión.")
        
        return expire_date
    
ServiceFormSet = inlineformset_factory(Invoice, Service, 
                                       fields=['quantity','specification', 'price'], 
                                       extra=1,  # Número de formularios vacíos adicionales
                                       can_delete=True)  # Permite eliminar servicios

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['invoice', 'quantity', 'specification', 'price']
        widgets = {
            'quantity': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
                'placeholder': 'Cantidad',
            }),
            'specification': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200 resize-none',
                'rows': 3,
                'placeholder': 'Agrega especificaciones del servicio aquí...',
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-orange-400 bg-gray-700 text-gray-200',
                'placeholder': 'Precio',
            }),
            'DELETE': forms.HiddenInput(),
        }
