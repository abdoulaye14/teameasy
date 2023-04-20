from django.apps import AppConfig


class GestionActivitesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_activites'

    def ready(self):
        import gestion_activites.signals
