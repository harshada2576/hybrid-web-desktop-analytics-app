/**
 * Upload Form Component
 * 
 * Handles CSV file selection and upload.
 * Displays backend validation errors clearly.
 */

import React, { useState } from 'react';
import './UploadForm.css';

function UploadForm({ onUploadSuccess, onUploadError }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.name.endsWith('.csv')) {
      setSelectedFile(file);
    } else {
      setSelectedFile(null);
      alert('Please select a CSV file');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first');
      return;
    }

    setUploading(true);
    try {
      await onUploadSuccess(selectedFile);
      setSelectedFile(null);
      // Reset file input
      document.getElementById('csv-file-input').value = '';
    } catch (err) {
      // Error handled by parent
      onUploadError(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-form">
      <h3>Upload CSV Dataset</h3>
      <div className="upload-controls">
        <input
          id="csv-file-input"
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          disabled={uploading}
        />
        <button 
          onClick={handleUpload} 
          disabled={!selectedFile || uploading}
          className="upload-btn"
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      {selectedFile && (
        <div className="file-info">
          Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
        </div>
      )}
    </div>
  );
}

export default UploadForm;
