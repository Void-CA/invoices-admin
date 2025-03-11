from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice  # Asegúrate de definir este modelo
from .forms import InvoiceForm  # Asegúrate de definir este formulario

def invoice_list(request):
    facturas = Invoice.objects.all()
    return render(request, 'facturas/invoices_list.html', {'invoices': facturas})

def invoice_detail(request, factura_id):  
    factura = get_object_or_404(Invoice, id=factura_id)
    return render(request, 'facturas/invoice_detail.html', {'invoice': factura})


def create_invoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    return render(request, 'facturas/invoice_form.html', {'form': form})

def edit_invoice(request, factura_id):
    factura = get_object_or_404(Invoice, id=factura_id)
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=factura)
    return render(request, 'facturas/formulario_factura.html', {'form': form})

def delete_invoice(request, factura_id):
    factura = get_object_or_404(Invoice, id=factura_id)
    factura.delete()
    return redirect('invoice_list')

def test(request):
    return render(request, 'facturas/testing.html')

def clients(request):
    return render(request, 'facturas/clients.html')

def add_client(request):
    return render(request, 'facturas/add_client.html')