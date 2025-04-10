from django.urls import path
from . import views  # Importa las vistas de clientes

urlpatterns = [
    path('', views.client_list, name='clients'),
    path('new/', views.client_form, name='client_create'),
    path('<int:client_id>/', views.client_detail, name='client_detail'),
    path('edit/<int:client_id>/', views.client_form, name='client_edit'),
    path('delete/<int:client_id>/', views.delete_client, name='client_delete'),
    path('buscar/', views.buscar_clientes, name='buscar_clientes'),
    path('get_clients/', views.get_clients, name='get_clients'),
]
