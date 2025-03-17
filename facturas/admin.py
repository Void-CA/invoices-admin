from django.contrib import admin
from .models import Client, Service, Invoice

admin.site.register(Client)
admin.site.register(Service)
admin.site.register(Invoice)
