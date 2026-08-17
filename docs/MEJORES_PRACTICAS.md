# Mejores Prácticas de Programación

## 📋 Tabla de Contenidos

1. [Estándares de Código](#estándares-de-código)
2. [Manejo de Errores](#manejo-de-errores)
3. [Seguridad](#seguridad)
4. [Performance](#performance)
5. [Testing](#testing)
6. [Documentación](#documentación)
7. [Control de Versiones](#control-de-versiones)

---

## 📝 Estándares de Código

### Python

#### Nombres de Variables y Funciones

✅ **Correcto:**
```python
def calcular_vector_features(solicitud_historia):
    """Calcula características lingüísticas."""
    complejidad_puntuacion = 0
    palabras_clave = ["complejo", "integración"]
    return features

class PreprocessadorDatos:
    """Preprocesa datos de Excel."""
    
def obtener_valor_maximo(lista_valores):
    """Obtiene el valor máximo."""
    return max(lista_valores) if lista_valores else 0
```

❌ **Incorrecto:**
```python
def cvf(sh):  # Demasiado corto
    cp = 0  # Abreviado
    pk = ["complejo"]
    return f

class PD:  # Abreviado
    
def ovm(lv):  # Nombres muy cortos
    return max(lv)
```

#### Longitud de Líneas

```python
# Máximo 100 caracteres por línea
# Usar paréntesis para dividir líneas largas

# ✅ Correcto
resultado = funciones.calcular_estimacion(
    historia=solicitud,
    modelos=modelos_entrenados,
    incluir_confianza=True
)

# ❌ Incorrecto
resultado = funciones.calcular_estimacion(historia=solicitud, modelos=modelos_entrenados, incluir_confianza=True)
```

#### Imports

```python
# ✅ Correcto - Ordenados y agrupados
# 1. Librería estándar
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# 2. Librerías de terceros
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from fastapi import FastAPI

# 3. Módulos locales
from models.epic_estimation_models import EstimationModels
from utils.data_preprocessing import PreprocessadorDatos

# ❌ Incorrecto - Desordenados
from fastapi import FastAPI
import os
from models.epic_estimation_models import EstimationModels
import pandas as pd
import sys
```

#### Docstrings

```python
# ✅ Usar formato Google/NumPy
def crear_vector_features(request: SolicitudEstimacionHistoria) -> np.ndarray:
    """
    Crea vector de características a partir de una historia.
    
    Extrae 10 características lingüísticas del título, descripción
    y criterios de aceptación usando análisis de texto.
    
    Args:
        request: Objeto SolicitudEstimacionHistoria con datos
        
    Returns:
        np.ndarray: Vector normalizado de shape (1, 10)
        
    Raises:
        ValueError: Si título o descripción están vacíos
        
    Note:
        Las características se normalizan usando StandardScaler
        que fue ajustado durante entrenamiento.
        
    Example:
        >>> req = SolicitudEstimacionHistoria(
        ...     title="Implementar API",
        ...     description="Crear API REST completa"
        ... )
        >>> features = crear_vector_features(req)
        >>> print(features.shape)
        (1, 10)
    """
    pass

# ✅ Docstrings en clases
class EstimationModels:
    """
    Gestor de modelos de estimación usando ensemble.
    
    Mantiene modelos Random Forest y Árbol Decisión para cada
    métrica objetivo (puntos, tiempo, costo, esfuerzo).
    Las predicciones se combinan con media ponderada (70% RF, 30% DT).
    
    Attributes:
        rf_models (dict): Modelos Random Forest por target
        dt_models (dict): Modelos Árbol Decisión por target
        scalers (dict): Normalizadores por target
        model_metrics (dict): Puntuaciones R² de validación
    """
    pass
```

### JavaScript/React

#### Nombres de Componentes

```javascript
// ✅ Correcto - PascalCase para componentes
function ResultadosEstimación() {
  return <div>Resultados</div>;
}

function CargaArchivo() {
  return <input type="file" />;
}

// ❌ Incorrecto - camelCase para componentes
function resultadosEstimacion() {
  return <div>Resultados</div>;
}

function cargaArchivo() {
  return <input type="file" />;
}
```

#### Funciones Utilitarias

```javascript
// ✅ Correcto - camelCase
const obtenerValoresMaximos = (resultados) => {
  return {
    puntos: Math.max(...resultados.map(r => r.puntos)),
    tiempo: Math.max(...resultados.map(r => r.tiempo))
  };
};

const formatearDinero = (cantidad) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'USD'
  }).format(cantidad);
};

// ❌ Incorrecto
const ObtenerValoresMaximos = (resultados) => { ... };
const gVM = (resultados) => { ... };
```

#### Estructura de Componentes

```jsx
// ✅ Correcto - Estructura clara
import React, { useState, useEffect } from 'react';
import './EstimationResults.css';

/**
 * Renderiza tabla de resultados de estimaciones con métricas.
 * 
 * @param {Object} props
 * @param {Array} props.resultados - Array de estimaciones
 * @param {Function} props.onExportar - Callback para exportar
 * @returns {JSX.Element}
 */
function EstimationResults({ resultados, onExportar }) {
  // 1. Estados
  const [expandido, setExpandido] = useState(null);
  
  // 2. Efectos
  useEffect(() => {
    console.log('Resultados actualizados:', resultados);
  }, [resultados]);
  
  // 3. Funciones locales
  const obtenerClaseConfianza = (r2) => {
    if (r2 >= 0.8) return 'confianza-alta';
    return 'confianza-media';
  };
  
  // 4. Renderizado
  return (
    <div className="contenedor-resultados">
      <table className="tabla-resumen">
        {/* Contenido */}
      </table>
    </div>
  );
}

export default EstimationResults;
```

---

## 🐛 Manejo de Errores

### Backend Python

#### Niveles de Error

```python
import logging

logger = logging.getLogger(__name__)

# DEBUG - Información detallada para diagnóstico
logger.debug("Vector de features creado: [5.2, 0.8, 3.0, ...]")

# INFO - Confirmación de operaciones exitosas
logger.info("Modelos entrenados exitosamente. R² promedio: 0.85")

# WARNING - Algo inesperado pero manejable
logger.warning("Archivo CSV tiene columnas con valores faltantes: descripción (5%)")

# ERROR - Error grave pero manejable
logger.error("Falla al cargar modelos: archivo corrupto", exc_info=True)

# CRITICAL - Error muy grave
logger.critical("Base de datos no disponible", exc_info=True)
```

#### Try-Except Específicos

```python
# ✅ Correcto - Excepciones específicas
try:
    df = pd.read_csv(ruta_archivo)
except FileNotFoundError:
    logger.error(f"Archivo no encontrado: {ruta_archivo}")
    raise HTTPException(status_code=404, detail="Archivo no encontrado")
except pd.errors.ParserError as e:
    logger.error(f"Error parsing CSV: {e}")
    raise HTTPException(status_code=400, detail="Formato de CSV inválido")
except Exception as e:
    logger.error(f"Error inesperado: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Error interno")

# ❌ Incorrecto - Captura todo
try:
    df = pd.read_csv(ruta_archivo)
except:  # Nunca hagas esto
    print("Error")  # Usar logging
```

#### Validación de Entrada

```python
# ✅ Usar Pydantic para validación automática
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class SolicitudEstimacionHistoria(BaseModel):
    title: str = Field(..., min_length=1, max_length=500,
                      description="Título de la historia")
    description: str = Field(..., min_length=5, max_length=5000,
                            description="Descripción detallada")
    acceptance_criteria: Optional[List[str]] = Field(
        default=None,
        description="Criterios de aceptación"
    )
    priority: Optional[str] = Field(default=None, regex="^(high|medium|low)$")
    
    @validator('title')
    def validar_titulo(cls, v):
        if not v.strip():
            raise ValueError('Título no puede estar vacío')
        return v.strip()

# La validación es automática al crear instancia
try:
    solicitud = SolicitudEstimacionHistoria(
        title="",  # Error - vacío
        description="Test"
    )
except ValidationError as e:
    print(e.errors())  # Detalles de errores
```

### Frontend JavaScript

#### Manejo de Promesas

```javascript
// ✅ Correcto - Async/Await con try-catch
async function procesarArchivo(archivo) {
  try {
    const formData = new FormData();
    formData.append('file', archivo);
    
    const respuesta = await fetch('/api/estimate/batch', {
      method: 'POST',
      body: formData
    });
    
    if (!respuesta.ok) {
      throw new Error(`Error HTTP: ${respuesta.status}`);
    }
    
    const datos = await respuesta.json();
    return datos;
    
  } catch (error) {
    console.error('Error procesando archivo:', error);
    throw error;  // Re-lanzar para que el llamador lo maneje
  }
}

// ✅ Correcto - .catch() para promesas
fetch('/api/data')
  .then(resp => {
    if (!resp.ok) throw new Error('HTTP error ' + resp.status);
    return resp.json();
  })
  .then(datos => procesarDatos(datos))
  .catch(error => {
    console.error('Error:', error);
    mostrarErrorAlUsuario(error.message);
  });

// ❌ Incorrecto - No manejar errores
fetch('/api/data')
  .then(resp => resp.json())
  .then(datos => procesarDatos(datos))
  // Sin catch - si hay error, se pierde silenciosamente
```

#### Manejo de Errores en Componentes React

```javascript
// ✅ Usar Error Boundaries
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { tieneError: false, error: null };
  }
  
  static getDerivedStateFromError(error) {
    return { tieneError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Error capturado:', error, errorInfo);
  }
  
  render() {
    if (this.state.tieneError) {
      return <div>Error: {this.state.error.message}</div>;
    }
    return this.props.children;
  }
}

// Uso
<ErrorBoundary>
  <EstimationResults resultados={resultados} />
</ErrorBoundary>

// ✅ Estados para errores en componentes funcionales
function CargaArchivo() {
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);
  
  const manejarCarga = async (archivo) => {
    setCargando(true);
    setError(null);
    
    try {
      await procesarArchivo(archivo);
    } catch (err) {
      setError(err.message);
      console.error('Error en carga:', err);
    } finally {
      setCargando(false);
    }
  };
  
  return (
    <div>
      {error && <div className="alerta-error">{error}</div>}
      {/* Resto del componente */}
    </div>
  );
}
```

---

## 🔐 Seguridad

### Validación de Input

```python
# ✅ Siempre validar entrada en Backend
@app.post("/estimate/single")
async def estimar_historia(request: SolicitudEstimacionHistoria):
    # Pydantic valida automáticamente
    # No necesitas if/else manual
    pass

# ❌ Nunca confiar en validación del cliente
# El usuario podría enviar datos malformados intencionalmente
```

### Inyección de SQL

```python
# ✅ Usar ORMs o parameterized queries
resultado = db.query(Usuario).filter(Usuario.email == email).first()

# ❌ Nunca hacer string formatting directo
query = f"SELECT * FROM usuarios WHERE email = '{email}'"  # Vulnerable
```

### Cross-Site Scripting (XSS)

```javascript
// ❌ Incorrecto - permite XSS
function mostrarTitulo(titulo) {
  document.getElementById('titulo').innerHTML = titulo;
}

// ✅ Correcto - escapa HTML automáticamente
function mostrarTitulo(titulo) {
  document.getElementById('titulo').textContent = titulo;
}

// O en React (automático)
<h1>{titulo}</h1>  // Escapa automáticamente
```

### CORS Configuration

```python
# ✅ Correcto - Restrictivo en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tudominio.com",
        "https://www.tudominio.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ❌ Incorrecto - Permite cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Muy permisivo
)
```

---

## ⚡ Performance

### Optimización de Consultas ML

```python
# ✅ Cachear modelos en memoria
@app.on_event("startup")
async def cargar_modelos():
    global modelos
    modelos = EstimationModels()
    modelos.cargar()  # Una sola vez al iniciar

# Reutilizar en cada solicitud - NO cargar/guardar constantemente

# ✅ Usar predicciones por lotes
def predecir_lote(historias, modelos):
    features = np.array([crear_vector_features(h) for h in historias])
    # Una sola predicción para todo el lote
    predicciones = modelos.predecir(features, target='puntos')
    return predicciones

# ❌ Evitar predicciones individuales en loops
for historia in historias:
    features = crear_vector_features(historia)
    resultado = modelos.predecir(features, target='puntos')  # Repetido
```

### Compresión de Respuestas

```python
# ✅ FastAPI comprime automáticamente con GZip
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Reduce tamaño de respuestas JSON ~70%
```

### Lazy Loading en Frontend

```javascript
// ✅ Cargar componentes bajo demanda
const ResultadosEstimacion = React.lazy(() => 
  import('./components/EstimationResults')
);

function App() {
  return (
    <Suspense fallback={<div>Cargando...</div>}>
      <ResultadosEstimacion />
    </Suspense>
  );
}

// ❌ Evitar cargar todo de una vez
// import * from './componentes'  // Carga todo
```

---

## ✅ Testing

### Tests Backend

```python
import pytest
from httpx import AsyncClient

@pytest.fixture
async def cliente():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_estimar_historia(cliente):
    """Prueba estimación de historia individual."""
    respuesta = await cliente.post(
        "/estimate/single",
        json={
            "title": "Test historia",
            "description": "Descripción de prueba",
            "acceptance_criteria": ["Criterio 1"]
        }
    )
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "point_estimate" in datos
    assert datos["model_confidence"]["point"]["ensemble"] > 0

@pytest.mark.asyncio
async def test_error_campos_faltantes(cliente):
    """Prueba validación de campos requeridos."""
    respuesta = await cliente.post(
        "/estimate/single",
        json={"title": "Solo título"}  # Falta descripción
    )
    
    assert respuesta.status_code == 422  # Validación fallida
```

### Tests Frontend

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import EstimationResults from './EstimationResults';

describe('EstimationResults', () => {
  it('renderiza tabla de resultados', () => {
    const resultados = {
      resultados: [{
        story_title: "Test",
        point_estimate: { ensemble: 8.5 },
        time_estimate: { ensemble: 4.2 },
        cost_estimate: { ensemble: 1450 },
        effort_estimate: { ensemble: 145.3 },
        model_confidence: {
          point: { ensemble: 0.9876 }
        }
      }]
    };
    
    render(<EstimationResults results={resultados} />);
    
    expect(screen.getByText("Test")).toBeInTheDocument();
    expect(screen.getByText("8.5")).toBeInTheDocument();
  });
  
  it('expande y contrae detalles', () => {
    // ... test
  });
});
```

---

## 📚 Documentación

### Docstrings Completos

```python
def crear_vector_features(request: SolicitudEstimacionHistoria) -> np.ndarray:
    """
    Transforma una solicitud de historia en vector de características.
    
    Esta función implementa ingeniería de características lingüísticas
    para convertir texto no estructurado (título, descripción, criterios)
    en un vector numérico de 10 características que capturan aspectos
    importantes de la complejidad de una historia.
    
    Características extraídas:
        1. Puntuación de complejidad: palabras clave (complejo, integración)
        2. Puntuación de alcance: indicadores de múltiples subsistemas
        3. Cantidad de criterios: count(acceptance_criteria)
        4. Palabras técnicas: detecta términos técnicos comunes
        5. Indicadores de integración: palabras como "integrar", "conectar"
        6. Requisitos testing: palabras como "test", "validar"
        7. Prioridad: encoded value (0-1)
        8. Tipo de issue: encoded value (feature=0.5, bug=0.3, etc)
        9. Cantidad de números: count(digits)
        10. Variedad léxica: unique_words / total_words
    
    Args:
        request (SolicitudEstimacionHistoria): Solicitud con datos
        
    Returns:
        np.ndarray: Vector normalizado de shape (1, 10) con valores
                   entre -1 y 1 (normalizado por StandardScaler)
    
    Raises:
        ValueError: Si título o descripción están vacíos
        TypeError: Si request no es tipo SolicitudEstimacionHistoria
    
    Examples:
        >>> req = SolicitudEstimacionHistoria(
        ...     title="Implementar autenticación",
        ...     description="Sistema completo de autenticación con JWT",
        ...     acceptance_criteria=["Token valida", "Refresh funciona"],
        ...     priority="high",
        ...     issue_type="feature"
        ... )
        >>> features = crear_vector_features(req)
        >>> features.shape
        (1, 10)
        >>> features[0, 0]  # Primera característica (complejidad)
        0.45
    
    Note:
        Las características se normalizan usando un StandardScaler que
        fue ajustado durante el entrenamiento. Esto garantiza consistencia
        entre entrenamiento e inferencia. Los valores fuera del rango
        típico pueden indicar historias inusuales.
        
        Para debugging, se pueden imprimir valores crudos antes de escalar.
    
    See Also:
        EstimationModels.predict(): Usa estas características
        data_preprocessing.procesar_excel_usuario(): Procesa lotes
    """
    pass
```

### Archivos README en Carpetas

```markdown
# backend/

Contiene el servidor FastAPI y toda la lógica de Machine Learning.

## Estructura

- `app/main.py`: Servidor FastAPI con endpoints
- `models/epic_estimation_models.py`: Modelos ML
- `utils/data_preprocessing.py`: Procesamiento de datos
- `trained_models/`: Modelos entrenados guardados
- `training_data_improved.csv`: Dataset de entrenamiento
```

---

## 🔄 Control de Versiones

### Mensajes de Commit

```bash
# ✅ Correcto - Mensajes descriptivos
git commit -m "Agregar métricas R² en respuesta de API" \
  -m "- Almacenar puntuaciones R² para cada modelo durante entrenamiento
- Exponer model_confidence en endpoints /estimate/single y /models/stats
- Actualizar modelos Pydantic para incluir métricas de confiabilidad"

# ✅ Usar convención Conventional Commits
git commit -m "feat: agregar cálculo de R² en métricas"
git commit -m "fix: corregir normalización de features"
git commit -m "docs: actualizar arquitectura en ARQUITECTURA.md"

# ❌ Incorrecto - Mensajes vagos
git commit -m "fixes"
git commit -m "cambios varios"
git commit -m "actualizar código"
```

### Branching Strategy

```bash
# Usar GitFlow
main                    # Producción (releases)
├── develop            # Integración (features completadas)
│   ├── feature/agregar-r2-metrics
│   ├── bugfix/corregir-parsing-excel
│   └── hotfix/performance-lento

# Crear rama de feature
git checkout -b feature/nombre-descriptivo develop

# Completar feature
git checkout develop
git merge --no-ff feature/nombre-descriptivo
```

---

## 📊 Checklist de Calidad de Código

- [ ] Todo código tiene docstrings
- [ ] Excepciones específicas (no bare `except`)
- [ ] Validación de entrada en APIs
- [ ] Logging en niveles apropiados
- [ ] Variables con nombres descriptivos
- [ ] Máximo 100 caracteres por línea
- [ ] Importaciones ordenadas
- [ ] Sin código comentado innecesariamente
- [ ] Tests para funcionalidad crítica
- [ ] Sin secrets en código
- [ ] Type hints en Python
- [ ] Componentes React con prop-types o TypeScript
- [ ] Manejo de errores en try-catch
- [ ] CORS configurado restrictivamente
- [ ] Logging no expone información sensible

---

**Versión**: 1.0
**Última actualización**: Agosto 2026
