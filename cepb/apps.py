from django.apps import AppConfig


class CepbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cepb'
    verbose_name = 'CEPB Application'

    def ready(self):
        # Importez vos templatetags ici
        from . import templatetags
