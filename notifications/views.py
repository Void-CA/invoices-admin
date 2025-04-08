from django.shortcuts import render
from django.utils import timezone
from facturas.models import Invoice
from django.core.paginator import Paginator

def notifications(request):
    today = timezone.now().date()
    pending_invoices = Invoice.objects.filter(state='pendiente', expire_date__gte=today)
    overdue_invoices = Invoice.objects.filter(state='pendiente', expire_date__lt=today)

    paginator = Paginator(pending_invoices, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'pending_invoices.html', {
        'page_obj': page_obj,
        'pending_invoices': pending_invoices,
        'overdue_invoices': overdue_invoices,
    })
