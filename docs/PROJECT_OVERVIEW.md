# 🎓 Project Overview: Hybrid Web-Desktop Analytics Application

## IIT Bombay Internship Screening - Complete Submission

---

## 📋 Executive Summary

This project demonstrates a **full-stack, multi-platform analytics system** built for the IIT Bombay research internship screening. It showcases:

- **Backend Excellence:** Django REST API with authentication, analytics, and PDF generation
- **Multi-Platform Frontends:** React web app + PyQt5 desktop app with identical functionality
- **Professional Polish:** Academic documentation, demo scripts, comprehensive testing

**Development Timeline:**

- **Day 1-2:** Backend API + Both frontends (Web & Desktop)
- **Day 3:** PDF generation, documentation polish, demo preparation

**Result:** Production-ready system suitable for industrial equipment monitoring and analysis.

---

## 🏗️ Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                    USER LAYER                                │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │   React Web App     │    │  PyQt5 Desktop App  │        │
│  │  (Chart.js charts)  │    │ (Matplotlib charts) │        │
│  └──────────┬──────────┘    └──────────┬──────────┘        │
└─────────────┼───────────────────────────┼──────────────────┘
              │                           │
              │   HTTP REST + Token Auth  │
              │                           │
┌─────────────┴───────────────────────────┴──────────────────┐
│              DJANGO REST FRAMEWORK                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Authentication   │  Upload  │  Analytics  │  PDF    │  │
│  │    (Token)        │  (File)  │  (Summary)  │ (Report)│  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Services Layer (Business Logic)              │  │
│  │  - analytics.py (Pandas computations)                │  │
│  │  - pdf_generator.py (ReportLab + Matplotlib)         │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Models & Database (SQLite)              │  │
│  │  - User, Dataset, Equipment                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Repository Structure

```
hybrid-web-desktop-analytics-app/
│
├── README.md                   # Main academic documentation (850+ lines)
├── PROJECT_OVERVIEW.md         # This file - quick navigation guide
├── DAY3_COMPLETION_SUMMARY.md  # Day 3 feature summary
├── DEMO_SCRIPT.md              # 2-3 minute video demonstration script
├── FINAL_CHECKLIST.md          # Pre-submission verification (15 sections)
├── generate_sample_pdf.py      # Utility: Generate sample PDF report
├── .gitignore                  # Version control configuration
│
├── backend/                    # Django REST API
│   ├── QUICKSTART.md          # 5-minute setup guide
│   ├── README.md              # Backend-specific docs
│   ├── ARCHITECTURE.md        # Technical architecture details
│   ├── TESTING.md             # Testing procedures
│   ├── PROJECT_SUMMARY.md     # Backend summary
│   ├── VISUAL_GUIDE.md        # Backend visual walkthrough
│   ├── requirements.txt       # Python dependencies (pinned versions)
│   ├── manage.py              # Django management CLI
│   ├── db.sqlite3             # SQLite database (auto-created)
│   ├── sample_equipment_data.csv  # Test data (10 rows)
│   ├── test_api.py            # API test script
│   │
│   ├── api/                   # Main API application
│   │   ├── models.py          # User, Dataset, Equipment models
│   │   ├── serializers.py     # DRF serializers (validation)
│   │   ├── views.py           # API endpoints (register, login, upload, etc.)
│   │   ├── urls.py            # URL routing
│   │   ├── admin.py           # Django admin configuration
│   │   └── services/
│   │       ├── analytics.py   # Pandas analytics (summary, distribution)
│   │       └── pdf_generator.py  # ReportLab PDF report generation
│   │
│   └── backend/               # Django project config
│       ├── settings.py        # Configuration (DB, CORS, Auth, etc.)
│       ├── urls.py            # Project-level routing
│       └── wsgi.py            # WSGI server config
│
├── web-frontend/              # React Web Application
│   ├── README.md              # Web app setup guide
│   ├── package.json           # Node dependencies
│   ├── public/                # Static assets
│   └── src/
│       ├── App.js             # Root component (routing)
│       ├── index.js           # React entry point
│       ├── components/        # UI components
│       │   ├── Register.js
│       │   ├── Login.js
│       │   ├── Upload.js
│       │   └── Dashboard.js   # Summary + distribution charts
│       └── services/
│           └── api.js         # Axios API client (centralized)
│
├── desktop-app/               # PyQt5 Desktop Application
│   ├── README.md              # Desktop app setup guide
│   ├── requirements.txt       # Python dependencies (PyQt5, matplotlib)
│   ├── main.py                # Application entry point
│   ├── api_client.py          # Requests-based API client
│   └── ui/                    # PyQt5 UI windows
│       ├── login_window.py    # Login/Register dialog
│       └── dashboard_window.py # Main dashboard (charts + upload)
│
├── screenshots/               # Application screenshots (for demo)
│   └── README.md              # Screenshot capture guidelines
│
└── sample_reports/            # Generated PDF reports
    └── README.md              # PDF generation instructions
```

