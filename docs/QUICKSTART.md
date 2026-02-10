# Quick Start Guide - IIT Bombay Analytics

## Complete Setup in 3 Terminals

### Terminal 1: Backend Server

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Backend ready at:** http://localhost:8000

### Terminal 2: Web Application

```bash
cd web-frontend
npm install
npm start
```

**Web app opens at:** http://localhost:3000

### Terminal 3: Desktop Application

```bash
cd desktop-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Desktop app window opens automatically**

---

## First Time Setup

### Create Test User

**Option 1: Django Shell**

```bash
cd backend
python manage.py shell
```

```python
from django.contrib.auth.models import User
User.objects.create_user('testuser', 'test@example.com', 'TestPass123')
exit()
```

**Option 2: Use Registration in Apps**
Both web and desktop apps support registration.

---

## Using the Applications

### 1. Login

- Username: `testuser`
- Password: `TestPass123`

### 2. Upload CSV

Use the sample file: `backend/sample_equipment_data.csv`

### 3. View Analytics

- Summary statistics appear in table
- Distribution chart shows equipment types
- History shows your uploads

---

## Verification Checklist

✅ Backend responds at http://localhost:8000/api/  
✅ Web app loads at http://localhost:3000  
✅ Desktop app window opens  
✅ Login works on both apps  
✅ CSV upload succeeds  
✅ Charts display data

---

## Common Issues

**Backend won't start:**

- Check Python version (3.8+)
- Ensure `pip install -r requirements.txt` completed

**Web app won't start:**

- Check Node.js version (16+)
- Delete `node_modules` and run `npm install` again

**Desktop app won't start:**

- Check PyQt5 installed: `pip list | grep PyQt5`
- Reinstall: `pip install --force-reinstall PyQt5`

**CORS errors:**

- Backend settings.py has CORS_ALLOW_ALL_ORIGINS = True
- Restart backend server

---

## What to Expect

### Web Application

- Modern React interface
- Token stored in localStorage
- Chart.js bar chart
- Responsive design

### Desktop Application

- Native PyQt5 window
- Token in memory only
- Matplotlib embedded chart
- Background upload (no freezing)

### Both Show Identical:

- Summary statistics
- Equipment distribution
- Upload history
- Error messages

---

## Quick Test Scenario

1. Start all 3 terminals
2. Login to web app
3. Upload CSV
4. Note the summary statistics
5. Login to desktop app
6. See **same** statistics
7. Upload another CSV from desktop
8. Refresh web app (F5)
9. See **same** updated data

This proves: **Two clients, one system.**

---

## Time Estimate

- Backend setup: 3 minutes
- Web app setup: 2 minutes
- Desktop app setup: 2 minutes
- First login + test: 2 minutes

**Total: ~10 minutes** from clone to working applications.

---

## Next Steps

See individual README files:

- [backend/README.md](backend/README.md) - Backend details
- [web-frontend/README.md](web-frontend/README.md) - React app guide
- [desktop-app/README.md](desktop-app/README.md) - PyQt5 app guide

Main project README: [README.md](README.md)
