import React, { useRef } from 'react';

export default function ExcelUpload({ onUpload, loading }) {
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      if (!file.name.match(/\.(xlsx|xls)$/)) {
        alert('Please select an Excel file (.xlsx or .xls)');
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
        alert('Please drop an Excel file (.xlsx or .xls)');
        return;
      }
      onUpload(file);
    }
  };

  return (
    <div className="upload-card">
      <h2>Upload Stories for Estimation</h2>
      
      <div 
        className="drop-zone"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="drop-icon">📁</div>
        <h3>Drag and drop Excel file here</h3>
        <p>or click to browse</p>
        <p className="formats">Supported: .xlsx, .xls</p>
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
          <p>Processing stories...</p>
        </div>
      )}

      <div className="requirements">
        <h4>Required Excel Columns:</h4>
        <ul>
          <li><strong>Titulo</strong> - Story title</li>
          <li><strong>Historia de Usuario</strong> - Story description</li>
          <li><strong>Criterios de Aceptación</strong> - Acceptance criteria</li>
        </ul>
      </div>
    </div>
  );
}
