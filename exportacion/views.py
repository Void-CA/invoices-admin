# exportacion/views.py
from django.shortcuts import render
from django.http import JsonResponse
from facturas.utils import filter_invoices
from facturas.models import Invoice
from .export_helpers import export_to_csv, export_to_excel, export_to_pdf

def export_invoices(request):
    # Usamos la función filter_invoices para obtener el queryset filtrado
    invoices = filter_invoices(request)

    # Obtener el formato elegido (por defecto CSV)
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
