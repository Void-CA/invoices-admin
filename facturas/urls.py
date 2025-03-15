from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('create/', views.create_invoice, name='create_invoice'),
    path('clients/', views.clients, name='clients'),
    path('clients/new/', views.client_form, name='client_create'),
    path('clients/edit/<int:client_id>/', views.client_form, name='client_edit'),
    path('edit/<int:invoice_id>/', views.edit_invoice, name='edit_invoice'),
    path('delete/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('test/', views.test, name='test'),
]
