from django.shortcuts import render, redirect
from django import forms
from .models import ConfiguracionImpresion
from .utils import listar_impresoras

class ImpresoraForm(forms.Form):
    impresora = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        impresoras = listar_impresoras()
        self.fields['impresora'].choices = [(imp, imp) for imp in impresoras]

def seleccionar_impresora(request):
    if request.method == 'POST':
        form = ImpresoraForm(request.POST)
        if form.is_valid():
            seleccion = form.cleaned_data['impresora']
            ConfiguracionImpresion.objects.all().delete()  # Si solo guardas una global
            ConfiguracionImpresion.objects.create(impresora_predeterminada=seleccion)
            return redirect('impresora_confirmacion')
    else:
        form = ImpresoraForm()

    return render(request, 'settings.html', {'form': form})
