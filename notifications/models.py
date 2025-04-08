from django.db import models

class Notification(models.Model):
    # Mensaje de la notificación
    message = models.TextField()

    # Tipo de notificación (por ejemplo, "factura", "promoción", "advertencia")
    notification_type = models.CharField(max_length=50, choices=(
        ('invoice_due', 'Factura vencida'),
        ('invoice_pending', 'Factura pendiente'),
        ('general', 'Mensaje general'),
    ), default='general')

    # Timestamp de la notificación
    timestamp = models.DateTimeField(auto_now_add=True)

    # Indicador de si la notificación ha sido leída o no
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']
