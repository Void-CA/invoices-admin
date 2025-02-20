from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_facturas, name='lista_facturas'),
    path('nueva/', views.crear_factura, name='crear_factura'),
    path('<int:id>/', views.detalle_factura, name='detalle_factura'),
    path('<int:id>/editar/', views.editar_factura, name='editar_factura'),
    path('<int:id>/eliminar/', views.eliminar_factura, name='eliminar_factura'),
]
