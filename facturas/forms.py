from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'date', 'total']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})  # 📅 Activa el calendario
        }
