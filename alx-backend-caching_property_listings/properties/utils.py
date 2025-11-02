from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

def get_all_properties():
    """
    Retrieve all Property objects, using Redis cache for 1 hour (3600 seconds).
    """
    properties = cache.get('all_properties')

    if properties is None:
        print("Cache miss: Fetching from database...")
        properties = list(Property.objects.all())  # Convert queryset to list for caching
        cache.set('all_properties', properties, 3600)
    else:
        print("Cache hit: Using cached data.")

    return properties

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.

    Returns:
        dict: {
            'keyspace_hits': int,
            'keyspace_misses': int,
            'hit_ratio': float
        }
    """
    # Connect to Redis using django-redis
    redis_conn = get_redis_connection("default")

    # Fetch Redis server info
    info = redis_conn.info()

    # Extract relevant metrics
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    # Compute hit ratio safely (avoid division by zero)
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": round(hit_ratio, 4),
    }

    # Log metrics for monitoring
    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics
