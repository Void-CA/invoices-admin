from django.shortcuts import render
from facturas.models import Invoice
from .models import Client
from .forms import ClientForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

def client_list(request):
    clients = Client.objects.all()
    return render(request, "clients.html", {"clients": clients})

def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    invoices = Invoice.objects.filter(client=client).order_by('-emitted_date')

    paginator = Paginator(invoices, 5)  # 5 facturas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'client_detail.html', {
        'client': client,
        'page_obj': page_obj,
    })

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return redirect('clients')

def client_form(request, client_id=None):
    if client_id: 
        client = get_object_or_404(Client, id=client_id)
    else:  
        client = None
    
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients') 
    else:
        form = ClientForm(instance=client)

    return render(request, 'client_form.html', {'form': form})

def buscar_clientes(request):
    query = request.GET.get("q", "").strip()
    if not query:
        clientes = Client.objects.all()
    else:
        clientes = Client.objects.filter(
            Q(name__icontains=query) |
            Q(ruc__icontains=query) |
            Q(phone__icontains=query)
        )

    data = [{"id": c.id ,"name": c.name, "ruc": c.ruc, "phone": c.phone, "address": c.address} for c in clientes]
    return JsonResponse({"resultados": data})