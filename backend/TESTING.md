# 🧪 API Testing Guide

Complete test cases for all backend endpoints with expected inputs/outputs.

---

## 🔧 Setup

**Base URL**: `http://127.0.0.1:8000`

**Headers for authenticated requests**:

```json
{
  "Authorization": "Token YOUR_TOKEN_HERE"
}
```

---

## 1️⃣ Authentication Tests

### Test 1.1: Register User (Success)

**Endpoint**: `POST /api/auth/register/`

**Request**:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123"
}
```

**Expected Response** (201):

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

### Test 1.2: Register User (Duplicate Username)

**Request**:

```json
{
  "username": "testuser",
  "email": "new@example.com",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123"
}
```

**Expected Response** (400):

```json
{
  "error": "Registration failed",
  "details": {
    "username": ["A user with that username already exists."]
  }
}
```

---

### Test 1.3: Register User (Password Mismatch)

**Request**:

```json
{
  "username": "user2",
  "email": "user2@example.com",
  "password": "SecurePass123",
  "password_confirm": "DifferentPass456"
}
```

**Expected Response** (400):

```json
{
  "error": "Registration failed",
  "details": {
    "password": ["Password fields didn't match."]
  }
}
```

---

### Test 1.4: Login User (Success)

**Endpoint**: `POST /api/auth/login/`

**Request**:

```json
{
  "username": "testuser",
  "password": "SecurePass123"
}
```

**Expected Response** (200):

```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

### Test 1.5: Login User (Invalid Credentials)

**Request**:

```json
{
  "username": "testuser",
  "password": "WrongPassword"
}
```

**Expected Response** (400):

```json
{
  "error": "Invalid credentials",
  "details": "Username or password is incorrect"
}
```

---

### Test 1.6: Logout User (Success)

**Endpoint**: `POST /api/auth/logout/`

**Headers**: `Authorization: Token YOUR_TOKEN`

**Expected Response** (200):

```json
{
  "message": "Logout successful"
}
```

---

### Test 1.7: Access Protected Endpoint Without Token

**Endpoint**: `GET /api/summary/`

**No Authorization Header**

**Expected Response** (401):

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 2️⃣ Dataset Upload Tests

### Test 2.1: Upload Valid CSV (Success)

**Endpoint**: `POST /api/upload/`

**Headers**: `Authorization: Token YOUR_TOKEN`

**Request** (multipart/form-data):

```
file: sample_equipment_data.csv
```

**CSV Content**:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Centrifugal,150.5,300,85.2
Compressor B,Rotary,200.0,450,95.0
Valve C,Gate,50.25,200,70.5
```

**Expected Response** (201):

```json
{
  "message": "Dataset uploaded successfully",
  "dataset": {
    "id": 1,
    "uploaded_at": "2026-02-04T10:30:45.123456Z",
    "summary": {
      "total_equipment": 3,
      "average_flowrate": 133.58,
      "average_pressure": 316.67,
      "average_temperature": 83.57,
      "equipment_distribution": [
        { "type": "Centrifugal", "count": 1 },
        { "type": "Rotary", "count": 1 },
        { "type": "Gate", "count": 1 }
      ]
    }
  }
}
```

---

### Test 2.2: Upload Invalid File Type

**Request** (multipart/form-data):

```
file: document.pdf
```

**Expected Response** (400):

```json
{
  "error": "Validation failed",
  "details": {
    "file": ["Only CSV files are allowed."]
  }
}
```

---

### Test 2.3: Upload CSV with Missing Columns

**CSV Content**:

```csv
Equipment Name,Type,Flowrate
Pump A,Centrifugal,150.5
```

**Expected Response** (400):

```json
{
  "error": "CSV validation failed",
  "details": "Missing required columns: Pressure, Temperature. Required columns are: Equipment Name, Type, Flowrate, Pressure, Temperature"
}
```

---

### Test 2.4: Upload CSV with Non-Numeric Values

**CSV Content**:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Centrifugal,invalid,300,85.2
```

**Expected Response** (400):

```json
{
  "error": "CSV validation failed",
  "details": "Column 'Flowrate' must contain only numeric values. Found invalid values: ['invalid']"
}
```

---

### Test 2.5: Upload CSV Exceeding Size Limit

**Request** (multipart/form-data):

```
file: large_file.csv (> 10MB)
```

**Expected Response** (400):

```json
{
  "error": "Validation failed",
  "details": {
    "file": ["File size must not exceed 10MB."]
  }
}
```

---

### Test 2.6: Verify 5-Upload Limit

**Steps**:

1. Upload 5 CSV files successfully
2. Upload 6th CSV file
3. Check history - should only show 5 most recent

**Expected Behavior**:

- Oldest upload automatically deleted
- Only last 5 uploads visible in history

---

## 3️⃣ Analytics Tests

### Test 3.1: Get Summary (Success)

**Endpoint**: `GET /api/summary/`

**Headers**: `Authorization: Token YOUR_TOKEN`

**Expected Response** (200):

```json
{
  "total_equipment": 3,
  "average_flowrate": 133.58,
  "average_pressure": 316.67,
  "average_temperature": 83.57
}
```

---

### Test 3.2: Get Summary (No Datasets)

**Scenario**: User hasn't uploaded any CSV yet

**Expected Response** (404):

```json
{
  "error": "No datasets found",
  "details": "Please upload a dataset first"
}
```

---

### Test 3.3: Get Distribution (Success)

**Endpoint**: `GET /api/distribution/`

**Headers**: `Authorization: Token YOUR_TOKEN`

**Expected Response** (200):

