/**
 * Summary Table Component
 * 
 * Displays analytics summary statistics from backend.
 */

import React from 'react';
import './SummaryTable.css';

function SummaryTable({ summary }) {
  if (!summary) {
    return (
      <div className="summary-table">
        <h3>Summary Statistics</h3>
        <p className="no-data">No data available. Please upload a CSV file.</p>
      </div>
    );
  }

  return (
    <div className="summary-table">
      <h3>Summary Statistics</h3>
      <table>
        <thead>
          <tr>
            <th>Metric</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Total Equipment</td>
            <td>{summary.total_equipment}</td>
          </tr>
          <tr>
            <td>Average Flowrate</td>
            <td>{summary.average_flowrate?.toFixed(2)}</td>
          </tr>
          <tr>
            <td>Average Pressure</td>
            <td>{summary.average_pressure?.toFixed(2)}</td>
          </tr>
          <tr>
            <td>Average Temperature</td>
            <td>{summary.average_temperature?.toFixed(2)}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default SummaryTable;
