from django.db import models
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@receiver([post_save, post_delete], sender=Property)
def clear_property_cache(sender, **kwargs):
    cache.delete('all_properties')
