# Project/celery.py

import os
from celery import Celery

# Définir les paramètres de configuration pour Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Créer une instance Celery
app = Celery('project')

# Charger la configuration depuis Django settings, en utilisant le namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger automatiquement les tâches des applications Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')
