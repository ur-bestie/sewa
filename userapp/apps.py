from django.apps import AppConfig


class UserappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userapp'


    def ready(self):
            import userapp.signals  # Import the signals to connect them
            userapp.signals.start_stock_update_thread()