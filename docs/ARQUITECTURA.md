# Arquitectura del Sistema de Estimación de Épicas

## 🏗️ Vista General

El sistema es una aplicación fullstack de dos capas arquitectónica:

```
┌─────────────────────────────────────────────────────────────────┐
│                   FRONTEND (React/Next.js)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Encabezado │ Carga Excel │ Resultados                   │   │
│  │            │             ├─ Tabla de Estimaciones       │   │
│  │            │             ├─ Barras de Progreso          │   │
│  │            │             └─ Comparación Modelos + R²    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↕
                     API REST HTTP
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI - Python)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Endpoints REST                                           │   │
│  │  • POST /train          - Entrena modelos               │   │
│  │  • POST /estimate/single - Estima una historia          │   │
│  │  • POST /estimate/batch - Estima por lote (Excel)       │   │
│  │  • GET /models/stats    - Obtiene estadísticas          │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Motor de ML (EstimationModels)                           │   │
│  │  ├─ 4 Modelos Ensemble (1 por métrica)                 │   │
│  │  │  ├─ Random Forest (70%)                              │   │
│  │  │  └─ Árbol de Decisión (30%)                          │   │
│  │  ├─ Extractor de Features (10 características)           │   │
│  │  ├─ Normalizador de Datos (StandardScaler)              │   │
│  │  └─ Almacén de Métricas (puntuaciones R²)               │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Procesamiento de Datos                                  │   │
│  │  ├─ Manejador de Archivos Excel                         │   │
│  │  ├─ Generador de Vectores de Features                    │   │
│  │  └─ Validación y Normalización de Datos                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Almacenamiento Persistente                              │   │
│  │  ├─ trained_models/models.pkl (Modelos entrenados)      │   │
│  │  ├─ training_data_improved.csv (Conjunto de datos)      │   │
│  │  └─ Métricas del Modelo (puntuaciones R²)               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 📦 Componentes Principales

### Arquitectura del Backend

#### 1. **Capa API (main.py)**
```python
Aplicación FastAPI con 4 endpoints principales:
├── POST /train                  # Entrena modelos con CSV
├── POST /estimate/single        # Estima una historia
├── POST /estimate/batch         # Procesa archivo Excel
└── GET /models/stats            # Retorna métricas R²
```

**Responsabilidades:**
- Validación de entrada
- Manejo de CORS
- Transformación de request/response
- Manejo de errores HTTP

#### 2. **Motor de ML (epic_estimation_models.py)**
```python
Clase EstimationModels:
├── train(X, y_dict)             # Entrena 4 modelos
├── predict(features, target)    # Realiza predicción
├── save()                        # Guarda modelos + métricas
└── load()                        # Carga modelos + métricas

Cada modelo:
├── Random Forest (n_estimators=100)
├── Árbol de Decisión (max_depth=10)
└── Ensemble (promedio ponderado)
```

**Fórmula de Ensemble:**
```
predicción = (RandomForest * 0.7 + ÁrbolDecisión * 0.3)
```

#### 3. **Ingeniería de Features (create_feature_vector)**
```
Transforma historia de usuario en vector de 10 características:

[puntuación_complejidad, puntuación_alcance, cantidad_criterios, palabras_técnicas,
 indicadores_integración, requisitos_testing, prioridad_codificada,
 tipo_problema_codificado, cantidad_números, variedad_léxica]
```

**Algoritmo:**
```python
def crear_vector_features(request: SolicitudEstimacionHistoria):
    # 1. Extrae texto (título + descripción + criterios)
    # 2. Tokeniza y cuenta palabras clave
    # 3. Analiza patrones lingüísticos
    # 4. Escala con StandardScaler (ajuste durante entrenamiento)
    # 5. Retorna vector normalizado [1, 10]
```

#### 4. **Preprocesamiento de Datos (data_preprocessing.py)**
```python
PreprocessadorDatosJira:
├── Valida formato Excel
├── Extrae columnas necesarias
├── Filtra datos inválidos
└── Convierte en formato compatible

