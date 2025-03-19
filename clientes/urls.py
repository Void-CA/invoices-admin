from django.urls import path
from . import views  # Importa las vistas de clientes

urlpatterns = [
    path('', views.client_list, name='clients'),
    path('new/', views.client_form, name='client_create'),
    path('edit/<int:client_id>/', views.client_form, name='client_edit'),
]
