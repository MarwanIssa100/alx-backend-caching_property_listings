# ALX Backend Caching Property Listings

A Django application for property listings with PostgreSQL database and Redis caching.

## Features

- Django web application
- PostgreSQL database for data persistence
- Redis for caching and session storage
- Dockerized environment for easy deployment

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx_backend_caching_property_listings
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Run database migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create a superuser (optional)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**
   - Django Admin: http://localhost:8000/admin/
   - Main Application: http://localhost:8000/

## Services

- **Web (Django)**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Database Configuration

- **Database**: property_listings_db
- **Username**: property_user
- **Password**: property_password
- **Host**: postgres (from within containers) or localhost (from host)

## Redis Configuration

- **Host**: redis (from within containers) or localhost (from host)
- **Port**: 6379
- **Database**: 1 (for caching)

## Development

### Running commands in the container
```bash
# Run Django shell
docker-compose exec web python manage.py shell

# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic
```

### Viewing logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs postgres
docker-compose logs redis
```

## Stopping the services
```bash
docker-compose down
```

## Stopping and removing volumes (data will be lost)
```bash
docker-compose down -v
```

## Project Structure

```
alx_backend_caching_property_listings/
├── alx_backend_caching_property_listings/
│   ├── settings.py          # Django settings with PostgreSQL and Redis config
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── properties/
│   └── models.py            # Property model
├── docker-compose.yml       # Docker services configuration
├── Dockerfile               # Django app container configuration
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## Environment Variables

The following environment variables are configured in docker-compose.yml:

### PostgreSQL
- `POSTGRES_DB`: property_listings_db
- `POSTGRES_USER`: property_user
- `POSTGRES_PASSWORD`: property_password

### Django
- `DEBUG`: 1 (development mode)

## Caching

The application uses Redis for:
- Django cache backend
- Session storage
- Any custom caching needs

Cache configuration is in `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```