```json
{
  "distribution": [
    { "type": "Centrifugal", "count": 2 },
    { "type": "Rotary", "count": 1 },
    { "type": "Gate", "count": 1 },
    { "type": "Steam", "count": 1 }
  ]
}
```

---

### Test 3.4: Get Distribution (No Datasets)

**Expected Response** (404):

```json
{
  "error": "No datasets found",
  "details": "Please upload a dataset first"
}
```

---

## 4️⃣ History Tests

### Test 4.1: Get History (Empty)

**Endpoint**: `GET /api/history/`

**Headers**: `Authorization: Token YOUR_TOKEN`

**Scenario**: No uploads yet

**Expected Response** (200):

```json
{
  "history": []
}
```

---

### Test 4.2: Get History (With Uploads)

**Scenario**: User uploaded 3 CSV files

**Expected Response** (200):

```json
{
  "history": [
    {
      "id": 3,
      "file": "/media/datasets/sample_data_3.csv",
      "uploaded_at": "2026-02-04T12:00:00.000000Z"
    },
    {
      "id": 2,
      "file": "/media/datasets/sample_data_2.csv",
      "uploaded_at": "2026-02-04T11:00:00.000000Z"
    },
    {
      "id": 1,
      "file": "/media/datasets/sample_data_1.csv",
      "uploaded_at": "2026-02-04T10:00:00.000000Z"
    }
  ]
}
```

**Note**: Ordered by most recent first

---

## 5️⃣ Complete Workflow Test

### Test 5.1: Full User Journey

**Step 1**: Register

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"journeytest","email":"journey@test.com","password":"Pass123","password_confirm":"Pass123"}'
```

**Step 2**: Extract token from response

**Step 3**: Upload CSV

```bash
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@sample_equipment_data.csv"
```

**Step 4**: Get Summary

```bash
curl -X GET http://127.0.0.1:8000/api/summary/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Step 5**: Get Distribution

```bash
curl -X GET http://127.0.0.1:8000/api/distribution/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Step 6**: Get History

```bash
curl -X GET http://127.0.0.1:8000/api/history/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Step 7**: Logout

```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Step 8**: Try accessing summary (should fail)

```bash
curl -X GET http://127.0.0.1:8000/api/summary/ \
  -H "Authorization: Token YOUR_TOKEN"
# Expected: 401 Unauthorized
```

---

## 6️⃣ Edge Cases

### Test 6.1: Empty CSV File

**CSV Content**:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
```

**Expected Response** (400):

```json
{
  "error": "CSV validation failed",
  "details": "CSV file is empty"
}
```

---

### Test 6.2: CSV with Extra Columns

**CSV Content**:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature,Extra Column
Pump A,Centrifugal,150.5,300,85.2,ignored
```

**Expected Response** (201):

- Should succeed (extra columns ignored)
- Summary computed correctly

---

### Test 6.3: CSV with Missing Values

**CSV Content**:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Centrifugal,150.5,,85.2
```

**Expected Response** (201):

- Should succeed
- Average pressure computed ignoring NaN values

---

### Test 6.4: Concurrent Uploads (Same User)

**Scenario**:

- Start upload 1
- Before upload 1 completes, start upload 2

**Expected Behavior**:

- Both uploads processed
- Only last 5 kept
- No race condition errors

---

## 7️⃣ Security Tests

### Test 7.1: SQL Injection Attempt

**Request**:

```json
{
  "username": "admin' OR '1'='1",
  "password": "password"
}
```

**Expected Response** (400):

- Login fails
- No SQL injection successful

---

### Test 7.2: Path Traversal in CSV Upload

**Request** (multipart/form-data):

```
file: ../../etc/passwd (renamed to passwd.csv)
```

**Expected Behavior**:

- File stored in designated `media/datasets/` directory
- No path traversal

---

### Test 7.3: Access Another User's Data

**Scenario**:

1. User A uploads CSV
2. User B tries to access User A's summary

**Expected Response** (404):

- User B sees "No datasets found"
- Data isolation maintained

---

## 📊 Performance Tests

### Test 8.1: Large CSV (Within Limit)

**CSV Size**: 9MB, ~100,000 rows

**Expected**:

- Upload succeeds
- Processing time < 10 seconds
- Summary computed correctly

---

### Test 8.2: Multiple Sequential Uploads

**Scenario**: Upload 10 CSV files sequentially

**Expected**:

- All uploads succeed
- Only last 5 retained
- No memory leaks

---

## ✅ Test Coverage Summary

| Category       | Tests | Coverage |
| -------------- | ----- | -------- |
| Authentication | 7     | 100%     |
| Upload         | 6     | 100%     |
| Analytics      | 4     | 100%     |
| History        | 2     | 100%     |
| Edge Cases     | 4     | 95%      |
| Security       | 3     | Basic    |
| Performance    | 2     | Basic    |

---

## 🛠️ Running Tests with Postman

1. Import the `POSTMAN_COLLECTION.json` (if provided)
2. Set environment variable `BASE_URL` = `http://127.0.0.1:8000`
3. Run "Register User" first to get token
4. Save token in environment variable `AUTH_TOKEN`
5. Run remaining tests in order

---

## 🧩 Python Unit Tests (Future)

```python
# tests/test_services.py
from api.services.analytics import compute_summary_statistics

def test_compute_summary_valid_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("Equipment Name,Type,Flowrate,Pressure,Temperature\n"
                       "Pump A,Centrifugal,150,300,85\n")

    result = compute_summary_statistics(str(csv_file))

    assert result['total_equipment'] == 1
    assert result['average_flowrate'] == 150.0
```

---

**All tests should pass for successful IIT Bombay evaluation** ✅
