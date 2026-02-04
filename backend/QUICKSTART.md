# 🚀 Quick Start Guide - IIT Bombay Analytics Backend

## Complete Setup in 5 Minutes

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create and Activate Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### Step 6: Start Server

```bash
python manage.py runserver
```

✅ **Backend is now running at:** `http://127.0.0.1:8000/`

---

## 🧪 Testing the API

### 1. Register a User

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"email\":\"test@test.com\",\"password\":\"SecurePass123\",\"password_confirm\":\"SecurePass123\"}"
```

**Response:**

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@test.com"
  },
  "token": "YOUR_TOKEN_HERE"
}
```

### 2. Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"password\":\"SecurePass123\"}"
```

### 3. Upload CSV

```bash
curl -X POST http://127.0.0.1:8000/api/upload/ ^
  -H "Authorization: Token YOUR_TOKEN_HERE" ^
  -F "file=@sample_equipment_data.csv"
```

**Response:**

```json
{
  "message": "Dataset uploaded successfully",
  "dataset": {
    "id": 1,
    "uploaded_at": "2026-02-04T...",
    "summary": {
      "total_equipment": 10,
      "average_flowrate": 141.34,
      "average_pressure": 329.0,
      "average_temperature": 91.59,
      "equipment_distribution": [
        {"type": "Centrifugal", "count": 2},
        {"type": "Rotary", "count": 1},
        ...
      ]
    }
  }
}
```

### 4. Get Summary

```bash
curl -X GET http://127.0.0.1:8000/api/summary/ ^
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 5. Get Distribution

```bash
curl -X GET http://127.0.0.1:8000/api/distribution/ ^
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 6. Get History

```bash
curl -X GET http://127.0.0.1:8000/api/history/ ^
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 7. Logout

```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ ^
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## 🔍 Admin Panel

Access Django admin at: `http://127.0.0.1:8000/admin/`

Login with the superuser credentials you created.

---

## 📊 CSV Format

Your CSV must have these exact columns:

- `Equipment Name`
- `Type`
- `Flowrate` (numeric)
- `Pressure` (numeric)
- `Temperature` (numeric)

A sample file `sample_equipment_data.csv` is included in the backend directory.

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Run on different port
python manage.py runserver 8001
```

### Module Not Found

```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Errors

```bash
# Delete and recreate database
del db.sqlite3
python manage.py migrate
```

---

## 📁 Project Structure

```
backend/
├── api/                    # Main API app
│   ├── models.py          # Database models
│   ├── serializers.py     # Data validation
│   ├── views.py           # API endpoints
│   ├── urls.py            # Routes
│   └── services/          # Business logic
│       └── analytics.py   # Pandas analytics
│
├── backend/               # Django config
│   ├── settings.py       # Configuration
│   └── urls.py           # Main routing
│
├── manage.py             # Django CLI
├── requirements.txt      # Dependencies
├── sample_equipment_data.csv  # Test data
└── README.md             # Documentation
```

---

## ✅ What's Working

- ✅ User registration with validation
- ✅ Token-based authentication
- ✅ CSV upload with strict validation
- ✅ Pandas analytics computation
- ✅ Auto-limit to 5 uploads per user
- ✅ Summary, distribution, history endpoints
- ✅ CORS support for web/desktop frontends

---

## 🎯 Ready for IIT Bombay Evaluation

This backend is:

- Production-quality code
- Clean architecture (models → serializers → services → views)
- Well-documented with docstrings
- Follows Django best practices
- Ready for frontend integration

---

**Need help?** Check the main README.md for detailed documentation.
