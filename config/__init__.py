# myproject/__init__.py
from __future__ import absolute_import, unicode_literals

# Esto asegura que el app de Celery se cargue cuando se ejecute `django.setup()`
from .celery import app as celery_app

__all__ = ('celery_app',)
