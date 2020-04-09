from django.apps import AppConfig


class UserAuthenticationConfig(AppConfig):
    name = 'apps.user_authentication'

    def ready(self):
        import apps.user_authentication.signals
