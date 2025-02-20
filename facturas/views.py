from django.shortcuts import render, get_object_or_404, redirect
from .models import Factura  # Asegúrate de definir este modelo
from .forms import FacturaForm  # Asegúrate de definir este formulario

def lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'facturas/lista_facturas.html', {'facturas': facturas})

def detalle_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    return render(request, 'facturas/detalle_factura.html', {'factura': factura})

def crear_factura(request):
    if request.method == "POST":
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_facturas')
    else:
        form = FacturaForm()
    return render(request, 'facturas/formulario_factura.html', {'form': form})

def editar_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    if request.method == "POST":
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            return redirect('lista_facturas')
    else:
        form = FacturaForm(instance=factura)
    return render(request, 'facturas/formulario_factura.html', {'form': form})

def eliminar_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    factura.delete()
    return redirect('lista_facturas')
