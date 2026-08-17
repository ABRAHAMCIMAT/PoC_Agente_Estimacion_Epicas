# Sistema de Estimación de Épicas - EJECUTADO LOCALMENTE

## ✓ Estado: FUNCIONANDO COMPLETAMENTE

### Backend (FastAPI) - Puerto 8000
- ✓ Servidor en ejecución
- ✓ Modelos ML entrenados
- ✓ Endpoints operativos:
  - `/health` - Verificación de estado
  - `/train` - Entrenamiento de modelos con CSV
  - `/estimate/single` - Estimación individual
  - `/estimate/excel` - Estimación desde Excel
  - `/estimate/batch` - Estimación por lotes
  - `/models/stats` - Estadísticas de modelos

### Frontend (Next.js) - Puerto 3000
- ✓ Servidor en ejecución
- ✓ Interfaz web activa
- ✓ Funcionalidades:
  - Drag & Drop de archivos Excel
  - Procesamiento de historias de usuario
  - Visualización de predicciones
  - Exportación a CSV

### Modelos Entrenados
- ✓ Puntos de Historia (ensemble RF+DT)
- ✓ Duración de Sprints (días)
- ✓ Costo estimado ($)
- ✓ Esfuerzo requerido

### Predicciones Realizadas
- 5 historias de usuario estimadas exitosamente
- Comparación de modelos: Ensemble vs RandomForest vs DecisionTree
- Resultados almacenados en JSON

## Cómo Usar

1. **Abre el navegador:**
   ```
   http://localhost:3000
   ```

2. **Prepara un archivo Excel** con columnas:
   - Titulo
   - Historia de Usuario  
   - Criterios de Aceptación

3. **Sube el archivo:**
   - Arrastra el archivo al área de drop
   - O haz clic para seleccionar

4. **Visualiza los resultados:**
   - Puntos estimados (ensemble)
   - Duración en días
   - Costo estimado
   - Esfuerzo requerido

5. **Descarga los resultados:**
   - Botón "Export to CSV"
   - Formato: story, points, days, cost, effort

## Archivos de Prueba Disponibles

- `HU_test.xlsx` - 5 historias de ejemplo para probar
- `training_data.csv` - Datos usados para entrenar los modelos
- `predictions_result.json` - Últimas predicciones generadas

## API Documentation

Accede a la documentación interactiva (Swagger):
```
http://localhost:8000/docs
```

## Tecnología

**Backend:**
- FastAPI 0.104.1
- Uvicorn 0.24.0
- scikit-learn 1.3.2 (ML models)
- pandas 2.1.3 (Data processing)

**Frontend:**
- Next.js 14.0.0
- React 18.2.0
- axios (HTTP client)

**ML Models:**
- RandomForest Regressor (200 árboles, depth=70)
- Decision Tree Regressor (depth=20-30)
- Ensemble (promedio RF + DT)
- StandardScaler para normalización

## Características del Sistema

✓ Entrenamiento de modelos desde CSV JIRA
✓ Predicción de 4 targets independientes
✓ Comparación de modelos (ensemble vs individual)
✓ Interfaz web moderna y responsiva
✓ Soporte para archivos Excel
✓ Exportación de resultados
✓ API REST completa
✓ Documentación automática (Swagger)

## Notas Técnicas

- Sin dependencias de PyTorch/Transformers (simplificado para Windows)
- Features: Priority, IssueType, DescriptionLength (normalizados)
- Tamaño de feature vector: 3 dimensiones
- Escalado de features: StandardScaler
- Validación: 80/20 train/test split

## Próximos Pasos

Para producción:
1. Entrenar con datos JIRA reales (archivo CSV)
2. Ajustar hiperparámetros según distribución de datos
3. Implementar autenticación
4. Agregar logging y monitoreo
5. Dockerizar para despliegue
6. Agregar más features (historiales, patrones)

---
**Sistema completamente operativo desde 2026-08-17**
