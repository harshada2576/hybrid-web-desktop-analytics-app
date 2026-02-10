"""
API Client for PyQt5 Desktop Application

Centralized backend communication module.
Handles authentication and all data operations.
"""

import requests
from typing import Dict, List, Optional, Any


class APIClient:
    """
    Client for IIT Bombay Analytics Backend API.
    
    Thread-safe for use with PyQt5 threading.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        """
        Initialize API client.
        
        Args:
            base_url: Backend API base URL
        """
        self.base_url = base_url
        self.token: Optional[str] = None
        self.username: Optional[str] = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication token."""
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers
    
    # ================================
    # Authentication Methods
    # ================================
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login user and store token.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Response data with user info and token
            
        Raises:
            requests.HTTPError: If login fails
        """
        url = f"{self.base_url}/auth/login/"
        response = requests.post(url, json={
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data['token']
            self.username = data['user']['username']
            return data
        else:
            response.raise_for_status()
    
    def logout(self) -> Dict[str, Any]:
        """
        Logout current user.
        
        Returns:
            Response confirmation
            
        Raises:
            requests.HTTPError: If logout fails
        """
        url = f"{self.base_url}/auth/logout/"
        response = requests.post(url, headers=self._get_headers())
        
        if response.status_code == 200:
            self.token = None
            self.username = None
            return response.json()
        else:
            response.raise_for_status()
    
    def register(self, username: str, email: str, password: str, 
                 password_confirm: str) -> Dict[str, Any]:
        """
        Register new user.
        
        Args:
            username: Desired username
            email: User email
            password: Password
            password_confirm: Password confirmation
            
        Returns:
            Response data with user info and token
            
        Raises:
            requests.HTTPError: If registration fails
        """
        url = f"{self.base_url}/auth/register/"
        response = requests.post(url, json={
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password_confirm
        })
        
        if response.status_code == 201:
            data = response.json()
            self.token = data['token']
            self.username = data['user']['username']
            return data
        else:
            response.raise_for_status()
    
    # ================================
    # Data Methods
    # ================================
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Upload CSV file to backend.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Response data with upload confirmation and summary
            
        Raises:
            requests.HTTPError: If upload fails
        """
        url = f"{self.base_url}/upload/"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                url, 
                files=files, 
                headers=self._get_headers()
            )
        
        if response.status_code == 201:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics.
        
        Returns:
            Summary data with averages and totals
            
        Raises:
            requests.HTTPError: If request fails
        """
        url = f"{self.base_url}/summary/"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_distribution(self) -> List[Dict[str, Any]]:
        """
        Get equipment type distribution.
        
        Returns:
            List of equipment types with counts
            
        Raises:
            requests.HTTPError: If request fails
        """
        url = f"{self.base_url}/distribution/"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            data = response.json()
            return data.get('distribution', [])
        else:
            response.raise_for_status()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get upload history.
        
        Returns:
            List of past uploads
            
        Raises:
            requests.HTTPError: If request fails
        """
        url = f"{self.base_url}/history/"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            data = response.json()
            return data.get('history', [])
        else:
            response.raise_for_status()
    
    def download_report(self, save_path: str) -> bool:
        """
        Download PDF analytics report.
        
        Args:
            save_path: Path where the PDF should be saved
            
        Returns:
            True if successful
            
        Raises:
            requests.HTTPError: If request fails
        """
        url = f"{self.base_url}/report/pdf/"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            response.raise_for_status()
