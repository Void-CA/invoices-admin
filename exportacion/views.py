from django.shortcuts import render
from facturas.models import Invoice
from .export_helpers import export_to_csv, export_to_excel, export_to_pdf

def export_invoices(request):
    # Filtrar las invoices según los parámetros (puedes obtenerlos de `request.GET`)
    invoices = Invoice.objects.all()

    # Filtrar por fecha si el parámetro "fecha" está presente en la solicitud
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    if fecha_inicio and fecha_fin:
        invoices = invoices.filter(fecha__range=[fecha_inicio, fecha_fin])

    # Filtrar por estado si el parámetro "estado" está presente en la solicitud
    estado = request.GET.get('estado')
    if estado:
        invoices = invoices.filter(estado=estado)

    # Filtrar por cliente si el parámetro "cliente" está presente en la solicitud
    cliente = request.GET.get('cliente')
    if cliente:
        invoices = invoices.filter(cliente__nombre__icontains=cliente)

    # Obtener el formato elegido (por defecto CSV)
    formato = request.GET.get('formato', 'csv')

    if formato == 'csv':
        return export_to_csv(invoices)
    elif formato == 'excel':
        return export_to_excel(invoices)
    elif formato == 'pdf':
        return export_to_pdf(invoices)
    else:
        return render(request, 'error.html', {'message': 'Formato no soportado'})

def export_page(request):
    # Aquí puedes pasar los datos que quieras mostrar en la página (por ejemplo, facturas filtradas)
    # Para este caso, solo pasaremos todas las facturas como ejemplo
    invoices = Invoice.objects.all()

    # Renderizamos la página export_page.html
    return render(request, 'export_page.html', {'invoices': invoices})
