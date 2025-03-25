from django.shortcuts import render
from .models import Client
from .forms import ClientForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q

def client_list(request):
    clients = Client.objects.all()
    return render(request, "clientes/clients.html", {"clients": clients})

def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, "clientes/client_detail.html", {"client": client})

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

    return render(request, 'clientes/client_form.html', {'form': form})

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