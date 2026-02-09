/**
 * Login Component
 * 
 * Handles user authentication.
 * On success, stores token and redirects to dashboard.
 */

import React, { useState } from 'react';
import { authAPI } from '../services/api';
import './Login.css';

function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await authAPI.login(username, password);
      
      // Store token in localStorage
      localStorage.setItem('token', data.token);
      localStorage.setItem('username', data.user.username);
      
      // Notify parent component
      onLoginSuccess(data.user);
    } catch (err) {
      // Display backend error message
      if (err.response && err.response.data) {
        setError(err.response.data.error || err.response.data.details || 'Login failed');
      } else {
        setError('Network error. Please check if backend is running.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>IIT Bombay Analytics</h1>
        <h2>Login</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
              disabled={loading}
            />
          </div>
          
          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
