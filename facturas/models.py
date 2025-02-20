from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    ESTADOS_FACTURA = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=10, choices=ESTADOS_FACTURA, default='pendiente')

    def calcular_total(self):
        total = sum(item.subtotal() for item in self.detalles.all())
        self.total = total
        self.save()
    
    def __str__(self):
        return f"Factura {self.id} - {self.cliente.nombre}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name="detalles", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    def subtotal(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Factura {self.factura.id}"
