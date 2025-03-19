from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now

class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        validators=[RegexValidator(regex=r'^\d{7,15}$', message="Número inválido")]
    )
    ruc = models.CharField(max_length=13, default="None")

    def __str__(self):
        return self.name

class Service(models.Model):
    specification = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.specification

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
    emitted_date = models.DateField(default=now)
    expire_date = models.DateField(null=True, blank=True)
    service = models.ManyToManyField(Service, related_name="invoices")
    state = models.CharField(max_length=10, choices=ESTADOS_FACTURA, default='pagado')
    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES, default='Ingreso')
    print_number = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    @property
    def calc_total(self):
        return sum(service.price for service in self.service.all())

    def __str__(self):
        return f"Factura {self.id} - {self.client.name}"
