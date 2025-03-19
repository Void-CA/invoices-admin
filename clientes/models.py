from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
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