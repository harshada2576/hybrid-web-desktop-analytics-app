/**
 * API Service - Centralized backend communication
 * 
 * All API calls go through this module.
 * Handles authentication headers automatically.
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Get authorization header with stored token
 */
const getAuthHeader = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Token ${token}` } : {};
};

/**
 * Authentication APIs
 */
export const authAPI = {
  /**
   * Login user
   * @param {string} username 
   * @param {string} password 
   * @returns {Promise} Response with token and user data
   */
  login: async (username, password) => {
    const response = await axios.post(`${API_BASE_URL}/auth/login/`, {
      username,
      password
    });
    return response.data;
  },

  /**
   * Register new user
   * @param {string} username 
   * @param {string} email 
   * @param {string} password 
   * @param {string} password_confirm 
   * @returns {Promise} Response with token and user data
   */
  register: async (username, email, password, password_confirm) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register/`, {
      username,
      email,
      password,
      password_confirm
    });
    return response.data;
  },

  /**
   * Logout current user
   * @returns {Promise} Logout confirmation
   */
  logout: async () => {
    const response = await axios.post(
      `${API_BASE_URL}/auth/logout/`,
      {},
      { headers: getAuthHeader() }
    );
    return response.data;
  }
};

/**
 * Data APIs
 */
export const dataAPI = {
  /**
   * Upload CSV file
   * @param {File} file - CSV file object
   * @returns {Promise} Upload response with summary
   */
  uploadCSV: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
      `${API_BASE_URL}/upload/`,
      formData,
      {
        headers: {
          ...getAuthHeader(),
          'Content-Type': 'multipart/form-data'
        }
      }
    );
    return response.data;
  },

  /**
   * Get summary statistics
   * @returns {Promise} Summary data
   */
  getSummary: async () => {
    const response = await axios.get(`${API_BASE_URL}/summary/`, {
      headers: getAuthHeader()
    });
    return response.data;
  },

  /**
   * Get equipment type distribution
   * @returns {Promise} Distribution data
   */
  getDistribution: async () => {
    const response = await axios.get(`${API_BASE_URL}/distribution/`, {
      headers: getAuthHeader()
    });
    return response.data;
  },

  /**
   * Get upload history (last 5)
   * @returns {Promise} History list
   */
  getHistory: async () => {
    const response = await axios.get(`${API_BASE_URL}/history/`, {
      headers: getAuthHeader()
    });
    return response.data;
  }
};

export default { authAPI, dataAPI };
