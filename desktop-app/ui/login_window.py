"""
Login Window for PyQt5 Desktop Application

Handles user authentication with clean UI.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import requests


class LoginWindow(QWidget):
    """
    Login window with username/password authentication.
    
    Signals:
        login_success: Emitted when login succeeds with username
    """
    
    login_success = pyqtSignal(str)
    
    def __init__(self, api_client):
        """
        Initialize login window.
        
        Args:
            api_client: APIClient instance for backend communication
        """
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle('IIT Bombay Analytics - Login')
        self.setFixedSize(450, 450)
        
        # Center window on screen
        self.center_on_screen()
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(50, 40, 50, 40)
        
        # Title
        title = QLabel('IIT Bombay Analytics')
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        subtitle = QLabel('Login')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle.setFont(subtitle_font)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Username field
        username_label = QLabel('Username:')
        label_font = QFont()
        label_font.setPointSize(10)
        username_label.setFont(label_font)
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        self.username_input.setMinimumHeight(40)
        layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel('Password:')
        password_label.setFont(label_font)
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        layout.addWidget(self.password_input)
        
        # Enable login on Enter key
        self.password_input.returnPressed.connect(self.handle_login)
        
        layout.addSpacing(20)
        
        # Login button
        self.login_button = QPushButton('Login')
        self.login_button.setMinimumHeight(45)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        layout.addWidget(self.login_button)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def center_on_screen(self):
        """Center window on screen."""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def handle_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(
                self, 
                'Input Error', 
                'Please enter both username and password.'
            )
            return
        
        # Disable button during login
        self.login_button.setEnabled(False)
        self.login_button.setText('Logging in...')
        
        try:
            # Call API
            self.api_client.login(username, password)
            
            # Emit success signal
            self.login_success.emit(username)
            
            # Close login window
            self.close()
            
        except requests.HTTPError as e:
            # Display backend error
            error_msg = 'Login failed'
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', error_data.get('details', error_msg))
                except:
                    error_msg = f'Login failed: {e.response.status_code}'
            
            QMessageBox.critical(self, 'Login Error', str(error_msg))
            
        except requests.RequestException as e:
            QMessageBox.critical(
                self, 
                'Network Error', 
                'Could not connect to backend. Please ensure the server is running.'
            )
        
        finally:
            # Re-enable button
            self.login_button.setEnabled(True)
            self.login_button.setText('Login')