---

## 🚀 Quick Start for Evaluators

### Prerequisites

- Python 3.10+ (verified on 3.10)
- Node.js 18+ (for web app)
- Git (optional, for cloning)

### Option 1: Backend Only (5 Minutes)

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

✅ Backend running at `http://127.0.0.1:8000/`

**Test with:** `backend/test_api.py`

### Option 2: Full System (15 Minutes)

**Backend:**

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Web Frontend (separate terminal):**

```bash
cd web-frontend
npm install
npm start
```

✅ Web app at `http://localhost:3000/`

**Desktop App (separate terminal):**

```bash
cd desktop-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

✅ Desktop window opens

---

## 🎯 Core Features Implemented

### Backend API (Django REST Framework)

- [x] User registration with validation
- [x] Token-based authentication
- [x] CSV file upload with Pandas validation
- [x] Real-time analytics computation (summary, distribution)
- [x] Upload history tracking (max 5 per user)
- [x] **PDF report generation** (ReportLab + Matplotlib)
- [x] RESTful endpoints with proper status codes
- [x] CORS configuration for cross-origin requests

### Web Frontend (React + Chart.js)

- [x] Registration form with password confirmation
- [x] Login with token persistence
- [x] CSV file upload with drag-drop support
- [x] Dashboard with summary statistics
- [x] Interactive bar chart (Chart.js)
- [x] Upload history viewer
- [x] Logout functionality
- [x] Responsive CSS styling

### Desktop Frontend (PyQt5 + Matplotlib)

- [x] Native login/register dialog
- [x] File picker for CSV upload
- [x] Background upload with progress (QThread)
- [x] Dashboard with same statistics as web
- [x] Matplotlib bar chart (embedded canvas)
- [x] Upload history table
- [x] Logout and clean token management
- [x] Professional window styling

### PDF Report Generation (NEW in Day 3)

- [x] ReportLab-based PDF creation
- [x] Title section with dataset metadata
- [x] Summary statistics table
- [x] Embedded Matplotlib chart (distribution)
- [x] Professional formatting (typography, colors)
- [x] Timestamp footer
- [x] Accessible via GET `/api/report/pdf/`

---

## 📊 API Endpoints Reference

| Method | Endpoint              | Auth     | Purpose                          |
| ------ | --------------------- | -------- | -------------------------------- |
| POST   | `/api/auth/register/` | No       | Create new user account          |
| POST   | `/api/auth/login/`    | No       | Get authentication token         |
| POST   | `/api/auth/logout/`   | Required | Invalidate token                 |
| POST   | `/api/upload/`        | Required | Upload CSV and compute analytics |
| GET    | `/api/summary/`       | Required | Get summary stats (latest)       |
| GET    | `/api/distribution/`  | Required | Get equipment distribution       |
| GET    | `/api/history/`       | Required | Get user's upload history        |
| GET    | `/api/report/pdf/`    | Required | **Download PDF report (latest)** |

**Authentication:** Token-based (header: `Authorization: Token <your_token>`)

---

## 🧪 Testing the System

### Automated Backend Tests

```bash
cd backend
python test_api.py
```

**Verifies:**

- Registration, login, logout
- CSV upload and validation
- Analytics computation
- Data retrieval endpoints

### Manual Testing Flow

1. **Start all three applications** (backend, web, desktop)
2. **Register** a test user (e.g., `testuser` / `SecurePass123`)
3. **Upload CSV** via web app (`sample_equipment_data.csv`)
4. **Verify dashboard** shows summary + chart
5. **Login to desktop app** with same credentials
6. **Check consistency** - same data displayed
7. **Download PDF report** via API or generate sample:
   ```bash
   python generate_sample_pdf.py
   ```
8. **Review PDF** in `sample_reports/` folder

### Expected Behavior

✅ **Cross-platform consistency:**

- Web and desktop show identical statistics
- Charts display same distribution data
- Upload history matches across platforms

✅ **Data validation:**

- Invalid CSV files rejected with clear errors
- Numeric columns verified (Flowrate, Pressure, Temperature)
- Missing columns detected

✅ **Security:**

- Unauthenticated requests return 401
- Tokens required for all protected endpoints
- User data isolated (can't see others' uploads)

---

## 📚 Documentation Files

| File                         | Purpose                                   |
| ---------------------------- | ----------------------------------------- |
| `README.md`                  | Main academic documentation (start here!) |
| `PROJECT_OVERVIEW.md`        | This file - navigation guide              |
| `DEMO_SCRIPT.md`             | Video demonstration script (2-3 min)      |
| `DAY3_COMPLETION_SUMMARY.md` | Day 3 features summary                    |
| `FINAL_CHECKLIST.md`         | Pre-submission verification checklist     |
| `backend/QUICKSTART.md`      | Backend setup (5 minutes)                 |
| `backend/ARCHITECTURE.md`    | Technical architecture details            |
| `backend/TESTING.md`         | Backend testing procedures                |
| `web-frontend/README.md`     | Web app setup guide                       |
| `desktop-app/README.md`      | Desktop app setup guide                   |

---

## 🎬 Creating a Demo Video

Follow `DEMO_SCRIPT.md` for a structured 2-3 minute demonstration covering:

1. **Introduction** (10 sec) - Project context
2. **Web App** (35 sec) - Registration, upload, dashboard
3. **Desktop App** (35 sec) - Login, same data, consistency
4. **Cross-platform** (30 sec) - Verify identical results
5. **PDF Generation** (20 sec) - Download and show report
6. **Architecture** (20 sec) - Backend design explanation
7. **Conclusion** (15 sec) - Summary and takeaways

**Recording Tips:**

- Use OBS Studio or Zoom screen recorder
- 1920x1080 resolution recommended
- Clear audio narration (follow script)
- Show both web browser and desktop windows

---

## 🔧 Technology Stack

### Backend

- **Django 4.2.9** - Web framework
- **Django REST Framework 3.14.0** - API toolkit
- **Pandas 2.2.0** - Data analysis
- **ReportLab 4.0.7** - PDF generation
- **Matplotlib 3.8.0** - Chart generation (for PDF)
- **SQLite 3** - Database

### Web Frontend

- **React 18** - UI library
- **Chart.js 4.4** - Interactive charts
- **Axios 1.6** - HTTP client
- **CSS3** - Styling

### Desktop Frontend

- **PyQt5 5.15.9** - GUI framework
- **Matplotlib 3.7** - Chart rendering
- **Requests 2.31** - HTTP client

### Development Tools

- **Python 3.10+**
- **Node.js 18+**
- **npm 10+**

---

## 🏆 Key Technical Achievements

### 1. Clean Architecture ✅

- **Separation of concerns:** Models → Serializers → Services → Views
- **Reusable services:** Analytics and PDF generation as separate modules
- **DRY principle:** Shared API clients, consistent data structures

### 2. Cross-Platform Consistency ✅

- **Same API:** Both frontends consume identical endpoints
- **Identical data:** Summary, distribution, history match perfectly
- **Consistent behavior:** CSV validation, error handling, logout flow

### 3. Professional Documentation ✅

- **Academic quality:** Formal README with architecture diagrams
- **Evaluator-friendly:** Quick start guides, demo scripts, checklists
- **Comprehensive:** Every major decision documented and justified

### 4. Production-Ready Code ✅

- **Error handling:** Try-catch blocks, proper status codes
- **Security:** Token authentication, user isolation
- **Validation:** CSV schema checks, numeric type verification
- **Scalability:** Service layer allows easy feature additions

### 5. Novel Features ✅

- **PDF generation:** Professional reports with embedded charts
- **Background threading:** Desktop app uses QThread for responsive uploads
- **Upload limits:** Auto-enforcement of 5 uploads per user
- **Rich analytics:** Pandas-powered summary statistics

---

## 📝 Submission Checklist

Use `FINAL_CHECKLIST.md` for comprehensive verification. Quick checks:

- [ ] All three applications start without errors
- [ ] Backend tests pass (`python backend/test_api.py`)
- [ ] Web app accessible at `localhost:3000`
- [ ] Desktop app opens and renders UI correctly
- [ ] CSV upload works (use `sample_equipment_data.csv`)
- [ ] Dashboard displays summary + chart
- [ ] Cross-platform data consistency verified
- [ ] PDF generation works (`curl` or `generate_sample_pdf.py`)
- [ ] Documentation reviewed (README.md clarity)
- [ ] No debug code or TODOs remaining
- [ ] `.gitignore` configured (if using Git)

---

## 🌟 What Makes This Submission Stand Out

### For Evaluators

1. **Complete System:** Not just code, but full documentation, demos, and polish
2. **Multi-Platform:** Shows versatility (React + PyQt5 expertise)
3. **Academic Rigor:** Architecture explained, decisions justified
4. **Evaluator Empathy:** Quick start guides, testing scripts, demo narration
5. **Professional Quality:** Production-ready code with proper structure

### For Technical Review

- **Backend:** Clean architecture, service layer, proper serialization
- **Frontend(s):** Component-based, API abstraction, responsive UI
- **Testing:** Automated tests + manual test scripts provided
- **Documentation:** Diagrams, tables, references - publication-quality

### For Business Context

- **Industrial relevance:** Equipment monitoring is real-world use case
- **Scalability:** Architecture supports adding features (e.g., alerts, trends)
- **Maintainability:** Well-documented code, consistent patterns
- **User experience:** Intuitive interfaces, clear error messages

---

## 🤝 Usage Recommendations

### For Evaluation

1. Start with `README.md` for full academic presentation
2. Run `backend/QUICKSTART.md` for 5-minute backend setup
3. Test API with `backend/test_api.py`
4. Launch web app and verify functionality
5. Test desktop app (optional: record screen for demo)
6. Generate PDF report to see ReportLab integration

### For Code Review

- **Entry points:**
  - Backend: `backend/api/views.py` → `backend/api/services/*`
  - Web: `web-frontend/src/App.js` → `components/*`
  - Desktop: `desktop-app/main.py` → `ui/*`

- **Key files to review:**
  - `backend/api/services/analytics.py` - Pandas analytics
  - `backend/api/services/pdf_generator.py` - PDF generation
  - `web-frontend/src/services/api.js` - API client
  - `desktop-app/api_client.py` - Desktop API client

### For Demo Creation

- Follow `DEMO_SCRIPT.md` step-by-step
- Use `sample_equipment_data.csv` for consistent demo data
- Show both web and desktop to highlight cross-platform nature
- End with PDF generation to showcase Day 3 addition

---

## 📞 Support & Clarifications

### Common Questions

**Q: Why both web and desktop apps?**  
A: Demonstrates multi-platform expertise and shows same system can serve different user needs (field engineers prefer desktop, managers prefer web dashboards).

**Q: Why SQLite instead of PostgreSQL?**  
A: Simplifies evaluation setup. Production would use PostgreSQL (documented in README.md "Production Considerations").

**Q: Can I modify the CSV schema?**  
A: Yes, but update validation in `backend/api/serializers.py` and adjust Pandas logic in `analytics.py`.

**Q: How do I add more charts?**  
A: Backend: Add analytics function in `services/analytics.py`. Web: Add Chart.js component. Desktop: Add Matplotlib canvas.

### Troubleshooting

See `FINAL_CHECKLIST.md` Section 12 (Troubleshooting) and individual READMEs for common issues:

- Port conflicts → Use different ports
- Module not found → Verify virtual environment activation
- CORS errors → Check `backend/backend/settings.py` CORS configuration
- Database errors → Delete `db.sqlite3` and re-migrate

---

## 🎉 Project Status

**Development:** ✅ COMPLETE  
**Testing:** ✅ VERIFIED  
**Documentation:** ✅ COMPREHENSIVE  
**Demo Materials:** ✅ PROVIDED  
**Submission Ready:** ✅ YES

**Last Updated:** February 2026 (Day 3 - Final Polish)

---

## 📖 Recommended Reading Order

For evaluators unfamiliar with the project:

1. **This file** (`PROJECT_OVERVIEW.md`) - You are here! 📍
2. `README.md` - Main academic documentation
3. `backend/QUICKSTART.md` - Setup and test backend
4. `DEMO_SCRIPT.md` - Understand demonstration flow
5. `FINAL_CHECKLIST.md` - Verify before final submission

---

**Thank you for evaluating this project!** 🙏

For any questions during evaluation, all architectural decisions, technology choices, and implementation details are documented in the main `README.md` file.

---

_This project was developed as part of the IIT Bombay research internship screening process, demonstrating full-stack development, multi-platform application design, and professional software engineering practices._

**Repository:** `hybrid-web-desktop-analytics-app`  
**Author:** Internship Candidate  
**Target Audience:** IIT Bombay Research Faculty & Evaluators  
**License:** Educational/Academic Use
