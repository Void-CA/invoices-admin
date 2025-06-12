# exportacion/views.py
from django.shortcuts import render
from django.http import JsonResponse
from facturas.utils import filter_invoices
from facturas.models import Invoice
from .export_helpers import export_to_csv, export_to_excel, export_to_pdf

def export_invoices(request):
    query = request.GET.get('q', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    estado = request.GET.get('estado', '')
    tipo_factura = request.GET.get('tipo_factura', '')
    cliente = request.GET.get('cliente', '')
    monto_min = request.GET.get('monto_min', '')
    monto_max = request.GET.get('monto_max', '')

    invoices = filter_invoices(query, fecha_inicio, fecha_fin, estado, tipo_factura, cliente, monto_min, monto_max)

    formato = request.GET.get('formato', 'csv')

    if formato == 'csv':
        return export_to_csv(invoices)
    elif formato == 'excel':
        return export_to_excel(invoices)
    elif formato == 'pdf':
        return export_to_pdf(invoices)
    else:
        return JsonResponse({'message': 'Formato no soportado'}, status=400)


def export_page(request):
    invoices = Invoice.objects.all()
    return render(request, 'export_page.html', {'invoices': invoices})
