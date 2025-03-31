from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# Define o nome do módulo de configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enterprise.settings")

# Cria a instância do Celery
app = Celery("enterprise")

# Usando o arquivo de configurações do Django, com prefixo CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Carrega tarefas automaticamente de todas as apps registradas no Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
