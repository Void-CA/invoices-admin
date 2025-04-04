# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.stats_page, name='stats_page'),  # Ruta para la página de inicio
]
