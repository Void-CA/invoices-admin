from django import forms
from .models import Factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente', 'fecha', 'total']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})  # 📅 Activa el calendario
        }
