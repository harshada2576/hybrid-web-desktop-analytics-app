/**
 * History List Component
 * 
 * Displays last 5 uploads with timestamps.
 */

import React from 'react';
import './HistoryList.css';

function HistoryList({ history }) {
  if (!history || history.length === 0) {
    return (
      <div className="history-list">
        <h3>Upload History</h3>
        <p className="no-data">No upload history yet.</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="history-list">
      <h3>Upload History (Last 5)</h3>
      <table>
        <thead>
          <tr>
            <th>Upload ID</th>
            <th>Uploaded At</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{formatDate(item.uploaded_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoryList;
