from django.urls import path
from . import views

urlpatterns = [
    path('', views.seleccionar_impresora, name='settings'),
]
