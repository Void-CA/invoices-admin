# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notifications, name='notification_list'),
]