procesar_excel_usuario(archivo):
├── Lee archivo Excel
├── Procesa cada historia
└── Retorna lista de SolicitudEstimacionHistoria
```

### Arquitectura del Frontend

#### 1. **Páginas (index.jsx)**
- Punto de entrada de la aplicación
- Manejo de estado global
- Orquestación de componentes

#### 2. **Componentes**

**Encabezado.jsx:**
- Logo y título
- Información de versión
- Enlaces de navegación

**CargaExcel.jsx:**
- Arrastrar y soltar archivos
- Validación local
- Interfaz de carga
- Indicador de progreso

**ResultadosEstimación.jsx:**
- Tabla de estimaciones
- Barras de progreso coloreadas
- Comparación de modelos
- Métricas R² con color-coding
- Exportación a CSV

#### 3. **Estilos (globals.css)**
- CSS Grid para diseño responsivo
- Animaciones suaves
- Color-coding intuitivo
- Consultas de medios para móvil

## 🔄 Flujos de Datos

### Flujo 1: Entrenar Modelos
```
Usuario sube CSV
    ↓
Backend: POST /train
    ↓
PreprocessadorDatos.procesar()
    ↓
EstimationModels.entrenar()
    - Divide: 80% entrenamiento, 20% validación
    - Entrena 4 modelos (puntos, tiempo, costo, esfuerzo)
    - Calcula R² para cada modelo
    ↓
Guarda modelos.pkl + métricas
    ↓
Retorna {"estado": "entrenado", "métricas": {...}}
```

### Flujo 2: Estimar Historia Individual
```
Usuario completa formulario
    ↓
Frontend: POST /estimate/single
    ↓
Backend: crear_vector_features()
    - Extrae 10 características lingüísticas
    - Normaliza con normalizador
    ↓
Para cada objetivo (puntos, tiempo, costo, esfuerzo):
    - RandomForest.predict()
    - ÁrbolDecisión.predict()
    - Ensemble = (RandomForest*0.7 + ÁrbolDecisión*0.3)
    ↓
Obtiene confianza_modelo (puntuaciones R²)
    ↓
Retorna RespuestaEstimación con todas las predicciones
    ↓
Frontend: Renderiza tabla + comparación
```

### Flujo 3: Procesar Excel (Lote)
```
Usuario sube archivo Excel
    ↓
Frontend: POST /estimate/batch con multipart/form-data
    ↓
Backend: Recibe ArchivoSubido
    ↓
PreprocessadorDatos.procesar_excel_usuario()
    - Lee columnas: Título, Historia, Criterios
    - Valida estructura
    - Crea SolicitudEstimacionHistoria[] 
    ↓
Para cada historia:
    - crear_vector_features()
    - predecir() para 4 objetivos
    - Obtiene métricas R²
    ↓
Retorna RespuestaEstimacionLote
    ↓
Frontend: 
    - Renderiza tabla con desplazamiento
    - Expandir/contraer detalles
    - Exportar CSV
```

## 📊 Flujo de Datos - Formato de Datos

### Entrada Típica (Excel)
```
| Título                      | Historia de Usuario | Criterios de Aceptación |
|-----|
| Implementar login           | Sistema seguro...   | Validar correo,         |
|                             |                     | Usar JWT,               |
|                             |                     | Tiempo de espera 24h    |
```

### Vector de Features (Interno)
```python
[
  5.2,        # complejidad (palabras clave como "complejo", "integración")
  0.8,        # alcance (indica trabajo múltiple)
  3.0,        # cantidad de criterios de aceptación
  2.0,        # palabras técnicas ("JWT", "validar", "token")
  0.5,        # indicadores de integración
  1.0,        # requisitos de pruebas
  0.75,       # prioridad (0-1, codificado)
  0.33,       # tipo de problema (característica, error, refactor) codificado
  4.0,        # cantidad de números en descripción
  0.65        # variedad léxica (palabras_únicas / palabras_totales)
]
```

### Respuesta de la API
```json
{
  "título_historia": "Implementar login",
  "estimación_puntos": {
    "ensemble": 8.5,
    "bosque_aleatorio": 8.3,
    "árbol_decisión": 8.7
  },
  "estimación_tiempo": {...},
  "estimación_costo": {...},
  "estimación_esfuerzo": {...},
  "confianza_modelo": {
    "puntos": {
      "ensemble": 0.9876,
      "bosque_aleatorio": 0.9862,
      "árbol_decisión": 0.9875
    },
    "tiempo": {...},
    "costo": {...},
    "esfuerzo": {...}
  }
}
```

## 🔐 Seguridad y Validación

### Validación de Entrada
```python
# Todos los endpoints validan:
- Campos requeridos presentes
- Tipos de datos correctos
- Longitud máxima de strings
- Formato de archivos
```

### Configuración CORS
```python
# Solo localhost en desarrollo
# Restringido en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True
)
```

### Manejo de Errores
```python
try:
    predicción = modelo.predict(features)
