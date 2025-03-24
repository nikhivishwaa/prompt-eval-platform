from temp.cache import update_challenge, remove_challenge, Event
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Event)
def handle_cache_update(sender, instance=None, **kwargs):
    update_challenge(instance)

