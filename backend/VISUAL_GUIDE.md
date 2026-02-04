# 🎨 Visual Quick Reference Guide

Quick visual reference for the IIT Bombay Analytics Backend.

---

## 📡 API Endpoints Map

```
http://127.0.0.1:8000/
│
└── api/
    │
    ├── auth/
    │   ├── register/     [POST]  ⭕ No Auth Required
    │   ├── login/        [POST]  ⭕ No Auth Required
    │   └── logout/       [POST]  🔒 Token Required
    │
    ├── upload/           [POST]  🔒 Token Required
    ├── summary/          [GET]   🔒 Token Required
    ├── distribution/     [GET]   🔒 Token Required
    └── history/          [GET]   🔒 Token Required

Legend:
⭕ Public endpoint (no authentication)
🔒 Protected endpoint (requires Authorization header)
```

---

## 🔄 Request/Response Flow

### Upload CSV Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. Client: POST /api/upload/                               │
│     Headers: Authorization: Token abc123                    │
│     Body: file=sample.csv                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  2. View: upload_dataset()                                  │
│     • Check authentication                                  │
│     • Validate serializer                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Model: DatasetUpload.save()                             │
│     • Check if user has 5+ uploads                          │
│     • If yes: delete oldest upload                          │
│     • Save new upload                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Service: compute_summary_statistics()                   │
│     • Load CSV with Pandas                                  │
│     • Validate columns                                      │
│     • Compute statistics                                    │
│     • Return dictionary                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Model: Update summary_json                              │
│     • Store computed summary                                │
│     • Save to database                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  6. View: Return Response                                   │
│     • HTTP 201 Created                                      │
│     • JSON with summary data                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Relationships

```
┌──────────────────┐
│      User        │
│  (Django Auth)   │
├──────────────────┤
│  id (PK)         │
│  username        │
│  email           │
│  password        │
└────────┬─────────┘
         │
         │ 1:N (one user, many uploads)
         │
         ▼
┌──────────────────┐         ┌──────────────────┐
│  DatasetUpload   │    1:1  │      Token       │
├──────────────────┤◄────────┤  (DRF Auth)      │
│  id (PK)         │         ├──────────────────┤
│  file            │         │  key (PK)        │
│  uploaded_at     │         │  user_id (FK)    │
│  summary_json    │         │  created         │
│  user_id (FK)    │         └──────────────────┘
└──────────────────┘

Max 5 DatasetUpload records per user (auto-enforced)
```

---

## 📂 File Structure Explained

```
backend/
│
├── 📁 api/                          Main API application
│   ├── 📄 models.py                 DatasetUpload model
│   ├── 📄 serializers.py            Request/response validation
│   ├── 📄 views.py                  7 API endpoints
│   ├── 📄 urls.py                   API routes
│   ├── 📄 admin.py                  Django admin config
│   ├── 📄 apps.py                   App configuration
│   └── 📁 services/                 Business logic layer
│       └── 📄 analytics.py          Pandas computations
│
├── 📁 backend/                      Django configuration
│   ├── 📄 settings.py               Project settings
│   ├── 📄 urls.py                   Main URL router
│   ├── 📄 wsgi.py                   WSGI server config
│   └── 📄 asgi.py                   ASGI server config
│
├── 📄 manage.py                     Django CLI tool
├── 📄 requirements.txt              Python dependencies
│
├── 📄 README.md                     Main documentation
├── 📄 QUICKSTART.md                 5-minute setup
├── 📄 ARCHITECTURE.md               Design explained
├── 📄 TESTING.md                    Test cases
├── 📄 PROJECT_SUMMARY.md            Complete summary
├── 📄 VISUAL_GUIDE.md               This file
│
├── 📄 sample_equipment_data.csv    Test CSV file
├── 📄 test_api.py                  Python test script
└── 📄 .gitignore                   Git ignore rules
```

---

## 🔐 Authentication Flow

```
┌─────────────┐
│   CLIENT    │
└──────┬──────┘
       │
       │ 1. POST /api/auth/register/
       │    {username, email, password}
       ▼
┌─────────────────────────┐
│   DJANGO BACKEND        │
│  • Create user          │
│  • Hash password        │
│  • Generate token       │
└──────┬──────────────────┘
       │
       │ 2. Response: {user, token}
       ▼
┌─────────────┐
│   CLIENT    │
│ Store token │
│ in memory/  │
│ localStorage│
└──────┬──────┘
       │
       │ 3. All subsequent requests
       │    Header: Authorization: Token abc123
       ▼
┌─────────────────────────┐
│   DJANGO BACKEND        │
│  • Verify token         │
│  • Identify user        │
│  • Process request      │
└─────────────────────────┘
```

---

## 📊 CSV Processing Pipeline

```
┌───────────────────┐
│   Upload CSV      │
└─────────┬─────────┘
          │
          ▼
┌────────────────────────────────────────┐
│  Serializer Validation                 │
│  ✓ File extension (.csv)               │
│  ✓ File size (< 10MB)                  │
└─────────┬──────────────────────────────┘
          │
          ▼
┌────────────────────────────────────────┐
│  Model Validation                      │
│  ✓ CSV file type                       │
└─────────┬──────────────────────────────┘
          │
          ▼
┌────────────────────────────────────────┐
│  Save to Storage                       │
│  • Check 5-upload limit                │
│  • Delete oldest if needed             │
│  • Save new file                       │
└─────────┬──────────────────────────────┘
          │
          ▼
┌────────────────────────────────────────┐
│  Service: Load with Pandas             │
│  df = pd.read_csv(file_path)           │
└─────────┬──────────────────────────────┘
          │
          ▼
┌────────────────────────────────────────┐
│  Service: Validate Columns             │
│  ✓ Equipment Name                      │
│  ✓ Type                                │
│  ✓ Flowrate (numeric)                  │
│  ✓ Pressure (numeric)                  │
│  ✓ Temperature (numeric)               │
└─────────┬──────────────────────────────┘
          │
          ▼
┌────────────────────────────────────────┐
│  Service: Compute Analytics            │
│  • total_equipment = len(df)           │
│  • average_flowrate = df.mean()        │
│  • average_pressure = df.mean()        │
│  • average_temperature = df.mean()     │
│  • equipment_distribution = counts()   │
└─────────┬──────────────────────────────┘
          │
          ▼
┌────────────────────────────────────────┐
│  Store Summary in Database             │
│  dataset.summary_json = {...}          │
└─────────┬──────────────────────────────┘
          │
          ▼
┌────────────────────────────────────────┐
│  Return Response                       │
│  HTTP 201 + summary data               │
└────────────────────────────────────────┘
```

