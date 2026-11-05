#!/usr/bin/env bash
set -euo pipefail
on_error() {
  echo
  echo 'No se pudo abrir POS FBM. Puedes revisar el servicio con:'
  echo 'journalctl --user -u frida-pos-e1 -n 30 --no-pager'
  if [[ -t 0 ]]; then read -r -p 'Presiona Enter para cerrar…' || true; fi
}
trap on_error ERR
url=http://127.0.0.1:8870/dashboard.html
echo 'Iniciando POS FBM…'
systemctl --user start frida-pos-e1.service
for attempt in {1..30}; do
  if curl --connect-timeout 1 --max-time 2 --fail --silent --output /dev/null "$url"; then
    echo "Sistema listo: $url"
    if [[ "${1:-}" != '--no-browser' ]]; then xdg-open "$url"; fi
    exit 0
  fi
  sleep 1
done
echo 'El servidor no respondió. Revisa el servicio antes de volver a intentar.' >&2
exit 1
