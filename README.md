# Epic Estimation System

A full-stack AI-powered system for estimating epic complexity using machine learning models trained on historical JIRA data.

## Features

- 🤖 **ML-Based Estimation**: Uses ensemble of Random Forest and Decision Tree models
- 📊 **Multi-Target Predictions**: Estimates story points, time, cost, and effort
- 📁 **Excel Upload**: Batch process stories from Excel files
- 🔍 **Semantic Similarity**: Finds similar historical stories for comparison
- 🎯 **REST API**: FastAPI backend for seamless integration
- 💻 **Modern Frontend**: Next.js + React web interface

## Architecture

```
epic-estimation-system/
├── backend/                 # FastAPI application
│   ├── app/
│   │   └── main.py         # FastAPI server with endpoints
│   ├── models/
│   │   └── epic_estimation_models.py   # ML model classes
│   ├── utils/
│   │   └── data_preprocessing.py       # Data preprocessing
│   ├── trained_models/     # Saved model artifacts (after training)
│   └── requirements.txt
│
└── frontend/               # Next.js React application
    ├── pages/
    │   ├── index.jsx       # Main page
    │   ├── _app.jsx        # App wrapper
    └── components/
        ├── Header.jsx
        ├── ExcelUpload.jsx
        └── EstimationResults.jsx
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- JIRA data export (CSV format) with the following columns:
  - `Custom field (Story Points)` - Historical story points
  - `Duracion_Sprint` - Sprint duration in days
  - `Costo_por_dia` - Daily cost
  - `Esfuerzo_por_Puntos_Historia` - Effort per story point

## Installation & Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local if needed
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

## Training the Models

### Step 1: Prepare JIRA Data

Export your JIRA data as CSV with the required columns. Place it in the root directory or anywhere accessible.

### Step 2: Train Models

You can train models through the API:

```bash
# Start the backend
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# In another terminal, train the models
curl -F "file=@path/to/Jira.csv" http://localhost:8000/train
```

Or use Python directly:

```python
from backend.models.epic_estimation_models import create_and_train_models

models = create_and_train_models(
    csv_path='Jira.csv',
    model_dir='backend/trained_models'
)
```

## Running the System Locally

### 1. Start the Backend Server

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### 2. Start the Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:3000`

### 3. Use the System

1. Open `http://localhost:3000` in your browser
2. Prepare an Excel file with columns:
   - **Titulo** - Story title
   - **Historia de Usuario** - Story description  
   - **Criterios de Aceptación** - Acceptance criteria (one per line or single cell)
3. Upload the file
4. View detailed estimations with model comparison

## API Endpoints

### Health Check
```
GET /health
```

### Train Models
```
POST /train
Content-Type: multipart/form-data

file: <JIRA_CSV_FILE>
```

### Estimate Single Story
```
POST /estimate/single
Content-Type: application/json

{
  "title": "Story title",
  "description": "Story description",
  "acceptance_criteria": ["Criterion 1", "Criterion 2"],
  "priority": "High",
  "issue_type": "Story"
}
```

### Estimate from Excel
```
POST /estimate/excel
Content-Type: multipart/form-data

file: <EXCEL_FILE>
```

### Get Model Statistics
```
GET /models/stats
```

## Excel File Format

Required columns in Excel:
- **Titulo** (Text) - Story title
- **Historia de Usuario** (Text) - Full story description
- **Criterios de Aceptación** (Text) - Acceptance criteria (newline separated)

Example:
| Titulo | Historia de Usuario | Criterios de Aceptación |
|--------|---------------------|------------------------|
| Login Feature | As a user, I want to log in securely | - Validates email<br>- Encrypts password<br>- Sends confirmation |
| API Integration | As a developer, I need REST APIs | - GET /users implemented<br>- POST /users implemented |

## Model Details

### Models Used
1. **RandomForestRegressor** - Good for complex relationships
   - max_depth: 70
   - n_estimators: 200
   - Features: log2 of total features

2. **DecisionTreeRegressor** - Fast interpretable predictions
   - max_depth: 30 (for story points), 20 (for others)
   - min_samples_leaf: 2
   - min_samples_split: 10

3. **Ensemble** - Average of RF and DT predictions

### Training Data Requirements
- Minimum 50 historical stories recommended
- Should include stories of varying complexity
- All required columns should be populated

## Troubleshooting

### Backend won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check port 8000 is not in use
- Review logs for specific errors

### Frontend won't connect to backend
- Verify backend is running at `http://localhost:8000`
- Check CORS is enabled in FastAPI app
- Review browser console for network errors

### Models not trained
- Ensure JIRA CSV has all required columns
- Check file encoding is UTF-8
- Verify CSV data quality (no all-null columns)

### Estimation fails
- Ensure models have been trained first
- Check Excel file format matches requirements
- Review API logs for specific errors

## Development

### Adding New Features

1. **Backend**: Modify `backend/app/main.py` or create new modules in `backend/utils/`
2. **Frontend**: Add new components in `frontend/components/`
3. **Models**: Extend `backend/models/epic_estimation_models.py`

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Performance Tips

1. **Model Training**: Faster with more CPU cores. Consider using n_jobs=-1
2. **Predictions**: Batch processing is more efficient than single predictions
3. **Embeddings**: Disabled by default. Enable for semantic similarity (slower, more accurate)

## API Response Format

```json
{
  "story_title": "Story Title",
  "point_estimate": {
    "ensemble": 5.0,
    "random_forest": 5.2,
    "decision_tree": 4.8
  },
  "time_estimate": {
    "ensemble": 3.5,
    "random_forest": 3.8,
    "decision_tree": 3.2
  },
  "cost_estimate": {
    "ensemble": 1200,
    "random_forest": 1250,
    "decision_tree": 1150
  },
  "effort_estimate": {
    "ensemble": 250,
    "random_forest": 260,
    "decision_tree": 240
  },
  "semantic_estimate": {
    "p50": 5.0,
    "p85": 8.0,
    "fib": 5,
    "top_sim": 0.92,
    "top_points": 5
  }
}
```

## Configuration

### Backend Configuration

Edit `backend/app/main.py`:
- `MODEL_DIR` - Directory to save trained models
- `CORS` settings for API access

### Frontend Configuration

Edit `frontend/next.config.js`:
- `NEXT_PUBLIC_API_URL` - Backend API endpoint
- Port and host settings

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of the PoC_Agente_Estimacion_Epicas research.

## Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review API logs
3. Check browser console for client-side errors
4. Open an issue with error details and reproduction steps
