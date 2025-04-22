from django.db import models

class ConfiguracionImpresion(models.Model):
    impresora_predeterminada = models.CharField(max_length=255)
