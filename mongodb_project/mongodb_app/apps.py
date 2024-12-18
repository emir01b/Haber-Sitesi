# mongodb_app/apps.py
from django.apps import AppConfig

class MongodbAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mongodb_app'
