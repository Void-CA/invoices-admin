from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now
from clientes.models import Client
from django.db.models import Max

class Invoice(models.Model):
    ESTADOS_FACTURA = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]

    INVOICE_TYPES = [
        ('Ingreso', 'Ingreso'),
        ('Egreso', 'Egreso'),
        ('Caja', 'Caja'),
    ]

    client = models.ForeignKey(Client, related_name="invoices", on_delete=models.CASCADE)
    provider = models.CharField(max_length=100, blank=True, null=True)
    emitted_date = models.DateField(default=now)
    expire_date = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=10, choices=ESTADOS_FACTURA, default='pagado')
    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES, default='Ingreso')
    print_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    @property
    def calc_total(self):
        return sum(service.price for service in self.services.all())  # Usando related_name="services"

    def __str__(self):
        return f"Factura {self.id} - {self.client.name}"


class Service(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    invoice = models.ForeignKey(Invoice, related_name="services", on_delete=models.CASCADE)
    specification = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.specification
