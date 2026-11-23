"""Настройки Gunicorn. Файл с таким именем Gunicorn находит сам."""
import os

bind = '0.0.0.0:8000'
workers = int(os.environ.get('GUNICORN_WORKERS', 3))
timeout = 30
accesslog = '-' # журнал запросов — в stdout, его увидит docker logs
errorlog = '-'

# Сокет управления (gunicornc, с версии 25.1) нам не нужен: у пользователя app нет домашней папки
control_socket_disable = True