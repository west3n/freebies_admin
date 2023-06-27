from django.apps import AppConfig


class FreebiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'freebies'

    def ready(self):
        from freebies import signals
