"""
Main Entry Point for PyQt5 Desktop Application

IIT Bombay Analytics Desktop Client
"""

import sys
from PyQt5.QtWidgets import QApplication
from api_client import APIClient
from ui.login_window import LoginWindow
from ui.dashboard_window import DashboardWindow


def main():
    """
    Main application entry point.
    
    Initializes PyQt5 application and shows login window.
    """
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName('IIT Bombay Analytics')
    
    # Create API client
    api_client = APIClient()
    
    # Store dashboard reference to prevent garbage collection
    dashboard_window = None
    
    # Create and show login window
    login_window = LoginWindow(api_client)
    
    # Connect login success to dashboard
    def show_dashboard(username):
        nonlocal dashboard_window
        dashboard_window = DashboardWindow(api_client, username)
        dashboard_window.show()
    
    login_window.login_success.connect(show_dashboard)
    login_window.show()
    
    # Start application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
