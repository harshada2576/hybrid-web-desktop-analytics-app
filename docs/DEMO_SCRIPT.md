# Demo Video Script

## IIT Bombay Analytics Application

### Duration: 2-3 minutes

---

## Pre-Recording Checklist

- [ ] Start all three terminals (backend, web, desktop)
- [ ] Clear browser cache and localStorage
- [ ] Close desktop app if running
- [ ] Have `sample_equipment_data.csv` ready
- [ ] Test user credentials ready (`testuser` / `TestPass123`)
- [ ] Screen recorder ready (OBS, QuickTime, etc.)
- [ ] Audio microphone tested

---

## Script: Narration and Actions

### [00:00 - 00:10] Introduction (10 seconds)

**[SCREEN: Show project folder structure or title slide]**

**NARRATE:**

> "Hello. This is my submission for the IIT Bombay internship screening task. I've built a hybrid analytics application with a Django REST backend serving both a React web client and a PyQt5 desktop client. Let me demonstrate how they work together."

**ACTION:** Open terminal showing three running processes (backend, web, desktop)

---

### [00:10 - 00:45] Web Application Demo (35 seconds)

**[SCREEN: Browser with http://localhost:3000]**

**NARRATE:**

> "First, the web application. I'm logging in with my test credentials..."

**ACTION:**

- Type username: `testuser`
- Type password: `TestPass123`
- Click "Login"

**[SCREEN: Dashboard appears]**

**NARRATE:**

> "The dashboard loads. Now I'll upload a CSV file containing equipment data."

**ACTION:**

- Click "Choose File"
- Select `sample_equipment_data.csv`
- Click "Upload"

**[SCREEN: Analytics appear]**

**NARRATE:**

> "Immediately, we see summary statistics: total equipment count, average flowrate, pressure, and temperature. Below is a Chart.js visualization showing the distribution by equipment type—four pumps, three valves, and three compressors. The upload history shows this is the first dataset."

**ACTION:** Point cursor to:

- Summary table
- Distribution chart
- History section

---

### [00:45 - 01:20] Desktop Application Demo (35 seconds)

**[SCREEN: Desktop application window]**

**NARRATE:**

> "Now, the desktop application built with PyQt5. I'll log in using the same credentials."

**ACTION:**

- Enter username: `testuser`
- Enter password: `TestPass123`
- Click "Login"

**[SCREEN: Desktop dashboard appears]**

**NARRATE:**

> "Notice the interface is different—native desktop UI with Qt widgets—but the data is identical. Same summary statistics, same distribution chart rendered with Matplotlib instead of Chart.js, and same upload history showing one entry."

**ACTION:** Point to:

- Summary statistics table
- Matplotlib bar chart
- Upload history table

**NARRATE:**

> "Let me upload another dataset from the desktop app."

**ACTION:**

- Click "Select CSV File"
- Choose another CSV (or same file)
- Click "Upload"
- Show upload progress (brief loading state)

**[SCREEN: Desktop dashboard updates]**

**NARRATE:**

> "The upload happens in a background thread, so the UI doesn't freeze. The analytics update immediately."

---

### [01:20 - 01:50] Cross-Platform Consistency (30 seconds)

**[SCREEN: Switch back to web browser, press F5 to refresh]**

**NARRATE:**

> "Switching back to the web application and refreshing... the history now shows two uploads. The same data appears in both clients because both are consuming the same Django REST API."

**ACTION:**

- Refresh browser (F5)
- Show updated history with 2 entries
- Scroll through dashboard

**[SCREEN: Split screen or quick cuts between web and desktop]**

**NARRATE:**

> "Both applications use identical terminology: 'Total Equipment,' 'Average Flowrate,' 'Average Pressure,' 'Average Temperature.' The distribution charts show the same data with different rendering libraries."

**ACTION:** Highlight matching elements side-by-side (if possible)

---

### [01:50 - 02:10] PDF Report Generation (20 seconds)

**[SCREEN: Browser or terminal]**

**NARRATE:**

> "The system also generates PDF reports. I'll request one through the API."

**ACTION:**

- Option A: Click a "Download PDF" button (if wired in UI)
- Option B: Use curl command in terminal:
  ```bash
  curl -H "Authorization: Token YOUR_TOKEN" \
       http://localhost:8000/api/report/pdf/ \
       -o report.pdf
  ```

**[SCREEN: Open generated PDF]**

**NARRATE:**

> "The PDF contains the title, summary statistics table, and an embedded distribution chart—a complete analytical report ready for stakeholders."

**ACTION:** Scroll through PDF showing:

- Title section
- Summary table
- Distribution chart
- Footer

---

### [02:10 - 02:30] Backend Architecture (20 seconds)

**[SCREEN: Code editor showing project structure or architecture diagram]**

**NARRATE:**

> "Behind the scenes, the Django backend uses a layered architecture. Views handle HTTP requests, the service layer contains Pandas-based analytics logic, and serializers validate data. This separation makes the code testable and maintainable."

**ACTION:** Briefly show:

- `backend/api/views.py` (thin views)
- `backend/api/services/analytics.py` (business logic)
- `backend/api/models.py` (data layer)

---

### [02:30 - 02:45] Conclusion (15 seconds)

**[SCREEN: Return to project folder or final slide]**

**NARRATE:**

> "To summarize: a Django REST backend, a React web client, and a PyQt5 desktop client—all working together as one unified system. The code is documented, the setup is reproducible, and the architecture follows best practices. Thank you for reviewing my submission."

**ACTION:** Show folder structure one last time with:

- `backend/` folder
- `web-frontend/` folder
- `desktop-app/` folder
- `README.md`

**[SCREEN: Fade to black or end screen with text:]**

```
IIT Bombay Internship Screening
Hybrid Analytics Application
Completed: February 2026
```

---

## Alternative Shorter Version (2 minutes)

If time is tight, combine sections:

1. **[00:00-00:05]** Quick intro
2. **[00:05-00:40]** Web demo (login, upload, show analytics)
3. **[00:40-01:10]** Desktop demo (login, verify same data)
4. **[01:10-01:30]** Cross-platform consistency (refresh web, show matching data)
5. **[01:30-01:50]** PDF generation (quick show)
6. **[01:50-02:00]** Closing statement

---

## Recording Tips

### Visual Quality

- **Resolution:** 1920x1080 minimum
- **Frame rate:** 30fps or 60fps
- **Screen area:** Focus on application windows, minimize visible desktop clutter

### Audio Quality

- **Microphone:** Use headset or external mic (not laptop mic)
- **Environment:** Quiet room, minimize background noise
- **Volume:** Speak clearly at moderate pace
- **Script:** Practice 2-3 times before recording

### Pacing

- **Don't rush:** Allow 1-2 seconds after each action for viewer comprehension
- **Mouse movements:** Deliberate and smooth, not erratic
- **Pauses:** Brief pause before switching applications
- **Breathing:** Natural pauses between sentences

### Technical Setup

- **Close notifications:** Turn off system notifications
- **Browser tabs:** Close unnecessary tabs
- **Terminal cleanup:** Clear history, show only relevant commands
- **App state:** Start with clean state (logged out initially)

---

## Post-Recording Checklist

- [ ] Video under 3 minutes total
- [ ] Audio clear and audible
- [ ] All key features demonstrated
- [ ] No sensitive information visible (tokens, passwords in plaintext)
- [ ] Video exports successfully to common format (MP4)
- [ ] File size reasonable (<100MB)

---

## Fallback: No-Narration Version

If you prefer not to narrate, create a silent demo with text overlays:

**Text Overlay Examples:**

- "Logging into Web Application..."
- "Uploading CSV dataset..."
- "Summary statistics computed by Pandas"
- "Chart rendered with Chart.js"
- "Switching to Desktop Application..."
- "Same data, different client"
- "Both clients use same backend API"

Use simple, clear text on dark background with high contrast.

---

## Video File Naming

Save as: `IIT_Bombay_Analytics_Demo_[YourName].mp4`

Example: `IIT_Bombay_Analytics_Demo_John_Doe.mp4`

---

## Distribution

Upload to:

1. **YouTube** (unlisted link)
2. **Google Drive** (with link sharing enabled)
3. **Cloud storage** provided by IIT Bombay

Include video link in submission email or form.

---

## Estimated Time Breakdown

| Section     | Time     | Content                   |
| ----------- | -------- | ------------------------- |
| Intro       | 10s      | Project overview          |
| Web App     | 35s      | Login, upload, analytics  |
| Desktop App | 35s      | Login, verify consistency |
| Consistency | 30s      | Cross-platform demo       |
| PDF Report  | 20s      | Generate and show PDF     |
| Backend     | 20s      | Code structure overview   |
| Conclusion  | 15s      | Closing statement         |
| **Total**   | **2:45** | ~165 seconds              |

---

## Common Mistakes to Avoid

❌ Speaking too fast - viewers need time to absorb  
❌ Skipping the cross-platform verification - that's the key point!  
❌ Not showing the backend code structure - demonstrates architectural understanding  
❌ Forgetting to show data consistency between clients  
❌ Poor audio quality - re-record if necessary  
❌ Visible errors or crashes - test thoroughly before recording  
❌ Too long (>3 min) - edit to be concise

---

## Final Note

Remember: The evaluator wants to see:

1. ✅ **It works** - All features functional
2. ✅ **It's consistent** - Same data across platforms
3. ✅ **You understand it** - Clear explanation of architecture
4. ✅ **It's professional** - Polished presentation

Good luck with your demo recording!
