# Documentación de la API REST

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Autenticación](#autenticación)
3. [Endpoints](#endpoints)
4. [Modelos de Datos](#modelos-de-datos)
5. [Códigos de Estado HTTP](#códigos-de-estado-http)
6. [Ejemplos Prácticos](#ejemplos-prácticos)

## 🎯 Introducción

La API de Estimación de Épicas es un servicio REST construido con FastAPI que proporciona funcionalidades para:
- Entrenar modelos de Machine Learning
- Estimar historias de usuario individuales
- Procesar lotes de historias desde archivos Excel
- Obtener estadísticas de modelos entrenados

**URL Base:** `http://localhost:8000` (desarrollo)
**Versión:** 1.0.0
**Formato:** JSON

## 🔐 Autenticación

Actualmente, la API **no requiere autenticación**. En producción se recomienda agregar:

```python
# Implementación futura de JWT
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/datos-protegidos")
async def datos_protegidos(credentials = Depends(security)):
    return {"mensaje": "Acceso permitido"}
```

Para uso actual, es responsabilidad del servidor frontend/cliente confiar en CORS.

## 📡 Endpoints

### 1. Entrenar Modelos

#### POST `/train`

Entrena o reemplaza los modelos de estimación con datos de un archivo CSV.

**Parámetros:**
- `file` (FormData, requerido): Archivo CSV con históricas de entrenamientoo

**Estructura del CSV esperada:**
```
Titulo,Historia de Usuario,Criterios de Aceptación,Custom field (Story Points),Duracion_Sprint,Costo_por_dia,Esfuerzo_por_Puntos_Historia
```

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/train" \
  -F "file=@training_data_improved.csv"
```

**Respuesta (200 OK):**
```json
{
  "status": "entrenado",
  "información_entrenamiento": {
    "historias_procesadas": 150,
    "características_extraídas": 10,
    "modelos_creados": ["point", "time", "cost", "effort"]
  },
  "métricas": {
    "point": {
      "ensemble": 0.9876,
      "random_forest": 0.9862,
      "decision_tree": 0.9875,
      "mae": 0.1402,
      "rmse": 0.3597
    },
    "time": {
      "ensemble": 0.7537,
      "random_forest": 0.7927,
      "decision_tree": 0.7047,
      "mae": 0.7580,
      "rmse": 0.9675
    },
    "cost": {
      "ensemble": 0.7729,
      "random_forest": 0.8089,
      "decision_tree": 0.7249,
      "mae": 140.3235,
      "rmse": 177.8650
    },
    "effort": {
      "ensemble": 0.9620,
      "random_forest": 0.9634,
      "decision_tree": 0.9602,
      "mae": 7.6557,
      "rmse": 9.5569
    }
  },
  "ubicación_modelos": "C:\\...\\trained_models\\models.pkl"
}
```

**Errores Posibles:**
- `400 Bad Request`: Archivo inválido o falta formato
- `500 Internal Server Error`: Error durante entrenamiento

---

### 2. Estimar Historia Individual

#### POST `/estimate/single`

Estima puntos, tiempo, costo y esfuerzo para una historia de usuario individual.

**Body (JSON):**
```json
{
  "title": "string",
  "description": "string",
  "acceptance_criteria": ["string"],
  "priority": "string (opcional)",
  "issue_type": "string (opcional)"
}
```

**Parámetros Detallados:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `title` | string | ✓ | Título o nombre de la historia |
| `description` | string | ✓ | Descripción detallada de la historia |
| `acceptance_criteria` | array | ✗ | Lista de criterios de aceptación |
| `priority` | string | ✗ | Nivel de prioridad (high, medium, low) |
| `issue_type` | string | ✗ | Tipo de historia (feature, bug, refactor) |

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/estimate/single" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar autenticación con JWT",
    "description": "Agregar sistema de autenticación robusto con tokens JWT. Sistema debe validar credenciales y emitir tokens con tiempo de expiración. Integrar con base de datos de usuarios existente.",
    "acceptance_criteria": [
      "Sistema valida correctamente correo y contraseña",
      "Token JWT se expira después de 24 horas",
      "Se puede refrescar token sin volver a autenticar",
      "Las contraseñas se almacenan con hash bcrypt"
    ],
    "priority": "high",
    "issue_type": "feature"
  }'
```

**Respuesta (200 OK):**
```json
{
  "story_title": "Implementar autenticación con JWT",
  "point_estimate": {
    "ensemble": 8.5,
    "random_forest": 8.3,
    "decision_tree": 8.7
  },
  "time_estimate": {
    "ensemble": 4.2,
    "random_forest": 4.1,
    "decision_tree": 4.3
  },
  "cost_estimate": {
    "ensemble": 1450.50,
    "random_forest": 1420.30,
    "decision_tree": 1480.70
  },
  "effort_estimate": {
    "ensemble": 145.3,
    "random_forest": 143.5,
    "decision_tree": 147.1
  },
  "model_confidence": {
    "point": {
      "ensemble": 0.9876,
      "random_forest": 0.9862,
      "decision_tree": 0.9875
    },
    "time": {
      "ensemble": 0.7537,
      "random_forest": 0.7927,
      "decision_tree": 0.7047
    },
    "cost": {
      "ensemble": 0.7729,
      "random_forest": 0.8089,
      "decision_tree": 0.7249
    },
    "effort": {
      "ensemble": 0.9620,
      "random_forest": 0.9634,
      "decision_tree": 0.9602
    }
  }
}
```

**Errores Posibles:**
- `400 Bad Request`: Campos requeridos faltantes
- `503 Service Unavailable`: Modelos no entrenados

---

### 3. Estimar Lote (Excel)

#### POST `/estimate/batch`

Procesa un archivo Excel con múltiples historias y retorna estimaciones para todas.

**Body (FormData):**
- `file` (file, requerido): Archivo Excel (.xlsx)

**Estructura esperada del Excel:**
```
| Titulo | Historia de Usuario | Criterios de Aceptación |
|--------|---------------------|------------------------|
| HU001  | Descripción...      | Criterio 1, Criterio 2  |
```

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/estimate/batch" \
  -F "file=@historias.xlsx"
```

**Respuesta (200 OK):**
```json
{
  "total_historias": 5,
  "procesadas_exitosamente": 5,
  "errores": 0,
  "resultados": [
    {
      "story_title": "Historia 1",
      "point_estimate": {...},
      "time_estimate": {...},
      "cost_estimate": {...},
      "effort_estimate": {...},
      "model_confidence": {...}
    },
    {
      "story_title": "Historia 2",
      ...
    }
  ]
}
```

**Errores Posibles:**
- `400 Bad Request`: Archivo no es Excel válido
- `413 Payload Too Large`: Archivo muy grande (>10MB)
- `422 Unprocessable Entity`: Formato de datos inválido

---

### 4. Obtener Estadísticas de Modelos

#### GET `/models/stats`

Retorna información sobre los modelos actualmente entrenados.

**Parámetros:** Ninguno

**Ejemplo:**
```bash
curl -X GET "http://localhost:8000/models/stats"
```

**Respuesta (200 OK):**
```json
{
  "models_trained": true,
  "targets": ["point", "time", "cost", "effort"],
  "training_samples": 150,
  "features_count": 10,
  "model_location": "C:\\...\\trained_models\\models.pkl",
  "model_metrics": {
    "point": {
      "ensemble": 0.9876,
      "random_forest": 0.9862,
      "decision_tree": 0.9875
    },
    "time": {
      "ensemble": 0.7537,
      "random_forest": 0.7927,
      "decision_tree": 0.7047
    },
    "cost": {
      "ensemble": 0.7729,
      "random_forest": 0.8089,
      "decision_tree": 0.7249
    },
    "effort": {
      "ensemble": 0.9620,
      "random_forest": 0.9634,
      "decision_tree": 0.9602
    }
  }
}
```

**Respuesta si no hay modelos (200 OK):**
```json
{
  "models_trained": false,
  "targets": [],
  "training_samples": null,
  "features_count": null,
  "model_location": "C:\\...\\trained_models\\models.pkl",
  "model_metrics": {}
}
```

---

## 📦 Modelos de Datos

### SolicitudEstimacionHistoria

```json
{
  "title": "string (1-500 chars)",
  "description": "string (1-5000 chars)",
  "acceptance_criteria": ["string"],
  "priority": "string (opcional)",
  "issue_type": "string (opcional)"
}
```

### RespuestaEstimación

```json
{
  "story_title": "string",
  "point_estimate": {
    "ensemble": "número",
    "random_forest": "número",
    "decision_tree": "número"
  },
  "time_estimate": {
    "ensemble": "número",
    "random_forest": "número",
    "decision_tree": "número"
  },
  "cost_estimate": {
    "ensemble": "número",
    "random_forest": "número",
    "decision_tree": "número"
  },
  "effort_estimate": {
    "ensemble": "número",
    "random_forest": "número",
    "decision_tree": "número"
  },
  "model_confidence": {
    "point": {"ensemble": "número R²", "random_forest": "número R²", "decision_tree": "número R²"},
    "time": {...},
    "cost": {...},
    "effort": {...}
  }
}
```

### RespuestaEstimacionLote

```json
{
  "total_historias": "número",
  "procesadas_exitosamente": "número",
  "errores": "número",
  "resultados": ["RespuestaEstimación[]"]
}
```

### RespuestaEntrenamiento

```json
{
  "status": "entrenado",
  "información_entrenamiento": {
    "historias_procesadas": "número",
    "características_extraídas": "número",
    "modelos_creados": ["string"]
  },
  "métricas": {
    "point": {...},
    "time": {...},
    "cost": {...},
    "effort": {...}
  },
  "ubicación_modelos": "string"
}
```

---

## 📊 Códigos de Estado HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Solicitud exitosa |
| 400 | Bad Request | Solicitud inválida (campos faltantes, formato incorrecto) |
| 404 | Not Found | Endpoint no encontrado |
| 413 | Payload Too Large | Archivo demasiado grande |
| 422 | Unprocessable Entity | Datos no pueden ser procesados |
| 500 | Internal Server Error | Error del servidor |
| 503 | Service Unavailable | Modelos no están disponibles |

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Flujo Completo

```bash
# 1. Entrenar modelos
curl -X POST "http://localhost:8000/train" \
  -F "file=@training_data.csv"

# 2. Verificar entrenamiento
curl -X GET "http://localhost:8000/models/stats"

# 3. Estimar una historia
curl -X POST "http://localhost:8000/estimate/single" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Crear API REST",
    "description": "Desarrollar API REST completa con CRUD",
    "acceptance_criteria": ["GET funciona", "POST funciona", "Validación"],
    "priority": "high",
    "issue_type": "feature"
  }'
```

### Ejemplo 2: Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Estimar una historia
historia = {
    "title": "Corregir bug de login",
    "description": "Los usuarios no pueden hacer login con espacios en nombre de usuario",
    "acceptance_criteria": [
        "El login acepta espacios antes/después",
        "La contraseña se valida correctamente",
        "Mensaje de error es claro"
    ],
    "priority": "high",
    "issue_type": "bug"
}

response = requests.post(
    f"{BASE_URL}/estimate/single",
    json=historia
)

resultado = response.json()
print(f"Puntos estimados: {resultado['point_estimate']['ensemble']}")
print(f"Confiabilidad R²: {resultado['model_confidence']['point']['ensemble']:.4f}")
```

### Ejemplo 3: JavaScript/Node.js

```javascript
const axios = require('axios');

const baseURL = 'http://localhost:8000';

async function estimarHistoria(historia) {
  try {
    const response = await axios.post(
      `${baseURL}/estimate/single`,
      historia
    );
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
    throw error;
  }
}

// Uso
const historia = {
  title: "Implementar reportes",
  description: "Crear sistema de reportes con gráficos",
  acceptance_criteria: [
    "Gráficos de barras funcionan",
    "Se puede exportar a PDF",
    "Datos se actualizan en tiempo real"
  ],
  priority: "medium",
  issue_type: "feature"
};

estimarHistoria(historia).then(resultado => {
  console.log('Estimación:', resultado);
});
```

### Ejemplo 4: Procesar Excel

```python
import requests

# Cargar y procesar archivo Excel
with open('historias.xlsx', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/estimate/batch',
        files=files
    )

resultado = response.json()
print(f"Total historias: {resultado['total_historias']}")
print(f"Procesadas: {resultado['procesadas_exitosamente']}")
print(f"Errores: {resultado['errores']}")

# Exportar resultados
for estimacion in resultado['resultados']:
    print(f"\n{estimacion['story_title']}")
    print(f"  Puntos: {estimacion['point_estimate']['ensemble']}")
    print(f"  Días: {estimacion['time_estimate']['ensemble']}")
    print(f"  Costo: ${estimacion['cost_estimate']['ensemble']:.2f}")
    print(f"  Esfuerzo: {estimacion['effort_estimate']['ensemble']:.1f}h")
```

---

## 🔍 Rate Limiting

Actualmente no hay límite de velocidad. En producción se recomienda:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/estimate/single")
@limiter.limit("100/minute")
async def estimate_single(request):
    pass
```

---

## 📝 Documentación Interactiva

La API incluye documentación interactiva automática disponible en:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Estas interfaces permiten probar los endpoints directamente desde el navegador.

---

**Versión**: 1.0
**Última actualización**: Agosto 2026
