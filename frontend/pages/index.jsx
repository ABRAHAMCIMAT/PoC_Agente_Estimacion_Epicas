import React, { useState } from 'react';
import ExcelUpload from '../components/ExcelUpload';
import EstimationResults from '../components/EstimationResults';
import Header from '../components/Header';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleExcelUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/estimate/excel', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to estimate stories');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Header />
      
      <main className={styles.main}>
        <section className={styles.uploadSection}>
          <ExcelUpload 
            onUpload={handleExcelUpload} 
            loading={loading}
          />
        </section>

        {error && (
          <div className={styles.error}>
            <p>❌ Error: {error}</p>
          </div>
        )}

        {results && (
          <EstimationResults results={results} />
        )}
      </main>
    </div>
  );
}
