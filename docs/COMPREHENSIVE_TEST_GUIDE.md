# 🧪 Comprehensive Test Suite

## IIT Bombay Analytics - Complete Application Testing

**Purpose:** Verify all components work correctly before submission  
**Duration:** ~10 minutes  
**Date:** February 9, 2026

---

## ✅ Pre-Test Checklist

- [ ] Backend server NOT running (we'll start it fresh)
- [ ] No conflicting processes on ports 8000 or 3000
- [ ] Clean terminal windows available

---

## 🔧 Test 1: Backend Complete Test

### 1.1 Setup & Start

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Expected:**

```
System check identified no issues (0 silenced).
Django version 4.2.9, using settings 'backend.settings'
Starting development server at http://127.0.0.1:8000/
```

✅ **PASS if:** Server starts without errors

### 1.2 Run Automated API Tests

**In a new terminal:**

```powershell
cd backend
venv\Scripts\activate
python test_api.py
```

**Expected Output:**

```
✅ ALL TESTS COMPLETED!
Backend is working correctly! 🎉
```

✅ **PASS if:** All 9 API tests pass (register, login, upload, summary, distribution, history, logout, auth check)

### 1.3 PDF Generation Test

**While server is running:**

```powershell
cd C:\Users\Admin\Desktop\hybrid-web-desktop-analytics-app
python generate_sample_pdf.py
```

**Expected:**

```
✓ Sample report generated: C:\...\sample_reports\sample_analysis_report.pdf
File size: ~23 KB
```

**Verify:** Open PDF file, check:

- [ ] Title section visible
- [ ] Summary statistics table rendered
- [ ] Bar chart embedded correctly
- [ ] Footer with timestamp

✅ **PASS if:** PDF opens and contains all sections

---

## 🌐 Test 2: Web Frontend Test

### 2.1 Setup & Start

**New terminal:**

```powershell
cd web-frontend
npm install
npm start
```

**Expected:**

- Dependencies install successfully
- Browser opens to http://localhost:3000
- No console errors

⏱️ **Duration:** ~3-5 minutes for npm install

### 2.2 Manual Test Flow

#### Registration

1. Click "Register" tab
2. Fill form:
   - Username: `webuser`
   - Email: `web@test.com`
   - Password: `SecurePass123`
   - Confirm: `SecurePass123`
3. Click "Register"

✅ **PASS if:** "Registration successful! Redirecting..." message appears

#### Upload

4. Click "Choose File"
5. Select `backend/sample_equipment_data.csv`
6. Click "Upload Dataset"

✅ **PASS if:**

- Upload progress shows
- "Upload successful!" message
- Dashboard renders

#### Dashboard Verification

7. Check Summary Section:
   - [ ] Total Equipment: 15
   - [ ] Average Flowrate: 119.8
   - [ ] Average Pressure: 6.11
   - [ ] Average Temperature: 117.47

8. Check Chart:
   - [ ] Bar chart visible
   - [ ] 6 equipment types shown
   - [ ] Labels readable

9. Check Upload History:
   - [ ] 1 upload listed
   - [ ] Filename shown
   - [ ] Timestamp visible

#### Logout

10. Click "Logout"

✅ **PASS if:** Returns to login screen

---

## 🖥️ Test 3: Desktop Application Test

### 3.1 Setup & Start

**New terminal:**

```powershell
cd desktop-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Expected:**

- Window opens with "Login / Register" dialog
- No console errors

### 3.2 Manual Test Flow

#### Login

1. Tab to "Login"
2. Enter:
   - Username: `webuser`
   - Password: `SecurePass123`
3. Click "Login"

✅ **PASS if:** Dashboard window opens

#### Cross-Platform Verification

4. Check Summary Section:
   - [ ] Total Equipment: 15 (same as web)
   - [ ] Average Flowrate: 119.8 (same as web)
   - [ ] Average Pressure: 6.11 (same as web)
   - [ ] Average Temperature: 117.47 (same as web)

5. Check Chart:
   - [ ] Matplotlib bar chart visible
   - [ ] Same 6 equipment types
   - [ ] Same counts as web app

6. Check Upload History Table:
   - [ ] Same upload entry as web
   - [ ] Matches timestamp

✅ **CRITICAL PASS:** Desktop shows IDENTICAL data to web app

#### Upload from Desktop

7. Click "Upload CSV"
8. Select `backend/sample_equipment_data.csv`
9. Click "Open"

✅ **PASS if:**

- Progress bar shows activity
- Success message displayed
- Chart updates (or stays same if same file)

#### Logout

10. Click "Logout"

✅ **PASS if:** Returns to login dialog

---

## 🔄 Test 4: Cross-Platform Consistency Test

### Objective: Verify both clients see same data

1. Login to **web app** (browser)
2. Login to **desktop app** (simultaneously)
3. Upload CSV from **web app**
4. Click refresh or reload in **web dashboard**
5. Click "Logout" then "Login" in **desktop app**

✅ **PASS if:** Both show same upload count, same statistics, same history

---

## 📄 Test 5: PDF API Endpoint Test

### 5.1 Get Fresh Token

**Use test_api.py or login via web/desktop to get token**

### 5.2 Test PDF Download

```powershell
# Replace TOKEN with actual token from login
$token = "YOUR_TOKEN_HERE"
$headers = @{"Authorization" = "Token $token"}
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/report/pdf/" -Headers $headers -OutFile "downloaded_report.pdf"

# Verify
if (Test-Path downloaded_report.pdf) {
    Write-Host "✅ PDF API working: $((Get-Item downloaded_report.pdf).Length) bytes"
    Start-Process downloaded_report.pdf
} else {
    Write-Host "❌ PDF download failed"
}
```

✅ **PASS if:** PDF downloads and opens correctly

---

## 📊 Test Summary Matrix

| Component   | Test                    | Status | Notes              |
| ----------- | ----------------------- | ------ | ------------------ |
| Backend     | Server Start            | ⬜     | Port 8000          |
| Backend     | API Tests (9 endpoints) | ⬜     | test_api.py        |
| Backend     | PDF Generation          | ⬜     | 23KB PDF           |
| Backend     | PDF API Endpoint        | ⬜     | Download via token |
| Web         | Installation            | ⬜     | npm install        |
| Web         | Registration            | ⬜     | New user           |
| Web         | CSV Upload              | ⬜     | 15 equipment       |
| Web         | Dashboard               | ⬜     | Stats + Chart      |
| Web         | Logout                  | ⬜     | Token cleared      |
| Desktop     | Installation            | ⬜     | pip install        |
| Desktop     | Login                   | ⬜     | Existing user      |
| Desktop     | Dashboard               | ⬜     | Same data as web   |
| Desktop     | CSV Upload              | ⬜     | Background thread  |
| Desktop     | Logout                  | ⬜     | Return to login    |
| Consistency | Cross-platform          | ⬜     | Web == Desktop     |

---

## 🚨 Common Issues & Fixes

### Issue 1: "Port 8000 already in use"

**Solution:**

```powershell
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue 2: "Module not found" errors

**Solution:**

```powershell
# Ensure venv is activated
venv\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: Web app "Network Error"

**Check:**

- Backend server is running
- URL is http://127.0.0.1:8000 (not localhost)
- CORS configured in backend/settings.py

### Issue 4: Desktop app freezes on upload

**This is EXPECTED:** UI may freeze briefly during upload (non-threaded operations)
**If persistent:** Check backend logs for errors

### Issue 5: "Invalid token" errors

**Solution:** Token expired or wrong. Login again to get fresh token.

---

## ✅ Final Verification

### All Tests Passed?

- [ ] Backend: 9/9 API tests pass
- [ ] Backend: PDF generation works
- [ ] Web: Complete user flow works
- [ ] Desktop: Complete user flow works
- [ ] Cross-platform: Data matches exactly

### Submission Ready

If all boxes checked:

**🎉 YOUR APPLICATION IS 100% FUNCTIONAL AND READY FOR SUBMISSION! 🎉**

---

## 📝 Test Log Template

**Date:** **\_\_\_**  
**Tester:** **\_\_\_**  
**Environment:** Windows / macOS / Linux

**Results:**

| Test              | Pass/Fail       | Notes |
| ----------------- | --------------- | ----- |
| Backend API       | ⬜ Pass ⬜ Fail |       |
| Backend PDF       | ⬜ Pass ⬜ Fail |       |
| Web Registration  | ⬜ Pass ⬜ Fail |       |
| Web Upload        | ⬜ Pass ⬜ Fail |       |
| Web Dashboard     | ⬜ Pass ⬜ Fail |       |
| Desktop Login     | ⬜ Pass ⬜ Fail |       |
| Desktop Upload    | ⬜ Pass ⬜ Fail |       |
| Desktop Dashboard | ⬜ Pass ⬜ Fail |       |
| Data Consistency  | ⬜ Pass ⬜ Fail |       |

**Overall Status:** ⬜ PASS ⬜ FAIL

**Issues Encountered:**

---

**Resolution:**

---

---

**For Evaluators:** Run this test suite to verify the complete system. Expected time: 10 minutes for full verification.
