from django.apps import AppConfig


class AbstractUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


    def ready(self):
        import users.signals

