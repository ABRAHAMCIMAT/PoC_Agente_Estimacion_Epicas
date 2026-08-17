import React, { useState } from 'react';

export default function EstimationResults({ results }) {
  const [expandedStory, setExpandedStory] = useState(null);

  const toggleExpand = (index) => {
    setExpandedStory(expandedStory === index ? null : index);
  };

  const exportToCSV = () => {
    if (!results?.results?.length) return;

    const headers = [
      'Título de Historia',
      'Puntos (Ensemble)',
      'Días (Ensemble)',
      'Costo (Ensemble)',
      'Esfuerzo (Ensemble)',
      'Puntos (RF)',
      'Puntos (DT)',
      'Días (RF)',
      'Días (DT)',
      'Costo (RF)',
      'Costo (DT)',
      'Esfuerzo (RF)',
      'Esfuerzo (DT)'
    ];

    const rows = results.results.map(r => [
      r.story_title,
      r.point_estimate.ensemble.toFixed(2),
      r.time_estimate.ensemble.toFixed(2),
      r.cost_estimate.ensemble.toFixed(2),
      r.effort_estimate.ensemble.toFixed(2),
      r.point_estimate.random_forest.toFixed(2),
      r.point_estimate.decision_tree.toFixed(2),
      r.time_estimate.random_forest.toFixed(2),
      r.time_estimate.decision_tree.toFixed(2),
      r.cost_estimate.random_forest.toFixed(2),
      r.cost_estimate.decision_tree.toFixed(2),
      r.effort_estimate.random_forest.toFixed(2),
      r.effort_estimate.decision_tree.toFixed(2)
    ]);

    let csv = headers.join(',') + '\n';
    rows.forEach(row => {
      csv += row.join(',') + '\n';
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `estimaciones-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    window.URL.revokeObjectURL(url);
  };

  if (!results) return null;

  return (
    <div className="results-section">
      <div className="results-header">
        <h2>📈 Resultados de Estimación</h2>
        <div className="results-stats">
          <span>[OK] {results.successful} estimadas</span>
          {results.failed > 0 && <span>[ERROR] {results.failed} fallidas</span>}
        </div>
      </div>

      {results.errors && results.errors.length > 0 && (
        <div className="results-errors">
          <h3>[ALERTA] Errores:</h3>
          {results.errors.map((error, idx) => (
            <p key={idx}>{error.story}: {error.error}</p>
          ))}
        </div>
      )}

      {results.successful > 0 && (
        <>
          <button className="export-btn" onClick={exportToCSV}>
            📊 Descargar CSV
          </button>

          <div className="story-list">
            {results.results.map((story, index) => (
              <div key={index} className="story-card">
                <div 
                  className="story-header"
                  onClick={() => toggleExpand(index)}
                >
                  <div className="title-section">
                    <h3>{story.story_title}</h3>
                  </div>
                  <div className="summary-metrics">
                    <span className="metric">
                      <span className="label">Puntos:</span>
                      <span className="value">
                        {story.point_estimate.ensemble.toFixed(1)}
                      </span>
                    </span>
                    <span className="metric">
                      <span className="label">Días:</span>
                      <span className="value">
                        {story.time_estimate.ensemble.toFixed(1)}
                      </span>
                    </span>
                    <span className="metric">
                      <span className="label">Costo:</span>
                      <span className="value">
                        ${story.cost_estimate.ensemble.toFixed(0)}
                      </span>
                    </span>
                    <span className="metric">
                      <span className="label">Esfuerzo:</span>
                      <span className="value">
                        {story.effort_estimate.ensemble.toFixed(1)}
                      </span>
                    </span>
                  </div>
                  <span className="expand-icon">
                    {expandedStory === index ? '▼' : '▶'}
                  </span>
                </div>

                {expandedStory === index && (
                  <div className="story-details">
                    <div className="model-comparison">
                      <h4>Comparación de Modelos (Ensemble vs Individual)</h4>
                      
                      <table className="comparison-table">
                        <thead>
                          <tr>
                            <th>Métrica</th>
                            <th>Ensemble</th>
                            <th>Random Forest</th>
                            <th>Árbol de Decisión</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>Puntos de Historia</td>
                            <td><strong>{story.point_estimate.ensemble.toFixed(2)}</strong></td>
                            <td>{story.point_estimate.random_forest.toFixed(2)}</td>
                            <td>{story.point_estimate.decision_tree.toFixed(2)}</td>
                          </tr>
                          <tr>
                            <td>Duración (Días)</td>
                            <td><strong>{story.time_estimate.ensemble.toFixed(2)}</strong></td>
                            <td>{story.time_estimate.random_forest.toFixed(2)}</td>
                            <td>{story.time_estimate.decision_tree.toFixed(2)}</td>
                          </tr>
                          <tr>
                            <td>Costo ($)</td>
                            <td><strong>${story.cost_estimate.ensemble.toFixed(2)}</strong></td>
                            <td>${story.cost_estimate.random_forest.toFixed(2)}</td>
                            <td>${story.cost_estimate.decision_tree.toFixed(2)}</td>
                          </tr>
                          <tr>
                            <td>Esfuerzo</td>
                            <td><strong>{story.effort_estimate.ensemble.toFixed(2)}</strong></td>
                            <td>{story.effort_estimate.random_forest.toFixed(2)}</td>
                            <td>{story.effort_estimate.decision_tree.toFixed(2)}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    {story.semantic_estimate && (
                      <div className="semantic-estimate">
                        <h4>Estimación por Similitud Semántica</h4>
                        <p>
                          Basado en historias similares:
                          Percentil 50: {story.semantic_estimate.p50.toFixed(1)} puntos,
                          Percentil 85: {story.semantic_estimate.p85.toFixed(1)} puntos,
                          Fibonacci: {story.semantic_estimate.fib.toFixed(0)} puntos
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
