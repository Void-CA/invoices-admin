from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vindell.settings')

app = Celery('vindell')

# Usa la configuración de Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carga las tareas de todos los módulos de aplicaciones registradas
app.autodiscover_tasks()
