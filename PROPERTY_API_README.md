# Property Listings API

This Django application provides a RESTful API for property listings with Redis caching.

## Features

- **Property Listings**: Get all properties with detailed information
- **Redis Caching**: 15-minute cache duration for improved performance
- **JSON Response**: Clean, structured JSON responses
- **Admin Interface**: Manage properties through Django admin

## API Endpoints

### GET /properties/

Returns all properties in the database.

**Response Format:**
```json
{
    "properties": [
        {
            "id": 1,
            "title": "Modern Downtown Apartment",
            "description": "Beautiful 2-bedroom apartment in the heart of downtown with city views.",
            "price": "250000.00",
            "location": "Downtown",
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        }
    ],
    "count": 1
}
```

**Cache Duration:** 15 minutes (900 seconds)

## Setup and Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Sample Data (Optional)
```bash
python manage.py populate_properties
```

### 4. Cache Management (Optional)
```bash
# Clear property cache only
python manage.py clear_property_cache

# Clear all cache
python manage.py clear_property_cache --all
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

### 6. Access the API
- **Property Listings**: http://localhost:8000/properties/
- **Admin Interface**: http://localhost:8000/admin/

## Caching

The property list endpoint uses a two-layer caching strategy:

### 1. View-Level Caching (`@cache_page`)
- **Duration**: 15 minutes (900 seconds)
- **Scope**: Entire HTTP response
- **Key**: Based on URL and request parameters

### 2. Data-Level Caching (`get_all_properties()`)
- **Duration**: 1 hour (3600 seconds)
- **Scope**: Database queryset
- **Key**: `'all_properties'`
- **Strategy**: 
  - Check Redis for `'all_properties'` key
  - If not found, fetch `Property.objects.all()`
  - Store in Redis for 1 hour
  - Return the queryset

### Cache Behavior:
- **First request**: Data fetched from database, cached at both levels
- **Subsequent requests (within 15 min)**: Served from view cache
- **After 15 min, within 1 hour**: Data fetched from data cache, view response cached
- **After 1 hour**: Fresh data fetched from database

### Automatic Cache Invalidation:
The cache is automatically cleared when properties are modified:
- **Property Created**: Cache cleared via `post_save` signal
- **Property Updated**: Cache cleared via `post_save` signal  
- **Property Deleted**: Cache cleared via `post_delete` signal

## Testing

Run the test suite:
```bash
python manage.py test properties
```

## Docker Setup

If using Docker Compose:
```bash
docker-compose up -d
```

This will start:
- Django application
- PostgreSQL database
- Redis cache server

## Admin Interface

Access the Django admin at `/admin/` to:
- Add new properties
- Edit existing properties
- Delete properties
- View all properties in a table format

## Signals and Cache Management

### Automatic Cache Invalidation

The application uses Django signals to automatically clear the property cache when data changes:

- **`post_save` signal**: Clears cache when properties are created or updated
- **`post_delete` signal**: Clears cache when properties are deleted
- **Location**: `properties/signals.py`

This ensures that the cache always contains fresh data after any property modifications.

### App Configuration

The signals are automatically loaded when the app starts:

- **`properties/apps.py`**: Overrides `ready()` method to import signals
- **`properties/__init__.py`**: Sets default app configuration
- **Automatic Loading**: Signals are registered when Django starts

## Utility Functions

### `get_all_properties()`

Located in `properties/utils.py`, this function provides intelligent caching for property data:

```python
from properties.utils import get_all_properties

# Get all properties (cached for 1 hour)
properties = get_all_properties()
```

**Features:**
- Checks Redis cache first using key `'all_properties'`
- Falls back to database query if cache miss
- Automatically caches results for 1 hour (3600 seconds)
- Returns Django QuerySet for further filtering/operations

## Model Structure

The Property model includes:
- `title`: Property title (CharField, max 255 chars)
- `description`: Property description (TextField)
- `price`: Property price (DecimalField, 10 digits, 2 decimal places)
- `location`: Property location (CharField, max 255 chars)
- `created_at`: Creation timestamp (auto-generated)
- `updated_at`: Last update timestamp (auto-updated)
