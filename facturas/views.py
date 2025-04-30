from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.contrib import messages
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Invoice, Service
from clientes.models import Client
from .forms import InvoiceForm, ServiceForm
from datetime import datetime
from .utils import *
import requests

def invoice_list(request, invoice_list = Invoice.objects.all()):
    paginator = Paginator(invoice_list, 10)  # 10 facturas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'facturas/invoices_list.html', {'page_obj': page_obj})

def search_invoices(request):
    query = request.GET.get('q', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    estado = request.GET.get('estado', '')
    tipo_factura = request.GET.get('tipo_factura', '')
    cliente = request.GET.get('cliente', '')
    monto_min = request.GET.get('monto_min', '')
    monto_max = request.GET.get('monto_max', '')
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)

    # Filtrar las facturas
    invoices = filter_invoices(query, fecha_inicio, fecha_fin, estado, tipo_factura, cliente, monto_min, monto_max)

    # Paginación de las facturas
    page_obj, paginator = paginate_invoices(invoices, page, per_page)

    # Convertir los datos en JSON
    data = [
        {
            "id": invoice.id,
            "print_number": invoice.print_number,
            "client": invoice.client.name,
            "calc_total": invoice.calc_total,
            "emitted_date": invoice.emitted_date,
            "expire_date": invoice.expire_date
        }
        for invoice in page_obj
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
            form_i.fields['specification'].widget.attrs.update({'class': 'bg-gray-100 border border-gray-300 rounded-md py-2 px-3 w-full', 'rows': 3,'placeholder': 'Nombre del servicio'})
            form_i.fields['price'].widget.attrs.update({'class': 'bg-gray-100 border border-gray-300 rounded-md py-2 px-3 w-full', 'start': 0, 'step': 0.01, 'placeholder': 'C$'})

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

@csrf_exempt
def print_invoice(request, invoice_id):
    print("Método recibido:", request.method)
    try:
        if request.method == 'POST':
            print("Obteniendo factura...")
            invoice = get_object_or_404(Invoice, id=invoice_id)

            print("Construyendo contexto...")
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

            filename = f'invoice_{invoice.id}.pdf'
            print(f"Generando PDF: {filename}")
            pdf_path = create_pdf(context, filename)
            print(f"PDF generado en: {pdf_path}")

            print("Abriendo archivo PDF...")
            with open(pdf_path, 'rb') as pdf_file:
                print("Preparando archivo para enviar...")
                files = {'file': (filename, pdf_file, 'application/pdf')}
                data = {'printer_name': "EPSON3E2859 (L3250 Series)"}

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
