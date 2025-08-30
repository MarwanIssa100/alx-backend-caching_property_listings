from django.test import TestCase, Client
from django.urls import reverse
from .models import Property
from decimal import Decimal
import json

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
