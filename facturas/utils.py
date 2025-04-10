from datetime import datetime
from django.db.models import Q
from .models import Invoice 
from django.core.paginator import Paginator

def filter_invoices(query, fecha_inicio, fecha_fin, estado, tipo_factura, cliente, monto_min, monto_max):
    # Crear un filtro básico para la búsqueda por query
    filters = Q(client__name__icontains=query) | Q(print_number__icontains=query)

    # Filtrar por fecha de inicio
    if fecha_inicio:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            filters &= Q(emitted_date__gte=fecha_inicio)
        except ValueError:
            pass

    # Filtrar por fecha de fin
    if fecha_fin:
        try:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            filters &= Q(emitted_date__lte=fecha_fin)
        except ValueError:
            pass

    # Filtrar por estado
    if estado:
        filters &= Q(state=estado)

    # Filtrar por tipo de factura
    if tipo_factura:
        filters &= Q(invoice_type=tipo_factura)

    # Filtrar por cliente
    if cliente:
        filters &= Q(client__id=cliente)

    # Obtener las facturas que coinciden con los filtros
    invoices = Invoice.objects.filter(filters).distinct()

    # Filtrar por monto
    if monto_min:
        invoices = [invoice for invoice in invoices if invoice.calc_total >= float(monto_min)]

    if monto_max:
        invoices = [invoice for invoice in invoices if invoice.calc_total <= float(monto_max)]

    return invoices



def paginate_invoices(invoices, page, per_page):
    paginator = Paginator(invoices, per_page)
    page_obj = paginator.get_page(page)

    return page_obj, paginator