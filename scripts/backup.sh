#!/usr/bin/env bash
# Бэкап базы и загруженных файлов: ./scripts/backup.sh -> backups/2026-11-08_102455/
set -euo pipefail
cd "$(dirname "$0")/.."

dir="backups/$(date +%Y-%m-%d_%H%M%S)"
mkdir -p "$dir"
# Если что-то пошло не так — удаляем недоделанный бэкап, чтобы не принять его за целый
trap 'echo "Бэкап НЕ сделан" >&2; rm -rf "$dir"' ERR

docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > "$dir/db.sql.gz"
docker compose exec -T web tar czf - -C /app media > "$dir/media.tar.gz"

echo "Готово: $dir"
ls -lh "$dir"
