from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse


def home(request):
    return JsonResponse({
        "project": "DRF Notes API",
        "version": "1.0.0",
        "status": "running",
        "documentation": {
            "swagger": "/api/docs/",
            "redoc": "/api/redoc/",
            "schema": "/api/schema/",
        },
        "endpoints": {
            "health": "/api/health/",
            "auth": "/api/auth/",
            "admin": "/admin/",
        }
    })


def health(request):
    """Жив ли сервис: отвечает ли база и кеш. Для Docker, nginx и мониторинга."""
    status = {'database': 'ok', 'cache': 'ok'}
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception:
        status['database'] = 'error'
    try:
        cache.set('health_check', 'ok', timeout=5)
        if cache.get('health_check') != 'ok':
            raise RuntimeError
    except Exception:
        status['cache'] = 'error'
    healthy = all(value == 'ok' for value in status.values())
    return JsonResponse(status, status=200 if healthy else 503)
