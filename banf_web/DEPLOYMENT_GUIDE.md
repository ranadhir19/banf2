# BANF Web Application - Deployment Guide

## Overview

This guide documents the complete infrastructure needed to build the BANF web application on Wix.

**Dev Site:** https://banfwix.wixsite.com/banf1  
**Site ID:** c13ae8c5-7053-4f2d-9a9a-371869be4395  
**Account:** Banfjax@gmail.com

---

## Phase 1: CMS Collections (Priority Order)

### Core Collections (Create First)

| # | Collection Name | Purpose | Key Fields |
|---|----------------|---------|------------|
| 1 | **Members** | Member profiles | memberId, email, firstName, lastName, phone, address, memberType, status, joinDate |
| 2 | **Admins** | Admin users | adminId, email, name, role, permissions, status |
| 3 | **Events** | Event listings | eventId, title, description, date, location, price, capacity, status |
| 4 | **EventRegistrations** | Event signups | registrationId, eventId, memberId, guests, paymentStatus |
| 5 | **Payments** | Payment records | paymentId, memberId, amount, type, status, transactionId, date |
| 6 | **Surveys** | Survey definitions | surveyId, title, questions, targetAudience, status, deadline |
| 7 | **SurveyResponses** | Survey answers | responseId, surveyId, memberId, answers, submittedAt |
| 8 | **Complaints** | Complaint tickets | complaintId, category, description, status, priority, assignedTo |

### Secondary Collections

| # | Collection Name | Purpose |
|---|----------------|---------|
| 9 | **Sponsors** | Sponsor profiles and tiers |
| 10 | **Vendors** | Vendor directory |
| 11 | **Volunteers** | Volunteer signups |
| 12 | **Magazine** | E-Magazine issues |
| 13 | **Articles** | Magazine articles |
| 14 | **RadioShows** | Radio show schedules |
| 15 | **GuideListings** | Jacksonville Guide entries |
| 16 | **StreamingEvents** | Live streaming sessions |

### Full Collection List (130+)

See `collection_schemas.json` for complete schema definitions.

---

## Phase 2: Pages to Create

### Public Pages

| Page | URL | Template | Description |
|------|-----|----------|-------------|
| Events | /events | Dynamic | Event listing with registration |
| Membership | /membership | Dynamic | Membership info & signup |
| EC Members | /ec-members | Static | Executive Committee bios |
| Magazine | /magazine | Dynamic | E-Magazine archive |
| Radio | /radio | Dynamic | Community Radio player |
| Guide | /guide | Dynamic | Jacksonville Newcomer Guide |
| Sponsors | /sponsors | Dynamic | Sponsor showcase |
| Vendors | /vendors | Dynamic | Vendor directory |
| Volunteer | /volunteer | Dynamic | Volunteer signup form |

### Member Pages (Require Login)

| Page | URL | Template | Description |
|------|-----|----------|-------------|
| Member Dashboard | /member-dashboard | Members-only | Personal member portal |
| Surveys | /surveys | Members-only | Survey participation |
| Streaming Console | /streaming-console | Members-only | Live streaming viewer |

### Admin Pages (Require Admin Login)

| Page | URL | Template | Description |
|------|-----|----------|-------------|
| Admin Dashboard | /admin-dashboard | Admin-only | Admin control panel |
| Admin Login | /admin-login | Lightbox | Admin authentication |

### Authentication Pages

| Page | URL | Template | Description |
|------|-----|----------|-------------|
| Login | /login | Lightbox | Member login |
| Register | /register | Lightbox | Member registration |
| Complaints | /complaints | Anonymous | Anonymous complaint form |

---

## Phase 3: Backend Code (Velo)

### Step 1: Enable Dev Mode

1. Open Wix Editor
2. Go to **Dev Mode** → **Turn on Dev Mode**
3. This enables the code panel

### Step 2: Create Backend Folder Structure

