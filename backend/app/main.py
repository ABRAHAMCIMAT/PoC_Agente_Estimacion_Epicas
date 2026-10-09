"""
FastAPI backend for epic estimation.
Provides REST endpoints for:
- Model training
- Batch prediction from Excel
- Single story estimation
- Model statistics
"""

import os

# Import our custom modules
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.epic_estimation_models import EstimationModels
from utils.data_preprocessing import JiraDataPreprocessor, process_user_excel

# ============================================================================
# Request/Response Models
# ============================================================================

class StoryEstimationRequest(BaseModel):
    """Request for estimating a single story."""
    title: str
    description: str
    acceptance_criteria: Optional[List[str]] = None
    priority: Optional[str] = None
    issue_type: Optional[str] = None


class BatchEstimationRequest(BaseModel):
    """Request for batch estimation (used for Excel processing)."""
    stories: List[StoryEstimationRequest]


class EstimationResponse(BaseModel):
    """Response with estimation results."""
    story_title: str
    point_estimate: Dict[str, float]  # ensemble, random_forest, decision_tree
    time_estimate: Dict[str, float]
    cost_estimate: Dict[str, float]
    effort_estimate: Dict[str, float]
    semantic_estimate: Optional[Dict[str, float]] = None
    model_confidence: Optional[Dict[str, Dict[str, float]]] = None  # R² scores


class ModelStatsResponse(BaseModel):
    """Response with model statistics."""
    models_trained: bool
    targets: List[str]
    training_samples: Optional[int]
    features_count: Optional[int]
    model_location: str
    model_metrics: Optional[Dict[str, Dict[str, float]]] = None  # R² and other metrics


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Epic Estimation API",
    description="ML-based API for estimating story points, time, cost, and effort",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
estimation_models: Optional[EstimationModels] = None
jira_data_preprocessor: Optional[JiraDataPreprocessor] = None
training_in_progress = False

# Configuration
MODEL_DIR = Path(__file__).parent.parent / "trained_models"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_FILE = MODEL_DIR / "models.pkl"


# ============================================================================
# Startup and Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup."""
    global estimation_models

    print("Starting up Epic Estimation API...")

    # Try to load existing models
    if MODEL_FILE.exists():
        try:
            estimation_models = EstimationModels(str(MODEL_DIR))
            estimation_models.load(str(MODEL_FILE))
            print(f"[OK] Loaded existing models from {MODEL_FILE}")
        except Exception as e:
            print(f"[ERROR] Failed to load models: {e}")
            print("  Models will need to be trained before predictions can be made")
    else:
        print("[INFO] No trained models found")
        print("  Call POST /train endpoint with JIRA CSV to train models")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("Shutting down Epic Estimation API...")


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "models_loaded": estimation_models is not None and bool(estimation_models.rf_models),
        "timestamp": pd.Timestamp.now().isoformat()
    }


# ============================================================================
# Model Training Endpoints
# ============================================================================

