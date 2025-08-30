from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from .models import Property
from .utils import get_all_properties
from decimal import Decimal
import json
from unittest.mock import patch

# Create your tests here.

class PropertyListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test property
        self.property = Property.objects.create(
            title='Test Property',
            description='Test Description',
            price=Decimal('300000.00'),
            location='Test Location'
        )

    def test_property_list_view(self):
        """Test that the property_list view returns correct JSON response"""
        response = self.client.get(reverse('properties:property_list'))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check content type
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Parse JSON response
        data = json.loads(response.content)
        
        # Check response structure
        self.assertIn('properties', data)
        self.assertIn('count', data)
        self.assertEqual(data['count'], 1)
        
        # Check property data
        property_data = data['properties'][0]
        self.assertEqual(property_data['title'], 'Test Property')
        self.assertEqual(property_data['description'], 'Test Description')
        self.assertEqual(property_data['price'], '300000.00')
        self.assertEqual(property_data['location'], 'Test Location')
        self.assertIn('id', property_data)
        self.assertIn('created_at', property_data)
        self.assertIn('updated_at', property_data)

    def test_property_list_view_empty(self):
        """Test that the view handles empty property list correctly"""
        # Delete all properties
        Property.objects.all().delete()
        
        response = self.client.get(reverse('properties:property_list'))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['properties']), 0)


class GetAllPropertiesTest(TestCase):
    def setUp(self):
        # Clear cache before each test
        cache.clear()
        # Create test properties
        self.property1 = Property.objects.create(
            title='Test Property 1',
            description='Test Description 1',
            price=Decimal('300000.00'),
            location='Test Location 1'
        )
        self.property2 = Property.objects.create(
            title='Test Property 2',
            description='Test Description 2',
            price=Decimal('400000.00'),
            location='Test Location 2'
        )

    def test_get_all_properties_from_database(self):
        """Test that get_all_properties fetches from database when cache is empty"""
        # Clear cache to ensure we fetch from database
        cache.clear()
        
        properties = get_all_properties()
        
        # Should return all properties
        self.assertEqual(properties.count(), 2)
        self.assertIn(self.property1, properties)
        self.assertIn(self.property2, properties)
        
        # Should now be cached
        cached_properties = cache.get('all_properties')
        self.assertIsNotNone(cached_properties)
        self.assertEqual(cached_properties.count(), 2)

    def test_get_all_properties_from_cache(self):
        """Test that get_all_properties returns cached data when available"""
        # First call should cache the data
        properties1 = get_all_properties()
        self.assertEqual(properties1.count(), 2)
        
        # Delete from database to simulate cache-only scenario
        Property.objects.all().delete()
        
        # Second call should return cached data
        properties2 = get_all_properties()
        self.assertEqual(properties2.count(), 2)
        self.assertIn(self.property1, properties2)
        self.assertIn(self.property2, properties2)

    def test_get_all_properties_empty_database(self):
        """Test that get_all_properties handles empty database correctly"""
        # Clear cache and delete all properties
        cache.clear()
        Property.objects.all().delete()
        
        properties = get_all_properties()
        
        # Should return empty queryset
        self.assertEqual(properties.count(), 0)
        
        # Should be cached
        cached_properties = cache.get('all_properties')
        self.assertIsNotNone(cached_properties)
        self.assertEqual(cached_properties.count(), 0)


class PropertySignalsTest(TestCase):
    def setUp(self):
        # Clear cache before each test
        cache.clear()

    def test_post_save_signal_clears_cache_on_create(self):
        """Test that post_save signal clears cache when property is created"""
        # Populate cache first
        properties = get_all_properties()
        self.assertIsNotNone(cache.get('all_properties'))
        
        # Create a new property (this should trigger the signal)
        with patch('builtins.print') as mock_print:
            property = Property.objects.create(
                title='New Property',
                description='New Description',
                price=Decimal('500000.00'),
                location='New Location'
            )
        
        # Cache should be cleared
        self.assertIsNone(cache.get('all_properties'))
        
        # Check that print statement was called
        mock_print.assert_called_with("Cache cleared: Property 'New Property' was created")

    def test_post_save_signal_clears_cache_on_update(self):
        """Test that post_save signal clears cache when property is updated"""
        # Create a property first
        property = Property.objects.create(
            title='Test Property',
            description='Test Description',
            price=Decimal('300000.00'),
            location='Test Location'
        )
        
        # Populate cache
        properties = get_all_properties()
        self.assertIsNotNone(cache.get('all_properties'))
        
        # Update the property (this should trigger the signal)
        with patch('builtins.print') as mock_print:
            property.title = 'Updated Property'
            property.save()
        
        # Cache should be cleared
        self.assertIsNone(cache.get('all_properties'))
        
        # Check that print statement was called
        mock_print.assert_called_with("Cache cleared: Property 'Updated Property' was updated")

    def test_post_delete_signal_clears_cache(self):
        """Test that post_delete signal clears cache when property is deleted"""
        # Create a property first
        property = Property.objects.create(
            title='Test Property',
            description='Test Description',
            price=Decimal('300000.00'),
            location='Test Location'
        )
        
        # Populate cache
        properties = get_all_properties()
        self.assertIsNotNone(cache.get('all_properties'))
        
        # Delete the property (this should trigger the signal)
        with patch('builtins.print') as mock_print:
            property.delete()
        
        # Cache should be cleared
        self.assertIsNone(cache.get('all_properties'))
        
        # Check that print statement was called
        mock_print.assert_called_with("Cache cleared: Property 'Test Property' was deleted")
