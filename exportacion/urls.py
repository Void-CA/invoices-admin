from django.urls import path
from . import views

urlpatterns = [
    path('exportar/', views.export_invoices, name='export_invoices'),
    path('', views.export_page, name='export_page'),    
]
