from django.shortcuts import render
from .models import Client
from .forms import ClientForm
from django.shortcuts import render, redirect, get_object_or_404

def client_list(request):
    clients = Client.objects.all()
    return render(request, "clientes/clients.html", {"clients": clients})

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