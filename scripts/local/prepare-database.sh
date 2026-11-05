#!/usr/bin/env bash
set -euo pipefail
container=pos-frida-e1-postgres
if ! docker info >/dev/null 2>&1; then
  echo 'Docker no está disponible. Abre Docker o inicia su servicio y vuelve a abrir POS FBM.' >&2
  exit 1
fi
docker start "$container" >/dev/null
for attempt in {1..60}; do
  if docker exec "$container" pg_isready -U pos_e1_app >/dev/null 2>&1; then exit 0; fi
  sleep 1
done
echo 'La base de datos no terminó de iniciar. Revisa Docker antes de volver a intentar.' >&2
exit 1
