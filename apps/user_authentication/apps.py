from django.apps import AppConfig


class UserAuthenticationConfig(AppConfig):
    name = 'apps.user_authentication'
    verbose_name = "User Authentication"

    def ready(self):
        import apps.user_authentication.signals
