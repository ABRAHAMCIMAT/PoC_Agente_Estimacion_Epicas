#!/usr/bin/env python3
import sys
import os

os.chdir('backend')
sys.path.insert(0, '.')

from models.epic_estimation_models import EstimationModels
from app.main import create_feature_vector
from pydantic import BaseModel
import pandas as pd
import numpy as np

print('[INFO] Reentrenando modelo con metricas R2...')
df = pd.read_csv('training_data_improved.csv', encoding='utf-8')

class StoryReq(BaseModel):
    title: str
    description: str
    acceptance_criteria: list = None
    priority: str = None
    issue_type: str = None

X_features = []
for idx, row in df.iterrows():
    criteria_col = 'Criterios de Aceptación'
    criteria_list = str(row[criteria_col]).split('\n') if row[criteria_col] else []
    story_req = StoryReq(
        title=str(row['Titulo']),
        description=str(row['Historia de Usuario']),
        acceptance_criteria=criteria_list
    )
    features = create_feature_vector(story_req)
    X_features.append(features[0])

X = np.array(X_features, dtype=np.float32)

y_dict = {
    'point': df['Custom field (Story Points)'].values.astype(np.float32),
    'time': df['Duracion_Sprint'].values.astype(np.float32),
    'cost': df['Costo_por_dia'].values.astype(np.float32),
    'effort': df['Esfuerzo_por_Puntos_Historia'].values.astype(np.float32)
}

models = EstimationModels('trained_models')
models.train(X, y_dict)
models.save('trained_models/models.pkl')

print('[OK] Modelo reentrenado con metricas R2 guardadas')
print('')
print('Metricas del modelo:')
for target, metrics in models.model_metrics.items():
    print('  ' + target.upper() + ':')
    print('    - Ensemble R2: {:.4f}'.format(metrics.get('ensemble', 0)))
    print('    - Random Forest R2: {:.4f}'.format(metrics.get('random_forest', 0)))
    print('    - Decision Tree R2: {:.4f}'.format(metrics.get('decision_tree', 0)))