except ValueError as e:
    raise HTTPException(status_code=400, detail="Vector de features inválido")
except Exception as e:
    logging.error(f"Error: {e}")
    raise HTTPException(status_code=500, detail="Error interno")
```

## ⚡ Consideraciones de Rendimiento

### Almacenamiento en Caché
- Modelos se cargan una sola vez en memoria
- StandardScaler se reutiliza
- Sin llamadas a base de datos (sin estado)

### Escalabilidad
- Solicitud por solicitud (sin estado)
- Puede ejecutar múltiples trabajadores
- Procesamiento por lotes con chunks

### Latencia Típica
```
Estimación individual: ~50-100ms
Lote de 100: ~5-10s
Entrenamiento completo: ~30s
```

## 📈 Modelo de ML Detallado

### Proceso de Entrenamiento
```python
1. Lectura de datos (150 historias)
2. Extracción de features (10 características c/u)
3. Divide: 120 entrenamiento, 30 validación
4. StandardScaler.fit(X_entrenamiento)
5. Para cada objetivo:
   a) RandomForest.fit(X_entrenamiento, y_entrenamiento)
   b) ÁrbolDecisión.fit(X_entrenamiento, y_entrenamiento)
   c) Calcula R² en conjunto de validación
   d) Guarda modelo + normalizador + métricas

6. R² = 1 - (SS_res / SS_tot)
   Donde:
   - SS_res = suma((y_actual - y_predicción)²)
   - SS_tot = suma((y_actual - y_media)²)
```

### Proceso de Predicción
```python
1. Recibe SolicitudEstimacionHistoria
2. crear_vector_features() → [1, 10]
3. Normaliza: normalizador.transform([1, 10])
4. Predice:
   - RandomForest.predict() → valor
   - ÁrbolDecisión.predict() → valor
   - Ensemble = (RandomForest * 0.7 + ÁrbolDecisión * 0.3)
5. Retorna con puntuaciones R² del entrenamiento
```

## 🛠️ Decisiones Arquitectónicas

### ¿Por qué Ensemble?
- Reduce el sobreajuste
- Combina fortalezas de múltiples algoritmos
- Mejora generalización

### ¿Por qué 10 Features Lingüísticas?
- Captura contexto del dominio Ágil
- Ignora ruido de longitud de texto
- Correlaciona bien con esfuerzo real

### ¿Por qué FastAPI?
- Rápido (async/await)
- Validación automática con Pydantic
- OpenAPI/Swagger automático
- Excelente documentación

### ¿Por qué Next.js?
- Renderización en servidor si es necesario
- Recarga en caliente en desarrollo
- Compilación optimizada
- Fácil despliegue

## 🔮 Limitaciones Actuales

1. **Modelos entrenados con datos sintéticos**
   - Solución: Reentrenar con datos reales

2. **Sin persistencia de histórico**
   - Solución: Agregar PostgreSQL

3. **Sin autenticación**
   - Solución: Agregar autenticación JWT

4. **Conjunto único de características**
   - Solución: Perfilar por equipo/proyecto

5. **Sin intervalos de confianza**
   - Solución: Implementar regresión de cuantiles

---

**Versión**: 1.0
**Última actualización**: Agosto 2026
