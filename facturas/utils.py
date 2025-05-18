from datetime import datetime
from django.db.models import Q
from .models import Invoice 
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from weasyprint import HTML
import tempfile
import os


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

import os
from django.conf import settings
from django.template.loader import get_template
from weasyprint import HTML

def create_pdf(context, filename='factura_generada.pdf'):
    """
    Genera un PDF a partir de un contexto y lo guarda en una ruta específica.
    Utiliza WeasyPrint para la generación del PDF y Django para el renderizado de la plantilla HTML.

    Args:
        context (dict): Diccionario que contiene el contexto para renderizar la plantilla.
        filename (str, optional): Nombre del archivo en que se guardara el pdf. Defaults to 'factura_generada.pdf'.

    Returns:
        _type_: _description_
    """
    # Usar el sistema de plantillas de Django para renderizar
    template = get_template('facturas/print_template.html')

    # Definir ruta absoluta dentro del proyecto
    output_dir = os.path.join(settings.BASE_DIR, 'pdf_output')
    os.makedirs(output_dir, exist_ok=True)  # crea la carpeta si no existe
    output_path = os.path.join(output_dir, filename)

    # Renderiza el HTML con el contexto
    html_rendered = template.render(context)

    # Generar el PDF con WeasyPrint
    HTML(string=html_rendered).write_pdf(output_path)

    print(f"PDF generado correctamente en: {output_path}")
    return output_path

    