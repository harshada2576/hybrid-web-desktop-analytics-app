/**
 * Distribution Chart Component
 * 
 * Displays equipment type distribution using Chart.js.
 * Uses neutral colors and clear axis labels.
 */

import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import './DistributionChart.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function DistributionChart({ distribution }) {
  if (!distribution || distribution.length === 0) {
    return (
      <div className="distribution-chart">
        <h3>Equipment Type Distribution</h3>
        <p className="no-data">No data available. Please upload a CSV file.</p>
      </div>
    );
  }

  // Prepare data for Chart.js
  const labels = distribution.map(item => item.type);
  const counts = distribution.map(item => item.count);

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: 'Count',
        data: counts,
        backgroundColor: 'rgba(99, 132, 255, 0.7)',
        borderColor: 'rgba(99, 132, 255, 1)',
        borderWidth: 1
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `Count: ${context.parsed.y}`;
          }
        }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Equipment Type',
          font: {
            size: 14
          }
        }
      },
      y: {
        title: {
          display: true,
          text: 'Count',
          font: {
            size: 14
          }
        },
        beginAtZero: true,
        ticks: {
          stepSize: 1
        }
      }
    }
  };

  return (
    <div className="distribution-chart">
      <h3>Equipment Type Distribution</h3>
      <div className="chart-container">
        <Bar data={chartData} options={options} />
      </div>
    </div>
  );
}

export default DistributionChart;
