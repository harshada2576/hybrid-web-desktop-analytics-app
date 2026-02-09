# React Web Application - Setup Guide

## Overview

React-based web client for IIT Bombay Analytics system.

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running on `http://localhost:8000`

## Installation

### 1. Navigate to web frontend directory

```bash
cd web-frontend
```

### 2. Install dependencies

```bash
npm install
```

## Running the Application

### Start development server

```bash
npm start
```

The application will open automatically at `http://localhost:3000`

## Project Structure

```
web-frontend/
├── src/
│   ├── components/           # React components
│   │   ├── Login.js         # Login page
│   │   ├── UploadForm.js    # CSV upload
│   │   ├── SummaryTable.js  # Statistics table
│   │   ├── DistributionChart.js  # Chart.js visualization
│   │   └── HistoryList.js   # Upload history
│   │
│   ├── services/
│   │   └── api.js           # Centralized API service
│   │
│   ├── App.js               # Main application
│   └── index.js             # Entry point
│
└── package.json
```

## Usage

### 1. Login

- Use existing backend credentials
- Token stored in localStorage

### 2. Upload CSV

- Click "Choose File" and select CSV
- Click "Upload" button
- Backend validates CSV format

### 3. View Analytics

- **Summary Table**: Shows total equipment and averages
- **Distribution Chart**: Bar chart of equipment types (Chart.js)
- **History**: Last 5 uploads

### 4. Logout

- Click "Logout" button in header
- Clears token and returns to login

## API Configuration

Backend URL is configured in `src/services/api.js`:

```javascript
const API_BASE_URL = "http://localhost:8000/api";
```

Change this if backend runs on different host/port.

## Error Handling

- All backend errors displayed clearly to user
- Network errors handled gracefully
- UI never crashes on API errors

## Building for Production

```bash
npm run build
```

Creates optimized build in `build/` directory.

## Technologies Used

- **React 18**: UI framework
- **Axios**: HTTP client
- **Chart.js**: Data visualization
- **react-chartjs-2**: React wrapper for Chart.js
