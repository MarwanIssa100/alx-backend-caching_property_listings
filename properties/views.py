from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

# Create your views here.

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to return all properties with Redis caching.
    Cache duration: 15 minutes (60 * 15 seconds)
    """
    properties = Property.objects.all()
    
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
