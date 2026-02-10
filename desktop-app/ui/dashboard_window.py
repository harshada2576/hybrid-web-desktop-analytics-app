"""
Dashboard Window for PyQt5 Desktop Application

Main application window with CSV upload, analytics display, and charts.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFileDialog, QTableWidget, 
    QTableWidgetItem, QMessageBox, QGroupBox, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import requests
from datetime import datetime


class UploadWorker(QThread):
    """
    Background worker for CSV upload to prevent UI freezing.
    
    Signals:
        upload_complete: Emitted when upload succeeds
        upload_error: Emitted when upload fails with error message
    """
    
    upload_complete = pyqtSignal()
    upload_error = pyqtSignal(str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        """Execute upload in background thread."""
        try:
            self.api_client.upload_csv(self.file_path)
            self.upload_complete.emit()
        except requests.HTTPError as e:
            error_msg = 'Upload failed'
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', error_data.get('details', error_msg))
                except:
                    error_msg = f'Upload failed: {e.response.status_code}'
            self.upload_error.emit(str(error_msg))
        except Exception as e:
            self.upload_error.emit(f'Upload error: {str(e)}')


class DashboardWindow(QMainWindow):
    """
    Main dashboard window with analytics and visualization.
    """
    
    def __init__(self, api_client, username):
        """
        Initialize dashboard window.
        
        Args:
            api_client: APIClient instance
            username: Logged in username
        """
        super().__init__()
        self.api_client = api_client
        self.username = username
        self.upload_worker = None
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle('IIT Bombay Analytics Dashboard')
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # Upload section
        upload_section = self.create_upload_section()
        main_layout.addWidget(upload_section)
        
        # Content splitter (left and right panels)
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel (summary and history)
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel (chart)
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        central_widget.setLayout(main_layout)
    
    def create_header(self):
        """Create header with title and logout button."""
        header = QHBoxLayout()
        
        # Title
        title = QLabel('IIT Bombay Analytics Dashboard')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        header.addWidget(title)
        
        header.addStretch()
        
        # User info and logout
        user_label = QLabel(f'Welcome, {self.username}')
        header.addWidget(user_label)
        
        # Download report button
        download_btn = QPushButton('Download Report (PDF)')
        download_btn.clicked.connect(self.download_report)
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        header.addWidget(download_btn)
        
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.handle_logout)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        header.addWidget(logout_btn)
        
        return header
    
    def create_upload_section(self):
        """Create CSV upload section."""
        group = QGroupBox('Upload CSV Dataset')
        layout = QHBoxLayout()
        
        self.file_label = QLabel('No file selected')
        layout.addWidget(self.file_label)
        
        layout.addStretch()
        
        select_btn = QPushButton('Select CSV File')
        select_btn.clicked.connect(self.select_file)
        layout.addWidget(select_btn)
        
        self.upload_btn = QPushButton('Upload')
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover:enabled {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        layout.addWidget(self.upload_btn)
        
        group.setLayout(layout)
        return group
    
    def create_left_panel(self):
        """Create left panel with summary and history."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary section
        summary_group = QGroupBox('Summary Statistics')
        summary_layout = QVBoxLayout()
        
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(['Metric', 'Value'])
        self.summary_table.horizontalHeader().setStretchLastSection(True)
        self.summary_table.setEditTriggers(QTableWidget.NoEditTriggers)
        summary_layout.addWidget(self.summary_table)
        
        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)
        
        # History section
        history_group = QGroupBox('Upload History (Last 5)')
        history_layout = QVBoxLayout()
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(['Upload ID', 'Uploaded At'])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        history_layout.addWidget(self.history_table)
        
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_right_panel(self):
        """Create right panel with distribution chart."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        chart_group = QGroupBox('Equipment Type Distribution')
        chart_layout = QVBoxLayout()
        
        # Matplotlib figure
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasQTAgg(self.figure)
        chart_layout.addWidget(self.canvas)
        
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        widget.setLayout(layout)
        return widget
    
    def select_file(self):
        """Handle file selection."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select CSV File',
            '',
            'CSV Files (*.csv);;All Files (*)'
        )
        
        if file_path:
            self.selected_file_path = file_path
            self.file_label.setText(f'Selected: {file_path.split("/")[-1]}')
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        """Handle file upload."""
        if not hasattr(self, 'selected_file_path'):
            return
        
        # Disable upload button
        self.upload_btn.setEnabled(False)
        self.upload_btn.setText('Uploading...')
        
        # Create and start worker thread
        self.upload_worker = UploadWorker(self.api_client, self.selected_file_path)
        self.upload_worker.upload_complete.connect(self.on_upload_success)
        self.upload_worker.upload_error.connect(self.on_upload_error)
        self.upload_worker.start()
    
    def on_upload_success(self):
        """Handle successful upload."""
        self.upload_btn.setText('Upload')
        self.file_label.setText('No file selected')
        
        # Reload data
        self.load_data()
        
        QMessageBox.information(self, 'Success', 'Dataset uploaded successfully!')
    
    def on_upload_error(self, error_msg):
        """Handle upload error."""
        self.upload_btn.setEnabled(True)
        self.upload_btn.setText('Upload')
        
        QMessageBox.critical(self, 'Upload Error', error_msg)
    
    def load_data(self):
        """Load all dashboard data from backend."""
        try:
            # Load summary
            summary = self.api_client.get_summary()
            self.display_summary(summary)
            
            # Load distribution
            distribution = self.api_client.get_distribution()
            self.display_distribution(distribution)
            
            # Load history
            history = self.api_client.get_history()
            self.display_history(history)
            
        except requests.HTTPError as e:
            # Silently handle "no datasets" error
            if e.response is not None and e.response.status_code == 404:
                self.clear_displays()
    
    def display_summary(self, summary):
        """Display summary statistics in table."""
        self.summary_table.setRowCount(4)
        
        metrics = [
            ('Total Equipment', str(summary.get('total_equipment', 0))),
            ('Average Flowrate', f"{summary.get('average_flowrate', 0):.2f}"),
            ('Average Pressure', f"{summary.get('average_pressure', 0):.2f}"),
            ('Average Temperature', f"{summary.get('average_temperature', 0):.2f}")
        ]
        
        for row, (metric, value) in enumerate(metrics):
            self.summary_table.setItem(row, 0, QTableWidgetItem(metric))
            self.summary_table.setItem(row, 1, QTableWidgetItem(value))
    
    def display_distribution(self, distribution):
        """Display equipment distribution chart."""
        self.figure.clear()
        
        if not distribution:
            return
        
        ax = self.figure.add_subplot(111)
        
        types = [item['type'] for item in distribution]
        counts = [item['count'] for item in distribution]
        
        ax.bar(types, counts, color='steelblue', alpha=0.7)
        ax.set_xlabel('Equipment Type', fontsize=10)
        ax.set_ylabel('Count', fontsize=10)
        ax.set_title('Equipment Type Distribution', fontsize=11, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Rotate x-axis labels if needed
        if len(types) > 3:
            ax.tick_params(axis='x', rotation=45)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def display_history(self, history):
        """Display upload history in table."""
        self.history_table.setRowCount(len(history))
        
        for row, item in enumerate(history):
            upload_id = str(item.get('id', ''))
            uploaded_at = item.get('uploaded_at', '')
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                uploaded_at = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
            
            self.history_table.setItem(row, 0, QTableWidgetItem(upload_id))
            self.history_table.setItem(row, 1, QTableWidgetItem(uploaded_at))
    
    def clear_displays(self):
        """Clear all displays when no data available."""
        self.summary_table.setRowCount(0)
        self.history_table.setRowCount(0)
        self.figure.clear()
        self.canvas.draw()
    
    def download_report(self):
        """Handle PDF report download."""
        try:
            # Ask user where to save
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                'Save PDF Report',
                'equipment_analytics_report.pdf',
                'PDF Files (*.pdf)'
            )
            
            if file_path:
                # Download report
                self.api_client.download_report(file_path)
                QMessageBox.information(
                    self, 
                    'Success', 
                    f'Report downloaded successfully to:\n{file_path}'
                )
        
        except requests.HTTPError as e:
            error_msg = 'Download failed'
            if e.response is not None:
                if e.response.status_code == 404:
                    error_msg = 'No data available. Please upload a dataset first.'
                else:
                    try:
                        error_data = e.response.json()
                        error_msg = error_data.get('error', error_data.get('details', error_msg))
                    except:
                        error_msg = f'Download failed: {e.response.status_code}'
            QMessageBox.critical(self, 'Download Error', error_msg)
        
        except Exception as e:
            QMessageBox.critical(self, 'Download Error', f'Failed to download report: {str(e)}')
    
    def handle_logout(self):
        """Handle logout button click."""
        reply = QMessageBox.question(
            self,
            'Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.api_client.logout()
            except:
                pass  # Logout anyway
            
            # Show login window again
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow(self.api_client)
            self.login_window.login_success.connect(self.on_relogin)
            self.login_window.show()
            
            # Close this dashboard
            self.close()
    
    def on_relogin(self, username):
        """Handle successful re-login."""
        self.username = username
        self.new_dashboard = DashboardWindow(self.api_client, username)
        self.new_dashboard.show()
