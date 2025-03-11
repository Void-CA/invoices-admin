from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    ESTADOS_FACTURA = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    state = models.CharField(max_length=10, choices=ESTADOS_FACTURA, default='pendiente')

    def calcular_total(self):
        total = sum(item.subtotal() for item in self.detalles.all())
        self.total = total
        self.save()
    
    def __str__(self):
        return f"Factura {self.id} - {self.client.name}"

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="detalles", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en Factura {self.invoice.id}"
