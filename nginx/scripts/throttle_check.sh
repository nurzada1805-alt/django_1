#!/usr/bin/env bash
# 30 неверных попыток входа: сколько пропущено (401) и сколько отбито (429)
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose exec -T redis redis-cli -n 1 flushdb > /dev/null
passed=0
blocked=0
for i in $(seq 1 30); do
    code=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost/api/auth/token/ \
        -H "Content-Type: application/json" -d '{"username":"masha","password":"18051997n"}')
    case "$code" in
        401) passed=$((passed + 1)) ;;
        429) blocked=$((blocked + 1)) ;;
    esac
done
echo "401: $passed, 429: $blocked"