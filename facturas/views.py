from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory, inlineformset_factory
from .models import Invoice, Client, Service, InvoiceService
from .forms import InvoiceForm, ClientForm, ServiceForm, InvoiceServiceFormSet

def invoice_list(request):
    facturas = Invoice.objects.all()
    return render(request, 'facturas/invoices_list.html', {'invoices': facturas})

def invoice_detail(request, invoice_id):  
    factura = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'facturas/invoice_detail.html', {'invoice': factura})


def create_invoice(request):
    ServiceFormSet = modelformset_factory(Service, form=ServiceForm, extra=1)

    if request.method == "POST":
        invoice_form = InvoiceForm(request.POST)
        formset = ServiceFormSet(request.POST)

        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save()  # Guarda la factura en la BD
            for form in formset:
                service = form.save(commit=False)
                service.invoice = invoice  # Relaciona con la factura
                service.save()

            return redirect('invoice_list')  # Redirigir a la lista de facturas

    else:
        invoice_form = InvoiceForm()
        formset = ServiceFormSet(queryset=Service.objects.none())

    return render(request, 'facturas/invoice_form.html', {
        'invoice_form': invoice_form,
        'formset': formset
    })

def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    form = InvoiceForm(instance=invoice)
    formset = InvoiceServiceFormSet(instance=invoice)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceServiceFormSet(request.POST, instance=invoice)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('invoice_list')

    return render(request, 'facturas/invoice_form.html', {
        'invoice_form': form,
        'formset': formset,
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
    