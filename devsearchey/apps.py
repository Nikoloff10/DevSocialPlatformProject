from django.apps import AppConfig


class DevsearcheyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devsearchey'

    def ready(self):
        import devsearchey.signals