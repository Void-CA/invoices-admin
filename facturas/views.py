from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from .models import Invoice, Service
from .forms import InvoiceForm, ServiceForm
from django.shortcuts import render, redirect
from django.contrib import messages

def invoice_list(request):
    facturas = Invoice.objects.all()
    return render(request, 'facturas/invoices_list.html', {'invoices': facturas})

def invoice_detail(request, invoice_id):  
    factura = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'facturas/invoice_detail.html', {'invoice': factura})


def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = ServiceFormSet(request.POST)  # Asegurar que se crea correctamente

        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            services = formset.save(commit=False)

            for service in services:
                service.invoice = invoice
                service.save()

            messages.success(request, "Factura creada con éxito.")
            return redirect('invoice_list')
        else:
            messages.error(request, "Hubo un error al crear la factura.")
    else:
        form = InvoiceForm()
        formset = ServiceFormSet()  # ✅ Esto debe estar presente

    return render(request, 'facturas/invoice_form.html', {
        'invoice_form': form,
        'formset': formset  # ✅ Se pasa el formset correctamente
    })




ServiceFormSet = inlineformset_factory(Invoice, Service, fields=['specification', 'price'], extra=1, can_delete=True)

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



    