```
backend/
├── member-auth.jsw
├── admin-auth.jsw
├── events.jsw
├── payments.jsw
├── surveys.jsw
├── complaints.jsw
├── streaming-service.jsw
├── radio.jsw
├── magazine.jsw
├── guide.jsw
├── sponsors.jsw
├── vendors.jsw
├── volunteers.jsw
└── ... (42 total files)
```

### Step 3: Deploy Each Backend File

Copy contents from `velo_backend/` folder:

| File | Size | Purpose |
|------|------|---------|
| member-auth.jsw | 8,742 bytes | Member authentication |
| admin-auth.jsw | 6,234 bytes | Admin authentication |
| events.jsw | 12,456 bytes | Event management |
| payments.jsw | 15,678 bytes | Payment processing |
| surveys.jsw | 9,876 bytes | Survey management |
| complaints.jsw | 7,654 bytes | Complaint handling |
| streaming-service.jsw | 11,234 bytes | Live streaming |
| radio.jsw | 8,543 bytes | Radio management |
| magazine.jsw | 10,234 bytes | E-Magazine |
| guide.jsw | 9,123 bytes | Jacksonville Guide |

---

## Phase 4: Frontend Code

### MasterPage.js

Site-wide functionality:
- Authentication state management
- Navigation handling
- Global utilities

### Page Scripts

Each page needs its controller script:
- `events-page.js` - Event listing logic
- `member-dashboard.js` - Member portal logic
- `admin-dashboard.js` - Admin panel logic
- etc.

---

## Deployment Checklist

### Pre-Deployment

- [ ] Wix account logged in
- [ ] Dev Mode enabled
- [ ] All backend files prepared
- [ ] Collection schemas reviewed

### CMS Collections

- [ ] Members collection created
- [ ] Admins collection created
- [ ] Events collection created
- [ ] EventRegistrations collection created
- [ ] Payments collection created
- [ ] Surveys collection created
- [ ] SurveyResponses collection created
- [ ] Complaints collection created
- [ ] Sponsors collection created
- [ ] Vendors collection created
- [ ] Volunteers collection created
- [ ] All remaining collections created

### Pages

- [ ] /events page created
- [ ] /member-dashboard page created
- [ ] /admin-dashboard page created
- [ ] /login lightbox created
- [ ] /register lightbox created
- [ ] /streaming-console page created
- [ ] /ec-members page created
- [ ] /membership page created
- [ ] /magazine page created
- [ ] /radio page created
- [ ] /guide page created
- [ ] /surveys page created
- [ ] /complaints page created
- [ ] /volunteer page created
- [ ] /sponsors page created
- [ ] /vendors page created
- [ ] /admin-login lightbox created

### Backend Code

- [ ] member-auth.jsw deployed
- [ ] admin-auth.jsw deployed
- [ ] events.jsw deployed
- [ ] payments.jsw deployed
- [ ] All 42 backend files deployed

### Post-Deployment

- [ ] Site published
- [ ] All pages accessible
- [ ] Backend APIs working
- [ ] CMS data populated
- [ ] E2E tests passing

---

## Automation Scripts

### Infrastructure Builder

```bash
cd C:\projects\survey\banf_web
python infrastructure_builder.py
```

Options:
1. **Interactive** - Step-by-step with menu
2. **Auto-build** - Claude-guided automation
3. **Report only** - View what needs to be created

### E2E Tests

After deployment:

```bash
python comprehensive_e2e_test.py
```

---

## Troubleshooting

### Login Issues

If browser doesn't remember login:
1. Delete `browser_profile/` folder
2. Run script again
3. Complete manual login

### Collection Creation Fails

If auto-creation doesn't work:
1. Use Wix Dashboard manually: `https://manage.wix.com/dashboard/{SITE_ID}/database/data`
2. Click "Create Collection"
3. Follow prompts

### Page Creation Fails

If auto-creation doesn't work:
1. Use Wix Editor manually
2. Click "Pages" panel
3. Click "Add Page"
4. Enter page name

---

## Support

For issues with this deployment:
1. Check screenshots in `screenshots/` folder
2. Review build log
3. Verify Wix account access

