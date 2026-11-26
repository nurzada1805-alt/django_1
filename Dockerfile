FROM python:3.13-slim

# Python не пишет .pyc и сразу выводит логи (без буфера)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Сначала только зависимости: этот слой пересобирается, лишь когда меняется requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Пользователь без прав root и папки, куда ему можно писать
RUN groupadd --system app && useradd --system --gid app --no-create-home app \
    && mkdir -p /app/staticfiles /app/media \
    && chown app:app /app/staticfiles /app/media

# Потом код: он меняется часто, но слой с зависимостями остаётся в кеше
COPY --chown=app:app . .

USER app
EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi"]
