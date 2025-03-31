from __future__ import absolute_import, unicode_literals

# Certifique-se de que o Celery é carregado quando o Django for iniciado
from .celery import app as celery_app

__all__ = ('celery_app',)