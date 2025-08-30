from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics

# Create your views here.

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to return all properties with Redis caching.
    Cache duration: 15 minutes (60 * 15 seconds)
    Uses get_all_properties() utility function for additional Redis caching
    """
    properties = get_all_properties()
    
    # Convert to JSON-serializable format
    property_data = []
    for property in properties:
        property_data.append({
            'id': property.id,
            'title': property.title,
            'description': property.description,
            'price': str(property.price),  # Convert Decimal to string for JSON
            'location': property.location,
            'created_at': property.created_at.isoformat(),
            'updated_at': property.updated_at.isoformat(),
        })
    
    return JsonResponse({
        'properties': property_data,
        'count': len(property_data)
    })


def cache_metrics(request):
    """
    View to return Redis cache performance metrics.
    Returns cache hit/miss statistics and hit ratio.
    """
    metrics = get_redis_cache_metrics()
    
    return JsonResponse({
        'cache_metrics': metrics,
        'timestamp': '2024-01-01T12:00:00Z'  # You could use timezone.now().isoformat()
    })