---

## 🧪 Testing Workflow

```
┌──────────────────────────────────────────────────┐
│  Step 1: Start Server                           │
│  $ python manage.py runserver                   │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│  Step 2: Register User                          │
│  POST /api/auth/register/                       │
│  ➜ Get token                                    │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│  Step 3: Upload CSV                             │
│  POST /api/upload/                              │
│  Header: Authorization: Token <token>           │
│  ➜ Get summary                                  │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│  Step 4: Get Summary                            │
│  GET /api/summary/                              │
│  ➜ Verify analytics                             │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│  Step 5: Get Distribution                       │
│  GET /api/distribution/                         │
│  ➜ Verify type counts                           │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│  Step 6: Check History                          │
│  GET /api/history/                              │
│  ➜ Verify upload appears                        │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│  Step 7: Logout                                 │
│  POST /api/auth/logout/                         │
│  ➜ Token invalidated                            │
└──────────────────────────────────────────────────┘

Alternative: Run automated test script
$ python test_api.py
```

---

## 🎯 Quick Command Reference

### Setup Commands

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create admin (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver

# Run tests
python test_api.py
```

### Development Commands

```bash
# Make migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Check for issues
python manage.py check

# Collect static files
python manage.py collectstatic
```

---

## 📋 HTTP Status Codes Used

| Code | Meaning      | Usage                                           |
| ---- | ------------ | ----------------------------------------------- |
| 200  | OK           | Successful GET/POST (login, logout, summary)    |
| 201  | Created      | Successful resource creation (register, upload) |
| 400  | Bad Request  | Validation errors, invalid input                |
| 401  | Unauthorized | Missing or invalid token                        |
| 404  | Not Found    | No datasets found                               |
| 500  | Server Error | Unexpected server errors                        |

---

## 🔧 Configuration Checklist

### settings.py Key Settings

```python
# Debug (Development only)
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['*']  # Restrict in production

# Installed apps
'rest_framework'        # DRF
'rest_framework.authtoken'  # Token auth
'corsheaders'          # CORS support
'api'                  # Our app

# Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# CORS (allow React/PyQt5)
CORS_ALLOW_ALL_ORIGINS = True  # Dev only

# File limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Upload history
MAX_DATASET_HISTORY = 5
```

---

## 📦 Dependencies Overview

```
Django 4.2.9
├── Core framework
└── ORM, Auth, Admin

djangorestframework 3.14.0
├── REST API framework
├── Serializers
└── Token authentication

django-cors-headers 4.3.1
└── CORS middleware

pandas 2.1.4
├── CSV reading
└── Analytics computation

numpy 1.26.2
└── Pandas dependency

requests 2.31.0
└── Testing (test_api.py)
```

---

## 🎨 Response Format Examples

### Success Response (Upload)

```json
{
  "message": "Dataset uploaded successfully",
  "dataset": {
    "id": 1,
    "uploaded_at": "2026-02-04T10:30:45Z",
    "summary": {
      "total_equipment": 10,
      "average_flowrate": 141.34,
      "average_pressure": 329.0,
      "average_temperature": 91.59,
      "equipment_distribution": [
        { "type": "Centrifugal", "count": 2 },
        { "type": "Rotary", "count": 1 }
      ]
    }
  }
}
```

### Error Response (Validation)

```json
{
  "error": "CSV validation failed",
  "details": "Missing required columns: Pressure, Temperature"
}
```

---

## 🏆 Production Checklist

When deploying to production:

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper `SECRET_KEY`
- [ ] Configure `CORS_ALLOWED_ORIGINS` (specific domains)
- [ ] Use environment variables for secrets
- [ ] Set up HTTPS
- [ ] Configure static/media file serving
- [ ] Set up logging
- [ ] Enable database backups
- [ ] Add rate limiting
- [ ] Set up monitoring

---

## 📚 Documentation Navigation

```
📄 README.md              ➜ Start here (overview)
    │
    ├─ QUICKSTART.md      ➜ 5-minute setup guide
    │
    ├─ ARCHITECTURE.md    ➜ Design decisions explained
    │
    ├─ TESTING.md         ➜ Complete test cases
    │
    ├─ PROJECT_SUMMARY.md ➜ Final deliverables summary
    │
    └─ VISUAL_GUIDE.md    ➜ This file (quick reference)
```

---

## 🎯 Key Files to Review for Evaluation

1. **`api/models.py`** - See 5-upload limit enforcement
2. **`api/services/analytics.py`** - See Pandas analytics
3. **`api/views.py`** - See API endpoint implementations
4. **`api/serializers.py`** - See validation logic
5. **`backend/settings.py`** - See configuration

---

**This visual guide provides quick reference for common tasks and workflows.** 🎨

For detailed explanations, see the other documentation files.
