from django.shortcuts import render
from facturas.models import Invoice
from datetime import date, timedelta

def home(request):
    # Obtener las últimas 5 facturas ordenadas por fecha de emisión
    ultimas_facturas = Invoice.objects.all().order_by('-emitted_date')[:5]

    # Obtener facturas cuyo vencimiento está dentro de los próximos 7 días
    facturas_proximas = Invoice.objects.filter(expire_date__lte=date.today() + timedelta(days=7), state='pendiente')

    context = {
        'ultimas_facturas': ultimas_facturas,
        'facturas_proximas': facturas_proximas,
    }

    return render(request, 'index.html', context)
