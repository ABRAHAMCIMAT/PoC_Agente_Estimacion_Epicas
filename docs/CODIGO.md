# Documentación del Código Fuente

## 📋 Tabla de Contenidos

1. [Backend Python](#backend-python)
   - [main.py](#mainpy)
   - [epic_estimation_models.py](#epic_estimation_modelspy)
   - [data_preprocessing.py](#data_preprocessingpy)

2. [Frontend JavaScript](#frontend-javascript)
   - [pages/index.jsx](#pagesindexjsx)
   - [components/EstimationResults.jsx](#componentsestimationresultsjsx)

3. [Patrones de Codificación](#patrones-de-codificación)

---

## 🐍 Backend Python

### main.py

Servidor principal FastAPI con todos los endpoints de la API.

#### Estructura General

```python
# 1. Imports
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np

# 2. Modelos Pydantic (esquemas de validación)
class SolicitudEstimacionHistoria(BaseModel):
    title: str
    description: str
    acceptance_criteria: Optional[List[str]] = None
    priority: Optional[str] = None
    issue_type: Optional[str] = None

# 3. Configuración de FastAPI
app = FastAPI(title="API de Estimación de Épicas")
app.add_middleware(CORSMiddleware, ...)

# 4. Variables globales
estimation_models = None

# 5. Función de startup
@app.on_event("startup")
async def startup():
    global estimation_models
    estimation_models = EstimationModels()

# 6. Endpoints
@app.post("/train")
async def train(file: UploadFile = File(...)):
    pass

# 7. Funciones utilitarias
def crear_vector_features(request):
    pass
```

#### Funciones Clave

##### `crear_vector_features(request: SolicitudEstimacionHistoria) -> np.ndarray`

Convierte una solicitud de historia en un vector de 10 características.

**Parámetros:**
- `request`: Objeto con título, descripción, criterios, prioridad, tipo

**Retorna:**
- `np.ndarray`: Vector de shape (1, 10) con características normalizadas

**Características extraídas:**
1. **Puntuación de complejidad**: Conta palabras clave como "complejo", "integración", "refactor"
2. **Puntuación de alcance**: Detecta indicadores de alcance múltiple
3. **Cantidad de criterios**: Cuenta líneas en acceptance_criteria
4. **Palabras técnicas**: Detecta términos como "API", "base de datos", "autenticación"
5. **Indicadores de integración**: Busca palabras como "integrar", "conectar", "sincronizar"
6. **Requisitos de testing**: Cuenta palabras como "test", "prueba", "validar"
7. **Prioridad codificada**: Convierte string a valor 0-1
8. **Tipo codificado**: Convierte tipo de issue a valor 0-1
9. **Cantidad de números**: Cuenta dígitos en descripción
10. **Variedad léxica**: Calcula unique_words / total_words

**Implementación:**
```python
def crear_vector_features(request):
    # Combina texto
    texto_completo = f"{request.title} {request.description}"
    if request.acceptance_criteria:
        texto_completo += " " + " ".join(request.acceptance_criteria)
    
    texto_lower = texto_completo.lower()
    
    # Extrae 10 features
    features = []
    
    # Feature 1: Complejidad
    palabras_complejidad = ["complejo", "difícil", "integración", "refactor"]
    features.append(sum(1 for p in palabras_complejidad if p in texto_lower))
    
    # Feature 2: Alcance
    palabras_alcance = ["múltiple", "varios", "diferentes", "diversos"]
    features.append(sum(1 for p in palabras_alcance if p in texto_lower))
    
    # ... más features ...
    
    # Normaliza con StandardScaler
    features_array = np.array([features])
    features_normalizados = scaler.transform(features_array)
    
    return features_normalizados
```

##### `@app.post("/train")`

Punto de entrada para entrenar modelos.

```python
@app.post("/train")
async def entrenar(archivo: UploadFile = File(...)):
    """
    Entrena o reemplaza modelos de estimación.
    
    Parámetros:
        archivo: Archivo CSV con históricas
    
    Retorna:
        dict: Información de entrenamiento y métricas
    
    Levanta:
        HTTPException: Si el archivo es inválido
    """
    try:
        # 1. Validar archivo
        if not archivo.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Solo se aceptan archivos CSV")
        
        # 2. Leer archivo
        contenido = await archivo.read()
        df = pd.read_csv(BytesIO(contenido), encoding='utf-8')
        
        # 3. Procesar datos
        features, targets = procesar_datos(df)
        
        # 4. Entrenar modelos
        modelos = EstimationModels()
        modelos.entrenar(features, targets)
        
        # 5. Guardar modelos
        modelos.guardar()
        
        return {"estado": "entrenado", "métricas": modelos.model_metrics}
    
    except Exception as e:
        logging.error(f"Error en entrenamiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

### epic_estimation_models.py

Motor de Machine Learning que gestiona el entrenamiento y predicción.

#### Clase EstimationModels

```python
class EstimationModels:
    """
    Gestor de modelos de estimación ensemble.
    
    Atributos:
        rf_models (dict): Modelos Random Forest por target
        dt_models (dict): Modelos Árbol Decisión por target
        scalers (dict): Normalizadores por target
        model_metrics (dict): Puntuaciones R² de validación
    """
    
    def __init__(self, path: str = 'trained_models'):
        self.ruta = path
        self.rf_models = {}
        self.dt_models = {}
        self.scalers = {}
        self.model_metrics = {}
    
    def entrenar(self, X: np.ndarray, y_dict: dict):
        """
        Entrena todos los modelos.
        
        Parámetros:
            X: Array de features (n_samples, 10)
            y_dict: Dict con arrays de targets
                {'puntos': [...], 'tiempo': [...], ...}
        """
        # Split datos
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Entrenar para cada target
        for target_name, y_values in y_dict.items():
            # Normalizar
            scaler = StandardScaler()
            X_train_norm = scaler.fit_transform(X_train)
            X_val_norm = scaler.transform(X_val)
            
            # Entrenar Random Forest
            rf = RandomForestRegressor(n_estimators=100, max_depth=15)
            rf.fit(X_train_norm, y_train[target_name])
            
            # Entrenar Árbol Decisión
            dt = DecisionTreeRegressor(max_depth=10)
            dt.fit(X_train_norm, y_train[target_name])
            
            # Almacenar
            self.rf_models[target_name] = rf
            self.dt_models[target_name] = dt
            self.scalers[target_name] = scaler
            
            # Calcular R²
            y_pred_rf = rf.predict(X_val_norm)
            y_pred_dt = dt.predict(X_val_norm)
            y_pred_ensemble = (y_pred_rf * 0.7 + y_pred_dt * 0.3)
            
            self.model_metrics[target_name] = {
                'random_forest': r2_score(y_val[target_name], y_pred_rf),
                'decision_tree': r2_score(y_val[target_name], y_pred_dt),
                'ensemble': r2_score(y_val[target_name], y_pred_ensemble)
            }
    
    def predecir(self, features: np.ndarray, target: str) -> dict:
        """
        Realiza predicción para un target específico.
        
        Parámetros:
            features: Vector de features (1, 10)
            target: Nombre del target ('puntos', 'tiempo', etc)
        
        Retorna:
            dict: Predicciones de cada modelo
        """
        # Normalizar
        X_norm = self.scalers[target].transform(features)
        
        # Predecir con cada modelo
        pred_rf = self.rf_models[target].predict(X_norm)[0]
        pred_dt = self.dt_models[target].predict(X_norm)[0]
        
        # Ensemble
        pred_ensemble = (pred_rf * 0.7 + pred_dt * 0.3)
        
        return {
            'ensemble': pred_ensemble,
            'random_forest': pred_rf,
            'decision_tree': pred_dt
        }
    
    def guardar(self, ruta: str = None):
        """Guarda modelos entrenados a disco."""
        import pickle
        
        ruta = ruta or self.ruta
        os.makedirs(ruta, exist_ok=True)
        
        datos = {
            'rf_models': self.rf_models,
            'dt_models': self.dt_models,
            'scalers': self.scalers,
            'model_metrics': self.model_metrics,
            'features_columns': self.features_columns
        }
        
        with open(os.path.join(ruta, 'models.pkl'), 'wb') as f:
            pickle.dump(datos, f)
    
    def cargar(self, ruta: str = None):
        """Carga modelos desde disco."""
        import pickle
        
        ruta = ruta or self.ruta
        
        with open(os.path.join(ruta, 'models.pkl'), 'rb') as f:
            datos = pickle.load(f)
        
        self.rf_models = datos['rf_models']
        self.dt_models = datos['dt_models']
        self.scalers = datos['scalers']
        self.model_metrics = datos['model_metrics']
        self.features_columns = datos.get('features_columns', [])
```

---

### data_preprocessing.py

Procesamiento de datos de entrada (Excel, CSV).

#### Clase PreprocessadorDatosJira

```python
class PreprocessadorDatosJira:
    """
    Preprocesa datos de historias de usuario.
    """
    
    @staticmethod
    def procesar_excel_usuario(ruta_archivo):
        """
        Lee archivo Excel y lo convierte en lista de solicitudes.
        
        Parámetros:
            ruta_archivo: Path al archivo .xlsx
        
        Retorna:
            list: Lista de SolicitudEstimacionHistoria
        """
        df = pd.read_excel(ruta_archivo)
        
        historias = []
        for _, fila in df.iterrows():
            historia = SolicitudEstimacionHistoria(
                title=str(fila.get('Titulo', '')),
                description=str(fila.get('Historia de Usuario', '')),
                acceptance_criteria=str(fila.get('Criterios de Aceptación', '')).split('\n')
            )
            historias.append(historia)
        
        return historias
    
    @staticmethod
    def validar_formato(df):
        """Valida que el DataFrame tenga las columnas requeridas."""
        columnas_requeridas = ['Titulo', 'Historia de Usuario']
        
        for col in columnas_requeridas:
            if col not in df.columns:
                raise ValueError(f"Falta columna requerida: {col}")
        
        return True
```

---

## 🔵 Frontend JavaScript

### pages/index.jsx

Página principal de la aplicación React/Next.js.

#### Estructura

```jsx
import React, { useState } from 'react';
import Header from '../components/Header';
import ExcelUpload from '../components/ExcelUpload';
import EstimationResults from '../components/EstimationResults';

export default function Home() {
  const [resultados, setResultados] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);
  
  return (
    <div className="contenedor">
      <Header />
      <ExcelUpload 
        onCargaCompleta={manejarCargaCompleta}
        cargando={cargando}
      />
      {error && <div className="error">{error}</div>}
      {resultados && <EstimationResults results={resultados} />}
    </div>
  );
}

async function manejarCargaCompleta(archivo) {
  try {
    const formData = new FormData();
    formData.append('file', archivo);
    
    const response = await fetch('http://localhost:8000/estimate/batch', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) throw new Error('Error en servidor');
    
    const datos = await response.json();
    setResultados(datos);
  } catch (err) {
    setError(err.message);
  }
}
```

---

### components/EstimationResults.jsx

Componente que renderiza resultados de estimaciones.

#### Función Principal

```jsx
function ProgressBar({ valor, maximo, color = '#3b82f6' }) {
  const porcentaje = (valor / maximo) * 100;
  return (
    <div className="contenedor-barra-progreso">
      <div 
        className="relleno-barra-progreso" 
        style={{ width: `${porcentaje}%`, backgroundColor: color }}
      />
      <div className="valor-barra-progreso">{valor.toFixed(1)}</div>
    </div>
  );
}

export default function ResultadosEstimación({ resultados }) {
  const [historiaExpandida, setHistoriaExpandida] = useState(null);
  
  const obtenerValoresMaximos = () => {
    if (!resultados?.resultados?.length) return {};
    return {
      puntos: Math.max(...resultados.resultados.map(r => r.point_estimate.ensemble)),
      tiempo: Math.max(...resultados.resultados.map(r => r.time_estimate.ensemble)),
      costo: Math.max(...resultados.resultados.map(r => r.cost_estimate.ensemble)),
      esfuerzo: Math.max(...resultados.resultados.map(r => r.effort_estimate.ensemble))
    };
  };
  
  const obtenerClaseConfianza = (r2) => {
    if (r2 >= 0.8) return 'confianza-alta';
    if (r2 >= 0.6) return 'confianza-media';
    return 'confianza-baja';
  };
  
  return (
    <div className="contenedor-resultados">
      <table className="tabla-resumen">
        {/* Encabezados y filas */}
      </table>
      
      {/* Sección de detalles expandibles */}
      {resultados.resultados.map((historia, idx) => (
        historiaExpandida === idx && (
          <div key={`detalle-${idx}`} className="detalles-historia-expandida">
            {/* Tabla de comparación con R² */}
            <table className="tabla-comparacion">
              <tbody>
                <tr>
                  <td>Puntos de Historia</td>
                  <td>{historia.point_estimate.ensemble.toFixed(2)}</td>
                  {/* ... más celdas ... */}
                </tr>
                <tr className="fila-confianza">
                  <td className="etiqueta-confianza">Confiabilidad (R²)</td>
                  <td>
                    <span className={`insignia-confianza ${obtenerClaseConfianza(...)}`}>
                      {(...* 100).toFixed(1)}%
                    </span>
                    <span className="valor-r2">
                      (R²: {....toFixed(4)})
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        )
      ))}
    </div>
  );
}
```

---

## 🛠️ Patrones de Codificación

### 1. Manejo de Errores

**Patrón en Backend:**
```python
try:
    resultado = operación_riesgosa()
except ValueError as e:
    logging.warning(f"Valor inválido: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logging.error(f"Error inesperado: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Error interno")
```

**Patrón en Frontend:**
```javascript
try {
  const resultado = await fetch(url);
  if (!resultado.ok) {
    const error = await resultado.json();
    throw new Error(error.detail || "Error desconocido");
  }
  return await resultado.json();
} catch (error) {
  console.error('Error en petición:', error);
  mostrarNotificaciónError(error.message);
  throw error;
}
```

### 2. Validación de Entrada

**Uso de Pydantic:**
```python
class MiModelo(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    edad: int = Field(..., ge=0, le=150)
    email: EmailStr  # Validación automática de email
    
    class Config:
        schema_extra = {
            "example": {
                "nombre": "Juan",
                "edad": 30,
                "email": "juan@example.com"
            }
        }
```

### 3. Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Información de depuración")
logger.info("Operación completada exitosamente")
logger.warning("Posible problema identificado")
logger.error("Error grave", exc_info=True)
```

### 4. Documentación de Funciones

```python
def crear_vector_features(request: SolicitudEstimacionHistoria) -> np.ndarray:
    """
    Crea un vector de características a partir de una solicitud.
    
    Extrae 10 características lingüísticas del título, descripción
    y criterios de aceptación de una historia de usuario.
    
    Args:
        request: Objeto con datos de la historia
        
    Returns:
        Array normalizado de shape (1, 10) con características
        
    Raises:
        ValueError: Si los datos de entrada son inválidos
        
    Example:
        >>> request = SolicitudEstimacionHistoria(
        ...     title="Implementar login",
        ...     description="Sistema de autenticación..."
        ... )
        >>> features = crear_vector_features(request)
        >>> print(features.shape)
        (1, 10)
    """
    pass
```

### 5. Tipos y Type Hints

```python
from typing import Dict, List, Optional, Tuple
import numpy as np

def procesar_lote(
    historias: List[SolicitudEstimacionHistoria],
    modelos: Optional[EstimationModels] = None
) -> Tuple[List[dict], List[str]]:
    """
    Procesa un lote de historias.
    
    Returns:
        Tupla con (resultados, errores)
    """
    pass
```

---

## 📚 Recursos Adicionales

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Documentación React](https://react.dev/)
- [Scikit-learn Documentación](https://scikit-learn.org/)
- [Pandas Documentación](https://pandas.pydata.org/)

---

**Versión**: 1.0
**Última actualización**: Agosto 2026
