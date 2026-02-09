/**
 * Main App Component
 * 
 * Handles routing between login and dashboard.
 * Manages global error handling and user session.
 */

import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import UploadForm from './components/UploadForm';
import SummaryTable from './components/SummaryTable';
import DistributionChart from './components/DistributionChart';
import HistoryList from './components/HistoryList';
import { authAPI, dataAPI } from './services/api';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [summary, setSummary] = useState(null);
  const [distribution, setDistribution] = useState([]);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Check for existing session on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    if (token && username) {
      setIsLoggedIn(true);
      setUser({ username });
      loadDashboardData();
    }
  }, []);

  /**
   * Load all dashboard data
   */
  const loadDashboardData = async () => {
    try {
      // Load summary
      const summaryData = await dataAPI.getSummary();
      setSummary(summaryData);

      // Load distribution
      const distData = await dataAPI.getDistribution();
      setDistribution(distData.distribution);

      // Load history
      const histData = await dataAPI.getHistory();
      setHistory(histData.history);
    } catch (err) {
      // Silently handle "no datasets" error
      if (err.response && err.response.status === 404) {
        setSummary(null);
        setDistribution([]);
        setHistory([]);
      }
    }
  };

  /**
   * Handle successful login
   */
  const handleLoginSuccess = (userData) => {
    setIsLoggedIn(true);
    setUser(userData);
    loadDashboardData();
  };

  /**
   * Handle logout
   */
  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (err) {
      // Logout anyway even if API call fails
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      setIsLoggedIn(false);
      setUser(null);
      setSummary(null);
      setDistribution([]);
      setHistory([]);
    }
  };

  /**
   * Handle CSV upload
   */
  const handleUpload = async (file) => {
    setError('');
    setLoading(true);

    try {
      await dataAPI.uploadCSV(file);
      
      // Reload dashboard data
      await loadDashboardData();
      
      setError(''); // Clear any previous errors
    } catch (err) {
      // Display backend error
      if (err.response && err.response.data) {
        const errorMsg = err.response.data.error || err.response.data.details || 'Upload failed';
        setError(errorMsg);
      } else {
        setError('Network error. Please check if backend is running.');
      }
      throw err; // Re-throw to let UploadForm handle it
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle upload error
   */
  const handleUploadError = (err) => {
    // Error already handled in handleUpload
  };

  // Show login if not authenticated
  if (!isLoggedIn) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  // Show dashboard
  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>IIT Bombay Analytics Dashboard</h1>
          <div className="user-info">
            <span>Welcome, {user.username}</span>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
          </div>
        )}

        {loading && (
          <div className="loading-banner">
            Processing upload...
          </div>
        )}

        <UploadForm 
          onUploadSuccess={handleUpload}
          onUploadError={handleUploadError}
        />

        <div className="dashboard-grid">
          <div className="dashboard-left">
            <SummaryTable summary={summary} />
            <HistoryList history={history} />
          </div>
          <div className="dashboard-right">
            <DistributionChart distribution={distribution} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
