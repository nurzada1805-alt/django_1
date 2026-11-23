
FROM python:3.13-slim

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Создание пользователя и папок
RUN groupadd --system app && useradd --system --gid app --no-create-home app \
    && mkdir -p /app/staticfiles /app/media \
    && chown app:app /app/staticfiles /app/media

# Копирование проекта
COPY --chown=app:app . .

USER app

EXPOSE 8000

# ENTRYPOINT ["/app/docker/entrypoint.sh"]
COPY docker/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# CMD ["gunicorn", "config.wsgi"]
