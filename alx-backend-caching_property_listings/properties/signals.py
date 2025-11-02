from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

@receiver(post_save, sender=Property)
def clear_cache_on_save(sender, **kwargs):
    """Clear all_properties cache when a property is created or updated."""
    cache.delete('all_properties')
    print("Cache invalidated after property save/update.")

@receiver(post_delete, sender=Property)
def clear_cache_on_delete(sender, **kwargs):
    """Clear all_properties cache when a property is deleted."""
    cache.delete('all_properties')
    print("Cache invalidated after property delete.")
