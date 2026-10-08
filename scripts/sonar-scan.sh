#!/usr/bin/env bash
# Genera coverage de backend y frontend, y corre sonar-scanner contra la
# instancia local de SonarQube (docker-compose.sonar.yml).
#
# Uso:
#   docker compose -f docker-compose.sonar.yml up -d sonarqube   # una vez
#   # crear proyecto "poc-agente-estimacion-epicas" y generar un token en
#   # http://localhost:9000 (My Account > Security)
#   SONAR_TOKEN=squ_xxxxx ./scripts/sonar-scan.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -z "${SONAR_TOKEN:-}" ]; then
  echo "Error: falta SONAR_TOKEN."
  echo "Generalo en http://localhost:9000 -> My Account -> Security -> Generate Token"
  echo "Uso: SONAR_TOKEN=squ_xxxxx ./scripts/sonar-scan.sh"
  exit 1
fi

if ! curl -sf http://localhost:9000/api/system/status 2>/dev/null | grep -q '"status":"UP"'; then
  echo "Error: SonarQube no responde en http://localhost:9000"
  echo "Levantalo con: docker compose -f docker-compose.sonar.yml up -d sonarqube"
  exit 1
fi

echo "=== [1/3] Coverage backend (pytest) ==="
cd "$ROOT_DIR/backend"
if [ ! -d venv ]; then
  python3 -m venv venv
fi
./venv/bin/pip install -q -r requirements-dev.txt
./venv/bin/python -m pytest --cov=app --cov=models --cov=utils --cov-report=xml

echo "=== [2/3] Coverage frontend (jest) ==="
cd "$ROOT_DIR/frontend"
if [ ! -d node_modules ]; then
  npm install
fi
npm run test:coverage

echo "=== [3/3] sonar-scanner ==="
cd "$ROOT_DIR"
docker compose -f docker-compose.sonar.yml run --rm \
  -e SONAR_HOST_URL=http://sonarqube:9000 \
  -e SONAR_TOKEN="$SONAR_TOKEN" \
  scanner

echo ""
echo "Listo -> http://localhost:9000/dashboard?id=poc-agente-estimacion-epicas"
