from django.http import HttpResponse

def lista_facturas(request):
    return HttpResponse("Lista de facturas")

def crear_factura(request):
    return HttpResponse("Crear una factura")

def detalle_factura(request, id):
    return HttpResponse(f"Detalles de la factura {id}")

def editar_factura(request, id):
    return HttpResponse(f"Editar factura {id}")

def eliminar_factura(request, id):
    return HttpResponse(f"Eliminar factura {id}")
