#!/usr/bin/env bash
# Vorschau der Lese-App am PC: http://localhost:8790/
# Die App selbst braucht keinen Server – sie läuft auf dem Tablet offline (siehe README.md).
cd "$(dirname "$0")/public" || exit 1
PORT="${LESEN_PORT:-8790}"
echo "Lese-App: http://localhost:$PORT/   (Strg+C zum Beenden)"
( sleep 1; brave-browser --app="http://localhost:$PORT/" >/dev/null 2>&1 || xdg-open "http://localhost:$PORT/" >/dev/null 2>&1 ) &
exec python3 -m http.server "$PORT" --bind 127.0.0.1
