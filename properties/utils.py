from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

# Set up logger
logger = logging.getLogger(__name__)


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


def get_redis_cache_metrics():
    """
    Get Redis cache performance metrics.
    
    Connects to Redis via django_redis, retrieves keyspace_hits and keyspace_misses
    from INFO command, calculates hit ratio, and logs the metrics.
    
    Returns:
        dict: Dictionary containing cache metrics including:
            - keyspace_hits: Number of successful cache hits
            - keyspace_misses: Number of cache misses
            - hit_ratio: Calculated hit ratio (hits / (hits + misses))
            - total_requests: Total number of cache requests
            - error: Error message if connection fails (None if successful)
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO command output
        info = redis_conn.info()
        
        # Extract keyspace statistics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate total requests and hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = 0.0
        
        if total_requests > 0:
            hit_ratio = keyspace_hits / total_requests
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': round(hit_ratio, 4),  # Round to 4 decimal places
            'total_requests': total_requests,
            'error': None
        }
        
        # Log the metrics
        logger.info(
            f"Redis Cache Metrics - Hits: {keyspace_hits}, "
            f"Misses: {keyspace_misses}, Hit Ratio: {hit_ratio:.4f}, "
            f"Total Requests: {total_requests}"
        )
        
        return metrics
        
    except Exception as e:
        error_msg = f"Failed to get Redis cache metrics: {str(e)}"
        logger.error(error_msg)
        
        # Return error metrics
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'hit_ratio': 0.0,
            'total_requests': 0,
            'error': error_msg
        }
