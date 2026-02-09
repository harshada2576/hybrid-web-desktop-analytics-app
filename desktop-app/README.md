# PyQt5 Desktop Application - Setup Guide

## Overview

Desktop client for IIT Bombay Analytics system built with PyQt5.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Backend server running on `http://localhost:8000`

## Installation

### 1. Navigate to desktop app directory

```bash
cd desktop-app
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Project Structure

```
desktop-app/
├── main.py              # Application entry point
├── api_client.py        # Backend API client
├── requirements.txt     # Python dependencies
│
└── ui/
    ├── __init__.py
    ├── login_window.py      # Login window
    └── dashboard_window.py  # Main dashboard
```

## Usage

### 1. Login Window

- Enter username and password
- Click "Login" button
- Token stored in memory (not persisted)

### 2. Dashboard Window

#### CSV Upload

- Click "Select CSV File"
- Choose CSV file from file dialog
- Click "Upload" button
- Upload runs in background thread (UI doesn't freeze)

#### View Analytics

- **Summary Statistics**: Table showing totals and averages
- **Equipment Distribution**: Bar chart using Matplotlib
- **Upload History**: Last 5 uploads with timestamps

#### Logout

- Click "Logout" button
- Returns to login window

## API Configuration

Backend URL is configured in `api_client.py`:

```python
def __init__(self, base_url: str = "http://localhost:8000/api"):
```

Change this if backend runs on different host/port.

## Error Handling

- All errors displayed via message boxes
- Network errors handled gracefully
- Background threading prevents UI freezing
- Clear error messages from backend

## Code Architecture

### Separation of Concerns

- **api_client.py**: All backend communication
- **login_window.py**: Authentication UI
- **dashboard_window.py**: Main application UI
- **main.py**: Application bootstrap

### Threading

- CSV uploads run in background using QThread
- Prevents UI freezing during network operations
- Signals/slots for thread communication

### Chart Rendering

- Matplotlib embedded using Qt5Agg backend
- Bar chart with clear axis labels
- Academic styling (neutral colors, no fancy animations)

## Dependencies Explained

- **PyQt5**: GUI framework
- **requests**: HTTP client for API calls
- **matplotlib**: Data visualization

## Troubleshooting

### "No module named PyQt5"

```bash
pip install PyQt5==5.15.9
```

### "Connection refused"

Ensure backend server is running:

```bash
cd backend
python manage.py runserver
```

### Chart not displaying

Matplotlib backend issue. Ensure PyQt5 is properly installed.

## Building Executable (Optional)

Use PyInstaller to create standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

Executable will be in `dist/` directory.
