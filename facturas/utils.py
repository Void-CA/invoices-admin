# facturas/utils.py

from facturas.models import Invoice
from django.utils.dateparse import parse_date

def filter_invoices(request):
    """Filtrar facturas según los parámetros recibidos y devolver el queryset filtrado en formato JSON."""
    
    # Comenzamos con todas las facturas
    invoices = Invoice.objects.all()

    # Filtrar por fecha (rango)
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        if fecha_inicio and fecha_fin:
            invoices = invoices.filter(emitted_date__gte=fecha_inicio, emitted_date__lte=fecha_fin)

    # Filtrar por estado
    estado = request.GET.get('estado', '')
    if estado:
        invoices = invoices.filter(state=estado)

    # Filtrar por cliente
    cliente = request.GET.get('cliente', '')
    if cliente:
        invoices = invoices.filter(client__name__icontains=cliente)

    # Filtros adicionales si se necesitan, como rango de total
    total_min = request.GET.get('total_min', None)
    if total_min:
        invoices = invoices.filter(total__gte=total_min)

    return invoices
