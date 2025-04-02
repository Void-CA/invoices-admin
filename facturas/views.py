from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.contrib import messages
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.db.models import Q
from .models import Invoice, Service
from clientes.models import Client
from .forms import InvoiceForm, ServiceForm

def invoice_list(request):
    invoice_list = Invoice.objects.all()  # O cualquier filtro que estés utilizando
    paginator = Paginator(invoice_list, 10)  # 10 facturas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'facturas/invoices_list.html', {'page_obj': page_obj})

def search_invoices(request):
    query = request.GET.get('q', '')

    invoices = Invoice.objects.filter(
        Q(client__name__icontains=query) |
        Q(print_number__icontains=query)
    ).distinct()

    # Convertir los datos en JSON incluyendo `calc_total`
    data = [
        {
            "id": invoice.id,
            "print_number": invoice.print_number,
            "client": invoice.client.name,  # Accede correctamente al nombre del cliente
            "calc_total": invoice.calc_total,  # Accede a la propiedad
            "emitted_date": invoice.emitted_date,
            "expire_date": invoice.expire_date
        }
        for invoice in invoices
    ]

    return JsonResponse(data, safe=False)


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
        formset = ServiceFormSet() 
        for form_i in formset:
            form_i.fields['specification'].widget.attrs.update({'class': 'bg-gray-100 border border-gray-300 rounded-md py-2 px-3 w-full', 'rows': 1,'placeholder': 'Nombre del servicio'})
            form_i.fields['price'].widget.attrs.update({'class': 'bg-gray-100 border border-gray-300 rounded-md py-2 px-3 w-full', 'start': 0, 'step': 100, 'placeholder': 'C$'})

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
