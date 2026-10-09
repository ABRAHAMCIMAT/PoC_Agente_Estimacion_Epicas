import React, { useRef } from 'react';

export default function ExcelUpload({ onUpload, loading }) {
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      if (!file.name.match(/\.(xlsx|xls)$/)) {
        alert('Por favor selecciona un archivo Excel (.xlsx o .xls)');
        return;
      }
      onUpload(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add('drag-over');
  };

  const handleDragLeave = (e) => {
    e.currentTarget.classList.remove('drag-over');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');
    
    const file = e.dataTransfer.files?.[0];
    if (file) {
      if (!file.name.match(/\.(xlsx|xls)$/)) {
        alert('Por favor suelta un archivo Excel (.xlsx o .xls)');
        return;
      }
      onUpload(file);
    }
  };

  return (
    <div className="upload-card">
      <h2>Subir Historias de Usuario para Estimación</h2>
      
      <div 
        className="drop-zone"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="drop-icon">📁</div>
        <h3>Arrastra y suelta tu archivo Excel aquí</h3>
        <p>o haz clic para explorar</p>
        <p className="formats">Formatos soportados: .xlsx, .xls</p>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept=".xlsx,.xls"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
      />

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Procesando historias...</p>
        </div>
      )}

      <div className="requirements">
        <h4>Columnas Requeridas en Excel:</h4>
        <ul>
          <li><strong>Titulo</strong> - Título de la historia</li>
          <li><strong>Historia de Usuario</strong> - Descripción de la historia</li>
          <li><strong>Criterios de Aceptación</strong> - Criterios de aceptación</li>
        </ul>
      </div>
    </div>
  );
}
