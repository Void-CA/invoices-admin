import csv
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

headers = ['Número de Factura', 'Cliente', 'Tipo', 'Estado', 'Fecha de emisión', 'Fecha de expiración', 'Número de impresión', 'Descripción']
def export_to_csv(queryset):
    # Crea una respuesta HTTP para descargar el archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="facturas.csv"'
    
    writer = csv.writer(response)
    # Escribir el encabezado del archivo CSV
    writer.writerow(headers)  
    
    # Escribir las filas de datos
    for factura in queryset:
        writer.writerow([factura.id, factura.client.name, factura.invoice_type, factura.state, factura.emitted_date, factura.expire_date, factura.print_number, factura.description])
    
    return response

def export_to_excel(queryset):
    # Crea una respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="facturas.xlsx"'
    
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    
    for factura in queryset:
        ws.append([factura.id, factura.client.name, factura.invoice_type, factura.state, factura.emitted_date, factura.expire_date, factura.print_number, factura.description])
    
    wb.save(response)
    return response

def export_to_pdf(queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="facturas.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Factura Reporte")
    
    y_position = 730
    for factura in queryset:
        p.drawString(100, y_position, f"Factura #: {factura.print_number} - Cliente: {factura.client.name}")
        y_position -= 20
    
    p.showPage()
    p.save()
    
    return response