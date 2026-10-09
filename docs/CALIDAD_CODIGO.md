# Calidad de Código y Madurez del Desarrollo

Este documento describe las herramientas configuradas para medir y mantener la
calidad del código del proyecto: **Dependabot**, **CodeQL**, el **pipeline de
CI** (lint + tests + coverage) y **SonarQube** (self-hosted, local).

Todas corren sobre el repositorio privado
[`ABRAHAMCIMAT/PoC_Agente_Estimacion_Epicas`](https://github.com/ABRAHAMCIMAT/PoC_Agente_Estimacion_Epicas),
sin depender de ninguna cuenta externa de pago.

## 1. Dependabot

Configurado en [`.github/dependabot.yml`](../.github/dependabot.yml).

- Revisa semanalmente (lunes) las dependencias de `backend/` (pip),
  `frontend/` (npm) y los propios GitHub Actions.
- Abre un PR automático por cada actualización (agrupando minor/patch para no
  saturar de PRs), con labels `dependencies` + `backend`/`frontend`/`ci`.
- También habilita **Dependabot alerts** (vulnerabilidades conocidas en
  dependencias) — visibles en la pestaña **Security > Dependabot** del repo.
- Es gratis en GitHub para repos privados, no requiere ninguna configuración
  adicional más allá de este archivo.

## 2. CodeQL (análisis de seguridad estático)

Workflow: [`.github/workflows/codeql.yml`](../.github/workflows/codeql.yml).

- Corre en cada push/PR a `main` y además una vez por semana (lunes 06:00 UTC).
- Analiza JavaScript/TypeScript (frontend) y Python (backend) buscando
  vulnerabilidades conocidas (inyección, uso de funciones inseguras, etc.).

> **Nota sobre repos privados:** publicar las alertas en la pestaña
> **Security > Code scanning** requiere *GitHub Advanced Security*, que en
> repos privados es de pago (en repos públicos es gratis) — la misma
> restricción que aplica a SonarCloud. Como este repo se mantiene privado,
> el workflow corre el análisis igual (sirve como gate de calidad en cada
> PR) pero publica el resultado como **artifact descargable** (`codeql-python`,
> `codeql-javascript-typescript` en la pestaña *Actions* de cada ejecución)
> en vez de subirlo a Security. Para revisarlo: descargar el artifact y
> abrir el `.sarif` con la extensión *SARIF Viewer* de VS Code, o con
> `gh run download`. Si en algún momento el repo se hace público, basta
> quitar `upload: false` de `codeql.yml` para que vuelva a integrarse con
> la pestaña Security.

## 3. Pipeline de CI — lint + tests + coverage

Workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

Corre en cada push/PR a `main`, con dos jobs independientes:

| Job        | Lint                      | Tests                  | Coverage |
|------------|---------------------------|-------------------------|----------|
| `backend`  | `ruff check .`            | `pytest` (7 tests base) | `pytest-cov` → `coverage.xml` |
| `frontend` | `next lint` (eslint)      | `jest` (2 tests base)   | `jest --coverage` → `lcov.info` |

Los reportes de coverage se suben como **artifacts** del workflow (pestaña
**Actions** → ejecución → *Artifacts*), y son los mismos archivos que usa
SonarQube para calcular el % de cobertura.

Los tests actuales son un **esqueleto deliberadamente pequeño** (no existía
ningún test antes de esta configuración): `/health` del backend, las
funciones puras de `utils/data_preprocessing.py`, y un render básico del
componente `Header`. Sirven para que el pipeline tenga algo real que medir;
se espera que crezcan a medida que se agregue funcionalidad.

Para correrlos en local:

```bash
# Backend
cd backend
./venv/bin/pip install -r requirements-dev.txt
./venv/bin/python -m pytest --cov=app --cov=models --cov=utils --cov-report=term-missing

# Frontend
cd frontend
npm run test:coverage
```

## 4. SonarQube (self-hosted, local)

El repo es privado, y SonarCloud (la versión en la nube) solo es gratuita
para repos públicos. Para no pagar ni exponer el código, SonarQube
**Community Edition** corre 100% local vía Docker.

Archivos: [`docker-compose.sonar.yml`](../docker-compose.sonar.yml),
[`sonar-project.properties`](../sonar-project.properties),
[`scripts/sonar-scan.sh`](../scripts/sonar-scan.sh).

### Primer uso

```bash
# 1. Levantar el servidor (tarda ~1 min en arrancar)
docker compose -f docker-compose.sonar.yml up -d sonarqube

# 2. Abrir http://localhost:9000
#    Usuario/clave inicial: admin / admin (pide cambiarla al entrar)

# 3. Crear el proyecto (una sola vez):
#    "Create Project" (manually) -> Project key: poc-agente-estimacion-epicas

# 4. Generar un token: My Account -> Security -> Generate Token

# 5. Correr el análisis (genera coverage de backend+frontend y escanea):
SONAR_TOKEN=<tu-token> ./scripts/sonar-scan.sh
```

El dashboard queda en `http://localhost:9000/dashboard?id=poc-agente-estimacion-epicas`.

### Usos posteriores

Solo repetir el paso 5 (`./scripts/sonar-scan.sh`) antes de cada merge
importante a `main`; el token no cambia.

```bash
# Detener el servidor cuando no se use (libera RAM):
docker compose -f docker-compose.sonar.yml down
```

### Cómo leer las métricas ("madurez del desarrollo")

| Métrica | Qué mide | Dónde verla |
|---|---|---|
| **Quality Gate** | Pass/fail global: ¿el código cumple el estándar mínimo definido? | Arriba del dashboard (verde = OK) |
| **Reliability / Security / Maintainability Rating** | Letra A–E. A = sin problemas conocidos de ese tipo. | 3 tarjetas superiores |
| **Bugs / Vulnerabilities / Code Smells** | Conteo de problemas por categoría (A=0 bugs, etc.) | Pestaña *Issues* |
| **Coverage** | % de líneas cubiertas por tests automatizados | Pestaña *Measures* |
| **Duplicated Lines (%)** | Código copiado/pegado sin refactorizar | Pestaña *Measures* |
| **Technical Debt (sqale_index)** | Tiempo estimado para arreglar todos los code smells | Pestaña *Measures* |
| **Cyclomatic / Cognitive Complexity** | Qué tan difícil es de leer/mantener una función | Al entrar a un archivo específico |

**Snapshot de referencia (8-oct-2026, baseline inicial):**

| Métrica | Valor |
|---|---|
| Quality Gate | ✅ OK |
| Bugs / Vulnerabilities | 0 / 0 |
| Code Smells | 20 |
| Coverage | 0.3 % (tests recién agregados, cobertura mínima esperada en esta etapa) |
| Duplicación | 0.0 % |
| Reliability / Security / Maintainability | A / A / A |
| Líneas de código (ncloc) | 1,907 |

Este snapshot es el punto de partida: a medida que se agregue más código y
más tests, lo esperable es que `ncloc` y *code smells* suban, y que
`coverage` también suba si se agregan tests junto con cada feature nueva. Si
`coverage` baja mucho mientras `ncloc` sube rápido, es señal de que se está
agregando código sin tests.

## Resumen: qué corre dónde

| Herramienta | Dónde corre | Costo | Dispara con |
|---|---|---|---|
| Dependabot | GitHub | Gratis | Cron semanal (GitHub-hosted) |
| CodeQL | GitHub Actions | Gratis | Push/PR a `main` + cron semanal |
| Lint + tests + coverage | GitHub Actions | Gratis | Push/PR a `main` |
| SonarQube | Docker local | Gratis | Manual, con `scripts/sonar-scan.sh` |
