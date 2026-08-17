import React from 'react';
import styles from '../styles/Header.module.css';

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <h1 className={styles.title}>📊 Epic Estimation System</h1>
        <p className={styles.subtitle}>
          AI-powered story point, time, cost, and effort estimation
        </p>
      </div>
    </header>
  );
}
