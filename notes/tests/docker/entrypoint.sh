#!/bin/sh
# Выполняется при каждом старте контейнера web, потом запускает CMD
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput --verbosity 0
exec "$@"