@app.post("/train")
async def train_models(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Train models from CSV file.

    Required CSV columns at minimum:
    - Custom field (Story Points) [target variable]
    - Duracion_Sprint, Costo_por_dia, Esfuerzo_por_Puntos_Historia [optional]
    """
    global estimation_models, training_in_progress

    if training_in_progress:
        raise HTTPException(
            status_code=429,
            detail="Training already in progress"
        )

    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="File must be CSV format"
        )

    training_in_progress = True

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.csv',
            mode='wb'
        ) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # Train models
            print(f"Training models from {file.filename}...")

            # Read CSV and prepare data
            df = pd.read_csv(tmp_path, encoding='utf-8')
            df.columns = df.columns.str.strip()

            print(f"[INFO] Loaded {len(df)} rows with columns: {df.columns.tolist()}")

            # Required columns: target plus the text columns feature
            # extraction is based on
            required_col = 'Custom field (Story Points)'
            text_cols = ['Titulo', 'Historia de Usuario', 'Criterios de Aceptación']

            if required_col not in df.columns:
                raise ValueError(f"Missing required column: {required_col}")

            missing_text_cols = [c for c in text_cols if c not in df.columns]
            if missing_text_cols:
                raise ValueError(f"Missing required columns for feature extraction: {missing_text_cols}")

            # Drop rows with missing target
            df = df.dropna(subset=[required_col])

            if len(df) < 10:
                raise ValueError(f"Not enough data: {len(df)} rows after cleaning")

            # Build the same 10-feature linguistic vector used at prediction
            # time, so the trained scaler/models match what /estimate/* sends
            X_features = []
            for _, row in df.iterrows():
                criteria_raw = row.get('Criterios de Aceptación', '')
                criteria_list = []
                if pd.notna(criteria_raw) and isinstance(criteria_raw, str):
                    criteria_list = [c.strip() for c in criteria_raw.split('\n') if c.strip()]

                story_req = StoryEstimationRequest(
                    title=str(row.get('Titulo', '')),
                    description=str(row.get('Historia de Usuario', '')),
                    acceptance_criteria=criteria_list or None
                )
                X_features.append(create_feature_vector(story_req)[0])

            X = np.array(X_features, dtype=np.float32)

            # Prepare targets: use the real sprint/cost/effort columns when
            # available, falling back to synthetic values only if absent
            y_points = df[required_col].values.astype(np.float32)

            if 'Duracion_Sprint' in df.columns:
                y_time = df['Duracion_Sprint'].fillna(df['Duracion_Sprint'].median()).values.astype(np.float32)
            else:
                y_time = y_points * np.random.uniform(0.8, 1.2, len(y_points))

            if 'Costo_por_dia' in df.columns:
                y_cost = df['Costo_por_dia'].fillna(df['Costo_por_dia'].median()).values.astype(np.float32)
            else:
                y_cost = y_points * np.random.uniform(200, 400, len(y_points))

            if 'Esfuerzo_por_Puntos_Historia' in df.columns:
                y_effort = df['Esfuerzo_por_Puntos_Historia'].fillna(df['Esfuerzo_por_Puntos_Historia'].median()).values.astype(np.float32)
            else:
                y_effort = y_points * np.random.uniform(4, 16, len(y_points))

            y_dict = {
                'point': y_points,
                'time': y_time,
                'cost': y_cost,
                'effort': y_effort
            }

            # Create and train models
            estimation_models = EstimationModels(str(MODEL_DIR))
            estimation_models.train(X, y_dict)
            estimation_models.save(str(MODEL_FILE))

            print("[OK] Models trained successfully")

            return {
                "status": "success",
                "message": f"Models trained on {len(df)} samples",
                "models": list(estimation_models.rf_models.keys()),
                "model_file": str(MODEL_FILE)
            }

        finally:
            # Clean up temp file
            os.unlink(tmp_path)

    except Exception as e:
        print(f"Error during training: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Training failed: {str(e)}"
        )

    finally:
        training_in_progress = False


# ============================================================================
# Prediction Endpoints
# ============================================================================

@app.post("/estimate/single", response_model=EstimationResponse)
async def estimate_single_story(request: StoryEstimationRequest):
    """Estimate a single story."""
    if not estimation_models or not estimation_models.rf_models:
        raise HTTPException(
            status_code=503,
            detail="Models not trained. Call POST /train first."
        )

    try:
        # Create feature vector from story
        # This is a simplified version; in production, you'd encode all features
        features = create_feature_vector(request)

        # Make predictions
        point_pred = estimation_models.predict(features, 'point')
        time_pred = estimation_models.predict(features, 'time')
        cost_pred = estimation_models.predict(features, 'cost')
        effort_pred = estimation_models.predict(features, 'effort')

        # Try semantic estimation if corpus available
        semantic = None
        if estimation_models.embeddings is not None:
            try:
                text = f"{request.title}\n{request.description}"
                semantic = estimation_models.estimate_by_similarity(text)
            except Exception:
                pass

        # Get model confidence metrics (R² scores)
        model_confidence = None
        if hasattr(estimation_models, 'model_metrics') and estimation_models.model_metrics:
            model_confidence = {
                'point': estimation_models.model_metrics.get('point', {}),
                'time': estimation_models.model_metrics.get('time', {}),
                'cost': estimation_models.model_metrics.get('cost', {}),
                'effort': estimation_models.model_metrics.get('effort', {})
            }

        # Format response
        return EstimationResponse(
            story_title=request.title,
            point_estimate={
                'ensemble': float(point_pred['ensemble'][0]),
                'random_forest': float(point_pred['random_forest'][0]),
                'decision_tree': float(point_pred['decision_tree'][0])
            },
            time_estimate={
                'ensemble': float(time_pred['ensemble'][0]),
                'random_forest': float(time_pred['random_forest'][0]),
                'decision_tree': float(time_pred['decision_tree'][0])
            },
            cost_estimate={
                'ensemble': float(cost_pred['ensemble'][0]),
                'random_forest': float(cost_pred['random_forest'][0]),
                'decision_tree': float(cost_pred['decision_tree'][0])
            },
            effort_estimate={
                'ensemble': float(effort_pred['ensemble'][0]),
                'random_forest': float(effort_pred['random_forest'][0]),
                'decision_tree': float(effort_pred['decision_tree'][0])
            },
            semantic_estimate=semantic,
            model_confidence=model_confidence
        )

    except Exception as e:
        print(f"Error in estimation: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Estimation failed: {str(e)}"
        )


@app.post("/estimate/batch")
async def estimate_batch(request: BatchEstimationRequest):
    """Estimate multiple stories."""
    if not estimation_models or not estimation_models.rf_models:
        raise HTTPException(
            status_code=503,
            detail="Models not trained. Call POST /train first."
        )

    results = []
    errors = []

    for story in request.stories:
        try:
            result = await estimate_single_story(story)
            results.append(result)
        except Exception as e:
            errors.append({
                "story": story.title,
                "error": str(e)
            })

    return {
        "total": len(request.stories),
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors if errors else None
    }


@app.post("/estimate/excel")
async def estimate_from_excel(file: UploadFile = File(...)):
    """
    Upload Excel file with stories and get estimations.

    Expected columns: Titulo, Historia de Usuario, Criterios de Aceptación
    """
    if not estimation_models or not estimation_models.rf_models:
        raise HTTPException(
            status_code=503,
            detail="Models not trained. Call POST /train first."
        )

    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="File must be Excel format (.xlsx or .xls)"
        )

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.xlsx',
            mode='wb'
        ) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # Read Excel
            df = process_user_excel(tmp_path)

            # Convert to estimation requests
            requests = []
            for _, row in df.iterrows():
                criteria = row.get('Criterios de Aceptación', '')
                criteria_list = []
                if pd.notna(criteria):
                    if isinstance(criteria, str):
                        criteria_list = [c.strip() for c in criteria.split('\n') if c.strip()]
                    elif isinstance(criteria, list):
                        criteria_list = criteria

                requests.append(StoryEstimationRequest(
                    title=str(row.get('Titulo', 'Unknown')),
                    description=str(row.get('Historia de Usuario', '')),
                    acceptance_criteria=criteria_list if criteria_list else None
                ))

            # Get estimations
            batch_request = BatchEstimationRequest(stories=requests)
            result = await estimate_batch(batch_request)

            # Add Excel export capability
            result['export_url'] = '/estimate/excel/results'

            return result

        finally:
            os.unlink(tmp_path)

    except Exception as e:
        print(f"Error processing Excel: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Excel processing failed: {str(e)}"
        )


# ============================================================================
# Model Info Endpoints
# ============================================================================

@app.get("/models/stats", response_model=ModelStatsResponse)
async def get_model_stats():
    """Get statistics about trained models."""
    return ModelStatsResponse(
        models_trained=bool(estimation_models and estimation_models.rf_models),
        targets=list(estimation_models.rf_models.keys()) if estimation_models else [],
        training_samples=None,  # Would need to track during training
        features_count=len(estimation_models.features_columns) if estimation_models and estimation_models.features_columns else None,
        model_location=str(MODEL_FILE),
        model_metrics=estimation_models.model_metrics if estimation_models else None
    )


# ============================================================================
# Utility Functions
# ============================================================================

def create_feature_vector(request: StoryEstimationRequest) -> np.ndarray:
    """
    Create rich feature vector from story request.
    Extracts features from title, description, and criteria.
    """
    import re

    # Initialize 10-feature vector
    features = np.zeros((1, 10), dtype=np.float32)

    title = request.title or ''
    description = request.description or ''
    criteria = ' '.join(request.acceptance_criteria or [])
    full_text = f"{title} {description} {criteria}".lower()

    # Feature 0: Story complexity from title keywords
    complexity_keywords = ['complex', 'difícil', 'difícil', 'integración', 'integration',
                          'refactor', 'refactorización', 'arquitectura', 'architecture',
                          'seguridad', 'security', 'performance', 'database', 'api']
    complexity_score = sum(1 for kw in complexity_keywords if kw in full_text)
    features[0, 0] = min(complexity_score / 5.0, 1.0)

    # Feature 1: Story scope (text length normalized)
    text_length = len(description)
    features[0, 1] = min(text_length / 500.0, 1.0)

    # Feature 2: Number of acceptance criteria (indicates scope)
    criteria_count = len(request.acceptance_criteria or [])
    features[0, 2] = min(criteria_count / 5.0, 1.0)

    # Feature 3: Technical keywords (UI vs Backend vs Integration)
    tech_keywords = ['api', 'base de datos', 'database', 'backend', 'servidor',
                    'ui', 'frontend', 'interfaz', 'pantalla', 'screen', 'form',
                    'autenticación', 'authentication', 'cache', 'performance']
    tech_score = sum(1 for kw in tech_keywords if kw in full_text)
    features[0, 3] = min(tech_score / 4.0, 1.0)

    # Feature 4: Data/Integration keywords
    data_keywords = ['integración', 'integration', 'migración', 'migration', 'export',
                    'import', 'sync', 'sincronización', 'datos', 'data', 'csv', 'excel',
                    'api', 'rest', 'soap', 'webhook']
    data_score = sum(1 for kw in data_keywords if kw in full_text)
    features[0, 4] = min(data_score / 3.0, 1.0)

    # Feature 5: Testing requirements
    testing_keywords = ['test', 'prueba', 'unitario', 'unit', 'integration',
                       'validar', 'validación', 'verificar', 'qa']
    testing_score = sum(1 for kw in testing_keywords if kw in full_text)
    features[0, 5] = min(testing_score / 3.0, 1.0)

    # Feature 6: Priority encoding (from title hints)
    priority_keywords = {
        'urgent': 1.0, 'crítico': 1.0, 'critical': 1.0,
        'alta': 0.8, 'high': 0.8, 'importante': 0.8,
        'media': 0.5, 'medium': 0.5, 'normal': 0.5,
        'baja': 0.2, 'low': 0.2, 'menor': 0.2
    }
    priority_score = 0.5
    for kw, score in priority_keywords.items():
        if kw in full_text:
            priority_score = score
            break
    features[0, 6] = priority_score

    # Feature 7: Issue type hints
    type_keywords = {
        'feature': 0.8, 'característica': 0.8, 'nueva': 0.8,
        'bug': 0.4, 'error': 0.4, 'corrección': 0.4,
        'tarea': 0.3, 'task': 0.3, 'refactor': 0.6
    }
    type_score = 0.5
    for kw, score in type_keywords.items():
        if kw in full_text:
            type_score = score
            break
    features[0, 7] = type_score

    # Feature 8: Number words (estimation hints)
    numbers = re.findall(r'\d+', description)
    features[0, 8] = min(len(numbers) / 3.0, 1.0)

    # Feature 9: Unique word variety (simpler = more straightforward)
    words = description.split()
    if words:
        unique_ratio = len(set(words)) / max(len(words), 1)
        features[0, 9] = unique_ratio
    else:
        features[0, 9] = 0.5

    return features


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
