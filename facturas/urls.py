from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_facturas, name='lista_facturas'),
    path('crear/', views.crear_factura, name='crear_factura'),
    path('editar/<int:factura_id>/', views.editar_factura, name='editar_factura'),
    path('eliminar/<int:factura_id>/', views.eliminar_factura, name='eliminar_factura'),
    path('<int:factura_id>/', views.detalle_factura, name='detalle_factura'),
]