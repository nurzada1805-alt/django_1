from .settings import *  # noqa: F401,F403

# Быстрый хешер паролей: в тестах безопасность хеша не нужна, а скорость — да
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# Тесты не трогают настоящий Redis: cache.clear() в setUp() очистил бы его
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

# 401 и 404 в тестах — норма; предупреждения о них только засоряют вывод
LOGGING['root']['level'] = 'ERROR'  # noqa: F405
