from django.apps import AppConfig


class ChallengeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'challenge'

    def ready(self):
        from challenge.signals import handle_cache_update, post_save, Event

        post_save.connect(handle_cache_update, sender=Event)
