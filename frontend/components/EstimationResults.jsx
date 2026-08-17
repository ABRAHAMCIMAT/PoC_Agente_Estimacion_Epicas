import React, { useState } from 'react';

const ProgressBar = ({ value, max, color = '#3b82f6' }) => {
  const numValue = parseFloat(value);
  const percentage = (numValue / max) * 100;
  return (
    <div className="progress-bar-container">
      <div className="progress-bar-fill" style={{ width: `${percentage}%`, backgroundColor: color }}></div>
      <div className="progress-bar-value">{numValue.toFixed(1)}</div>
    </div>
  );
};

const MetricCard = ({ title, value, unit, color, maxValue }) => {
  const numValue = parseFloat(value);
  return (
    <div className="metric-card" style={{ borderLeftColor: color }}>
      <div className="metric-title">{title}</div>
      <div className="metric-value">{numValue.toFixed(1)} <span className="metric-unit">{unit}</span></div>
      {maxValue && <ProgressBar value={numValue} max={maxValue} color={color} />}
    </div>
  );
};

export default function EstimationResults({ results }) {
  const [expandedStory, setExpandedStory] = useState(null);

  const toggleExpand = (index) => {
    setExpandedStory(expandedStory === index ? null : index);
  };

  const getMaxValues = () => {
    if (!results?.results?.length) return {};
    return {
      points: Math.max(...results.results.map(r => r.point_estimate.ensemble)),
      time: Math.max(...results.results.map(r => r.time_estimate.ensemble)),
      cost: Math.max(...results.results.map(r => r.cost_estimate.ensemble)),
      effort: Math.max(...results.results.map(r => r.effort_estimate.ensemble))
    };
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

  const maxValues = getMaxValues();

  return (
    <div className="results-section">
      <div className="results-header">
        <h2>📈 Resultados de Estimación</h2>
        <div className="results-stats">
          <span className="stat-success">[OK] {results.successful} estimadas</span>
          {results.failed > 0 && <span className="stat-error">[ERROR] {results.failed} fallidas</span>}
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
          <div className="results-actions">
            <button className="export-btn" onClick={exportToCSV}>
              📊 Descargar CSV
            </button>
          </div>

          <div className="summary-table-container">
            <table className="summary-table">
              <thead>
                <tr>
                  <th className="col-title">Historia de Usuario</th>
                  <th className="col-metric">Puntos</th>
                  <th className="col-metric">Días</th>
                  <th className="col-metric">Costo ($)</th>
                  <th className="col-metric">Esfuerzo</th>
                  <th className="col-action">Detalles</th>
                </tr>
              </thead>
              <tbody>
                {results.results.map((story, index) => (
                  <tr key={index} className={`story-row ${expandedStory === index ? 'expanded' : ''}`}>
                    <td className="col-title">{story.story_title}</td>
                    <td className="col-metric">
                      <div className="metric-cell">
                        <span className="value">{story.point_estimate.ensemble.toFixed(1)}</span>
                        <div className="bar" style={{ 
                          width: `${(story.point_estimate.ensemble / maxValues.points) * 100}%`,
                          backgroundColor: '#10b981'
                        }}></div>
                      </div>
                    </td>
                    <td className="col-metric">
                      <div className="metric-cell">
                        <span className="value">{story.time_estimate.ensemble.toFixed(1)}</span>
                        <div className="bar" style={{ 
                          width: `${(story.time_estimate.ensemble / maxValues.time) * 100}%`,
                          backgroundColor: '#f59e0b'
                        }}></div>
                      </div>
                    </td>
                    <td className="col-metric">
                      <div className="metric-cell">
                        <span className="value">${story.cost_estimate.ensemble.toFixed(0)}</span>
                        <div className="bar" style={{ 
                          width: `${(story.cost_estimate.ensemble / maxValues.cost) * 100}%`,
                          backgroundColor: '#ef4444'
                        }}></div>
                      </div>
                    </td>
                    <td className="col-metric">
                      <div className="metric-cell">
                        <span className="value">{story.effort_estimate.ensemble.toFixed(1)}</span>
                        <div className="bar" style={{ 
                          width: `${(story.effort_estimate.ensemble / maxValues.effort) * 100}%`,
                          backgroundColor: '#8b5cf6'
                        }}></div>
                      </div>
                    </td>
                    <td className="col-action">
                      <button 
                        className="expand-btn"
                        onClick={() => toggleExpand(index)}
                        title={expandedStory === index ? "Ocultar detalles" : "Ver detalles"}
                      >
                        {expandedStory === index ? '▲' : '▼'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {results.results.map((story, index) => (
            expandedStory === index && (
              <div key={`detail-${index}`} className="story-details-expanded">
                <div className="detail-header">
                  <h3>Detalles: {story.story_title}</h3>
                </div>

                <div className="metrics-grid">
                  <MetricCard 
                    title="Puntos de Historia"
                    value={story.point_estimate.ensemble.toFixed(1)}
                    unit="pts"
                    color="#10b981"
                    maxValue={maxValues.points}
                  />
                  <MetricCard 
                    title="Duración"
                    value={story.time_estimate.ensemble.toFixed(1)}
                    unit="días"
                    color="#f59e0b"
                    maxValue={maxValues.time}
                  />
                  <MetricCard 
                    title="Costo"
                    value={story.cost_estimate.ensemble.toFixed(0)}
                    unit="$"
                    color="#ef4444"
                    maxValue={maxValues.cost}
                  />
                  <MetricCard 
                    title="Esfuerzo"
                    value={story.effort_estimate.ensemble.toFixed(1)}
                    unit="horas"
                    color="#8b5cf6"
                    maxValue={maxValues.effort}
                  />
                </div>

                <div className="model-comparison">
                  <h4>Comparación de Modelos</h4>
                  <table className="comparison-table">
                    <thead>
                      <tr>
                        <th>Métrica</th>
                        <th>Ensemble (Recomendado)</th>
                        <th>Random Forest</th>
                        <th>Árbol de Decisión</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Puntos de Historia</td>
                        <td className="ensemble-cell"><strong>{story.point_estimate.ensemble.toFixed(2)}</strong></td>
                        <td>{story.point_estimate.random_forest.toFixed(2)}</td>
                        <td>{story.point_estimate.decision_tree.toFixed(2)}</td>
                      </tr>
                      <tr>
                        <td>Duración (Días)</td>
                        <td className="ensemble-cell"><strong>{story.time_estimate.ensemble.toFixed(2)}</strong></td>
                        <td>{story.time_estimate.random_forest.toFixed(2)}</td>
                        <td>{story.time_estimate.decision_tree.toFixed(2)}</td>
                      </tr>
                      <tr>
                        <td>Costo ($)</td>
                        <td className="ensemble-cell"><strong>${story.cost_estimate.ensemble.toFixed(2)}</strong></td>
                        <td>${story.cost_estimate.random_forest.toFixed(2)}</td>
                        <td>${story.cost_estimate.decision_tree.toFixed(2)}</td>
                      </tr>
                      <tr>
                        <td>Esfuerzo</td>
                        <td className="ensemble-cell"><strong>{story.effort_estimate.ensemble.toFixed(2)}</strong></td>
                        <td>{story.effort_estimate.random_forest.toFixed(2)}</td>
                        <td>{story.effort_estimate.decision_tree.toFixed(2)}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                {story.semantic_estimate && (
                  <div className="semantic-estimate">
                    <h4>Estimación por Similitud Semántica</h4>
                    <div className="semantic-metrics">
                      <div className="semantic-item">
                        <span className="label">Percentil 50:</span>
                        <span className="value">{story.semantic_estimate.p50.toFixed(1)} puntos</span>
                      </div>
                      <div className="semantic-item">
                        <span className="label">Percentil 85:</span>
                        <span className="value">{story.semantic_estimate.p85.toFixed(1)} puntos</span>
                      </div>
                      <div className="semantic-item">
                        <span className="label">Secuencia Fibonacci:</span>
                        <span className="value">{story.semantic_estimate.fib.toFixed(0)} puntos</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )
          ))}
        </>
      )}
    </div>
  );
}
