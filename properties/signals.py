from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property


@receiver(post_save, sender=Property)
def clear_property_cache_on_save(sender, instance, created, **kwargs):
    """
    Clear the 'all_properties' cache when a Property is created or updated.
    
    Args:
        sender: The Property model class
        instance: The Property instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    cache.delete('all_properties')
    print(f"Cache cleared: Property '{instance.title}' was {'created' if created else 'updated'}")


@receiver(post_delete, sender=Property)
def clear_property_cache_on_delete(sender, instance, **kwargs):
    """
    Clear the 'all_properties' cache when a Property is deleted.
    
    Args:
        sender: The Property model class
        instance: The Property instance that was deleted
        **kwargs: Additional keyword arguments
    """
    cache.delete('all_properties')
    print(f"Cache cleared: Property '{instance.title}' was deleted")
