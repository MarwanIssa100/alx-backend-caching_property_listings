from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Get all properties with Redis caching.
    
    Returns:
        QuerySet: All Property objects
        
    Cache Strategy:
        - Check Redis for 'all_properties' key
        - If not found, fetch from database
        - Store in Redis for 1 hour (3600 seconds)
        - Return the queryset
    """
    # Try to get from cache first
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        # Return cached queryset
        return cached_properties
    
    # If not in cache, fetch from database
    properties = Property.objects.all()
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set('all_properties', properties, 3600)
    
    return properties
