from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.contrib import messages
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import transaction
from .models import Invoice, Service
from clientes.models import Client
from .forms import InvoiceForm, ServiceForm
from datetime import datetime
from .utils import *
import requests

def invoice_list(request):
    # Obtener filtros desde la URL
    cliente = request.GET.get('cliente', '')
    estado = request.GET.get('estado', '')

    # Aplicar filtros al queryset base
    invoice_list = Invoice.objects.all()
    if cliente:
        invoice_list = invoice_list.filter(cliente__icontains=cliente)
    if estado:
        invoice_list = invoice_list.filter(estado=estado)

    # Paginación
    paginator = Paginator(invoice_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pasar los filtros al template para que se mantengan
    context = {
        'page_obj': page_obj,
        'cliente': cliente,
        'estado': estado,
        'get_params': request.GET.urlencode(),  # para reconstruir URLs
    }
    return render(request, 'facturas/invoices_list.html', context)

def search_invoices(request):
    query = request.GET.get('q', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    estado = request.GET.get('estado', '')
    tipo_factura = request.GET.get('tipo_factura', '')
    cliente = request.GET.get('cliente', '')
    monto_min = request.GET.get('monto_min', '')
    monto_max = request.GET.get('monto_max', '')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))

    # Filtrar las facturas
    invoices = filter_invoices(query, fecha_inicio, fecha_fin, estado, tipo_factura, cliente, monto_min, monto_max)

    # Paginación de las facturas
    page_obj, paginator = paginate_invoices(invoices, page, per_page)

    # Convertir los datos en JSON
    data = {
        "invoices": [
            {
                "id": invoice.id,
                "print_number": invoice.print_number,
                "client": invoice.client.name,
                "calc_total": invoice.calc_total,
                "emitted_date": invoice.emitted_date,
                "expire_date": invoice.expire_date
            }
            for invoice in page_obj
        ],
        "pagination": {
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
            "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        }
    }

    return JsonResponse(data)

def invoice_detail(request, invoice_id):  
    factura = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'facturas/invoice_detail.html', {'invoice': factura})

ServiceFormSet = inlineformset_factory(Invoice, Service, fields=['specification', 'price'], extra=1, can_delete=True)
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = ServiceFormSet(request.POST, prefix='services')  # Usar prefijo 'services'

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
        formset = ServiceFormSet(prefix='services')  # Usar prefijo 'services'
        for form_i in formset:
            form_i.fields['specification'].widget.attrs.update({'class': 'bg-gray-100 border border-gray-300 rounded-md py-2 px-3 w-full', 'rows': 3,'placeholder': 'Nombre del servicio'})
            form_i.fields['price'].widget.attrs.update({'class': 'bg-gray-100 border border-gray-300 rounded-md py-2 px-3 w-full', 'start': 0, 'step': 0.01, 'placeholder': 'C$'})

    return render(request, 'facturas/invoice_form.html', {
        'invoice_form': form,
        'formset': formset  # ✅ Se pasa el formset correctamente
    })

def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        formset = ServiceFormSet(request.POST, instance=invoice, prefix='services')
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar la factura
                    invoice = form.save()
                    
                    # Guardar los servicios
                    services = formset.save(commit=False)
                    for service in services:
                        service.invoice = invoice
                        service.save()
                    
                    # Eliminar servicios marcados para eliminar
                    for service in formset.deleted_objects:
                        service.delete()
                    
                    messages.success(request, "Factura actualizada con éxito.")
                    return redirect('invoice_list')
            except Exception as e:
                messages.error(request, f"Error al guardar la factura: {str(e)}")
                print(f"Error al guardar la factura: {str(e)}")  # Para debugging
        else:
            if form.errors:
                print("Errores en el formulario:", form.errors)  # Para debugging
                messages.error(request, f"Errores en el formulario: {form.errors}")
            if formset.errors:
                print("Errores en el formset:", formset.errors)  # Para debugging
                messages.error(request, f"Errores en los servicios: {formset.errors}")
            if formset.non_form_errors():
                print("Errores no-form en el formset:", formset.non_form_errors())  # Para debugging
                messages.error(request, f"Errores en los servicios: {formset.non_form_errors()}")
    else:
        form = InvoiceForm(instance=invoice)
        formset = ServiceFormSet(instance=invoice, prefix='services')

    # Estética del formset
    for form_i in formset:
        form_i.fields['specification'].widget.attrs.update({
            'class': 'bg-gray-100 border border-gray-300 rounded-md py-2 px-3 w-full',
            'rows': 3,
            'placeholder': 'Nombre del servicio'
        })
        form_i.fields['price'].widget.attrs.update({
            'class': 'bg-gray-100 border border-gray-300 rounded-md py-2 px-3 w-full',
            'start': 0,
            'step': 0.01,
            'placeholder': 'C$'
        })

    return render(request, 'facturas/invoice_form.html', {
        'invoice_form': form,
        'formset': formset,
        'invoice': invoice,
        'is_edit': True,
    })

def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    return redirect('invoice_list')

@csrf_exempt
def print_invoice(request, invoice_id):
    try:
        if request.method == 'POST':
            invoice = get_object_or_404(Invoice, id=invoice_id)

            context = {
                'invoice': invoice,
                'services': invoice.services.all(),
                'client': invoice.client,
                'date': invoice.emitted_date,
                'total': invoice.calc_total,
                'state': invoice.state,
                'invoice_type': invoice.invoice_type,
                'address': invoice.client.address,
                'phone': invoice.client.phone,
            }

            filename = f'generated_invoice.pdf'
            pdf_path = create_pdf(context, filename)

            print("Abriendo archivo PDF...")
            with open(pdf_path, 'rb') as pdf_file:
                print("Preparando archivo para enviar...")
                files = {'file': (filename, pdf_file, 'application/pdf')}
                data = {'printer_name': settings.PRINTER_NAME}

                print("Enviando solicitud al servicio de impresión...")
                response = requests.post('http://host.docker.internal:5001/printing', files=files, data=data)
                print(f"Respuesta del servidor Flask: {response.status_code} - {response.text}")
                response.raise_for_status()

            return JsonResponse({'mensaje': 'Factura enviada a imprimir correctamente'})

        return JsonResponse({'error': 'Método no permitido'}, status=405)

    except FileNotFoundError:
        print("Error: archivo PDF no encontrado.")
        return JsonResponse({'error': 'No se encontró el archivo PDF generado'}, status=500)

    except requests.RequestException as e:
        print(f"Error al enviar a imprimir: {e}")
        return JsonResponse({'error': 'Error al enviar a imprimir', 'detalle': str(e)}, status=500)

    except Exception as e:
        print(f"Error inesperado: {e}")
        return JsonResponse({'error': 'Error interno en el servidor', 'detalle': str(e)}, status=500)

def download_invoice(request, invoice_id):
    return render(request, 'facturas/invoice_list.html')
    
def test(request):
    return render(request, 'facturas/testing.html')
