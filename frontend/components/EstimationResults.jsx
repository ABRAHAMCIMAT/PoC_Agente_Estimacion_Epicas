import React, { useState } from 'react';
import styles from '../styles/EstimationResults.module.css';

export default function EstimationResults({ results }) {
  const [expandedStory, setExpandedStory] = useState(null);

  const toggleExpand = (index) => {
    setExpandedStory(expandedStory === index ? null : index);
  };

  const exportToCSV = () => {
    if (!results?.results?.length) return;

    const headers = [
      'Story Title',
      'Story Points (Ensemble)',
      'Time (Days) (Ensemble)',
      'Cost ($) (Ensemble)',
      'Effort (Ensemble)',
      'Points (RF)',
      'Points (DT)',
      'Time (RF)',
      'Time (DT)',
      'Cost (RF)',
      'Cost (DT)',
      'Effort (RF)',
      'Effort (DT)'
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
    link.download = `estimations-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    window.URL.revokeObjectURL(url);
  };

  if (!results) return null;

  return (
    <div className={styles.resultsSection}>
      <div className={styles.header}>
        <h2>📈 Estimation Results</h2>
        <div className={styles.stats}>
          <span>✅ {results.successful} estimated</span>
          {results.failed > 0 && <span>❌ {results.failed} failed</span>}
        </div>
      </div>

      {results.errors && results.errors.length > 0 && (
        <div className={styles.errors}>
          <h3>⚠️ Errors:</h3>
          {results.errors.map((error, idx) => (
            <p key={idx}>{error.story}: {error.error}</p>
          ))}
        </div>
      )}

      {results.successful > 0 && (
        <>
          <button className={styles.exportBtn} onClick={exportToCSV}>
            📊 Export to CSV
          </button>

          <div className={styles.storyList}>
            {results.results.map((story, index) => (
              <div key={index} className={styles.storyCard}>
                <div 
                  className={styles.storyHeader}
                  onClick={() => toggleExpand(index)}
                >
                  <div className={styles.titleSection}>
                    <h3>{story.story_title}</h3>
                  </div>
                  <div className={styles.summaryMetrics}>
                    <span className={styles.metric}>
                      <span className={styles.label}>Points:</span>
                      <span className={styles.value}>
                        {story.point_estimate.ensemble.toFixed(1)}
                      </span>
                    </span>
                    <span className={styles.metric}>
                      <span className={styles.label}>Days:</span>
                      <span className={styles.value}>
                        {story.time_estimate.ensemble.toFixed(1)}
                      </span>
                    </span>
                    <span className={styles.metric}>
                      <span className={styles.label}>Cost:</span>
                      <span className={styles.value}>
                        ${story.cost_estimate.ensemble.toFixed(0)}
                      </span>
                    </span>
                    <span className={styles.metric}>
                      <span className={styles.label}>Effort:</span>
                      <span className={styles.value}>
                        {story.effort_estimate.ensemble.toFixed(1)}
                      </span>
                    </span>
                  </div>
                  <span className={styles.expandIcon}>
                    {expandedStory === index ? '▼' : '▶'}
                  </span>
                </div>

                {expandedStory === index && (
                  <div className={styles.storyDetails}>
                    <div className={styles.modelComparison}>
                      <h4>Model Comparison (Ensemble vs Individual)</h4>
                      
                      <table className={styles.comparisonTable}>
                        <thead>
                          <tr>
                            <th>Metric</th>
                            <th>Ensemble</th>
                            <th>Random Forest</th>
                            <th>Decision Tree</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>Story Points</td>
                            <td><strong>{story.point_estimate.ensemble.toFixed(2)}</strong></td>
                            <td>{story.point_estimate.random_forest.toFixed(2)}</td>
                            <td>{story.point_estimate.decision_tree.toFixed(2)}</td>
                          </tr>
                          <tr>
                            <td>Duration (Days)</td>
                            <td><strong>{story.time_estimate.ensemble.toFixed(2)}</strong></td>
                            <td>{story.time_estimate.random_forest.toFixed(2)}</td>
                            <td>{story.time_estimate.decision_tree.toFixed(2)}</td>
                          </tr>
                          <tr>
                            <td>Cost ($)</td>
                            <td><strong>${story.cost_estimate.ensemble.toFixed(2)}</strong></td>
                            <td>${story.cost_estimate.random_forest.toFixed(2)}</td>
                            <td>${story.cost_estimate.decision_tree.toFixed(2)}</td>
                          </tr>
                          <tr>
                            <td>Effort</td>
                            <td><strong>{story.effort_estimate.ensemble.toFixed(2)}</strong></td>
                            <td>{story.effort_estimate.random_forest.toFixed(2)}</td>
                            <td>{story.effort_estimate.decision_tree.toFixed(2)}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    {story.semantic_estimate && (
                      <div className={styles.semanticEstimate}>
                        <h4>Semantic Similarity Estimate</h4>
                        <p>
                          Based on similar historical stories:
                          50th percentile: {story.semantic_estimate.p50.toFixed(1)} points,
                          85th percentile: {story.semantic_estimate.p85.toFixed(1)} points,
                          Fibonacci-rounded: {story.semantic_estimate.fib.toFixed(0)} points
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
