from django import forms
from .models import Invoice, Client

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'date', 'total']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})  # 📅 Activa el calendario
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'RUC', 'email', 'phone']