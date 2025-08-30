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

### 4. Run the Development Server
```bash
python manage.py runserver
```

### 5. Access the API
- **Property Listings**: http://localhost:8000/properties/
- **Admin Interface**: http://localhost:8000/admin/

## Caching

The property list endpoint uses Redis caching with a 15-minute duration. This means:
- First request: Data is fetched from the database
- Subsequent requests (within 15 minutes): Data is served from Redis cache
- After 15 minutes: Cache expires and fresh data is fetched

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

## Model Structure

The Property model includes:
- `title`: Property title (CharField, max 255 chars)
- `description`: Property description (TextField)
- `price`: Property price (DecimalField, 10 digits, 2 decimal places)
- `location`: Property location (CharField, max 255 chars)
- `created_at`: Creation timestamp (auto-generated)
- `updated_at`: Last update timestamp (auto-updated)
