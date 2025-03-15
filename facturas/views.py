from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice, Client
from .forms import InvoiceForm, ClientForm  

def invoice_list(request):
    facturas = Invoice.objects.all()
    return render(request, 'facturas/invoices_list.html', {'invoices': facturas})

def invoice_detail(request, invoice_id):  
    factura = get_object_or_404(Invoice, id=invoice_id)
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

def edit_invoice(request, invoice_id):
    factura = get_object_or_404(Invoice, id=invoice_id)
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=factura)
    return render(request, 'facturas/invoice_form.html', {'form': form})

def delete_invoice(request, factura_id):
    factura = get_object_or_404(Invoice, id=factura_id)
    factura.delete()
    return redirect('invoice_list')

def test(request):
    return render(request, 'facturas/testing.html')

def clients(request):
    return render(request, 'facturas/clients.html')

def client_form(request, client_id=None):
    if client_id: 
        client = get_object_or_404(Client, id=client_id)
    else:  
        client = None
    
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients') 
    else:
        form = ClientForm(instance=client)

    return render(request, 'facturas/client_form.html', {'form': form})
    