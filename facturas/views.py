from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from .models import Invoice, Client, Service
from .forms import InvoiceForm, ClientForm, ServiceForm

def invoice_list(request):
    facturas = Invoice.objects.all()
    return render(request, 'facturas/invoices_list.html', {'invoices': facturas})

def invoice_detail(request, invoice_id):  
    factura = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'facturas/invoice_detail.html', {'invoice': factura})


def create_invoice(request):
    ServiceFormSet = formset_factory(ServiceForm, extra=1)  # Formset basado en formulario

    if request.method == "POST":
        invoice_form = InvoiceForm(request.POST)
        formset = ServiceFormSet(request.POST)

        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save()  # Guarda la factura primero

            services = []
            for form in formset:
                if form.cleaned_data:  # Evitar formularios vacíos
                    service = form.save()
                    services.append(service)

            # Asignar los servicios a la factura
            invoice.service.set(services)

            return redirect('invoice_list')  # Redirigir tras guardar

    else:
        invoice_form = InvoiceForm()
        formset = ServiceFormSet()

    return render(request, 'facturas/invoice_form.html', {
        'invoice_form': invoice_form,
        'formset': formset,
    })



ServiceFormSet = formset_factory(ServiceForm, extra=1)

def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    form = InvoiceForm(instance=invoice)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)

        if form.is_valid():
            form.save()
            return redirect('invoice_list')

    return render(request, 'facturas/invoice_form.html', {
        'invoice_form': form,
        'invoice': invoice,
    })

def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
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
    