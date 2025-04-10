from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST['usuario']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Cambia a donde quieras redirigir
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "login.html")

def logout_view(request):
    django_logout(request)
    return redirect('login')  # Cambia a la vista que corresponda para tu app
